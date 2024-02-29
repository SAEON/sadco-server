from sqlalchemy import Column, Numeric, String
from sqlalchemy.orm import relationship

from sadco.db import Base


class Scientists(Base):
    __tablename__ = 'scientists'

    code = Column(Numeric(precision=38, scale=0), primary_key=True, nullable=False)
    surname = Column(String(20), nullable=False)
    f_name = Column(String(20))
    title = Column(String(5))
    instit_code = Column(Numeric(precision=38, scale=0))
