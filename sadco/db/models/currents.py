from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class Currents(Base):
    __tablename__ = 'currents'

    station_id = Column(String(12), ForeignKey('sadco.station.station_id'), primary_key=True, nullable=False)
    subdes = Column(String(10))
    spldattim = Column(DateTime, primary_key=True, nullable=False)
    spldep = Column(Numeric(precision=6, scale=2), nullable=False)
    current_dir = Column(Numeric(precision=38, scale=0))
    current_speed = Column(Numeric(precision=7, scale=3))
    perc_good = Column(String(20))

    station = relationship('Station', uselist=False, back_populates='currents')
