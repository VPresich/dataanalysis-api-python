from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class DataSourceSchema(BaseModel):
    _id: UUID
    id_user: UUID
    source_number: int
    source_name: str
    file_name: str
    comment: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
