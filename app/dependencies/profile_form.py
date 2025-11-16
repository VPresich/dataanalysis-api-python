from fastapi import Form
from typing import Optional
from app.validation import ProfileValidation


async def profile_form(
    name: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    theme: Optional[str] = Form(None)
) -> ProfileValidation:
    return ProfileValidation(name=name, password=password, theme=theme)
