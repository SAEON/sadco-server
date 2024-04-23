import pandas as pd
import zipfile

from io import StringIO, BytesIO
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, exists, func, and_, or_
from sqlalchemy.orm import load_only, joinedload
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from sadco.const import DataType
from sadco.db.models import (Watphy, Survey, Station)

from sadco.api.models import (HydroDownloadModel, HydroWaterPhysicalDownloadModel, HydroWaterNutrientDownloadModel,
                              HydroWaterPollutionDownloadModel)

from sadco.db import Session

router = APIRouter()


@router.get(
    '/hydro/{survey_id}',
    response_class=StreamingResponse
)
async def download_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type')
):
    items = []

    match data_type:
        case DataType.WATER:
            items = ''
        case DataType.WATERNUTRIENTS:
            items = get_water_nutrient_items(survey_id)
        case DataType.WATERPOLLUTION:
            items = get_water_pollution_items(survey_id)

    return get_zipped_csv_response(items, survey_id, data_type)


def get_water_nutrient_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list).
            joinedload(Watphy.watnut)
        ).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list).
            joinedload(Watphy.watchem1)
        ).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list).
            joinedload(Watphy.watchl)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_hydro_water_nutrient_download_model(watphy, station, row.Survey).dict()
        for row in results
        for station in row.Survey.stations
        for watphy in station.watphy_list
    ]


def get_water_pollution_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list).
            joinedload(Watphy.watpol1)
        ).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list).
            joinedload(Watphy.watpol2)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_hydro_water_pollution_download_model(watphy, station, row.Survey).dict()
        for row in results
        for station in row.Survey.stations
        for watphy in station.watphy_list
    ]


def get_hydro_water_pollution_download_model(watphy: Watphy, station: Station,
                                             survey: Survey) -> HydroWaterPollutionDownloadModel:
    return HydroWaterPollutionDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        arsenic=watphy.watpol1.arsenic if watphy.watpol1 and watphy.watpol1.arsenic else 0,
        cadmium=watphy.watpol1.cadmium if watphy.watpol1 and watphy.watpol1.cadmium else 0,
        chromium=watphy.watpol1.chromium if watphy.watpol1 and watphy.watpol1.chromium else 0,
        cobalt=watphy.watpol1.cobalt if watphy.watpol1 and watphy.watpol1.cobalt else 0,
        copper=watphy.watpol1.copper if watphy.watpol1 and watphy.watpol1.copper else 0,
        iron=watphy.watpol1.iron if watphy.watpol1 and watphy.watpol1.iron else 0,
        lead=watphy.watpol1.lead if watphy.watpol1 and watphy.watpol1.lead else 0,
        manganese=watphy.watpol1.manganese if watphy.watpol1 and watphy.watpol1.manganese else 0,
        mercury=watphy.watpol1.mercury if watphy.watpol1 and watphy.watpol1.mercury else 0,
        nickel=watphy.watpol1.nickel if watphy.watpol1 and watphy.watpol1.nickel else 0,
        selenium=watphy.watpol1.selenium if watphy.watpol1 and watphy.watpol1.selenium else 0,
        zinc=watphy.watpol1.zinc if watphy.watpol1 and watphy.watpol1.zinc else 0,
        aluminium=watphy.watpol2.aluminium if watphy.watpol2 and watphy.watpol2.aluminium else 0,
        antimony=watphy.watpol2.antimony if watphy.watpol2 and watphy.watpol2.antimony else 0,
        bismuth=watphy.watpol2.bismuth if watphy.watpol2 and watphy.watpol2.bismuth else 0,
        molybdenum=watphy.watpol2.molybdenum if watphy.watpol2 and watphy.watpol2.molybdenum else 0,
        silver=watphy.watpol2.silver if watphy.watpol2 and watphy.watpol2.silver else 0,
        titanium=watphy.watpol2.titanium if watphy.watpol2 and watphy.watpol2.titanium else 0,
        vanadium=watphy.watpol2.vanadium if watphy.watpol2 and watphy.watpol2.vanadium else 0
    )


def get_hydro_water_nutrient_download_model(watphy: Watphy, station: Station,
                                            survey: Survey) -> HydroWaterNutrientDownloadModel:
    return HydroWaterNutrientDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        no2=watphy.watnut.no2 if watphy.watnut and watphy.watnut.no2 else 0,
        no3=watphy.watnut.no3 if watphy.watnut and watphy.watnut.no3 else 0,
        po4=watphy.watnut.po4 if watphy.watnut and watphy.watnut.po4 else 0,
        ptot=watphy.watnut.ptot if watphy.watnut and watphy.watnut.ptot else 0,
        sio3=watphy.watnut.sio3 if watphy.watnut and watphy.watnut.sio3 else 0,
        ph=watphy.watchem1.ph if watphy.watchem1 and watphy.watchem1.ph else 0,
        chla=watphy.watchl.chla if watphy.watchl and watphy.watchl.chla else 0,
    )


def get_hydro_water_physical_download_model(watphy: Watphy, station: Station,
                                            survey: Survey) -> HydroWaterPhysicalDownloadModel:
    return HydroWaterPhysicalDownloadModel(
        **(get_hydro_download_model(station, survey).dict()),
        instrument=watphy.sampling_device.name if watphy.sampling_device and watphy.sampling_device.name else '',
        temperature=watphy.temperature if watphy.temperature else 0,
        salinity=watphy.salinity if watphy.salinity else 0,
        dissolved_oxygen=watphy.disoxygen if watphy.disoxygen else 0,
        sound_velocity=watphy.soundv if watphy.soundv else 0,
    )


def get_hydro_download_model(station: Station, survey: Survey) -> HydroDownloadModel:
    return HydroDownloadModel(
        survey_id=station.survey_id,
        latitude=station.latitude,
        longitude=station.longitude,
        year=station.date_start.year,
        month=station.date_start.month,
        day=station.date_start.day,
        time='',
        station_name=station.stnnam if station.stnnam else '',
        station_id=station.station_id,
        platform_name=survey.planam if survey.planam else '',
        max_sampling_depth=station.max_spldep if station.max_spldep else 0,
    )


def get_zipped_csv_response(items, survey_id, data_type) -> StreamingResponse:
    """
    Converts a list of dictionary items to a streaming response of a zipped folder containing a csv file
    :param items: A list of dictionaries that contain the information for each row of the csv
    :param survey_id: The id of the applicable survey for file naming purposes
    :param data_type: The data type requested for file naming purposes
    """
    data = pd.DataFrame(items)

    stream = StringIO()

    data.to_csv(stream, index=False)

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, mode="w") as zip_archive:
        stream.seek(0)
        zip_archive.writestr(f"survey_{survey_id}.csv", stream.read())

    response = StreamingResponse(iter([zip_buffer.getvalue()]), media_type="application/zip")
    response.headers["Content-Disposition"] = f"attachment; filename=survey_{survey_id}_{data_type}.zip"

    return response
