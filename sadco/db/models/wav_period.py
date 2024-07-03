from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class WavPeriod(Base):
    __tablename__ = 'wav_period'

    station_id = Column(String(4), ForeignKey('sadco.wav_station.station_id'), nullable=False, primary_key=True)
    yearp = Column(Numeric(38, 0), nullable=False)
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

    wav_station = relationship("WavStation", back_populates="wav_periods", uselist=False)
