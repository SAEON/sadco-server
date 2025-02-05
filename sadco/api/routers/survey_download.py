from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func
from starlette.status import HTTP_404_NOT_FOUND

from sadco.api.lib.auth import Authorize, Authorized
from sadco.api.lib.download import get_csv_data, audit_download_request
from sadco.const import SADCOScope, DataType, SurveyType as ConstSurveyType
from sadco.db import Session
from sadco.db.models import (Watphy, Survey, Station, Sedphy, Weather, Currents, CurMooring, CurDepth, CurData,
                             Inventory, WetStation, WetPeriod, WavStation, WetData, WavData, CurWatphy, EDMInstrument2,
                             Watnut, Watchem1, Watchl, Watpol1, Watpol2, Watchem2, Sedpol1, Sedpol2, Sedchem1, Sedchem2)

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
            *get_hydro_water_fields()
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
            *get_hydro_water_fields(),
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
            *get_hydro_water_fields(),
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
        select(
            *get_hydro_water_fields(),
            Watchem1.dic,
            Watchem1.doc,
            Watchem1.fluoride,
            Watchem1.iodene,
            Watchem1.iodate,
            Watchem1.kjn,
            Watchem1.nh3,
            Watchem1.nitrogen,
            Watchem1.oxa,
            Watchem1.ph,
            Watchem2.calcium,
            Watchem2.cesium,
            Watchem2.hydrocarbons,
            Watchem2.magnesium,
            Watchem2.pah,
            Watchem2.potassium,
            Watchem2.rubidium,
            Watchem2.sodium,
            Watchem2.strontium,
            Watchem2.so4,
            Watchem2.sussol
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Watphy, Watphy.station_id == Station.station_id)
        .outerjoin(Watchem1, Watphy.code == Watchem1.watphy_code)
        .outerjoin(Watchem2, Watphy.code == Watchem2.watphy_code)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_water_nutrients_items(survey_id: str) -> list:
    stmt = (
        select(
            *get_hydro_water_fields(),
            Watnut.no2,
            Watnut.no3,
            Watnut.p,
            Watnut.po4,
            Watnut.ptot,
            Watnut.sio3,
            Watnut.sio4,
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Watphy, Watphy.station_id == Station.station_id)
        .join(Watnut, Watphy.code == Watnut.watphy_code)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique().all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_sediment_items(survey_id: str) -> list:
    stmt = (
        select(
            *get_hydro_sediment_fields(),
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Sedphy, Sedphy.station_id == Station.station_id)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique().all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_sediment_pollution_items(survey_id: str) -> list:
    stmt = (
        select(
            *get_hydro_sediment_fields(),
            Sedpol1.arsenic,
            Sedpol1.cadmium,
            Sedpol1.chromium,
            Sedpol1.cobalt,
            Sedpol1.copper,
            Sedpol1.iron,
            Sedpol1.lead,
            Sedpol1.manganese,
            Sedpol1.mercury,
            Sedpol1.nickel,
            Sedpol1.selenium,
            Sedpol1.zinc,
            Sedpol2.aluminium,
            Sedpol2.antimony,
            Sedpol2.bismuth,
            Sedpol2.molybdenum,
            Sedpol2.silver,
            Sedpol2.titanium,
            Sedpol2.vanadium
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Sedphy, Sedphy.station_id == Station.station_id)
        .outerjoin(Sedpol1, Sedpol1.sedphy_code == Sedphy.code)
        .outerjoin(Sedpol2, Sedpol2.sedphy_code == Sedphy.code)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique().all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_sediment_chemistry_items(survey_id: str) -> list:
    stmt = (
        select(
            *get_hydro_sediment_fields(),
            Sedchem1.fluoride,
            Sedchem1.kjn,
            Sedchem1.oxa,
            Sedchem1.toc,
            Sedchem1.ptot,
            Sedchem2.calcium,
            Sedchem2.magnesium,
            Sedchem2.potassium,
            Sedchem2.sodium,
            Sedchem2.strontium,
            Sedchem2.so3
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Sedphy, Sedphy.station_id == Station.station_id)
        .outerjoin(Sedchem1, Sedchem1.sedphy_code == Sedphy.code)
        .outerjoin(Sedchem2, Sedchem2.sedphy_code == Sedphy.code)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique().all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_hydro_weather_items(survey_id: str) -> list:
    stmt = (
        select(
            *get_hydro_fields(),
            Weather.nav_equip_type,
            Weather.atmosph_pres,
            Weather.surface_tmp,
            Weather.drybulb,
            Weather.wetbulb,
            Weather.cloud,
            Weather.vis_code,
            Weather.weather_code,
            Weather.water_color,
            Weather.transparency,
            Weather.wind_dir,
            Weather.wind_speed,
            Weather.swell_dir,
            Weather.swell_height,
            Weather.swell_period,
            Weather.dupflag
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Weather, Weather.station_id == Station.station_id)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique().all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_hydro_currents_items(survey_id: str) -> list:
    stmt = (
        select(
            *get_hydro_fields(),
            Currents.subdes,
            Currents.spldattim,
            Currents.spldep,
            Currents.current_dir,
            Currents.current_speed,
            Currents.perc_good
        )
        .join(Survey, Station.survey_id == Survey.survey_id)
        .join(Currents, Currents.station_id == Station.station_id)
        .where(Survey.survey_id == survey_id.replace('-', '/'))
    )

    if not (results := Session.execute(stmt).unique().all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_hydro_water_fields() -> list:
    return [
        *get_hydro_fields(),
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


def get_hydro_sediment_fields() -> list:
    return [
        *get_hydro_fields(),
        Sedphy.subdes,
        Sedphy.spldattim,
        Sedphy.spldep,
        Sedphy.spldis,
        Sedphy.splvol,
        Sedphy.sievsz,
        Sedphy.kurt,
        Sedphy.skew,
        Sedphy.meanpz,
        Sedphy.medipz,
        Sedphy.pctsat,
        Sedphy.pctsil,
        Sedphy.permty,
        Sedphy.porsty,
        Sedphy.dwf,
        Sedphy.cod
    ]


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
    ]
