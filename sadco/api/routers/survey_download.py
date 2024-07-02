import pandas as pd
import zipfile

from io import StringIO, BytesIO
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_404_NOT_FOUND

from sadco.api.models.survey_download import WeatherDownloadModel
from sadco.db.models import (Watphy, Survey, Station, Sedphy, Weather, Currents, CurMooring, CurDepth, CurData,
                             Inventory, WetStation, WetPeriod)

from sadco.api.models import (HydroDownloadModel, HydroWaterPhysicalDownloadModel,
                              HydroWaterNutrientAndChemistryDownloadModel, HydroWaterPollutionDownloadModel,
                              HydroWaterChemistryDownloadModel, HydroSedimentPhysicalDownloadModel,
                              HydroWaterNutrientsDownloadModel, HydroSedimentPollutionDownloadModel,
                              HydroSedimentChemistryDownloadModel, HydroWeatherDownloadModel,
                              HydroCurrentsDownloadModel, CurrentsDownloadModel)

from sadco.db import Session
from sadco.const import SADCOScope, DataType
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
            sampling_depth=cur_depth.spldep,
            instrument=cur_depth.edm_instrument2.name,
            time_interval=cur_depth.time_interval,
            passkey=cur_depth.passkey,
            parameters=cur_depth.parameters,
            **get_table_data(
                cur_data,
                [
                    'code',
                    'depth_code'
                ]
            ),
            ph=cur_data.cur_watphy.ph if cur_data.cur_watphy else None,
            salinity=cur_data.cur_watphy.salinity if cur_data.cur_watphy else None,
            dissolved_oxygen=cur_data.cur_watphy.dis_oxy if cur_data.cur_watphy else None,
        ).dict()
        for row in results
        for cur_depth in row.CurMooring.cur_depths
        for cur_data in cur_depth.cur_data_list
    ]


@router.get(
    '/weather/{survey_id}',
    response_class=StreamingResponse,
    dependencies=[Depends(Authorize(SADCOScope.WEATHER_DOWNLOAD))]
)
async def download_currents_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type')
):
    items = get_weather_items(survey_id)

    return get_zipped_csv_response(items, survey_id, data_type)


def get_weather_items(survey_id: str) -> list:
    stmt = (
        select(
            Inventory
        ).where(Inventory.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Inventory.wet_stations).
            joinedload(WetStation.wet_periods).
            joinedload(WetPeriod.wet_data_list)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        WeatherDownloadModel(
            station_name=wet_station.name,
            latitude=wet_station.latitude,
            longitude=wet_station.longitude,
            msl_height=wet_period.height_msl,
            surface_height=wet_period.height_surface,
            record_date=wet_data.date_time,
            ave_air_temp=wet_data.air_temp_ave,
            min_air_temp=wet_data.air_temp_min,
            min_air_temp_time=wet_data.air_temp_min_time,
            max_air_temp=wet_data.air_temp_max,
            max_air_temp_time=wet_data.air_temp_max_time,
            barometric_pressure=wet_data.barometric_pressure,
            fog=wet_data.fog,
            rainfall=wet_data.rainfall,
            relative_humidity=wet_data.relative_humidity,
            solar_radiation=wet_data.solar_radiation,
            max_solar_radiation=wet_data.solar_radiation_max,
            wind_direction=wet_data.wind_dir,
            ave_wind_speed=wet_data.wind_speed_ave,
            min_wind_speed=wet_data.wind_speed_min,
            max_wind_speed=wet_data.wind_speed_max,
            max_wind_speed_time=wet_data.wind_speed_max_time,
            max_wind_speed_duration=wet_data.wind_speed_max_length,
            max_wind_speed_direction=wet_data.wind_speed_max_dir,
            max_wind_speed_standard_deviation=wet_data.wind_speed_std
        ).dict()
        for row in results
        for wet_station in row.Inventory.wet_stations
        for wet_period in wet_station.wet_periods
        for wet_data in wet_period.wet_data_list
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
    items = get_hydro_data_type_items(data_type, survey_id)

    return get_zipped_csv_response(items, survey_id, data_type)


def get_hydro_data_type_items(data_type: str, survey_id: str) -> list:
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
            return get_hydro_weather_items(survey_id)
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


def get_hydro_weather_items(survey_id: str) -> list:
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
        **get_table_data(watphy.watchem1),
        **get_table_data(watphy.watchem2)
    )


def get_hydro_nutrients_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterNutrientsDownloadModel:
    return HydroWaterNutrientsDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        **get_table_data(watphy.watnut)
    )


def get_hydro_water_pollution_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterPollutionDownloadModel:
    return HydroWaterPollutionDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        **get_table_data(watphy.watpol1),
        **get_table_data(watphy.watpol2)
    )


def get_hydro_water_nutrients_and_chemistry_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterNutrientAndChemistryDownloadModel:
    return HydroWaterNutrientAndChemistryDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        no2=watphy.watnut.no2,
        no3=watphy.watnut.no3,
        po4=watphy.watnut.po4,
        ptot=watphy.watnut.ptot,
        sio3=watphy.watnut.sio3,
        ph=watphy.watchem1.ph,
        chla=watphy.watchl.chla,
    )


def get_hydro_water_physical_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterPhysicalDownloadModel:
    return HydroWaterPhysicalDownloadModel(
        **(get_hydro_download_model(station, survey).dict()),
        **get_table_data(
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
        **get_table_data(sedphy.sedpol1),
        **get_table_data(sedphy.sedpol2)
    )


def get_hydro_sediment_chemistry_download_model(
        sedphy: Sedphy,
        station: Station,
        survey: Survey
) -> HydroSedimentChemistryDownloadModel:
    return HydroSedimentChemistryDownloadModel(
        **(get_hydro_sediment_physical_download_model(sedphy, station, survey).dict()),
        **get_table_data(sedphy.sedchem1),
        **get_table_data(sedphy.sedchem2),
    )


def get_hydro_currents_download_model(
        survey: Survey,
        station: Station,
        currents: Currents
) -> HydroCurrentsDownloadModel:
    return HydroCurrentsDownloadModel(
        **(get_hydro_download_model(station, survey).dict()),
        **get_table_data(
            currents,
            fields_to_ignore=[
                'station_id'
            ]
        )
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
        station_name=station.stnnam,
        station_id=station.station_id,
        platform_name=survey.planam,
        max_sampling_depth=station.max_spldep,
    )


def get_table_data(fetched_model, fields_to_ignore: list = None) -> dict:
    """
    Builds and returns a dictionary of the fields from an api model and its respective db value.
    :param fetched_model: fetched db model whose values will be used.
    :param fields_to_ignore: fields from the model to be ignored.
    """
    table_data_dict = fetched_model.__dict__.copy()
    del table_data_dict['_sa_instance_state']
    for field_to_ignore in fields_to_ignore:
        del table_data_dict[field_to_ignore]

    return table_data_dict


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
