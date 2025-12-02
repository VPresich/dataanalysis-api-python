from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


class DataSourceSchema(BaseModel):
    id: UUID = Field(..., alias="_id")
    id_user: UUID
    source_number: int
    source_name: str
    file_name: str
    comment: str | None = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
