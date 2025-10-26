from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from typing import Annotated
from app.utils.constants import EMAIL_PATTERN, NAME_PATTERN, VALID_THEMES
import re


class RegisterValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Annotated[str, Field(min_length=2, max_length=32)]
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]
    app: Optional[str] = "dataanalysis"

    @field_validator("name")
    def validate_name(cls, v):
        if not re.match(NAME_PATTERN, v):
            raise ValueError("Name must contain only allowed characters (2-32 chars)")
        return v

    @field_validator("email")
    def validate_email(cls, v):
        if not re.match(EMAIL_PATTERN, v):
            raise ValueError("Invalid email format")
        return v


class LoginValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]
    app: Optional[str] = "dataanalysis"

    @field_validator("email")
    def validate_email(cls, v):
        if not re.match(EMAIL_PATTERN, v):
            raise ValueError("Invalid email format")
        return v


class ProfileValidation(BaseModel):
    name: Optional[Annotated[str, Field(min_length=2, max_length=32)]] = None
    email: Optional[EmailStr] = None
    password: Optional[Annotated[str, Field(min_length=6)]] = None
    theme: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, v):
        if v and not re.match(NAME_PATTERN, v):
            raise ValueError("Name must contain only allowed characters (2-32 chars)")
        return v

    @field_validator("email")
    def validate_email(cls, v):
        if v and not re.match(EMAIL_PATTERN, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("theme")
    def validate_theme(cls, v):
        if v and v.lower() not in VALID_THEMES:
            raise ValueError(f"Theme must be one of {VALID_THEMES}")
        return v.lower() if v else v


class ThemeValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    color: str

    @field_validator("color")
    def validate_color(cls, v):
        if v.lower() not in VALID_THEMES:
            raise ValueError(f"Theme must be one of {VALID_THEMES}")
        return v.lower()
