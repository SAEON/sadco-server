from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from sadco.db import Base


class Watphy(Base):

    __tablename__ = 'watphy'

    code = Column(Integer, primary_key=True, nullable=False)

    station_id = Column(String(12), ForeignKey('sadco.station.station_id'), nullable=False)
    device_code = Column(Integer, ForeignKey('sadco.sampling_device.code'), nullable=False)

    method_code = Column(Numeric(precision=38, scale=0), nullable=False)
    standard_code = Column(Numeric(precision=38, scale=0), nullable=False)
    subdes = Column(String(5))
    spldattim = Column(TIMESTAMP)
    spldep = Column(Numeric(precision=7, scale=3))
    filtered = Column(String(1))
    disoxygen = Column(Numeric(precision=4, scale=2))
    salinity = Column(Numeric(precision=5, scale=3))
    temperature = Column(Numeric(precision=5, scale=3))
    sound_flag = Column(String(1))
    soundv = Column(Numeric(precision=5, scale=1))
    turbidity = Column(Numeric(precision=7, scale=3))
    pressure = Column(Numeric(precision=7, scale=2))
    fluorescence = Column(Numeric(precision=8, scale=4))

    # The primary key for the below tables are watphy_code, they all share a one-to-one relationship with watphy
    watnut = relationship('Watnut', uselist=False, back_populates='watphy')
    watchem1 = relationship('Watchem1', uselist=False, back_populates='watphy')
    watchem2 = relationship('Watchem2', uselist=False, back_populates='watphy')
    watpol1 = relationship('Watpol1', uselist=False, back_populates='watphy')
    watpol2 = relationship('Watpol2', uselist=False, back_populates='watphy')
    watchl = relationship('Watchl', uselist=False, back_populates='watphy')
    watcurrents = relationship('Watcurrents', uselist=False, back_populates='watphy')

    station = relationship('Station', uselist=False, back_populates='watphy_list')
    sampling_device = relationship('SamplingDevice', uselist=False)


