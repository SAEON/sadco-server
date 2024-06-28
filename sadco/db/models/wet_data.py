from sqlalchemy import Column, Numeric, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class WetData(Base):
    __tablename__ = 'wet_data'

    station_id = Column(String(4), primary_key=True, nullable=False)
    period_code = Column(Integer, ForeignKey('sadco.wet_period.code'))
    date_time = Column(DateTime,  primary_key=True, nullable=False)
    air_temp_ave = Column(Numeric(precision=7, scale=4))
    air_temp_min = Column(Numeric(precision=7, scale=4))
    air_temp_min_time = Column(DateTime)
    air_temp_max = Column(Numeric(precision=7, scale=4))
    air_temp_max_time = Column(DateTime)
    barometric_pressure = Column(Numeric(precision=7, scale=2))
    fog = Column(Numeric(precision=5, scale=1))
    rainfall = Column(Numeric(precision=5, scale=1))
    relative_humidity = Column(Numeric(precision=4, scale=1))
    solar_radiation = Column(Numeric(precision=7, scale=2))
    solar_radiation_max = Column(Numeric(precision=7, scale=2))
    wind_dir = Column(Numeric(precision=5, scale=2))
    wind_speed_ave = Column(Numeric(precision=6, scale=3))
    wind_speed_min = Column(Numeric(precision=6, scale=3))
    wind_speed_max = Column(Numeric(precision=6, scale=3))
    wind_speed_max_time = Column(DateTime)
    wind_speed_max_length = Column(Integer)
    wind_speed_max_dir = Column(Numeric(precision=4, scale=1))
    wind_speed_std = Column(Numeric(precision=5, scale=2))

    # wet_station = relationship("WetStation", back_populates="wet_data_list", uselist=False)
    wet_period = relationship("WetPeriod", back_populates="wet_data_list", uselist=False)

