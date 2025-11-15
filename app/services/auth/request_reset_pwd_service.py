import os
from fastapi import HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models import User
from .send_token import send_token
from app.utils import generate_jwt


async def request_reset_pwd_service(email: str):
    """
    Sends a password reset email to the user.
    Raises 404 if user not found.
    The JWT token will include email only if provided.
    """
    require_email_verification = os.getenv("REQUIRE_EMAIL_VERIFICATION", "true").lower() == "true"

    async with get_db_session() as session:
        result = await session.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if require_email_verification and not user.verify:
            raise HTTPException(status_code=403, detail="Please verify your email before reset password.")

        reset_token = generate_jwt(user._id, expires_in=15 * 60, email=user.email)

        backend_base_url = os.getenv("FRONTEND_BASE_URL")
        reset_link = f"{backend_base_url}password/reset/{reset_token}"

        await send_token(user.email.lower(), "Reset your password", reset_link, "reset_password_email.html")
