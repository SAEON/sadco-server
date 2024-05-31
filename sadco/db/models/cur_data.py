from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from sadco.db import Base


class CurData(Base):
    __tablename__ = 'cur_data'

    code = Column(Numeric(38, 0), primary_key=True, nullable=False)
    depth_code = Column(Numeric(38, 0), ForeignKey(column='sadco.cur_depth.code'), nullable=False)
    datetime = Column(DateTime(timezone=False))
    speed = Column(Numeric(4, 3))
    direction = Column(Numeric(4, 2))
    temperature = Column(Numeric(4, 4))
    vert_velocity = Column(Numeric(2, 2))
    f_speed_9 = Column(Numeric(2, 2))
    f_direction_9 = Column(Numeric(4, 1))
    f_speed_14 = Column(Numeric(4, 2))
    f_direction_14 = Column(Numeric(4, 1))
    pressure = Column(Numeric(4, 4))

    cur_depth = relationship('CurDepth', back_populates='cur_data_list')
