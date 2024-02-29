from sqlalchemy import Column, Numeric, Integer, ForeignKey

from sadco.db import Base


class Watqc(Base):
    __tablename__ = 'watqc'

    watphy_code = Column(Integer, ForeignKey('sadco.watphy.code'), primary_key=True, nullable=False)
    spldep = Column(Numeric(precision=38, scale=0))
    disoxygen = Column(Numeric(precision=38, scale=0))
    salinity = Column(Numeric(precision=38, scale=0))
    temperature = Column(Numeric(precision=38, scale=0))
    no3 = Column(Numeric(precision=38, scale=0))
    po4 = Column(Numeric(precision=38, scale=0))
    sio3 = Column(Numeric(precision=38, scale=0))
    chla = Column(Numeric(precision=38, scale=0))
    dic = Column(Numeric(precision=38, scale=0))
    ph = Column(Numeric(precision=38, scale=0))
