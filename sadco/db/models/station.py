from sqlalchemy import Column, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.orm import relationship

from sadco.db import Base


class Station(Base):

    __tablename__ = 'station'

    station_id = Column(String(12), primary_key=True, nullable=False)

    survey_id = Column(String(9), ForeignKey('sadco.survey.survey_id'), primary_key=True, nullable=False)

    latitude = Column(Numeric(precision=8, scale=5), nullable=False)
    longitude = Column(Numeric(precision=8, scale=5), nullable=False)
    date_start = Column(TIMESTAMP(timezone=True), index=True, nullable=False)
    date_end = Column(TIMESTAMP(timezone=True), index=True, nullable=False)
    daynull = Column(String(1))
    stnnam = Column(String(10))
    stndep = Column(Numeric(precision=6, scale=2))
    offshd = Column(Numeric(precision=6, scale=3))
    passkey = Column(String(8))
    dupflag = Column(String(1))
    max_spldep = Column(Numeric(precision=6, scale=2))
    lat = Column(Numeric(precision=38, scale=0))
    lon = Column(Numeric(precision=38, scale=0))
    yearmon = Column(String(7))
    status_code = Column(Numeric(precision=38, scale=0), nullable=False)
    stn_ref = Column(String(5))
    notes = Column(String(2000))

    # view of associated watphy entries (one-to-many)
    watphy_list = relationship('Watphy')
    sedphy_list = relationship('Sedphy')
