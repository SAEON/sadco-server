import pandas as pd
import zipfile

from io import StringIO, BytesIO
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, inspect, text
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_404_NOT_FOUND

from sadco.const import DataType
from sadco.db.models import (Watphy, Survey, Station, Sedphy, Sedchem1, Sedchem2, Sedpol1, Sedpol2, Watchem1, Watchem2,
                             Watpol1, Watpol2, Watnut)

from sadco.api.models import (HydroDownloadModel, HydroWaterPhysicalDownloadModel,
                              HydroWaterNutrientAndChemistryDownloadModel, HydroWaterPollutionDownloadModel,
                              HydroWaterChemistryDownloadModel, HydroSedimentPhysicalDownloadModel,
                              HydroWaterNutrientsDownloadModel, HydroSedimentPollutionDownloadModel,
                              HydroSedimentChemistryDownloadModel)

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
            items = get_water_nutrients_items(survey_id)
        case DataType.SEDIMENT:
            items = get_sediment_items(survey_id)
        case DataType.SEDIMENTPOLLUTION:
            items = get_sediment_pollution_items(survey_id)
        case DataType.SEDIMENTCHEMISTRY:
            items = get_sediment_chemistry_items(survey_id)

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


def get_water_nutrients_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list).
            joinedload(Watphy.watnut)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_hydro_nutrients_download_model(watphy, station, row.Survey).dict()
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


def get_sediment_pollution_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.sedphy_list).
            joinedload(Sedphy.sedpol1)
        ).
        options(
            joinedload(Survey.stations).
            joinedload(Station.sedphy_list).
            joinedload(Sedphy.sedpol2)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_sediment_pollution_download_model(sedphy, station, row.Survey).dict()
        for row in results
        for station in row.Survey.stations
        for sedphy in station.sedphy_list
    ]


def get_sediment_chemistry_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.sedphy_list).
            joinedload(Sedphy.sedchem1)
        ).
        options(
            joinedload(Survey.stations).
            joinedload(Station.sedphy_list).
            joinedload(Sedphy.sedchem1)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_sediment_chemistry_download_model(sedphy, station, row.Survey).dict()
        for row in results
        for station in row.Survey.stations
        for sedphy in station.sedphy_list
    ]


def get_hydro_water_chemistry_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterChemistryDownloadModel:
    return HydroWaterChemistryDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        **get_table_data(Watchem1, watphy.watchem1, fields_to_ignore=['watphy_code']),
        **get_table_data(Watchem2, watphy.watchem2, fields_to_ignore=['watphy_code'])
    )


def get_hydro_nutrients_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterNutrientsDownloadModel:
    return HydroWaterNutrientsDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        **get_table_data(Watnut, watphy.watnut, fields_to_ignore=['watphy_code'])
    )


def get_hydro_water_pollution_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterPollutionDownloadModel:
    return HydroWaterPollutionDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        **get_table_data(Watpol1, watphy.watpol1, fields_to_ignore=['watphy_code']),
        **get_table_data(Watpol2, watphy.watpol2, fields_to_ignore=['watphy_code'])
    )


def get_hydro_water_nutrients_and_chemistry_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterNutrientAndChemistryDownloadModel:
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


def get_hydro_water_physical_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterPhysicalDownloadModel:
    return HydroWaterPhysicalDownloadModel(
        **(get_hydro_download_model(station, survey).dict()),
        instrument=watphy.sampling_device.name if watphy.sampling_device and watphy.sampling_device.name else '',
        temperature=watphy.temperature if watphy.temperature else 0,
        salinity=watphy.salinity if watphy.salinity else 0,
        dissolved_oxygen=watphy.disoxygen if watphy.disoxygen else 0,
        sound_velocity=watphy.soundv if watphy.soundv else 0,
    )


def get_sediment_physical_download_model(
        sedphy: Sedphy,
        station: Station,
        survey: Survey
) -> HydroSedimentPhysicalDownloadModel:
    return HydroSedimentPhysicalDownloadModel(
        **(get_hydro_download_model(station, survey).dict()),
        **get_table_data(Sedphy, sedphy, fields_to_ignore=[
            'code',
            'station_id',
            'device_code',
            'method_code',
            'standard_code',
            'spldattim'
        ]),
        spldattim=sedphy.spldattim.strftime("%m/%d/%Y %H:%M:%S") if sedphy.spldattim else ''
    )


def get_sediment_pollution_download_model(
        sedphy: Sedphy,
        station: Station,
        survey: Survey
) -> HydroSedimentPollutionDownloadModel:
    return HydroSedimentPollutionDownloadModel(
        **(get_sediment_physical_download_model(sedphy, station, survey).dict()),
        **get_table_data(Sedpol1, sedphy.sedpol1, fields_to_ignore=['sedphy_code']),
        **get_table_data(Sedpol2, sedphy.sedpol2, fields_to_ignore=['sedphy_code'])
    )


def get_sediment_chemistry_download_model(
        sedphy: Sedphy,
        station: Station, 
        survey: Survey
) -> HydroSedimentChemistryDownloadModel:
    return HydroSedimentChemistryDownloadModel(
        **(get_sediment_physical_download_model(sedphy, station, survey).dict()),
        **get_table_data(Sedchem1, sedphy.sedchem1, fields_to_ignore=['sedphy_code']),
        **get_table_data(Sedchem2, sedphy.sedchem2, fields_to_ignore=['sedphy_code'])
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


def get_table_data(db_model, fetched_model, fields_to_ignore: list = None) -> dict:
    return {
        field: getattr(fetched_model, field, 0)
        if fetched_model and getattr(fetched_model, field, 0) is not None else 0
        for field in inspect(db_model).columns.keys()
        if fields_to_ignore is None or not fields_to_ignore.__contains__(field)
    }


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
