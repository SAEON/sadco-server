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


class DataTypesModel(BaseModel):
    water: Optional[WaterModel]


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
    data_types: Optional[DataTypesModel]
    survey_type: str

