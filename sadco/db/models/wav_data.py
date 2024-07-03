from sqlalchemy import Column, String, Numeric, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from sadco.db import Base


class WavData(Base):
    __tablename__ = 'wav_data'

    code = Column(Integer, primary_key=True, nullable=False)
    station_id = Column(String(4), ForeignKey('sadco.wav_station.station_id'), nullable=False)
    date_time = Column(DateTime, nullable=False)
    number_readings = Column(Numeric(38, 0))
    record_length = Column(Numeric(4, 1))
    deltaf = Column(Numeric(8, 6))
    deltat = Column(Numeric(5, 2))
    frequency = Column(Numeric(8, 6))
    qp = Column(Numeric(5, 2))
    tb = Column(Numeric(5, 2))
    te = Column(Numeric(5, 2))
    wap = Column(Numeric(8, 2))
    eps = Column(Numeric(5, 3))
    hmo = Column(Numeric(5, 2))
    h1 = Column(Numeric(5, 2))
    hs = Column(Numeric(5, 2))
    hmax = Column(Numeric(5, 2))
    tc = Column(Numeric(5, 2))
    tp = Column(Numeric(5, 2))
    tz = Column(Numeric(5, 2))
    ave_direction = Column(Numeric(6, 2))
    ave_spreading = Column(Numeric(6, 2))
    instrument_code = Column(Numeric(38, 0))
    mean_direction = Column(Numeric(6, 2))
    mean_spreading = Column(Numeric(6, 2))

    wav_station = relationship('WavStation', back_populates='wav_data_list', uselist=False)