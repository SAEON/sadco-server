from sqlalchemy import Column, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class Survey(Base):
    """Represents a survey"""

    __tablename__ = 'survey'

    survey_id = Column(String(9), primary_key=True, nullable=False)
    institute = Column(String(7), nullable=False)

    instit_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.institutes.code'))
    prjnam = Column(String(10))
    expnam = Column(String(10))
    planam = Column(String(10))
    planam_code = Column(Numeric(precision=38, scale=0), ForeignKey('sadco.planam.code'))
    notes_1 = Column(String(200))
    notes_2 = Column(String(40))
    notes_3 = Column(String(40))
    notes_4 = Column(String(40))

    # view of associated stations (one-to-many)
    stations = relationship('Station')

    institute = relationship('Institutes')
    planam = relationship('Planam')

