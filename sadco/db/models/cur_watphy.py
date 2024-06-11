from sqlalchemy import Column, Numeric, ForeignKey, Integer
from sqlalchemy.orm import relationship

from sadco.db import Base


class CurWatphy(Base):
    __tablename__ = 'cur_watphy'

    depth_code = Column(Integer, ForeignKey(column='sadco.cur_depth.code'), nullable=False)
    data_code = Column(Integer, ForeignKey(column='sadco.cur_data.code'), nullable=False, primary_key=True)
    ph = Column(Numeric(4, 2))
    salinity = Column(Numeric(6, 4))
    dis_oxy = Column(Numeric(4, 2))

    cur_data = relationship('CurData', uselist=False, back_populates='cur_watphy')
    cur_depth = relationship('CurDepth', uselist=False, back_populates='cur_watphy_list')

