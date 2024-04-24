import pandas as pd
import zipfile

from io import StringIO, BytesIO
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_404_NOT_FOUND

from sadco.const import DataType
from sadco.db.models import (Watphy, Survey, Station, Sedphy, Sedchem1, Sedchem2, Sedpol1, Sedpol2)

from sadco.api.models import (HydroDownloadModel, HydroWaterPhysicalDownloadModel,
                              HydroWaterNutrientAndChemistryDownloadModel, HydroWaterPollutionDownloadModel,
                              HydroWaterChemistryDownloadModel, HydroSedimentPhysicalDownloadModel)

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
        case DataType.WATERNUTRIENTSANDCHEMISTRY:
            items = get_water_nutrients_and_chemistry_items(survey_id)
        case DataType.WATERPOLLUTION:
            items = get_water_pollution_items(survey_id)
        case DataType.WATERCHEMISTRY:
            items = get_water_chemistry_items(survey_id)
        case DataType.WATERNUTRIENTS:
            items = ''
        case DataType.SEDIMENT:
            items = get_sediment_items(survey_id)

    return get_zipped_csv_response(items, survey_id, data_type)


def get_water_nutrients_and_chemistry_items(survey_id: str) -> list:
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
        get_hydro_water_nutrients_and_chemistry_download_model(watphy, station, row.Survey).dict()
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


def get_water_chemistry_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list).
            joinedload(Watphy.watchem1)
        ).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list).
            joinedload(Watphy.watchem2)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_hydro_water_chemistry_download_model(watphy, station, row.Survey).dict()
        for row in results
        for station in row.Survey.stations
        for watphy in station.watphy_list
    ]


def get_sediment_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.sedphy_list)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_sediment_physical_download_model(sedphy, station, row.Survey).dict()
        for row in results
        for station in row.Survey.stations
        for sedphy in station.sedphy_list
    ]


def get_hydro_water_chemistry_download_model(watphy: Watphy, station: Station,
                                             survey: Survey) -> HydroWaterChemistryDownloadModel:
    return HydroWaterChemistryDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        dic=watphy.watchem1.dic if watphy.watchem1 and watphy.watchem1.dic else 0,
        doc=watphy.watchem1.doc if watphy.watchem1 and watphy.watchem1.doc else 0,
        fluoride=watphy.watchem1.fluoride if watphy.watchem1 and watphy.watchem1.fluoride else 0,
        iodene=watphy.watchem1.iodene if watphy.watchem1 and watphy.watchem1.iodene else 0,
        iodate=watphy.watchem1.iodate if watphy.watchem1 and watphy.watchem1.iodate else 0,
        kjn=watphy.watchem1.kjn if watphy.watchem1 and watphy.watchem1.kjn else 0,
        nh3=watphy.watchem1.nh3 if watphy.watchem1 and watphy.watchem1.nh3 else 0,
        nitrogen=watphy.watchem1.nitrogen if watphy.watchem1 and watphy.watchem1.nitrogen else 0,
        oxa=watphy.watchem1.oxa if watphy.watchem1 and watphy.watchem1.oxa else 0,
        ph=watphy.watchem1.ph if watphy.watchem1 and watphy.watchem1.ph else 0,
        calcium=watphy.watchem2.calcium if watphy.watchem2 and watphy.watchem2.calcium else 0,
        cesium=watphy.watchem2.cesium if watphy.watchem2 and watphy.watchem2.cesium else 0,
        hydrocarbons=watphy.watchem2.hydrocarbons if watphy.watchem2 and watphy.watchem2.hydrocarbons else 0,
        magnesium=watphy.watchem2.magnesium if watphy.watchem2 and watphy.watchem2.magnesium else 0,
        pah=watphy.watchem2.pah if watphy.watchem2 and watphy.watchem2.pah else 0,
        potassium=watphy.watchem2.potassium if watphy.watchem2 and watphy.watchem2.potassium else 0,
        rubidium=watphy.watchem2.rubidium if watphy.watchem2 and watphy.watchem2.rubidium else 0,
        sodium=watphy.watchem2.sodium if watphy.watchem2 and watphy.watchem2.sodium else 0,
        strontium=watphy.watchem2.strontium if watphy.watchem2 and watphy.watchem2.strontium else 0,
        so4=watphy.watchem2.so4 if watphy.watchem2 and watphy.watchem2.so4 else 0,
        sussol=watphy.watchem2.sussol if watphy.watchem2 and watphy.watchem2.sussol else 0,
    )


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


def get_hydro_water_nutrients_and_chemistry_download_model(watphy: Watphy, station: Station,
                                                           survey: Survey) -> HydroWaterNutrientAndChemistryDownloadModel:
    return HydroWaterNutrientAndChemistryDownloadModel(
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


def get_sediment_physical_download_model(sedphy: Sedphy, station: Station,
                                         survey: Survey) -> HydroSedimentPhysicalDownloadModel:
    return HydroSedimentPhysicalDownloadModel(
        **(get_hydro_download_model(station, survey).dict()),
        subdes=sedphy.subdes if sedphy.subdes else 0,
        spldattim=sedphy.spldattim if sedphy.spldattim else 0,
        spldep=sedphy.spldep if sedphy.spldep else 0,
        spldis=sedphy.spldis if sedphy.spldis else 0,
        splvol=sedphy.splvol if sedphy.splvol else 0,
        sievsz=sedphy.sievsz if sedphy.sievsz else 0,
        kurt=sedphy.kurt if sedphy.kurt else 0,
        skew=sedphy.skew if sedphy.skew else 0,
        meanpz=sedphy.meanpz if sedphy.meanpz else 0,
        medipz=sedphy.medipz if sedphy.medipz else 0,
        pctsat=sedphy.pctsat if sedphy.pctsat else 0,
        pctsil=sedphy.pctsil if sedphy.pctsil else 0,
        permty=sedphy.permty if sedphy.permty else 0,
        porsty=sedphy.porsty if sedphy.porsty else 0,
        dwf=sedphy.dwf if sedphy.dwf else 0,
        cod=sedphy.cod if sedphy.cod else 0
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
