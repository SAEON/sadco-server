from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from sadco.db import Base


class CurMooring(Base):
    __tablename__ = 'cur_mooring'

    code = Column(Integer, nullable=False, primary_key=True)
    client_code = Column(Numeric(38, 0), nullable=False)
    planam_code = Column(Numeric(38, 0))
    stnnam = Column(String(30))
    arenam = Column(String(30))
    description = Column(String(70))
    latitude = Column(Numeric(7, 5))
    longitude = Column(Numeric(8, 5))
    stndep = Column(Numeric(7, 2))
    date_time_start = Column(DateTime, nullable=False)
    date_time_end = Column(DateTime, nullable=False)
    number_of_depths = Column(Numeric(38, 0))
    publication_ref = Column(String(30))
    survey_id = Column(String(9), ForeignKey(column='sadco.inventory.survey_id'))
    prjnam = Column(String(100))

    cur_depths = relationship('CurDepth', back_populates='cur_mooring')
    inventory = relationship('Inventory', back_populates='cur_moorings')
