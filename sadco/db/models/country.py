from sqlalchemy import Column, Integer, String

from sadco.db import Base


class Country(Base):
    __tablename__ = 'country'

    code = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
