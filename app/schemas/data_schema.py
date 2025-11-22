from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class DataSchema(BaseModel):
    id: UUID = Field(..., alias="_id")
    id_source: UUID

    CVpositive: Optional[str] = "None"
    CVstable: Optional[str] = "None"
    CApositive: Optional[str] = "None"
    CAstable: Optional[str] = "None"
    CTpositive: Optional[str] = "None"
    CTstable: Optional[str] = "None"

    X: float = 0.0
    Y: float = 0.0
    Z: float = 0.0

    Kde: Optional[str] = "None"
    KdeWeighted: Optional[str] = "None"
    Gaussian: Optional[str] = "None"
    GaussianWeighted: Optional[str] = "None"

    EvaluationNum: Optional[str] = "None"
    IMMconsistentValue: Optional[str] = "None"
    probability: Optional[str] = "None"

    TrackConsistent: Optional[str] = "None"
    VelocityConsistent: Optional[str] = "None"
    IMMconsistent: Optional[str] = "None"
    IMMpositive: Optional[str] = "None"
    velocityOK: Optional[str] = "None"
    speed: Optional[str] = "None"

    TrackNum: int = 0
    Time: float = 0.0

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={UUID: str}
    )
