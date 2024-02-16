from odp.config.base import BaseConfig
from odp.config.mixins import DBConfigMixin


class SADCODBConfig(BaseConfig, DBConfigMixin):
    class Config:
        env_prefix = 'SADCO_DB_'


class SADCOConfig(BaseConfig):
    _subconfig = {
        'DB': SADCODBConfig,
    }


class Config(BaseConfig):
    _subconfig = {
        'SADCO': SADCOConfig,
    }


sadco_config = Config()
