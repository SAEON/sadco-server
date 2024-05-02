from sqlalchemy import Column, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class Weather(Base):
    __tablename__ = 'weather'

    station_id = Column(String(12), ForeignKey('sadco.station.station_id'), primary_key=True, nullable=False)
    nav_equip_type = Column(String(10))
    atmosph_pres = Column(Numeric(precision=5, scale=1))
    surface_tmp = Column(Numeric(precision=3, scale=1))
    drybulb = Column(Numeric(precision=3, scale=1))
    wetbulb = Column(Numeric(precision=3, scale=1))
    cloud = Column(String(5))
    vis_code = Column(String(2))
    weather_code = Column(String(2))
    water_color = Column(Numeric(precision=38, scale=0))
    transparency = Column(Numeric(precision=38, scale=0))
    wind_dir = Column(Numeric(precision=38, scale=0))
    wind_speed = Column(Numeric(precision=3, scale=1))
    swell_dir = Column(Numeric(precision=38, scale=0))
    swell_height = Column(Numeric(precision=3, scale=1))
    swell_period = Column(Numeric(precision=38, scale=0))
    dupflag = Column(String(1))

    station = relationship('Station', uselist=False, back_populates='weather_list')
