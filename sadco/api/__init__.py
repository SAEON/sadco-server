from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from sadco.api.routers import survey, survey_download, vos_survey
from sadco.db import Session
from odp.version import VERSION

app = FastAPI(
    title="SADCO API",
    description="SADCO | SADCO Data Api",
    version=VERSION,
    docs_url='/swagger',
    redoc_url='/docs',
)

app.include_router(survey.router, prefix='/survey', tags=['Survey'])
app.include_router(survey_download.router, prefix='/survey/download', tags=['Survey', 'Download'])

app.include_router(vos_survey.router, prefix='/vos_survey', tags=['Survey'])

app.add_middleware(
    CORSMiddleware,
    # allow_origins=config.ODP.API.ALLOW_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def db_middleware(request: Request, call_next):
    try:
        response: Response = await call_next(request)
        if 200 <= response.status_code < 400:
            Session.commit()
        else:
            Session.rollback()
    finally:
        Session.remove()

    return response
