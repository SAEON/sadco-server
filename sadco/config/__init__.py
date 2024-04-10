from pydantic.networks import AnyHttpUrl

from odp.config.base import BaseConfig
from odp.config.mixins import DBConfigMixin, AppConfigMixin


class SADCODBConfig(BaseConfig, DBConfigMixin):
    class Config:
        env_prefix = 'SADCO_DB_'


class SADCOCatalogConfig(BaseConfig, AppConfigMixin):
    class Config:
        env_prefix = 'SADCO_CATALOG_'


class SADCOConfig(BaseConfig):
    class Config:
        env_prefix = 'SADCO_'

    API_URL: AnyHttpUrl = None  # ODP API URL

    _subconfig = {
        'DB': SADCODBConfig,
        'CATALOG': SADCOCatalogConfig
    }


class Config(BaseConfig):
    _subconfig = {
        'SADCO': SADCOConfig,
    }


sadco_config = Config()
