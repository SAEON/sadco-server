from datetime import date
from typing import Optional

from pydantic import BaseModel


class VosSurveySearchResult(BaseModel):
    total: int


class VosSurveyDownloadModel(BaseModel):
    latitude: float
    longitude: float
    date_time: date
    callsign: str
    atmospheric_pressure: Optional[float]
    surface_temperature: Optional[float]
    drybulb: Optional[float]
    wetbulb: Optional[float]
    dewpoint: Optional[float]
    cloud_amount: Optional[str]
    swell_direction: Optional[int]
    swell_height: Optional[float]
    swell_period: Optional[int]
    wave_height: Optional[float]
    wave_period: Optional[int]
    wind_direction: Optional[int]
    wind_speed: Optional[float]
