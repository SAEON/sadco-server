from pydantic import BaseModel
from datetime import date


class DownloadAuditModel(BaseModel):
    timestamp: date
    survey_type: str
    parameters: str
