from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func, union
from starlette.status import HTTP_404_NOT_FOUND

from sadco.api.lib.auth import Authorize, Authorized
from sadco.api.lib.download import get_csv_data, audit_download_request
from sadco.api.models import VosSurveySearchResult
from sadco.const import SADCOScope, SurveyType
from sadco.db import Session
from sadco.db.models import VosMain, VosArch, VosArch2, VosMain2, VosMain68

router = APIRouter()


@router.get(
    '/vos_surveys/search',
    response_model=VosSurveySearchResult,
    dependencies=[Depends(Authorize(SADCOScope.VOS_READ))],
)
async def list_surveys(
        north_bound: float = Query(None, title='North bound latitude', ge=-90, le=90),
        south_bound: float = Query(None, title='South bound latitude', ge=-90, le=90),
        east_bound: float = Query(None, title='East bound longitude', ge=-180, le=180),
        west_bound: float = Query(None, title='West bound longitude', ge=-180, le=180),
        start_date: date = Query(None, title='Date range start'),
        end_date: date = Query(None, title='Date range end'),
        exclusive_region: bool = Query(False, title='Exclude partial spatial matches'),
        exclusive_interval: bool = Query(False, title='Exclude partial temporal matches'),
):
    stmt_vos_union = get_vos_union_statement(
        north_bound,
        south_bound,
        east_bound,
        west_bound,
        start_date,
        end_date,
        exclusive_region,
        exclusive_interval,
        is_count_only=True
    )

    total = Session.execute(
        select(func.sum(stmt_vos_union.c.vos_record_count))
    ).scalar_one()

    return VosSurveySearchResult(
        total=total
    )


@router.get(
    "/download",
    response_class=StreamingResponse
)
async def download_vos_survey_data(
        north_bound: float = Query(None, title='North bound latitude', ge=-90, le=90),
        south_bound: float = Query(None, title='South bound latitude', ge=-90, le=90),
        east_bound: float = Query(None, title='East bound longitude', ge=-180, le=180),
        west_bound: float = Query(None, title='West bound longitude', ge=-180, le=180),
        start_date: date = Query(None, title='Date range start'),
        end_date: date = Query(None, title='Date range end'),
        exclusive_region: bool = Query(False, title='Exclude partial spatial matches'),
        exclusive_interval: bool = Query(False, title='Exclude partial temporal matches'),
        auth: Authorized = Depends(Authorize(SADCOScope.VOS_DOWNLOAD))
):
    stmt_vos_union = get_vos_union_statement(
        north_bound,
        south_bound,
        east_bound,
        west_bound,
        start_date,
        end_date,
        exclusive_region,
        exclusive_interval
    )

    items = get_vos_items(stmt_vos_union)

    zipped_csv_data: dict = get_csv_data(items, 'VOS', 'VOS')

    audit_download_request(
        auth,
        zipped_csv_data.get('file_info'),
        SurveyType.VOS.value,
        north_bound=north_bound,
        south_bound=south_bound,
        east_bound=east_bound,
        west_bound=west_bound,
        start_date=start_date,
        end_date=end_date,
        exclusive_region=exclusive_region,
        exclusive_interval=exclusive_interval
    )

    return zipped_csv_data.get('zipped_response')


def get_vos_items(statement) -> list:
    if not (results := Session.execute(statement).all()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return results


def get_vos_union_statement(
        north_bound: float,
        south_bound: float,
        east_bound: float,
        west_bound: float,
        start_date: date,
        end_date: date,
        exclusive_region: bool,
        exclusive_interval: bool,
        is_count_only: bool = False
):
    """
    Build a statement that either counts or return the data for all the VOS tables based on the filters
    @param is_count_only: boolean parameter to control weather to return a statement that just counts the records or
    returns the actual data
    """
    vos_models = [VosMain, VosMain2, VosMain68, VosArch, VosArch2]
    vos_statements = []

    for vos_model in vos_models:
        stmt = get_statement(vos_model, is_count_only=is_count_only)

        stmt = get_filtered_statement(
            stmt,
            vos_model,
            north_bound,
            south_bound,
            east_bound,
            west_bound,
            start_date,
            end_date,
            exclusive_region,
            exclusive_interval
        )

        vos_statements.append(stmt)

    return union(*vos_statements)


def get_statement(vos_model, is_count_only: bool = False):
    if is_count_only:
        return (
            select(func.count().label('vos_record_count'))
            .select_from(
                vos_model
            )
        )
    else:
        return select(
            -vos_model.latitude,
            vos_model.longitude,
            vos_model.date_time,
            vos_model.daynull,
            vos_model.callsign,
            vos_model.country,
            vos_model.platform,
            vos_model.data_id,
            vos_model.quality_control,
            vos_model.source1,
            vos_model.load_id,
            vos_model.dupflag,
            vos_model.atmospheric_pressure,
            vos_model.surface_temperature,
            vos_model.surface_temperature_type,
            vos_model.drybulb,
            vos_model.wetbulb,
            vos_model.wetbulb_ice,
            vos_model.dewpoint,
            vos_model.cloud_amount,
            vos_model.cloud1,
            vos_model.cloud2,
            vos_model.cloud3,
            vos_model.cloud4,
            vos_model.cloud5,
            vos_model.visibility_code,
            vos_model.weather_code,
            vos_model.swell_direction,
            vos_model.swell_height,
            vos_model.swell_period,
            vos_model.wave_height,
            vos_model.wave_period,
            vos_model.wind_direction,
            vos_model.wind_speed,
            vos_model.wind_speed_type,
        )


def get_filtered_statement(
        stmt,
        vos_model,
        north_bound: float,
        south_bound: float,
        east_bound: float,
        west_bound: float,
        start_date: date,
        end_date: date,
        exclusive_region: bool,
        exclusive_interval: bool
):
    """
    Apply the filters and return the filtered statement
    """
    if exclusive_region:
        # We need to use the negation of North and South because they come from the DB as south
        if north_bound is not None:
            stmt = stmt.where(-vos_model.latitude <= north_bound)

        if south_bound is not None:
            stmt = stmt.where(-vos_model.latitude >= south_bound)

        if east_bound is not None:
            stmt = stmt.where(vos_model.longitude <= east_bound)

        if west_bound is not None:
            stmt = stmt.where(vos_model.longitude >= west_bound)

    else:
        if north_bound is not None:
            stmt = stmt.where(-vos_model.latitude <= north_bound)

        if south_bound is not None:
            stmt = stmt.where(-vos_model.latitude >= south_bound)

        if east_bound is not None:
            stmt = stmt.where(vos_model.longitude <= east_bound)

        if west_bound is not None:
            stmt = stmt.where(vos_model.longitude >= west_bound)

    if exclusive_interval:
        if start_date:
            stmt = stmt.where(vos_model.date_time >= start_date)

        if end_date:
            stmt = stmt.where(vos_model.date_time <= end_date)

    else:
        if start_date:
            stmt = stmt.where(vos_model.date_time >= start_date)

        if end_date:
            stmt = stmt.where(vos_model.date_time <= end_date)

    return stmt
