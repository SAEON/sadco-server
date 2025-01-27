from pydantic import BaseModel


class VosSurveySearchResult(BaseModel):
    total: int
