from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from sadco.db import Base


class EDMInstrument2(Base):
    __tablename__ = 'edm_instrument2'

    code = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(30))

    cur_depth = relationship('CurDepth', uselist=False, back_populates='edm_instrument2')
    wet_period = relationship('WetPeriod', uselist=False, back_populates='edm_instrument2')

