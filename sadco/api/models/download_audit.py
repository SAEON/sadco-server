from pydantic import BaseModel


class DownloadAuditModel(BaseModel):
    timestamp: str
    survey_type: str
    parameters: dict
