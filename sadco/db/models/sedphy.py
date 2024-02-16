from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class Sedphy(Base):
    __tablename__ = 'sedphy'

    code = Column(Numeric(precision=38, scale=0), primary_key=True)
    station_id = Column(String(12), ForeignKey('sadco.station.station_id'), nullable=False)
    device_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.sampling_device.code'), nullable=False)
    method_code = Column(Numeric(precision=38, scale=0), nullable=False)
    standard_code = Column(Numeric(precision=38, scale=0), nullable=False)
    subdes = Column(String(5))
    spldattim = Column(DateTime)
    spldep = Column(Numeric(precision=6, scale=2))
    spldis = Column(Numeric(precision=38, scale=0))
    splvol = Column(Numeric(precision=4, scale=1))
    sievsz = Column(Numeric(precision=7, scale=1))
    kurt = Column(Numeric(precision=7, scale=3))
    skew = Column(Numeric(precision=7, scale=3))
    meanpz = Column(Numeric(precision=38, scale=0))
    medipz = Column(Numeric(precision=38, scale=0))
    pctsat = Column(Numeric(precision=3, scale=1))
    pctsil = Column(Numeric(precision=3, scale=1))
    permty = Column(Numeric(precision=38, scale=0))
    porsty = Column(Numeric(precision=3, scale=1))
    dwf = Column(Numeric(precision=7, scale=4))
    cod = Column(Numeric(precision=5, scale=3))

    sedpol1_list = relationship('Sedpol1')
    sedpol2_list = relationship('Sedpol2')
    sedchem1_list = relationship('Sedchem1')
    sedchem2_list = relationship('Sedchem2')
