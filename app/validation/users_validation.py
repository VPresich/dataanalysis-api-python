from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Annotated
from app.utils.constants import NAME_PATTERN, VALID_THEMES
import re


class ProfileValidation(BaseModel):
    name: Optional[Annotated[str, Field(min_length=2, max_length=32)]] = None
    password: Optional[Annotated[str, Field(min_length=6)]] = None
    theme: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, v):
        if v and not re.match(NAME_PATTERN, v):
            raise ValueError("Name must contain only allowed characters (2-32 chars)")
        return v

    @field_validator("theme")
    def validate_theme(cls, v):
        if v is None:
            return v
        v_lower = v.lower()
        if v_lower not in VALID_THEMES:
            raise ValueError(f"Theme must be one of {VALID_THEMES}")
        return v_lower


class ThemeValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    theme: str

    @field_validator("theme")
    def validate_theme(cls, v):
        v_lower = v.lower()
        if v_lower not in VALID_THEMES:
            raise ValueError(f"Theme must be one of {VALID_THEMES}")
        return v_lower
