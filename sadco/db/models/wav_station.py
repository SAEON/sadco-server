from sqlalchemy import Column, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class WavStation(Base):
    __tablename__ = 'wav_station'

    station_id = Column(String(4), primary_key=True)
    survey_id = Column(String(9), ForeignKey('sadco.inventory.survey_id'))
    latitude = Column(Numeric(8, 5), nullable=False)
    longitude = Column(Numeric(8, 5), nullable=False)
    instrument_depth = Column(Numeric(38, 0))
    name = Column(String(30))
    water_depth = Column(Numeric(38, 0))

    inventory = relationship('Inventory', back_populates='wav_stations', uselist=False)
    wav_data_list = relationship('WavData', back_populates='wav_station')
    wav_periods = relationship('WavPeriod', back_populates='wav_station')
