from sqlalchemy import Column, Numeric, String
from sqlalchemy.orm import relationship

from sadco.db import Base


class SurveyType(Base):
    __tablename__ = 'survey_type'

    code = Column(Numeric(precision=38, scale=0), primary_key=True, nullable=False)
    name = Column(String(30))
    description = Column(String(100))
