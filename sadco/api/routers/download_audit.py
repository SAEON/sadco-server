from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND
from sadco.const import SADCOScope
from sadco.api.lib.auth import Authorize, Authorized
from sadco.api.lib.paging import Page, Paginator
from sadco.api.models import DownloadAuditModel
from sadco.db.models import DownloadAudit
from sadco.db import Session
from sqlalchemy import select

router = APIRouter()


@router.get(
    '/my_downloads',
    response_model=Page[DownloadAuditModel]
)
async def list_surveys(
        paginator: Paginator = Depends(),
        auth: Authorized = Depends(Authorize(SADCOScope.DOWNLOAD_READ))
):
    stmt = (select(
        DownloadAudit
    ).where(
        DownloadAudit.client_id == auth.client_id,
        DownloadAudit.user_id == auth.user_id
    ))

    return paginator.paginate(
        stmt,
        lambda row: DownloadAuditModel(
            timestamp=row.DownloadAudit.timestamp,
            survey_type=row.DownloadAudit.survey_type,
            parameters=row.DownloadAudit.parameters
        ),
        sort='timestamp',
    )


@router.get(
    '/all_downloads',
    response_model=Page[DownloadAuditModel],
    dependencies=[Depends(Authorize(SADCOScope.DOWNLOAD_ADMIN))]
)
async def list_surveys(
        paginator: Paginator = Depends()
):
    stmt = select(DownloadAudit)

    return paginator.paginate(
        stmt,
        lambda row: DownloadAuditModel(
            timestamp=row.DownloadAudit.timestamp,
            survey_type=row.DownloadAudit.survey_type,
            parameters=row.DownloadAudit.parameters
        ),
        sort='timestamp',
    )
