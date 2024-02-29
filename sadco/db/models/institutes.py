from sqlalchemy import Column, Numeric, String
from sqlalchemy.orm import relationship

from sadco.db import Base


class Institutes(Base):
    __tablename__ = 'institutes'

    code = Column(Numeric(precision=38, scale=0), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(String(50))
