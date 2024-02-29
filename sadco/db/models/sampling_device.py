from sqlalchemy import Column, Integer, String

from sadco.db import Base


class SamplingDevice(Base):
    __tablename__ = 'sampling_device'

    code = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(25), nullable=False)
