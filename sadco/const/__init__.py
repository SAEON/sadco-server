from enum import Enum


class SurveyType(str, Enum):
    """Survey Types."""
    HYDRO = 'Hydro'
    CURRENTS = 'Currents'
    WEATHER = 'Weather'
    WAVES = 'Waves'
    ECHOSOUNDING = 'Echo-Sounding'
    UTR = 'UTR'
    VOS = 'VOS'
    UNKNOWN = 'Unkown'


class DataType(str, Enum):
    """Data Types."""
    WATER = 'water'
    WATERCHEMISTRY = 'water chemistry'
    WATERPOLLUTION = 'water pollution'
    WATERNUTRIENTS = 'water nutrients'
    WATERCURRENTS = 'water currents'
    SEDIMENT = 'sediment'
    SEDIMENTCHEMISTRY = 'sediment chemistry'
    SEDIMENTPOLLUTION = 'sediment pollution'
