from sqlalchemy import Column, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base
from sadco.db.models import Watphy


class Watcurrents(Base):
    __tablename__ = 'watcurrents'

    watphy_code = Column(Integer, ForeignKey('sadco.watphy.code'), primary_key=True, nullable=False)
    current_dir = Column(Numeric(precision=38, scale=0))
    current_speed = Column(Numeric(precision=4, scale=2))

    watphy = relationship(Watphy, uselist=False)
