from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func, union
from starlette.status import HTTP_404_NOT_FOUND

from sadco.api.lib.download import get_zipped_csv_response
from sadco.db.models import VosMain, VosArch, VosArch2, VosMain2, VosMain68
from sadco.api.models import VosSurveySearchResult, VosSurveyDownloadModel
from sadco.api.lib.auth import Authorize
from sadco.db import Session
from sadco.const import SADCOScope

router = APIRouter()


@router.get(
    '/vos_surveys/search',
    response_model=VosSurveySearchResult,
    dependencies=[Depends(Authorize(SADCOScope.SURVEYS_READ))],
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
        exclusive_interval
    )

    total = Session.execute(
        select(func.count())
        .select_from(stmt_vos_union.subquery())
    ).scalar_one()

    return VosSurveySearchResult(
        total=total
    )


@router.get(
    "/download",
    response_class=StreamingResponse,
    dependencies=[Depends(Authorize(SADCOScope.UTR_DOWNLOAD))]
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

    return get_zipped_csv_response(items, 'VOS', 'VOS')


def get_vos_items(statement) -> list:
    if not (results := Session.execute(statement).unique()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return [
        VosSurveyDownloadModel(
            **row._mapping
        ).dict()
        for row in results
    ]


def get_vos_union_statement(
        north_bound: float,
        south_bound: float,
        east_bound: float,
        west_bound: float,
        start_date: date,
        end_date: date,
        exclusive_region: bool,
        exclusive_interval: bool
):
    vos_models = [VosMain, VosMain2, VosMain68, VosArch, VosArch2]
    vos_statements = []

    for vos_model in vos_models:
        stmt = (
            select(
                vos_model
            )
        )

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
