from sqlalchemy import Column, Numeric, Integer, String
from sqlalchemy.orm import relationship

from sadco.db import Base


class Planam(Base):
    """Platform Name. The name and other details of a physical research platform."""

    __tablename__ = 'planam'

    code = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    platform_code = Column(Numeric(precision=38, scale=0), nullable=False)
    callsign = Column(String(7))
    nodc_country_code = Column(String(2))
    nodc_ship_code = Column(String(2))
    wod_code = Column(Numeric(precision=38, scale=0))
