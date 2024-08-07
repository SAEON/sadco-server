from sqlalchemy import Column, Numeric, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from sadco.db import Base
from sadco.db.models import Watphy


class Watpol1(Base):
    __tablename__ = 'watpol1'

    watphy_code = Column(Integer, ForeignKey('sadco.watphy.code'), primary_key=True)
    arsenic = Column(Numeric(precision=7, scale=3))
    cadmium = Column(Numeric(precision=6, scale=3))
    chromium = Column(Numeric(precision=8, scale=3))
    cobalt = Column(Numeric(precision=7, scale=3))
    copper = Column(Numeric(precision=7, scale=3))
    iron = Column(Numeric(precision=9, scale=3))
    lead = Column(Numeric(precision=7, scale=3))
    manganese = Column(Numeric(precision=7, scale=3))
    mercury = Column(Numeric(precision=7, scale=4))
    nickel = Column(Numeric(precision=7, scale=3))
    selenium = Column(Numeric(precision=7, scale=3))
    zinc = Column(Numeric(precision=7, scale=3))

    watphy = relationship(Watphy, uselist=False, back_populates='watpol1')


class Watpol2(Base):
    __tablename__ = 'watpol2'

    watphy_code = Column(Integer, ForeignKey('sadco.watphy.code'), primary_key=True)
    aluminium = Column(Numeric(precision=5, scale=0))
    antimony = Column(Numeric(precision=7, scale=3))
    bismuth = Column(Numeric(precision=3, scale=1))
    molybdenum = Column(Numeric(precision=3, scale=1))
    silver = Column(Numeric(precision=7, scale=3))
    titanium = Column(Numeric(precision=4, scale=0))
    vanadium = Column(Numeric(precision=4, scale=2))

    watphy = relationship(Watphy, uselist=False, back_populates='watpol2')
