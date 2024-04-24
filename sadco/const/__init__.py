from enum import Enum


class SurveyType(str, Enum):
    """Survey Types."""
    HYDRO = 'hydro'
    CURRENTS = 'currents'
    WEATHER = 'weather'
    WAVES = 'waves'
    ECHOSOUNDING = 'echo-sounding'
    UTR = 'utr'
    VOS = 'vos'
    UNKNOWN = 'unkown'


class DataType(str, Enum):
    """Data Types."""
    WATER = 'water'
    WATERCHEMISTRY = 'water_chemistry'
    WATERPOLLUTION = 'water_pollution'
    WATERNUTRIENTS = 'water_nutrients'
    WATERCURRENTS = 'water currents'
    SEDIMENT = 'sediment'
    SEDIMENTCHEMISTRY = 'sediment_chemistry'
    SEDIMENTPOLLUTION = 'sediment_pollution'
    WATERNUTRIENTSANDCHEMISTRY = 'water_nutrients_and_chemistry'
