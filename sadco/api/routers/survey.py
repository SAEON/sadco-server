from datetime import date
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import joinedload
from starlette.status import HTTP_404_NOT_FOUND

from sadco.api.lib.paging import Page, Paginator
from sadco.db.models import (Inventory, SurveyType, Watphy, Watnut, Watpol1, Watpol2, CurData, Sedphy, Sedpol1, Sedpol2,
                             Sedchem1, Sedchem2, Watchem1, Watchem2, Watcurrents, Weather, Currents, Survey, Station,
                             SamplingDevice, InvStats, CurDepth, CurMooring)
from sadco.api.models import (SurveyModel, SurveyListItemModel, StationModel, WaterModel, WaterNutrientsModel,
                              WaterPollutionModel, WaterCurrentsModel, WaterChemistryModel, DataTypesModel,
                              SedimentModel, SedimentPollutionModel, SedimentChemistryModel, SurveyTypeModel,
                              CurrentsModel, WeatherModel, SurveySearchResult, SamplingDeviceModel, HydroSurveyModel,
                              CurrentDepthModel, CurrentsSurveyModel, PeriodCountsModel, PeriodsSurveyModel)

from sadco.api.lib.auth import Authorize
from sadco.db import Session
from sadco.const import SADCOScope, SurveyType as ConstSurveyType

router = APIRouter()


@router.get(
    '/surveys',
    response_model=Page[SurveyListItemModel],
    dependencies=[Depends(Authorize(SADCOScope.SURVEYS_READ))],
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


@router.get(
    '/surveys/search',
    response_model=SurveySearchResult,
    dependencies=[Depends(Authorize(SADCOScope.SURVEYS_READ))],
)
async def list_surveys(
        survey_id: str = Query(None, title='Survey ID'),
        sampling_device_code: int = Query(None, title='Sampling device'),
        survey_type_code: str = Query(None, title='Survey type'),
        north_bound: float = Query(None, title='North bound latitude', ge=-90, le=90),
        south_bound: float = Query(None, title='South bound latitude', ge=-90, le=90),
        east_bound: float = Query(None, title='East bound longitude', ge=-180, le=180),
        west_bound: float = Query(None, title='West bound longitude', ge=-180, le=180),
        start_date: date = Query(None, title='Date range start'),
        end_date: date = Query(None, title='Date range end'),
        exclusive_region: bool = Query(False, title='Exclude partial spatial matches'),
        exclusive_interval: bool = Query(False, title='Exclude partial temporal matches'),
        page: int = Query(1, ge=1, title='Page number'),
        size: int = Query(50, ge=0, title='Page size; 0=unlimited'),
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

    if survey_id is not None:
        stmt = stmt.where(Inventory.survey_id.like(f'{survey_id}%'))

    if exclusive_region:
        # We need to use the negation of North and South because they come from the DB as south
        if north_bound is not None:
            stmt = stmt.where(-Inventory.lat_north <= north_bound)

        if south_bound is not None:
            stmt = stmt.where(-Inventory.lat_south >= south_bound)

        if east_bound is not None:
            stmt = stmt.where(Inventory.long_east <= east_bound)

        if west_bound is not None:
            stmt = stmt.where(Inventory.long_west >= west_bound)

    else:
        if north_bound is not None:
            stmt = stmt.where(-Inventory.lat_south <= north_bound)

        if south_bound is not None:
            stmt = stmt.where(-Inventory.lat_north >= south_bound)

        if east_bound is not None:
            stmt = stmt.where(Inventory.long_west <= east_bound)

        if west_bound is not None:
            stmt = stmt.where(Inventory.long_east >= west_bound)

    if exclusive_interval:
        if start_date:
            stmt = stmt.where(Inventory.date_start >= start_date)

        if end_date:
            stmt = stmt.where(Inventory.date_end <= end_date)

    else:
        if start_date:
            stmt = stmt.where(Inventory.date_end >= start_date)

        if end_date:
            stmt = stmt.where(Inventory.date_start <= end_date)

    sampling_device_query = (
        select(func.count(Station.survey_id.distinct()).label('device_count'), SamplingDevice.code, SamplingDevice.name)
        .join(Sedphy, SamplingDevice.code == Sedphy.device_code)
        .join(Station, Station.station_id == Sedphy.station_id)
        .group_by(SamplingDevice.code)
    )

    if sampling_device_code is not None:
        sampling_device_query = sampling_device_query.where(SamplingDevice.code == sampling_device_code)

        stmt = stmt.join(Survey).join(Station).join(Sedphy).where(Sedphy.device_code == sampling_device_code)

    sampling_devices = [
        SamplingDeviceModel(
            code=row.code,
            name=row.name,
            count=row.device_count
        )
        for row in Session.execute(sampling_device_query)
    ]

    survey_type_query = (
        select(func.count(Inventory.survey_id.distinct()).label('survey_type_count'), SurveyType.code, SurveyType.name)
        .join(SurveyType)
        .group_by(SurveyType.code)
        .group_by(SurveyType.name)
    )

    if survey_type_code is not None:
        survey_type_query = survey_type_query.where(SurveyType.code == survey_type_code)

        stmt = stmt.where(Inventory.survey_type_code == survey_type_code)

    survey_types = [
        SurveyTypeModel(
            code=row.code,
            name=row.name,
            count=row.survey_type_count
        )
        for row in Session.execute(survey_type_query)
    ]

    total = Session.execute(
        select(func.count())
        .select_from(stmt.distinct().subquery())
    ).scalar_one()

    limit = size or total
    items = [
        SurveyListItemModel(
            id=row.Inventory.survey_id,
            project_name=row.Inventory.project_name,
            station_name=row.Inventory.cruise_name,
            platform_name=row.Inventory.planam.name if row.Inventory.planam else '',
            chief_scientist=get_chief_scientist(row.Inventory),
            institute=row.Inventory.institute.name if row.Inventory.institute else '',
            date_start=row.Inventory.date_start,
            date_end=row.Inventory.date_end,
            survey_type=row.Inventory.survey_type.name if row.Inventory.survey_type is not None else ''
        ) for row in Session.execute(
            stmt.
            order_by(Inventory.survey_id).
            distinct().
            offset(limit * (page - 1)).
            limit(limit)
        )
    ]

    return SurveySearchResult(
        items=items,
        sampling_devices=sampling_devices,
        survey_types=survey_types,
        total=total,
        page=page,
        pages=ceil(total / limit) if limit else 0,
    )


def get_chief_scientist(inventory: Inventory) -> str:
    if inventory.scientist_1:
        return (inventory.scientist_1.f_name.strip() + ' ' + inventory.scientist_1.surname.strip()).strip()

    return ''


@router.get(
    f"/{ConstSurveyType.HYDRO.value}/{{survey_id}}",
    response_model=HydroSurveyModel,
    dependencies=[Depends(Authorize(SADCOScope.HYDRO_READ))],
)
async def get_hydro_survey(
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

    return HydroSurveyModel(
        **get_survey_model(result.Inventory).dict(),
        data_types=get_data_types(result.Inventory.inv_stats)
    )


def get_survey_model(inventory: Inventory) -> SurveyModel:
    """
    Get the generic survey model
    """
    stations = get_stations(inventory)

    return SurveyModel(
        id=inventory.survey_id,
        project_name=inventory.project_name,
        station_name=inventory.cruise_name,
        platform_name=inventory.planam.name,
        chief_scientist=(
                inventory.scientist_1.f_name.strip() + ' ' + inventory.scientist_1.surname.strip()).strip(),
        institute=inventory.institute.name,
        date_start=inventory.date_start,
        date_end=inventory.date_end,
        lat_north=-inventory.lat_north,  # Use negation as the value from the db is South
        lat_south=-inventory.lat_south,  # Use negation as the value from the db is South
        long_west=inventory.long_west,
        long_east=inventory.long_east,
        survey_type=inventory.survey_type.name,
        stations=stations
    )


def get_stations(inventory: Inventory) -> list[StationModel]:
    """
    Get a model containing the positions of the stations for that specific survey_type.
    """
    stations = []
    match inventory.survey_type.name.lower():
        case ConstSurveyType.HYDRO.value:
            stations = inventory.survey.stations
        case ConstSurveyType.CURRENTS.value | ConstSurveyType.UTR.value:
            stations = inventory.cur_moorings
        case ConstSurveyType.WEATHER.value:
            stations = inventory.wet_stations
        case ConstSurveyType.WAVES.value:
            stations = inventory.wav_stations
        case ConstSurveyType.ECHOSOUNDING.value | ConstSurveyType.UNKNOWN.value:
            return [StationModel(
                latitude=-inventory.lat_north,
                longitude=inventory.long_west,
            )]

    station_models = [
        StationModel(
            latitude=-station.latitude,
            longitude=station.longitude
        ) for station in stations
    ]

    return station_models


def get_data_types(inventory_statistics: InvStats) -> DataTypesModel:
    """
    Get the datat types and their record counts for a given Inventory.
    If the data type is split into 2, the max is used.
    """
    data_types_model = DataTypesModel()

    if inventory_statistics.watphy_cnt and inventory_statistics.watphy_cnt > 0:
        water_model = WaterModel(
            record_count=inventory_statistics.watphy_cnt
        )

        if (inventory_statistics.watchem1_cnt and inventory_statistics.watchem1_cnt > 0) or (
                inventory_statistics.watchem2_cnt and inventory_statistics.watchem2_cnt > 0):
            water_model.water_chemistry = WaterChemistryModel(
                record_count=max(inventory_statistics.watchem1_cnt, inventory_statistics.watchem2_cnt)
            )

        if (inventory_statistics.watpol1_cnt and inventory_statistics.watpol1_cnt > 0) or (
                inventory_statistics.watpol2_cnt and inventory_statistics.watpol2_cnt > 0):
            water_model.water_pollution = WaterPollutionModel(
                record_count=max(inventory_statistics.watpol1_cnt, inventory_statistics.watpol2_cnt)
            )

        if inventory_statistics.watcurrents_cnt and inventory_statistics.watcurrents_cnt > 0:
            water_model.water_currents = WaterCurrentsModel(
                record_count=inventory_statistics.watcurrents_cnt
            )

        if inventory_statistics.watnut_cnt and inventory_statistics.watnut_cnt > 0:
            water_model.water_nutrients = WaterNutrientsModel(
                record_count=inventory_statistics.watnut_cnt
            )

        if inventory_statistics.watcurrents_cnt and inventory_statistics.watcurrents_cnt > 0:
            water_model.water_currents = WaterCurrentsModel(
                record_count=inventory_statistics.watcurrents_cnt
            )

        data_types_model.water = water_model

    if inventory_statistics.sedphy_cnt and inventory_statistics.sedphy_cnt > 0:
        sediment_model = SedimentModel(
            record_count=inventory_statistics.sedphy_cnt
        )

        if inventory_statistics.sedchem1_cnt > 0 or inventory_statistics.sedchem2_cnt > 0:
            sediment_model.sediment_chemistry = SedimentChemistryModel(
                record_count=max(inventory_statistics.sedchem1_cnt, inventory_statistics.sedchem2_cnt)
            )

        if inventory_statistics.sedpol1_cnt > 0 or inventory_statistics.sedpol2_cnt > 0:
            sediment_model.sediment_pollution = SedimentPollutionModel(
                record_count=max(inventory_statistics.sedpol1_cnt, inventory_statistics.sedpol2_cnt)
            )

        data_types_model.sediment = sediment_model

    if inventory_statistics.weather_cnt and inventory_statistics.weather_cnt > 0:
        data_types_model.weather = WeatherModel(
            record_count=inventory_statistics.weather_cnt
        )

    currents_count = get_hydro_current_count(inventory_statistics.survey_id)

    if currents_count > 0:
        data_types_model.currents = CurrentsModel(
            record_count=currents_count
        )

    return data_types_model


def get_hydro_current_count(survey_id: str) -> int:
    """
    Get the number of Current records for a given Hydro Survey
    """
    stmt = (
        select(
            func.count(Currents.station_id).label('currents_count')
        ).
        select_from(Survey).
        join(Station).
        outerjoin(Currents).
        where(Survey.survey_id == survey_id)
    )

    result = Session.execute(stmt).one_or_none()

    return result.currents_count


@router.get(
    f"/{ConstSurveyType.UTR.value}/{{survey_id}}",
    response_model=CurrentsSurveyModel,
    dependencies=[Depends(Authorize(SADCOScope.UTR_READ))],
)
async def get_utr_survey(
        survey_id: str
):
    return get_mooring_details(survey_id)


@router.get(
    f"/{ConstSurveyType.CURRENTS.value}/{{survey_id}}",
    response_model=CurrentsSurveyModel,
    dependencies=[Depends(Authorize(SADCOScope.CURRENTS_READ))],
)
async def get_currents_survey(
        survey_id: str
):
    return get_mooring_details(survey_id)


def get_mooring_details(survey_id: str):
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

    return CurrentsSurveyModel(
        **get_survey_model(result.Inventory).dict(),
        mooring_details=get_depth_details(result.Inventory.cur_moorings)
    )


def get_depth_details(current_moorings: list[CurMooring]) -> list[CurrentDepthModel]:
    return [
        CurrentDepthModel(
            depth=row.CurDepth.spldep,
            instrument_number=row.CurDepth.instrument_number,
            parameters=row.CurDepth.parameters,
            date_time_start=row.CurDepth.date_time_start,
            date_time_end=row.CurDepth.date_time_end,
            interval=row.CurDepth.time_interval,
            records=row.cur_data_records,
        )
        for current_mooring in current_moorings
        for row in get_current_depths(current_mooring.code)
    ]


def get_current_depths(cur_mooring_id: int) -> any:
    query = (
        Session.query(
            CurDepth,
            func.count(CurData.code).label('cur_data_records')
        ).
        join(CurData, CurDepth.code == CurData.depth_code).
        where(CurDepth.mooring_code == cur_mooring_id).
        group_by(CurDepth.code)
    )

    return query.all()


@router.get(
    f"/{ConstSurveyType.WEATHER.value}/{{survey_id}}",
    response_model=PeriodsSurveyModel,
    dependencies=[Depends(Authorize(SADCOScope.WEATHER_READ))],
)
async def get_weather_survey(
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

    return PeriodsSurveyModel(
        **get_survey_model(result.Inventory).dict(),
        period_counts=get_period_counts(result.Inventory.wet_stations, 'wet_period_counts')
    )


@router.get(
    f"/{ConstSurveyType.WAVES.value}/{{survey_id}}",
    response_model=PeriodsSurveyModel,
    dependencies=[Depends(Authorize(SADCOScope.WAVES_READ))],
)
async def get_waves_survey(
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

    return PeriodsSurveyModel(
        **get_survey_model(result.Inventory).dict(),
        period_counts=get_period_counts(result.Inventory.wav_stations, 'wav_periods')
    )


def get_period_counts(stations, related_periods_name: str) -> list:
    return [
        PeriodCountsModel(
            year=period.yearp,
            jan=period.m01,
            feb=period.m02,
            mar=period.m03,
            apr=period.m04,
            may=period.m05,
            jun=period.m06,
            jul=period.m07,
            aug=period.m08,
            sep=period.m09,
            oct=period.m10,
            nov=period.m11,
            dec=period.m12,
            total=get_period_counts_total(period)
        )
        for station in stations
        for period in getattr(station, related_periods_name)
    ]


def get_period_counts_total(period_counts) -> int:
    total = 0

    for key, value in period_counts.__dict__.items():
        if 'm' in key:
            total += value

    return total


@router.get(
    f"/{ConstSurveyType.ECHOSOUNDING.value}/{{survey_id}}",
    response_model=SurveyModel,
    dependencies=[Depends(Authorize(SADCOScope.ECHO_SOUNDING_READ))],
)
async def get_echo_sounding_survey(
        survey_id: str
):
    return get_survey_without_details(survey_id)


@router.get(
    f"/{ConstSurveyType.UNKNOWN.value}/{{survey_id}}",
    response_model=SurveyModel,
    dependencies=[Depends(Authorize(SADCOScope.UNKNOWN_READ))],
)
async def get_unknown_survey(
        survey_id: str
):
    return get_survey_without_details(survey_id)


def get_survey_without_details(survey_id: str) -> SurveyModel:
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

    return get_survey_model(result.Inventory)


def get_data_types_manually(survey_id: str) -> DataTypesModel:  # pragma: no cover
    """
    This function is not in use. It fetches and constructs data types for a specific survey.
    The values calculated using this function can be extracted from the inv_stats table.
    param survey_id: The survey id for which to construct the data types.
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


def get_water_model(survey_id: str) -> WaterModel:  # pragma: no cover
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


def get_sediment_model(survey_id: str) -> SedimentModel:  # pragma: no cover
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


def get_watphy_joined_count(child_1, child_2, survey_id: str) -> int:  # pragma: no cover
    return get_joined_count(child_1, child_2, Watphy, 'watphy_code', survey_id)


# pragma: no cover
def get_sedphy_joined_count(child_1, child_2, survey_id: str) -> int:  # pragma: no cover
    return get_joined_count(child_1, child_2, Sedphy, 'sedphy_code', survey_id)


def get_joined_count(child_1, child_2, parent_table, foreign_key_name, survey_id: str) -> int:  # pragma: no cover
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
