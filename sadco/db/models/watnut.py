from sqlalchemy import Column, Numeric, ForeignKey

from sadco.db import Base


class Watnut(Base):
    __tablename__ = 'watnut'

    watphy_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.watphy.code'), primary_key=True, nullable=False)
    no2 = Column(Numeric(precision=5, scale=2))
    no3 = Column(Numeric(precision=5, scale=2))
    p = Column(Numeric(precision=6, scale=3))
    po4 = Column(Numeric(precision=5, scale=2))
    ptot = Column(Numeric(precision=6, scale=3))
    sio3 = Column(Numeric(precision=6, scale=2))
    sio4 = Column(Numeric(precision=6, scale=2))

