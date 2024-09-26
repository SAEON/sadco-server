from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_404_NOT_FOUND

from sadco.db.models import (Watphy, Survey, Station, Sedphy, Weather, Currents, CurMooring, CurDepth, CurData,
                             Inventory, WetStation, WetPeriod, WavStation)

from sadco.api.models import (HydroDownloadModel, HydroWaterPhysicalDownloadModel,
                              HydroWaterNutrientAndChemistryDownloadModel, HydroWaterPollutionDownloadModel,
                              HydroWaterChemistryDownloadModel, HydroSedimentPhysicalDownloadModel,
                              HydroWaterNutrientsDownloadModel, HydroSedimentPollutionDownloadModel,
                              HydroSedimentChemistryDownloadModel, HydroWeatherDownloadModel,
                              HydroCurrentsDownloadModel, CurrentsDownloadModel, WeatherDownloadModel,
                              WavesDownloadModel)

from sadco.db import Session
from sadco.api.lib.download import get_csv_data, get_table_data, audit_download_request
from sadco.const import SADCOScope, DataType, SurveyType as ConstSurveyType
from sadco.api.lib.auth import Authorize, Authorized

router = APIRouter()


@router.get(
    f"/{ConstSurveyType.UTR.value}/{{survey_id}}",
    response_class=StreamingResponse
)
async def download_utr_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type'),
        auth: Authorized = Depends(Authorize(SADCOScope.UTR_DOWNLOAD))
):
    items = get_currents_items(survey_id)

    zipped_csv_data: dict = get_csv_data(items, survey_id, data_type)

    audit_download_request(auth, zipped_csv_data.get('file_info'), survey_id=survey_id, data_type=data_type)

    return zipped_csv_data.get('zipped_response')


@router.get(
    f"/{ConstSurveyType.CURRENTS.value}/{{survey_id}}",
    response_class=StreamingResponse
)
async def download_currents_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type'),
        auth: Authorized = Depends(Authorize(SADCOScope.CURRENTS_DOWNLOAD))
):
    items = get_currents_items(survey_id)

    zipped_csv_data: dict = get_csv_data(items, survey_id, data_type)

    audit_download_request(auth, zipped_csv_data.get('file_info'), survey_id=survey_id, data_type=data_type)

    return zipped_csv_data.get('zipped_response')


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
    f"/{ConstSurveyType.WEATHER.value}/{{survey_id}}",
    response_class=StreamingResponse
)
async def download_currents_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type'),
        auth: Authorized = Depends(Authorize(SADCOScope.WEATHER_DOWNLOAD))
):
    items = get_weather_items(survey_id)

    zipped_csv_data: dict = get_csv_data(items, survey_id, data_type)

    audit_download_request(auth, zipped_csv_data.get('file_info'), survey_id=survey_id, data_type=data_type)

    return zipped_csv_data.get('zipped_response')


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
    f"/{ConstSurveyType.WAVES.value}/{{survey_id}}",
    response_class=StreamingResponse
)
async def download_currents_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type'),
        auth: Authorized = Depends(Authorize(SADCOScope.WAVES_DOWNLOAD))
):
    items = get_waves_items(survey_id)

    zipped_csv_data: dict = get_csv_data(items, survey_id, data_type)

    audit_download_request(auth, zipped_csv_data.get('file_info'), survey_id=survey_id, data_type=data_type)

    return zipped_csv_data.get('zipped_response')


def get_waves_items(survey_id: str) -> list:
    stmt = (
        select(
            Inventory
        ).where(Inventory.survey_id == survey_id.replace('-', '/')).
        options(
            joinedload(Inventory.wav_stations).
            joinedload(WavStation.wav_data_list)
        )
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        WavesDownloadModel(
            station_name=wav_station.name,
            latitude=wav_station.latitude,
            longitude=wav_station.longitude,
            instrument_depth=wav_station.instrument_depth,
            water_depth=wav_station.water_depth,
            **get_table_data(
                wav_data,
                [
                    'code',
                    'station_id'
                ]
            )
        ).dict()
        for row in results
        for wav_station in row.Inventory.wav_stations
        for wav_data in wav_station.wav_data_list
    ]


@router.get(
    f"/{ConstSurveyType.HYDRO.value}/{{survey_id}}",
    response_class=StreamingResponse
)
async def download_hydro_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type'),
        auth: Authorized = Depends(Authorize(SADCOScope.HYDRO_DOWNLOAD))
):
    items = get_hydro_data_type_items(data_type, survey_id)

    zipped_csv_data: dict = get_csv_data(items, survey_id, data_type)

    audit_download_request(auth, zipped_csv_data.get('file_info'), survey_id=survey_id, data_type=data_type)

    return zipped_csv_data.get('zipped_response')


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
        **get_table_data(
            watphy.watchem1,
            fields_to_ignore=[
                'watphy_code'
            ]
        ),
        **get_table_data(
            watphy.watchem2,
            fields_to_ignore=[
                'watphy_code'
            ]
        )
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
        **get_table_data(
            watphy.watpol1,
            fields_to_ignore=[
                'watphy_code'
            ]
        ),
        **get_table_data(
            watphy.watpol2,
            fields_to_ignore=[
                'watphy_code'
            ]
        )
    )


def get_hydro_water_nutrients_and_chemistry_download_model(
        watphy: Watphy,
        station: Station,
        survey: Survey
) -> HydroWaterNutrientAndChemistryDownloadModel:
    return HydroWaterNutrientAndChemistryDownloadModel(
        **get_hydro_water_physical_download_model(watphy, station, survey).dict(),
        no2=watphy.watnut.no2 if watphy.watnut else None,
        no3=watphy.watnut.no3 if watphy.watnut else None,
        po4=watphy.watnut.po4 if watphy.watnut else None,
        ptot=watphy.watnut.ptot if watphy.watnut else None,
        sio3=watphy.watnut.sio3 if watphy.watnut else None,
        ph=watphy.watchem1.ph if watphy.watchem1 else None,
        chla=watphy.watchl.chla if watphy.watchl else None,
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
        **get_table_data(
            sedphy.sedpol1,
            fields_to_ignore=[
                'sedphy_code'
            ]
        ),
        **get_table_data(
            sedphy.sedpol2,
            fields_to_ignore=[
                'sedphy_code'
            ]
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
            sedphy.sedchem1,
            fields_to_ignore=[
                'sedphy_code'
            ]
        ),
        **get_table_data(
            sedphy.sedchem2,
            fields_to_ignore=[
                'sedphy_code'
            ]
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
            currents,
            fields_to_ignore=[
                'station_id',
                'spldattim'
            ]
        ),
        spldattim=currents.spldattim.strftime("%m/%d/%Y %H:%M:%S") if currents.spldattim else ''
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
