import pandas as pd
import zipfile

from io import StringIO, BytesIO
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, exists, func, and_, or_
from sqlalchemy.orm import load_only, joinedload
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from sadco.db.models import (Inventory, Planam, Scientists, Institutes, SurveyType, Watphy, Watnut, Watpol1, Watpol2,
                             Sedphy, Sedpol1, Sedpol2, Sedpol2, Sedchem1, Sedchem2, Watchem1, Watchem2, Watcurrents,
                             Weather, Currents, Survey, Station, SamplingDevice, InvStats, station)

from sadco.api.models import (HydroSurveyModel, HydroDownloadModel, HydroWaterPhysicalDownloadModel,
                              HydroWaterNutrientDownloadModel, HydroWaterPollutionDownloadModel)

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
    # TODO: Use a switch case with the data_type to decide which model to fetch.
    items = get_water_nutrient_items(survey_id)

    return get_zipped_csv_response(items, survey_id)


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


def get_zipped_csv_response(items, survey_id) -> StreamingResponse:
    """
    Converts a list of dictionary items to a streaming response of a zipped folder containing a csv file
    :param items: A list of dictionaries that contain the information for each row of the csv
    :param survey_id: The id of the applicable survey for file naming purposes
    """
    data = pd.DataFrame(items)

    stream = StringIO()

    data.to_csv(stream, index=False)

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, mode="w") as zip_archive:
        stream.seek(0)
        zip_archive.writestr(f"survey_{survey_id}.csv", stream.read())

    response = StreamingResponse(iter([zip_buffer.getvalue()]), media_type="application/zip")
    response.headers["Content-Disposition"] = f"attachment; filename=survey_{survey_id}.zip"

    return response
