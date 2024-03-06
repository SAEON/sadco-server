from sqlalchemy import Column, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base
from sadco.db.models import Watphy


class Watchl(Base):
    __tablename__ = 'watchl'

    watphy_code = Column(Integer, ForeignKey('sadco.watphy.code'), primary_key=True, nullable=False)
    chla = Column(Numeric(precision=6, scale=3))
    chlb = Column(Numeric(precision=6, scale=3))
    chlc = Column(Numeric(precision=6, scale=3))

    watphy = relationship(Watphy, uselist=False, back_populates='watchl')
