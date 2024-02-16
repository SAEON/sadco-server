from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from sadco.api.routers import marine
from sadco.db import Session
from odp.version import VERSION

app = FastAPI(
    title="SADCO API",
    description="SADCO | SADCO Data Api",
    version=VERSION,
    docs_url='/swagger',
    redoc_url='/docs',
)

app.include_router(marine.router, prefix='/marine', tags=['Survey'])

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
