from sqlalchemy import Column, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base
from sadco.db.models import Watphy


class Watchem1(Base):
    __tablename__ = 'watchem1'

    watphy_code = Column(Integer, ForeignKey('sadco.watphy.code'), primary_key=True)
    dic = Column(Numeric(precision=9, scale=3))
    doc = Column(Numeric(precision=6, scale=2))
    fluoride = Column(Numeric(precision=7, scale=3))
    iodene = Column(Numeric(precision=6, scale=3))
    iodate = Column(Numeric(precision=6, scale=3))
    kjn = Column(Numeric(precision=6, scale=2))
    nh3 = Column(Numeric(precision=5, scale=2))
    nitrogen = Column(Numeric(precision=6, scale=2))
    oxa = Column(Numeric(precision=6, scale=3))
    ph = Column(Numeric(precision=4, scale=2))

    watphy = relationship(Watphy, uselist=False, back_populates='watchem1')


class Watchem2(Base):
    __tablename__ = 'watchem2'

    watphy_code = Column(Integer, ForeignKey('sadco.watphy.code'), primary_key=True)
    calcium = Column(Numeric(precision=9, scale=3))
    cesium = Column(Numeric(precision=6, scale=3))
    hydrocarbons = Column(Numeric(precision=6, scale=2))
    magnesium = Column(Numeric(precision=7, scale=2))
    pah = Column(Numeric(precision=6, scale=2))
    potassium = Column(Numeric(precision=7, scale=3))
    rubidium = Column(Numeric(precision=6, scale=3))
    sodium = Column(Numeric(precision=7, scale=2))
    strontium = Column(Numeric(precision=8, scale=3))
    so4 = Column(Numeric(precision=6, scale=4))
    sussol = Column(Numeric(precision=6, scale=3))

    watphy = relationship(Watphy, uselist=False, back_populates='watchem2')
