from sqlalchemy import Column, Numeric, String, Integer, DateTime

from sadco.db import Base


class Vos:
    latitude = Column(Numeric(7, 5), primary_key=True, nullable=False)
    longitude = Column(Numeric(8, 5), primary_key=True, nullable=False)
    date_time = Column(DateTime, primary_key=True, nullable=False)
    daynull = Column(String(1))
    callsign = Column(String(30), primary_key=True, nullable=False)
    country = Column(String(2))
    platform = Column(String(1))
    data_id = Column(String(2))
    quality_control = Column(String(1))
    source1 = Column(String(1))
    load_id = Column(Integer, nullable=False)
    dupflag = Column(String(1))
    atmospheric_pressure = Column(Numeric(5, 1))
    surface_temperature = Column(Numeric(3, 1))
    surface_temperature_type = Column(String(1))
    drybulb = Column(Numeric(3, 1))
    wetbulb = Column(Numeric(3, 1))
    wetbulb_ice = Column(String(1))
    dewpoint = Column(Numeric(3, 1))
    cloud_amount = Column(String(1))
    cloud1 = Column(String(1))
    cloud2 = Column(String(1))
    cloud3 = Column(String(1))
    cloud4 = Column(String(1))
    cloud5 = Column(String(1))
    visibility_code = Column(String(2))
    weather_code = Column(String(2))
    swell_direction = Column(Integer)
    swell_height = Column(Numeric(3, 1))
    swell_period = Column(Integer)
    wave_height = Column(Numeric(3, 1))
    wave_period = Column(Integer)
    wind_direction = Column(Integer)
    wind_speed = Column(Numeric(3, 1))
    wind_speed_type = Column(String(1))


class VosMain(Base, Vos):
    __tablename__ = 'vos_main'


class VosMain2(Base, Vos):
    __tablename__ = 'vos_main2'


class VosMain68(Base, Vos):
    __tablename__ = 'vos_main68'


class VosArch(Base, Vos):
    __tablename__ = 'vos_arch'


class VosArch2(Base, Vos):
    __tablename__ = 'vos_arch2'



