from sqlalchemy import Column, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class WetStation(Base):
    __tablename__ = 'wet_station'

    station_id = Column(String(4), primary_key=True)
    survey_id = Column(String(9), ForeignKey('sadco.inventory.survey_id'))
    latitude = Column(Numeric(8, 5), nullable=False)
    longitude = Column(Numeric(8, 5), nullable=False)
    name = Column(String(30))
    client_code = Column(Numeric(38, 0), nullable=False)

    wet_period_counts = relationship('WetPeriodCounts', back_populates='wet_station')
    inventory = relationship('Inventory', back_populates='wet_stations', uselist=False)
