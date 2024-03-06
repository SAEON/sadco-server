from sqlalchemy import Column, Numeric, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class Sedphy(Base):
    __tablename__ = 'sedphy'

    code = Column(Integer, primary_key=True)
    station_id = Column(String(12), ForeignKey('sadco.station.station_id'), nullable=False)
    device_code = Column(Integer, nullable=False)
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

    sedpol1 = relationship('Sedpol1', uselist=False, back_populates='sedphy')
    sedpol2 = relationship('Sedpol2', uselist=False, back_populates='sedphy')
    sedchem1 = relationship('Sedchem1', uselist=False, back_populates='sedphy')
    sedchem2 = relationship('Sedchem2', uselist=False, back_populates='sedphy')
    station = relationship('Station', back_populates='sedphy_list')

