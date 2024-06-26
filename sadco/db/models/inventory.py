from sqlalchemy import Column, Numeric, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class Inventory(Base):
    __tablename__ = 'inventory'

    survey_id = Column(String(9), primary_key=True, nullable=False)
    data_centre = Column(String(5), nullable=False)
    project_name = Column(String(100))
    cruise_name = Column(String(50))
    national_pgm = Column(String(1))
    exchange_restrict = Column(String(1))
    coop_pgm = Column(String(1))
    coordinated_int = Column(String(1))
    planam_code = Column(Integer, ForeignKey(column='sadco.planam.code'))
    port_start = Column(String(20))
    port_end = Column(String(20))
    country_code = Column(Numeric(precision=38, scale=0), nullable=False)
    instit_code = Column(Integer, ForeignKey(column='sadco.institutes.code'))
    coord_code = Column(Numeric(precision=38, scale=0))
    sci_code_1 = Column(Integer, ForeignKey(column='sadco.scientists.code'))
    sci_code_2 = Column(Integer, ForeignKey(column='sadco.scientists.code'))
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    lat_north = Column(Numeric(precision=8, scale=5))
    lat_south = Column(Numeric(precision=8, scale=5))
    long_west = Column(Numeric(precision=8, scale=5))
    long_east = Column(Numeric(precision=8, scale=5))
    areaname = Column(String(50))
    domain = Column(String(10))
    track_chart = Column(String(1))
    target_country_code = Column(Numeric(precision=38, scale=0), nullable=False)
    stnid_prefix = Column(String(3))
    gmt_diff = Column(Numeric(precision=38, scale=0))
    gmt_freeze = Column(String(1))
    projection_code = Column(Numeric(precision=38, scale=0))
    spheroid_code = Column(Numeric(precision=38, scale=0))
    datum_code = Column(Numeric(precision=38, scale=0))
    data_recorded = Column(String(1))
    survey_type_code = Column(Integer, ForeignKey(column='sadco.survey_type.code'))
    data_available = Column(String(1))

    survey = relationship('Survey', uselist=False, back_populates='inventory')
    cur_moorings = relationship('CurMooring', back_populates='inventory')
    wet_stations = relationship('WetStation', back_populates='inventory')
    planam = relationship('Planam', uselist=False)
    institute = relationship('Institutes', uselist=False)
    survey_type = relationship('SurveyType', uselist=False)
    scientist_1 = relationship("Scientists", foreign_keys=[sci_code_1], backref="inventory.sci_code_1", uselist=False)
    scientist_2 = relationship("Scientists", foreign_keys=[sci_code_2], backref="inventory.sci_code_2", uselist=False)
    inv_stats = relationship("InvStats", uselist=False, back_populates="inventory")

