from fastapi import APIRouter, Depends
from sadco.const import SADCOScope
from sadco.api.lib.auth import Authorize, Authorized
from sadco.api.lib.paging import Page, Paginator
from sadco.api.models import DownloadAuditModel
from sadco.db.models import DownloadAudit
from sqlalchemy import select
import json

router = APIRouter()


@router.get(
    '/my_downloads',
    response_model=Page[DownloadAuditModel]
)
async def my_downloads(
        paginator: Paginator = Depends(),
        auth: Authorized = Depends(Authorize(SADCOScope.DOWNLOAD_READ))
):
    stmt = (select(
        DownloadAudit
    ).where(
        DownloadAudit.client_id == auth.client_id,
        DownloadAudit.user_id == auth.user_id
    ))

    return get_paginated_downloads(paginator, stmt)


@router.get(
    '/all_downloads',
    response_model=Page[DownloadAuditModel],
    dependencies=[Depends(Authorize(SADCOScope.DOWNLOAD_ADMIN))]
)
async def all_downloads(
        paginator: Paginator = Depends()
):
    stmt = select(DownloadAudit)

    return get_paginated_downloads(paginator, stmt)


def get_paginated_downloads(paginator, stmt):
    return paginator.paginate(
        stmt,
        lambda row: DownloadAuditModel(
            timestamp=row.DownloadAudit.timestamp.strftime("%d/%m/%Y %H:%M"),
            survey_type=row.DownloadAudit.survey_type,
            parameters=json.loads(row.DownloadAudit.parameters if row.DownloadAudit.parameters else '{}'),
        ),
        sort='timestamp',
    )
