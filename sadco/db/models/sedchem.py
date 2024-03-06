from sqlalchemy import Column, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base
from sadco.db.models import Sedphy


class Sedchem1(Base):
    __tablename__ = 'sedchem1'

    sedphy_code = Column(Integer, ForeignKey('sadco.sedphy.code'), primary_key=True)
    fluoride = Column(Numeric(precision=7, scale=3))
    kjn = Column(Numeric(precision=6, scale=2))
    oxa = Column(Numeric(precision=6, scale=3))
    toc = Column(Numeric(precision=6, scale=3))
    ptot = Column(Numeric(precision=6, scale=3))

    sedphy = relationship(Sedphy, uselist=False, back_populates='sedchem1')


class Sedchem2(Base):
    __tablename__ = 'sedchem2'

    sedphy_code = Column(Integer, ForeignKey('sadco.sedphy.code'), primary_key=True)
    calcium = Column(Numeric(precision=9, scale=3))
    magnesium = Column(Numeric(precision=7, scale=2))
    potassium = Column(Numeric(precision=7, scale=3))
    sodium = Column(Numeric(precision=7, scale=2))
    strontium = Column(Numeric(precision=8, scale=3))
    so3 = Column(Numeric(precision=6, scale=3))

    sedphy = relationship(Sedphy, uselist=False, back_populates='sedchem2')
