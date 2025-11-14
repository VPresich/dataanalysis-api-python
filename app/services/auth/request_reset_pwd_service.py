import os
from fastapi import HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models import User
from .send_token import send_token
from app.utils import generate_jwt


async def request_reset_pwd_service(email: str):
    """
    Resend a verification email to an unverified user.
    If user is already verified, raise 400.
    If user not found, raise 404.    """

    async with get_db_session() as session:
        result = await session.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        resetToken = generate_jwt(user._id, 15)

        await session.commit()
        backend_base_url = os.getenv("BACKEND_BASE_URL")
        redirect = f"{backend_base_url}password/reset/{resetToken}"

        return await send_token(email.lower(), "Reset your password", redirect, "reset_password_email.html")
