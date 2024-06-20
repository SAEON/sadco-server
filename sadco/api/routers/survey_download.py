import pandas as pd
import zipfile

from io import StringIO, BytesIO
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_404_NOT_FOUND

from sadco.const import DataType
from sadco.db.models import (Watphy, Survey, Station, Sedphy, Weather, Watchem1, Watchem2, Watnut, Watpol1, Watpol2,
                             Sedpol1, Sedpol2, Sedchem1, Sedchem2, Currents, CurMooring, CurDepth, CurData)

from sadco.api.models import (HydroDownloadModel, HydroWaterPhysicalDownloadModel,
                              HydroWaterNutrientAndChemistryDownloadModel, HydroWaterPollutionDownloadModel,
                              HydroWaterChemistryDownloadModel, HydroSedimentPhysicalDownloadModel,
                              HydroWaterNutrientsDownloadModel, HydroSedimentPollutionDownloadModel,
                              HydroSedimentChemistryDownloadModel, HydroWeatherDownloadModel,
                              HydroCurrentsDownloadModel, CurrentsDownloadModel)

from sadco.db import Session
from sadco.const import SADCOScope
from sadco.api.lib.auth import Authorize

router = APIRouter()


@router.get(
    '/currents/{survey_id}',
    response_class=StreamingResponse,
    dependencies=[Depends(Authorize(SADCOScope.CURRENTS_DOWNLOAD))]
)
async def download_currents_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type')
):
    items = get_currents_items(survey_id)

    return get_zipped_csv_response(items, survey_id, data_type)


def get_currents_items(survey_id: str) -> list:
    stmt = (
        select(
            CurMooring
        ).where(CurMooring.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(CurMooring.cur_depths).
            joinedload(CurDepth.cur_data_list).
            joinedload(CurData.cur_watphy)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        CurrentsDownloadModel(
            sampling_depth=cur_depth.spldep if cur_depth.spldep else 0,
            instrument=cur_depth.edm_instrument2.name if cur_depth.edm_instrument2 and cur_depth.edm_instrument2.name else '',
            time_interval=cur_depth.time_interval if cur_depth.time_interval else 0,
            passkey=cur_depth.passkey if cur_depth.passkey else '',
            parameters=cur_depth.parameters if cur_depth.parameters else '',
            datetime=cur_data.datetime if cur_data.datetime else '',
            speed=cur_data.speed if cur_data.speed else 0,
            direction=cur_data.direction if cur_data.direction else 0,
            temperature=cur_data.temperature if cur_data.temperature else 0,
            vert_velocity=cur_data.vert_velocity if cur_data.vert_velocity else 0,
            f_speed_9=cur_data.f_speed_9 if cur_data.f_speed_9 else 0,
            f_direction_9=cur_data.f_direction_9 if cur_data.f_direction_9 else 0,
            f_speed_14=cur_data.f_speed_14 if cur_data.f_speed_14 else 0,
            f_direction_14=cur_data.f_direction_14 if cur_data.f_direction_14 else 0,
            pressure=cur_data.pressure if cur_data.pressure else 0,
            ph=cur_data.cur_watphy.ph if cur_data.cur_watphy and cur_data.cur_watphy.ph else 0,
            salinity=cur_data.cur_watphy.salinity if cur_data.cur_watphy and cur_data.cur_watphy.salinity else 0,
            dissolved_oxygen=cur_data.cur_watphy.dis_oxy if cur_data.cur_watphy and cur_data.cur_watphy.dis_oxy else 0,
        ).dict()
        for row in results
        for cur_depth in row.CurMooring.cur_depths
        for cur_data in cur_depth.cur_data_list
    ]


@router.get(
    '/hydro/{survey_id}',
    response_class=StreamingResponse,
    dependencies=[Depends(Authorize(SADCOScope.HYDRO_DOWNLOAD))]
)
async def download_hydro_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type')
):
    items = get_data_type_items(data_type, survey_id)

    return get_zipped_csv_response(items, survey_id, data_type)


def get_data_type_items(data_type: str, survey_id: str) -> list:
    match data_type:
        case DataType.WATER:
            return get_water_items(survey_id)
        case DataType.WATERNUTRIENTSANDCHEMISTRY:
            return get_water_nutrients_and_chemistry_items(survey_id)
        case DataType.WATERPOLLUTION:
            return get_water_pollution_items(survey_id)
        case DataType.WATERCHEMISTRY:
            return get_water_chemistry_items(survey_id)
        case DataType.WATERNUTRIENTS:
            return get_water_nutrients_items(survey_id)
        case DataType.SEDIMENT:
            return get_sediment_items(survey_id)
        case DataType.SEDIMENTPOLLUTION:
            return get_sediment_pollution_items(survey_id)
        case DataType.SEDIMENTCHEMISTRY:
            return get_sediment_chemistry_items(survey_id)
        case DataType.WEATHER:
            return get_weather_items(survey_id)
        case DataType.CURRENTS:
            return get_hydro_currents_items(survey_id)


def get_water_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.watphy_list)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_hydro_water_physical_download_model(watphy, station, row.Survey).dict()
        for row in results
        for station in row.Survey.stations
        for watphy in station.watphy_list
    ]


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
        get_hydro_sediment_physical_download_model(sedphy, station, row.Survey).dict()
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
        get_hydro_sediment_pollution_download_model(sedphy, station, row.Survey).dict()
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
        get_hydro_sediment_chemistry_download_model(sedphy, station, row.Survey).dict()
        for row in results
        for station in row.Survey.stations
        for sedphy in station.sedphy_list
    ]


def get_weather_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.weather_list)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_hydro_weather_download_model(row.Survey, station, weather).dict()
        for row in results
        for station in row.Survey.stations
        for weather in station.weather_list
    ]


def get_hydro_currents_items(survey_id: str) -> list:
    stmt = (
        select(Survey).where(Survey.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Survey.stations).
            joinedload(Station.currents)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        get_hydro_currents_download_model(row.Survey, station, currents).dict()
        for row in results
        for station in row.Survey.stations
        for currents in station.currents
    ]


def get_hydro_weather_download_model(
        survey: Survey,
        station: Station,
        weather: Weather
) -> HydroWeatherDownloadModel:
    return HydroWeatherDownloadModel(
        **get_hydro_download_model(station, survey).dict(),
        **get_table_data(
            HydroWeatherDownloadModel,
            Weather,
            weather,
            fields_to_ignore=[
                'station_id'
            ]
        )
    )


def get_hydro_water_chemistry_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterChemistryDownloadModel:
    return HydroWaterChemistryDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        **get_table_data(
            HydroWaterChemistryDownloadModel,
            Watchem1,
            watphy.watchem1
        ),
        **get_table_data(
            HydroWaterChemistryDownloadModel,
            Watchem2,
            watphy.watchem2
        )
    )


def get_hydro_nutrients_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterNutrientsDownloadModel:
    return HydroWaterNutrientsDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        **get_table_data(
            HydroWaterNutrientsDownloadModel,
            Watnut,
            watphy.watnut
        )
    )


def get_hydro_water_pollution_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterPollutionDownloadModel:
    return HydroWaterPollutionDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        **get_table_data(
            HydroWaterPollutionDownloadModel,
            Watpol1,
            watphy.watpol1
        ),
        **get_table_data(
            HydroWaterPollutionDownloadModel,
            Watpol2,
            watphy.watpol2
        )
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
        **get_table_data(
            HydroWaterPhysicalDownloadModel,
            Watphy,
            watphy,
            fields_to_ignore=[
                'station_id',
                'spldattim'
            ]
        ),
        spldattim=watphy.spldattim.strftime("%m/%d/%Y %H:%M:%S") if watphy.spldattim else '',
    )


def get_hydro_sediment_physical_download_model(
        sedphy: Sedphy,
        station: Station,
        survey: Survey
) -> HydroSedimentPhysicalDownloadModel:
    return HydroSedimentPhysicalDownloadModel(
        **(get_hydro_download_model(station, survey).dict()),
        **get_table_data(
            HydroSedimentPhysicalDownloadModel,
            Sedphy,
            sedphy,
            fields_to_ignore=[
                'station_id',
                'spldattim'
            ]
        ),
        spldattim=sedphy.spldattim.strftime("%m/%d/%Y %H:%M:%S") if sedphy.spldattim else ''
    )


def get_hydro_sediment_pollution_download_model(
        sedphy: Sedphy,
        station: Station,
        survey: Survey
) -> HydroSedimentPollutionDownloadModel:
    return HydroSedimentPollutionDownloadModel(
        **(get_hydro_sediment_physical_download_model(sedphy, station, survey).dict()),
        **get_table_data(
            HydroSedimentPollutionDownloadModel,
            Sedpol1,
            sedphy.sedpol1
        ),
        **get_table_data(
            HydroSedimentPollutionDownloadModel,
            Sedpol2,
            sedphy.sedpol2
        )
    )


def get_hydro_sediment_chemistry_download_model(
        sedphy: Sedphy,
        station: Station,
        survey: Survey
) -> HydroSedimentChemistryDownloadModel:
    return HydroSedimentChemistryDownloadModel(
        **(get_hydro_sediment_physical_download_model(sedphy, station, survey).dict()),
        **get_table_data(
            HydroSedimentChemistryDownloadModel,
            Sedchem1,
            sedphy.sedchem1
        ),
        **get_table_data(
            HydroSedimentChemistryDownloadModel,
            Sedchem2,
            sedphy.sedchem2
        ),
    )


def get_hydro_currents_download_model(
        survey: Survey,
        station: Station,
        currents: Currents
) -> HydroCurrentsDownloadModel:
    return HydroCurrentsDownloadModel(
        **(get_hydro_download_model(station, survey).dict()),
        **get_table_data(
            HydroCurrentsDownloadModel,
            Currents,
            currents,
            fields_to_ignore=[
                'station_id'
            ]
        )
    )


def get_hydro_download_model(station: Station, survey: Survey) -> HydroDownloadModel:
    return HydroDownloadModel(
        survey_id=station.survey_id,
        latitude=station.latitude if station.latitude else 0,
        longitude=station.longitude if station.longitude else 0,
        year=station.date_start.year,
        month=station.date_start.month,
        day=station.date_start.day,
        time='',
        station_name=station.stnnam if station.stnnam else '',
        station_id=station.station_id,
        platform_name=survey.planam if survey.planam else '',
        max_sampling_depth=station.max_spldep if station.max_spldep else 0,
    )


def get_table_data(api_model, db_model, fetched_model, fields_to_ignore: list = None) -> dict:
    """
    Builds and returns a dictionary of the fields from an api model and its respective db value.
    :param api_model: The api model whose fields will be iterated through.
    :param db_model: The db model whose field names will be compared.
    :param fetched_model: fetched model whose values will be used.
    :param fields_to_ignore: fields to ignore.
    """
    return {
        field_name: getattr(fetched_model, field_name) if (
                fetched_model and getattr(fetched_model, field_name, None) is not None) else (
            0 if field_info.type_ in (int, float) else '')
        for field_name, field_info in api_model.__fields__.items()
        if (fields_to_ignore is None or not fields_to_ignore.__contains__(field_name)) and hasattr(db_model, field_name)
    }


def get_zipped_csv_response(items, survey_id, data_variant) -> StreamingResponse:
    """
    Converts a list of dictionary items to a streaming response of a zipped folder containing a csv file
    :param items: A list of dictionaries that contain the information for each row of the csv
    :param survey_id: The id of the applicable survey for file naming purposes
    :param data_variant: The variant of the data for file naming purposes
    """
    data_frame = pd.DataFrame(items)

    stream = StringIO()

    data_frame.to_csv(stream, index=False)

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, mode="w") as zip_archive:
        stream.seek(0)
        zip_archive.writestr(f"survey_{survey_id}.csv", stream.read())

    response = StreamingResponse(iter([zip_buffer.getvalue()]), media_type="application/zip")
    response.headers["Content-Disposition"] = f"attachment; filename=survey_{survey_id}_{data_variant}.zip"

    return response
