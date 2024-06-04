from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship

from sadco.db import Base


class CurData(Base):
    __tablename__ = 'cur_data'

    code = Column(Integer, primary_key=True, nullable=False)
    depth_code = Column(Integer, ForeignKey(column='sadco.cur_depth.code'), nullable=False)
    datetime = Column(DateTime(timezone=False))
    speed = Column(Numeric(7, 3))
    direction = Column(Numeric(6, 2))
    temperature = Column(Numeric(6, 4))
    vert_velocity = Column(Numeric(4, 2))
    f_speed_9 = Column(Numeric(4, 2))
    f_direction_9 = Column(Numeric(5, 1))
    f_speed_14 = Column(Numeric(4, 2))
    f_direction_14 = Column(Numeric(5, 1))
    pressure = Column(Numeric(8, 4))

    cur_depth = relationship('CurDepth', back_populates='cur_data_list')
