from sqlalchemy import Column, String, Numeric

from sadco.db import Base


class SadUsers(Base):
    """Respresents a SADCO User."""

    __tablename__ = 'sad_users'

    userid = Column(String(50), primary_key=True)
    password = Column(String(20), nullable=False)
    user_type = Column(Numeric(precision=38, scale=0), nullable=False)
    flag_type = Column(Numeric(precision=38, scale=0), nullable=False)
    flag_password = Column(String(20))
    fname = Column(String(50))
    surname = Column(String(50))
    affiliation = Column(String(50))
    address = Column(String(200))
    occupation = Column(String(20))
