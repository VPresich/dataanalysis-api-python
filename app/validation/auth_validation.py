from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Annotated
from app.utils.constants import EMAIL_PATTERN, NAME_PATTERN
import re


class RegisterValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Annotated[str, Field(min_length=2, max_length=32)]
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]

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

    @field_validator("email")
    def validate_email(cls, v):
        if not re.match(EMAIL_PATTERN, v):
            raise ValueError("Invalid email format")
        return v


class EmailValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str

    @field_validator("email")
    def validate_email(cls, v: str) -> str:
        """
        Validate email format using regex.
        """
        if not re.match(EMAIL_PATTERN, v):
            raise ValueError(f"Invalid email format: {v}")
        return v
