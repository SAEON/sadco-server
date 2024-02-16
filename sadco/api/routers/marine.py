from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import load_only, joinedload
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from sadco.api.lib.paging import Page, Paginator
from sadco.db.models import (Inventory, Planam, Scientists, Institutes, SurveyType, Watphy, Watnut, Watpol1, Watpol2,
                             Sedphy, Sedpol1, Sedpol2, Sedpol2, Sedchem1, Sedchem2, Watchem1, Watchem2)
from sadco.api.models import (SurveyModel, SurveyListItemModel, StationModel, WaterModel,
                              WaterNutrientsModel, WaterPollutionModel, WaterCurrentsModel, WaterChemistryModel,
                              DataTypesModel)

from sadco.db import Session
from sadco.db.models import Survey, Station
from sadco.db.models.watchem import Watchem1

router = APIRouter()


@router.get(
    '/surveys',
    response_model=Page[SurveyModel]
)
async def list_surveys(
        paginator: Paginator = Depends(),
):
    stmt = (
        select(
            Inventory
        )
    )

    return paginator.paginate(
        stmt,
        lambda row: SurveyListItemModel(
            id=row.Inventory.survey_id,
            project_name=row.Inventory.project_name,
            station_name=row.Inventory.cruise_name,
            platform_name=row.Inventory.planam.name,
            chief_scientist=(row.Inventory.scientist_1.f_name + ' ' + row.Inventory.scientist_1.surname),
            institute=row.Inventory.institute.name,
            date_start=row.Inventory.date_start,
            date_end=row.Inventory.date_end,
            survey_type=row.Inventory.survey_type.name
        ),
        sort='survey_id',
    )


@router.get(
    '/surveys/{survey_id}',
    response_model=SurveyModel
)
async def get_survey(
        survey_id: str
):
    stmt = (
        select(
            Inventory
        ).
        filter(
            Inventory.survey_id == survey_id.replace('-', '/')
        )
    )

    if not (result := Session.execute(stmt).one_or_none()):
        raise HTTPException(HTTP_404_NOT_FOUND)

    return SurveyModel(
        id=result.Inventory.survey_id,
        project_name=result.Inventory.project_name,
        station_name=result.Inventory.cruise_name,
        platform_name=result.Inventory.planam.name,
        chief_scientist=(result.Inventory.scientist_1.f_name + ' ' + result.Inventory.scientist_1.surname),
        institute=result.Inventory.institute.name,
        date_start=result.Inventory.date_start,
        date_end=result.Inventory.date_end,
        lat_north=result.Inventory.lat_north,
        lat_south=result.Inventory.lat_south,
        long_west=result.Inventory.long_west,
        long_east=result.Inventory.long_east,
        survey_type=result.Inventory.survey_type.name,
        stations=[
            StationModel(
                latitude=station.latitude,
                longitude=station.longitude
            ) for station in result.Inventory.survey.stations
        ],
        data_types=get_data_types(result.Inventory)
    )


def get_data_types(inventory: Inventory) -> DataTypesModel:
    data_types_model = DataTypesModel()

    # stmt = (
    #     select(
    #         func.count(Watphy.code).label('water_count'),
    #         func.count(Watnut.watphy_code).label('nutrients_count'),
    #         func.count(Watpol1.watphy_code).label('pollution_count')
    #     ).
    #     select_from(Survey).
    #     join(Station).
    #     outerjoin(Watphy).
    #     outerjoin(Watnut).
    #     outerjoin(Watpol1).
    #     where(Survey.survey_id == inventory.survey_id)
    # )
    #
    # result = Session.execute(stmt).one_or_none()
    #
    # if result.water_count > 0:
    #     water_model = WaterModel(
    #         record_count=result.water_count
    #     )
    #
    #     water_model.water_chemistry = get_water_chemistry_model(inventory)
    #
    #     if result.nutrients_count > 0:
    #         water_model.water_nutrients = WaterNutrientsModel(
    #             record_count=result.nutrients_count
    #         )

        # data_types_model.water = water_model

    data_types_model.water = get_water_model2(inventory)

    return data_types_model


def get_water_chemistry_model(inventory: Inventory) -> WaterChemistryModel:
    stmt = (
        select(
            func.count(Watphy.code)
        ).
        select_from(Survey).
        join(Station).
        join(Watphy).
        outerjoin(Watchem1).
        outerjoin(Watchem2).
        where(Survey.survey_id == inventory.survey_id)
    )

    result = Session.execute(stmt).scalar()

    if result > 0:
        return WaterChemistryModel(
            record_count=result
        )

    return WaterChemistryModel()


def get_water_model2(inventory: Inventory) -> WaterModel:
    water_count = 0
    water_chemistry_count = 0
    water_pollution_count = 0
    water_nutrients_count = 0

    for station in inventory.survey.stations:
        for watphy in station.watphy_list:
            water_count += 1

            if watphy.watchem1 or watphy.watchem2:
                water_chemistry_count += 1

            if watphy.watpol1 or watphy.watpol2:
                water_pollution_count += 1

            if watphy.watnut:
                water_nutrients_count += 1

    return WaterModel(
        water_pollution=WaterPollutionModel(
            record_count=water_pollution_count
        ),
        water_chemistry=WaterChemistryModel(
            record_count=water_chemistry_count
        ),
        water_nutrients=WaterNutrientsModel(
            record_count=water_nutrients_count
        )
    )
