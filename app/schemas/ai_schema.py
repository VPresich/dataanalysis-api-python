from pydantic import BaseModel


class AIChatRequest(BaseModel):
    id_source: str
    TrackNum: int


class AIChatResponse(BaseModel):
    status: str
    response: str
