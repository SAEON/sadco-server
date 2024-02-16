from sqlalchemy import Column, Numeric, ForeignKey

from sadco.db import Base


class Sedpol1(Base):
    __tablename__ = 'sedpol1'

    sedphy_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.sedphy.code'), primary_key=True)
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


class Sedpol2(Base):
    __tablename__ = 'sedpol2'

    sedphy_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.sedphy.code'), primary_key=True)
    aluminium = Column(Numeric(precision=5, scale=0))
    antimony = Column(Numeric(precision=7, scale=3))
    bismuth = Column(Numeric(precision=3, scale=1))
    molybdenum = Column(Numeric(precision=3, scale=1))
    silver = Column(Numeric(precision=7, scale=3))
    titanium = Column(Numeric(precision=4, scale=0))
    vanadium = Column(Numeric(precision=4, scale=2))

