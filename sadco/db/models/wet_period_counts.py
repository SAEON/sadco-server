from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class WetPeriodCounts(Base):
    __tablename__ = 'wet_period_counts'

    station_id = Column(String(4), ForeignKey('sadco.wet_station.station_id'), nullable=False, primary_key=True)
    yearp = Column(Numeric(38, 0), nullable=False, primary_key=True)
    m01 = Column(Numeric(38, 0))
    m02 = Column(Numeric(38, 0))
    m03 = Column(Numeric(38, 0))
    m04 = Column(Numeric(38, 0))
    m05 = Column(Numeric(38, 0))
    m06 = Column(Numeric(38, 0))
    m07 = Column(Numeric(38, 0))
    m08 = Column(Numeric(38, 0))
    m09 = Column(Numeric(38, 0))
    m10 = Column(Numeric(38, 0))
    m11 = Column(Numeric(38, 0))
    m12 = Column(Numeric(38, 0))

    wet_station = relationship("WetStation", back_populates="wet_period_counts", uselist=False)
