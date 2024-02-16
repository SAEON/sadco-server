from sqlalchemy import Column, Numeric, ForeignKey

from sadco.db import Base


class Watchl(Base):
    __tablename__ = 'watchl'

    watphy_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.watphy.code'), primary_key=True, nullable=False)
    chla = Column(Numeric(precision=6, scale=3))
    chlb = Column(Numeric(precision=6, scale=3))
    chlc = Column(Numeric(precision=6, scale=3))
