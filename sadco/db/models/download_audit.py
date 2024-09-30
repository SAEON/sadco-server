from sqlalchemy import Column, DateTime, Numeric, Integer, String

from sadco.db import Base


class DownloadAudit(Base):
    __tablename__ = 'download_audit'

    timestamp = Column(DateTime(timezone=False), nullable=False, primary_key=True)
    client_id = Column(String, nullable=False, primary_key=True)
    user_id = Column(String)
    survey_type = Column(String)
    parameters = Column(String)
    download_file_size = Column(Numeric)
    download_file_checksum = Column(String)
    