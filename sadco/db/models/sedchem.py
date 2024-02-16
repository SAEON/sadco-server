from sqlalchemy import Column, Numeric, ForeignKey

from sadco.db import Base


class Sedchem1(Base):
    __tablename__ = 'sedchem1'

    sedphy_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.sedphy.code'), primary_key=True)
    fluoride = Column(Numeric(precision=7, scale=3))
    kjn = Column(Numeric(precision=6, scale=2))
    oxa = Column(Numeric(precision=6, scale=3))
    toc = Column(Numeric(precision=6, scale=3))
    ptot = Column(Numeric(precision=6, scale=3))


class Sedchem2(Base):
    __tablename__ = 'sedchem2'

    sedphy_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.sedphy.code'), primary_key=True)
    calcium = Column(Numeric(precision=9, scale=3))
    magnesium = Column(Numeric(precision=7, scale=2))
    potassium = Column(Numeric(precision=7, scale=3))
    sodium = Column(Numeric(precision=7, scale=2))
    strontium = Column(Numeric(precision=8, scale=3))
    so3 = Column(Numeric(precision=6, scale=3))

