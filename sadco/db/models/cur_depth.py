from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from sadco.db import Base


class CurDepth(Base):
    __tablename__ = 'cur_depth'

    survey_id = Column(String(9))
    code = Column(Integer, nullable=False, primary_key=True)
    mooring_code = Column(Integer, ForeignKey(column='sadco.cur_mooring.code'), nullable=False)
    spldep = Column(Numeric(6, 2))
    instrument_number = Column(Integer, ForeignKey(column='sadco.edm_instrument2.code'))
    deployment_number = Column(String(20))
    date_time_start = Column(DateTime, nullable=False)
    date_time_end = Column(DateTime, nullable=False)
    time_interval = Column(Numeric(38, 0))
    number_of_records = Column(Numeric(38, 0))
    passkey = Column(String(20))
    date_loaded = Column(DateTime, nullable=False)
    parameters = Column(String(10))

    cur_mooring = relationship('CurMooring', uselist=False, back_populates='cur_depths')
    cur_data_list = relationship('CurData', back_populates='cur_depth')
    cur_watphy_list = relationship('CurWatphy', back_populates='cur_depth')
    edm_instrument2 = relationship('EDMInstrument2', back_populates='cur_depth')

