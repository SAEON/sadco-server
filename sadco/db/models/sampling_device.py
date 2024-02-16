from sqlalchemy import Column, Numeric, String

from sadco.db import Base


class SamplingDevice(Base):
    __tablename__ = 'sampling_device'

    code = Column(Numeric(precision=38, scale=0), primary_key=True, nullable=False)
    name = Column(String(25), nullable=False)
