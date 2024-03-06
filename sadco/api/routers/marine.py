from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import load_only, joinedload
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from sadco.api.lib.paging import Page, Paginator
from sadco.db.models import (Inventory, Planam, Scientists, Institutes, SurveyType, Watphy, Watnut, Watpol1, Watpol2,
                             Sedphy, Sedpol1, Sedpol2, Sedpol2, Sedchem1, Sedchem2, Watchem1, Watchem2, Watcurrents,
                             Weather, Currents, Survey, Station)
from sadco.api.models import (SurveyModel, SurveyListItemModel, StationModel, WaterModel,
                              WaterNutrientsModel, WaterPollutionModel, WaterCurrentsModel, WaterChemistryModel,
                              DataTypesModel, SedimentModel, SedimentPollutionModel, SedimentChemistryModel,
                              CurrentsModel, WeatherModel)

from sadco.db import Session
from sadco.db.models.watchem import Watchem1

router = APIRouter()


@router.get(
    '/surveys',
    response_model=Page[SurveyListItemModel]
)
async def list_surveys(
        paginator: Paginator = Depends(),
):
    stmt = (
        select(
            Inventory
        ).
        options(
            joinedload(Inventory.planam),
            joinedload(Inventory.scientist_1),
            joinedload(Inventory.scientist_2),
            joinedload(Inventory.institute),
            joinedload(Inventory.survey_type)
        )
    )

    return paginator.paginate(
        stmt,
        lambda row: SurveyListItemModel(
            id=row.Inventory.survey_id,
            project_name=row.Inventory.project_name,
            station_name=row.Inventory.cruise_name,
            platform_name=row.Inventory.planam.name if row.Inventory.planam else '',
            chief_scientist=get_chief_scientist(row.Inventory),
            institute=row.Inventory.institute.name if row.Inventory.institute else '',
            date_start=row.Inventory.date_start,
            date_end=row.Inventory.date_end,
            survey_type=row.Inventory.survey_type.name
        ),
        sort='survey_id',
    )


def get_chief_scientist(inventory: Inventory) -> str:
    if inventory.scientist_1:
        return (inventory.scientist_1.f_name.strip() + ' ' + inventory.scientist_1.surname.strip()).strip()

    return ''


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
        chief_scientist=(
                result.Inventory.scientist_1.f_name.strip() + ' ' + result.Inventory.scientist_1.surname.strip()).strip(),
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
        data_types=get_data_types(result.Inventory.survey_id)
    )


def get_data_types(survey_id: str) -> DataTypesModel:
    """
    Get the datat types and their record counts for a given survey.
    """
    data_types_model = DataTypesModel()

    stmt = (
        select(
            func.count(Currents.station_id).label('currents_count'),
            func.count(Weather.station_id).label('weather_count')
        ).
        select_from(Survey).
        join(Station).
        outerjoin(Currents).
        outerjoin(Weather).
        where(Survey.survey_id == survey_id)
    )

    result = Session.execute(stmt).one_or_none()

    if result.currents_count > 0:
        data_types_model.currents = CurrentsModel(
            record_count=result.currents_count
        )

    if result.weather_count > 0:
        data_types_model.weather = WeatherModel(
            record_count=result.weather_count
        )

    water_model = get_water_model(survey_id)

    if water_model.record_count > 0:
        data_types_model.water = water_model

    sediment_model = get_sediment_model(survey_id)

    if sediment_model.record_count > 0:
        data_types_model.sediment = sediment_model

    return data_types_model


def get_water_model(survey_id: str) -> WaterModel:
    stmt = (
        select(
            func.count(Watphy.code).label('water_count'),
            func.count(Watnut.watphy_code).label('nutrients_count'),
            func.count(Watcurrents.watphy_code).label('currents_count')
        ).
        select_from(Survey).
        join(Station).
        join(Watphy).
        outerjoin(Watnut).
        outerjoin(Watcurrents).
        where(Survey.survey_id == survey_id)
    )

    result = Session.execute(stmt).one_or_none()

    water_model = WaterModel(
        record_count=0
    )

    if result.water_count > 0:
        water_model.record_count = result.water_count

        water_chemistry_count = get_watphy_joined_count(Watchem1, Watchem2, survey_id)
        if water_chemistry_count > 0:
            water_model.water_chemistry = WaterChemistryModel(
                record_count=water_chemistry_count
            )

        water_pollution_count = get_watphy_joined_count(Watpol1, Watpol2, survey_id)
        if water_pollution_count > 0:
            water_model.water_pollution = WaterPollutionModel(
                record_count=water_pollution_count
            )

        if result.nutrients_count > 0:
            water_model.water_nutrients = WaterNutrientsModel(
                record_count=result.nutrients_count
            )

        if result.currents_count > 0:
            water_model.water_currents = WaterCurrentsModel(
                record_count=result.currents_count
            )

    return water_model


def get_sediment_model(survey_id: str) -> SedimentModel:
    stmt = (
        select(
            func.count(Sedphy.code)
        ).
        select_from(Survey).
        join(Station).
        join(Sedphy).
        where(Survey.survey_id == survey_id)
    )

    sediment_count = Session.execute(stmt).scalar()

    sediment_model = SedimentModel(
        record_count=0
    )

    if sediment_count > 0:
        sediment_model.record_count = sediment_count

        sediment_chemistry_count = get_sedphy_joined_count(Sedchem1, Sedchem2, survey_id)
        if sediment_chemistry_count > 0:
            sediment_model.sediment_chemistry = SedimentChemistryModel(
                record_count=sediment_chemistry_count
            )

        sediment_pollution_count = get_sedphy_joined_count(Sedpol1, Sedpol2, survey_id)
        if sediment_pollution_count > 0:
            sediment_model.sediment_pollution = SedimentPollutionModel(
                record_count=sediment_pollution_count
            )

    return sediment_model


def get_watphy_joined_count(child_1, child_2, survey_id: str) -> int:
    return get_joined_count(child_1, child_2, Watphy, 'watphy_code', survey_id)


def get_sedphy_joined_count(child_1, child_2, survey_id: str) -> int:
    return get_joined_count(child_1, child_2, Sedphy, 'sedphy_code', survey_id)


def get_joined_count(child_1, child_2, parent_table, foreign_key_name, survey_id: str) -> int:
    """
    :param child_1: one of the related child tables
    :param child_2: the other child table
    :param parent_table: parent table
    :param foreign_key_name: foreign key that links the child table to the parent table.
    :param survey_id: survey id
    :return: the union of record counts for child one and child 2 where they intersect with the parent.
    """
    stmt = (
        select(
            func.count(parent_table.code)
        ).
        select_from(Station).
        join(parent_table).
        outerjoin(child_1).
        outerjoin(child_2).
        where(
            and_(
                or_(parent_table.code == getattr(child_1, foreign_key_name),
                    parent_table.code == getattr(child_2, foreign_key_name)),
                (Station.survey_id == survey_id)
            )
        )
    )

    return Session.execute(stmt).scalar()
