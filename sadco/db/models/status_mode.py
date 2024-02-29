from sqlalchemy import Column, Numeric, String

from sadco.db import Base


class StatusMode(Base):
    __tablename__ = 'status_mode'

    code = Column(Numeric(precision=38, scale=0), primary_key=True, nullable=False)
    flagging = Column(String(10), nullable=False)
    quality = Column(String(10), nullable=False)
