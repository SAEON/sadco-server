from datetime import date, datetime
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


class HydroWaterPollutionDownloadModel(HydroWaterPhysicalDownloadModel):
    arsenic: Optional[float]
    cadmium: Optional[float]
    chromium: Optional[float]
    cobalt: Optional[float]
    copper: Optional[float]
    iron: Optional[float]
    lead: Optional[float]
    manganese: Optional[float]
    mercury: Optional[float]
    nickel: Optional[float]
    selenium: Optional[float]
    zinc: Optional[float]
    aluminium: Optional[float]
    antimony: Optional[float]
    bismuth: Optional[float]
    molybdenum: Optional[float]
    silver: Optional[float]
    titanium: Optional[float]
    vanadium: Optional[float]


class HydroWaterChemistryDownloadModel(HydroWaterPhysicalDownloadModel):
    dic: Optional[float]
    doc: Optional[float]
    fluoride: Optional[float]
    iodene: Optional[float]
    iodate: Optional[float]
    kjn: Optional[float]
    nh3: Optional[float]
    nitrogen: Optional[float]
    oxa: Optional[float]
    ph: Optional[float]
    calcium: Optional[float]
    cesium: Optional[float]
    hydrocarbons: Optional[float]
    magnesium: Optional[float]
    pah: Optional[float]
    potassium: Optional[float]
    rubidium: Optional[float]
    sodium: Optional[float]
    strontium: Optional[float]
    so4: Optional[float]
    sussol: Optional[float]


class HydroWaterNutrientsDownloadModel(HydroWaterPhysicalDownloadModel):
    no2: Optional[float]
    no3: Optional[float]
    p: Optional[float]
    po4: Optional[float]
    ptot: Optional[float]
    sio3: Optional[float]
    sio4: Optional[float]


class HydroSedimentPhysicalDownloadModel(HydroDownloadModel):
    subdes: Optional[str]
    spldattim: Optional[str]
    spldep: Optional[float]
    spldis: Optional[float]
    splvol: Optional[float]
    sievsz: Optional[float]
    kurt: Optional[float]
    skew: Optional[float]
    meanpz: Optional[float]
    medipz: Optional[float]
    pctsat: Optional[float]
    pctsil: Optional[float]
    permty: Optional[float]
    porsty: Optional[float]
    dwf: Optional[float]
    cod: Optional[float]


class HydroSedimentPollutionDownloadModel(HydroSedimentPhysicalDownloadModel):
    arsenic: Optional[float]
    cadmium: Optional[float]
    chromium: Optional[float]
    cobalt: Optional[float]
    copper: Optional[float]
    iron: Optional[float]
    lead: Optional[float]
    manganese: Optional[float]
    mercury: Optional[float]
    nickel: Optional[float]
    selenium: Optional[float]
    zinc: Optional[float]
    aluminium: Optional[float]
    antimony: Optional[float]
    bismuth: Optional[float]
    molybdenum: Optional[float]
    silver: Optional[float]
    titanium: Optional[float]
    vanadium: Optional[float]


class HydroSedimentChemistryDownloadModel(HydroSedimentPhysicalDownloadModel):
    fluoride: Optional[float]
    kjn: Optional[float]
    oxa: Optional[float]
    toc: Optional[float]
    ptot: Optional[float]
    calcium: Optional[float]
    magnesium: Optional[float]
    potassium: Optional[float]
    sodium: Optional[float]
    strontium: Optional[float]
    so3: Optional[float]


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
