from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from sadco.db import Base


class WetPeriod(Base):
    __tablename__ = 'wet_period'

    code = Column(Integer, primary_key=True)
    station_id = Column(String(4), ForeignKey('sadco.wet_station.station_id'))
    instrument_code = Column(Integer, ForeignKey('sadco.edm_instrument2.code'), nullable=False)
    height_surface = Column(Numeric(10, 1))
    height_msl = Column(Numeric(10, 1))
    speed_corr_factor = Column(Numeric(5, 2))
    speed_aver_method = Column(String(6))
    dir_aver_method = Column(String(6))
    wind_sampling_interval = Column(Numeric(9, 0))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    sample_interval = Column(Numeric(9, 0))
    number_records = Column(Numeric(9, 0))
    number_null_records = Column(Numeric(9, 0))
    load_date = Column(DateTime)

    wet_station = relationship('WetStation', uselist=False, back_populates='wet_periods')
    wet_data_list = relationship('WetData', back_populates='wet_period')
    edm_instrument2 = relationship('EDMInstrument2', uselist=False, back_populates='wet_period')


