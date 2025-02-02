from datetime import date
from typing import Optional

from pydantic import BaseModel


class SurveyListItemModel(BaseModel):
    id: str
    project_name: Optional[str]
    station_name: Optional[str]
    platform_name: Optional[str]
    chief_scientist: Optional[str]
    institute: Optional[str]
    date_start: Optional[date]
    date_end: Optional[date]
    survey_type: str


class SedimentPollutionModel(BaseModel):
    record_count: int


class SedimentChemistryModel(BaseModel):
    record_count: int


class SedimentModel(BaseModel):
    record_count: int
    sediment_pollution: Optional[SedimentPollutionModel]
    sediment_chemistry: Optional[SedimentChemistryModel]


class WaterPollutionModel(BaseModel):
    record_count: int


class WaterChemistryModel(BaseModel):
    record_count: int


class WaterCurrentsModel(BaseModel):
    record_count: int


class WaterNutrientsModel(BaseModel):
    record_count: int


class WaterModel(BaseModel):
    record_count: int
    water_pollution: Optional[WaterPollutionModel]
    water_chemistry: Optional[WaterChemistryModel]
    water_currents: Optional[WaterCurrentsModel]
    water_nutrients: Optional[WaterNutrientsModel]


class CurrentsModel(BaseModel):
    record_count: int


class WeatherModel(BaseModel):
    record_count: int


class DataTypesModel(BaseModel):
    water: Optional[WaterModel]
    sediment: Optional[SedimentModel]
    weather: Optional[WeatherModel]
    currents: Optional[CurrentsModel]


class StationModel(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]


class SurveyModel(BaseModel):
    id: str
    project_name: Optional[str]
    station_name: Optional[str]
    platform_name: Optional[str]
    chief_scientist: Optional[str]
    institute: Optional[str]
    date_start: Optional[date]
    date_end: Optional[date]
    lat_north: Optional[float]
    lat_south: Optional[float]
    long_west: Optional[float]
    long_east: Optional[float]
    stations: list[StationModel]
    survey_type: str


class HydroSurveyModel(SurveyModel):
    data_types: Optional[DataTypesModel]


class CurrentDepthModel(BaseModel):
    depth: float
    instrument_number: int
    parameters: str
    date_time_start: date
    date_time_end: date
    interval: int
    records: int  # number of cur_data
    quality_control: Optional[str] = 'Yes'


class CurrentsSurveyModel(SurveyModel):
    mooring_details: list[CurrentDepthModel]


class PeriodCountsModel(BaseModel):
    year: int
    jan: Optional[int]
    feb: Optional[int]
    mar: Optional[int]
    apr: Optional[int]
    may: Optional[int]
    jun: Optional[int]
    jul: Optional[int]
    aug: Optional[int]
    sep: Optional[int]
    oct: Optional[int]
    nov: Optional[int]
    dec: Optional[int]
    total: int


class PeriodsSurveyModel(SurveyModel):
    """
    Represents a survey that contains periods
    """
    period_counts: list[PeriodCountsModel]


class SearchFacetItemsModel(BaseModel):
    name: str
    code: str
    count: int


class SearchFacetModel(BaseModel):
    title: str
    query_key: str
    items: list[SearchFacetItemsModel]


class SurveySearchResult(BaseModel):
    items: list[SurveyListItemModel]
    search_facets: list[SearchFacetModel]
    filtered_facets: list[str]
    total: int
    page: int
    pages: int


class SurveyTypeModel(BaseModel):
    code: int
    name: str
    description: str
