from pydantic import BaseModel, Field, conint, ConfigDict


class DataSourceValidation(BaseModel):
    source_number: int = Field(..., description="Number of the source")
    source_name: str = Field("dataIMM", max_length=50, description="Name of the source")
    file_name: str = Field("logIMM.txt", max_length=255, description="File name associated with the source")
    comment: str | None = Field(None, max_length=500, description="Optional comment about the source")


class SourceNumberValidation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    source_number: conint(strict=True, gt=0) = Field(  # pyright: ignore[reportInvalidTypeForm]
        default=...,
        description="Source number must be a positive integer"
    )


class SourceUpdateValidation(BaseModel):
    source_name: str | None = Field(None, max_length=50, description="Name of the source")
    file_name: str | None = Field(None, max_length=255, description="File name associated with the source")
    comment: str | None = Field(None, max_length=500, description="Optional comment about the source")
