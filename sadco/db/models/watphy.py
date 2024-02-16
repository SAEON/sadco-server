from sqlalchemy import Column, Numeric, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from sadco.db import Base


class Watphy(Base):

    __tablename__ = 'watphy'

    code = Column(Numeric(precision=38, scale=0), primary_key=True, nullable=False)

    station_id = Column(String(12), ForeignKey('sadco.station.station_id', ondelete='CASCADE'), nullable=False)
    device_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.sampling_device.code'), nullable=False)

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

    sampling_device = relationship('SamplingDevice')
    watnut = relationship('Watnut')
    watchem1 = relationship('Watchem1')
    watchem2 = relationship('Watchem2')
    watpol1 = relationship('Watpol1')
    watpol2 = relationship('Watpol2')
    watchl = relationship('Watchl')


