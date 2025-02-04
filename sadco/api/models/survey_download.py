from typing import Optional

from pydantic import BaseModel


class HydroDownloadModel(BaseModel):
    survey_id: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    time: Optional[str]
    station_name: Optional[str]
    station_id: Optional[str]
    platform_name: Optional[str]
    max_sampling_depth: Optional[float]


class HydroWaterPhysicalDownloadModel(HydroDownloadModel):
    subdes: Optional[str]
    spldattim: Optional[str]
    spldep: Optional[float]
    filtered: Optional[str]
    disoxygen: Optional[float]
    salinity: Optional[float]
    temperature: Optional[float]
    sound_flag: Optional[str]
    soundv: Optional[float]
    turbidity: Optional[float]
    pressure: Optional[float]
    fluorescence: Optional[float]


class HydroWeatherDownloadModel(HydroDownloadModel):
    nav_equip_type: Optional[str]
    atmosph_pres: Optional[float]
    surface_tmp: Optional[float]
    drybulb: Optional[float]
    wetbulb: Optional[float]
    cloud: Optional[str]
    vis_code: Optional[str]
    weather_code: Optional[str]
    water_color: Optional[float]
    transparency: Optional[float]
    wind_dir: Optional[float]
    wind_speed: Optional[float]
    swell_dir: Optional[float]
    swell_height: Optional[float]
    swell_period: Optional[float]
    dupflag: Optional[str]


class HydroCurrentsDownloadModel(HydroDownloadModel):
    subdes: Optional[str]
    spldattim: Optional[str]
    spldep: Optional[float]
    current_dir: Optional[float]
    current_speed: Optional[float]
    perc_good: Optional[str]
