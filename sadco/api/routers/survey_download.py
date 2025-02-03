from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_404_NOT_FOUND

from sadco.api.lib.auth import Authorize, Authorized
from sadco.api.lib.download import get_csv_data, get_table_data, audit_download_request
from sadco.api.models import (HydroDownloadModel, HydroWaterPhysicalDownloadModel,
                              HydroWaterChemistryDownloadModel, HydroSedimentPhysicalDownloadModel,
                              HydroWaterNutrientsDownloadModel, HydroSedimentPollutionDownloadModel,
                              HydroSedimentChemistryDownloadModel, HydroWeatherDownloadModel,
                              HydroCurrentsDownloadModel)
from sadco.const import SADCOScope, DataType, SurveyType as ConstSurveyType
from sadco.db import Session
from sadco.db.models import (Watphy, Survey, Station, Sedphy, Weather, Currents, CurMooring, CurDepth, CurData,
                             Inventory, WetStation, WetPeriod, WavStation, WetData, WavData, CurWatphy, EDMInstrument2,
                             Watnut, Watchem1, Watchl, Watpol1, Watpol2)

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

    audit_download_request(auth, zipped_csv_data.get('file_info'), ConstSurveyType.UTR.value, survey_id=survey_id,
                           data_type=data_type)

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

    audit_download_request(auth, zipped_csv_data.get('file_info'), ConstSurveyType.CURRENTS.value, survey_id=survey_id,
                           data_type=data_type)

    return zipped_csv_data.get('zipped_response')


def get_currents_items(survey_id: str) -> list:
    stmt = (
        select(
            CurDepth.spldep.label("sampling_depth"),
            EDMInstrument2.name.label("instrument"),
            CurDepth.time_interval,
            CurDepth.passkey,
            CurDepth.parameters,
            CurData.datetime,
            CurData.speed,
            CurData.direction,
            CurData.temperature,
            CurData.vert_velocity,
            CurData.f_speed_9,
            CurData.f_direction_9,
            CurData.f_speed_14,
            CurData.f_direction_14,
            CurData.pressure,
            CurWatphy.ph,
            CurWatphy.salinity,
            CurWatphy.dis_oxy.label("dissolved_oxygen")
        )
        .join(CurMooring, CurDepth.mooring_code == CurMooring.code)
        .join(CurData, CurDepth.code == CurData.depth_code)
        .outerjoin(CurWatphy, CurData.code == CurWatphy.data_code)
        .outerjoin(EDMInstrument2, CurDepth.instrument_number == EDMInstrument2.code)
        .where(CurMooring.survey_id == survey_id.replace("-", "/"))
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


@router.get(
    f"/{ConstSurveyType.WEATHER.value}/{{survey_id}}",
    response_class=StreamingResponse
)
async def download_weather_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type'),
        auth: Authorized = Depends(Authorize(SADCOScope.WEATHER_DOWNLOAD))
):
    items = get_weather_items(survey_id)

    zipped_csv_data: dict = get_csv_data(items, survey_id, data_type)

    audit_download_request(auth, zipped_csv_data.get('file_info'), ConstSurveyType.WEATHER.value, survey_id=survey_id,
                           data_type=data_type)

    return zipped_csv_data.get('zipped_response')


def get_weather_items(survey_id: str) -> list:
    stmt = (
        select(
            WetStation.name.label("station_name"),
            WetStation.latitude,
            WetStation.longitude,
            WetPeriod.height_msl.label("msl_height"),
            WetPeriod.height_surface.label("surface_height"),
            WetData.date_time.label("record_date"),
            WetData.air_temp_ave.label("ave_air_temp"),
            WetData.air_temp_min.label("min_air_temp"),
            WetData.air_temp_min_time.label("min_air_temp_time"),
            WetData.air_temp_max.label("max_air_temp"),
            WetData.air_temp_max_time.label("max_air_temp_time"),
            WetData.barometric_pressure,
            WetData.fog,
            WetData.rainfall,
            WetData.relative_humidity,
            WetData.solar_radiation,
            WetData.solar_radiation_max.label("max_solar_radiation"),
            WetData.wind_dir.label("wind_direction"),
            WetData.wind_speed_ave.label("ave_wind_speed"),
            WetData.wind_speed_min.label("min_wind_speed"),
            WetData.wind_speed_max.label("max_wind_speed"),
            WetData.wind_speed_max_time.label("max_wind_speed_time"),
            WetData.wind_speed_max_length.label("max_wind_speed_duration"),
            WetData.wind_speed_max_dir.label("max_wind_speed_direction"),
            WetData.wind_speed_std.label("max_wind_speed_standard_deviation"),
        )
        .join(Inventory.wet_stations)
        .join(WetStation.wet_periods)
        .join(WetPeriod.wet_data_list)
        .where(Inventory.survey_id == survey_id.replace("-", "/"))
    )

    results = Session.execute(stmt).all()
    if not results:
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


@router.get(
    f"/{ConstSurveyType.WAVES.value}/{{survey_id}}",
    response_class=StreamingResponse
)
async def download_waves_survey_data(
        survey_id: str,
        data_type: str = Query(None, title='Data Type'),
        auth: Authorized = Depends(Authorize(SADCOScope.WAVES_DOWNLOAD))
):
    items = get_waves_items(survey_id)

    zipped_csv_data: dict = get_csv_data(items, survey_id, data_type)

    audit_download_request(auth, zipped_csv_data.get('file_info'), ConstSurveyType.WAVES.value, survey_id=survey_id,
                           data_type=data_type)

    return zipped_csv_data.get('zipped_response')


def get_waves_items(survey_id: str) -> list:
    stmt = (
        select(
            WavStation.latitude,
            WavStation.longitude,
            WavStation.instrument_depth,
            WavStation.name.label("station_name"),
            WavStation.water_depth,
            WavData.date_time,
            WavData.number_readings,
            WavData.record_length,
            WavData.deltaf,
            WavData.deltat,
            WavData.frequency,
            WavData.qp,
            WavData.tb,
            WavData.te,
            WavData.wap,
            WavData.eps,
            WavData.hmo,
            WavData.h1,
            WavData.hs,
            WavData.hmax,
            WavData.tc,
            WavData.tp,
            WavData.tz,
            WavData.ave_direction,
            WavData.ave_spreading,
            WavData.instrument_code,
            WavData.mean_direction,
            WavData.mean_spreading,
        )
        .join(Inventory.wav_stations)
        .join(WavStation.wav_data_list)
        .where(Inventory.survey_id == survey_id.replace("-", "/"))
    )

    if not (results := Session.execute(stmt).all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


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

    audit_download_request(auth, zipped_csv_data.get('file_info'),
                           ConstSurveyType.HYDRO.value,
                           survey_id=survey_id, data_type=data_type)

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
        select(
            *get_hydro_fields()
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Watphy, Watphy.station_id == Station.station_id)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_water_nutrients_and_chemistry_items(survey_id: str) -> list:
    stmt = (
        select(
            *get_hydro_fields(),
            Watnut.no2,
            Watnut.no3,
            Watnut.po4,
            Watnut.ptot,
            Watnut.sio3,
            Watchem1.ph,
            Watchl.chla
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Watphy, Watphy.station_id == Station.station_id)
        .outerjoin(Watchl, Watphy.code == Watchl.watphy_code)
        .outerjoin(Watnut, Watphy.code == Watnut.watphy_code)
        .outerjoin(Watchem1, Watphy.code == Watchem1.watphy_code)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique().all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_water_pollution_items(survey_id: str) -> list:
    stmt = (
        select(
            *get_hydro_fields(),
            Watpol1.arsenic,
            Watpol1.cadmium,
            Watpol1.chromium,
            Watpol1.cobalt,
            Watpol1.copper,
            Watpol1.iron,
            Watpol1.lead,
            Watpol1.manganese,
            Watpol1.mercury,
            Watpol1.nickel,
            Watpol1.selenium,
            Watpol1.zinc,
            Watpol2.aluminium,
            Watpol2.antimony,
            Watpol2.bismuth,
            Watpol2.molybdenum,
            Watpol2.silver,
            Watpol2.titanium,
            Watpol2.vanadium
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Watphy, Watphy.station_id == Station.station_id)
        .outerjoin(Watpol1, Watphy.code == Watpol1.watphy_code)
        .outerjoin(Watpol2, Watphy.code == Watpol2.watphy_code)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique().all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


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


def get_hydro_fields() -> list:
    return [
        Station.survey_id,
        Station.latitude,
        Station.longitude,
        func.date(Station.date_start).label('date'),
        Station.stnnam.label('station_name'),
        Station.station_id,
        Survey.planam.label('platform_name'),
        Station.max_spldep.label('max_sampling_depth'),
        Watphy.subdes,
        Watphy.spldattim,
        Watphy.spldep,
        Watphy.filtered,
        Watphy.disoxygen,
        Watphy.salinity,
        Watphy.temperature,
        Watphy.sound_flag,
        Watphy.soundv,
        Watphy.turbidity,
        Watphy.pressure,
        Watphy.fluorescence,
    ]


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
