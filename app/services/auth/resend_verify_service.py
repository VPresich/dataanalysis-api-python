import os
import uuid
from fastapi import HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models import User
from .send_token import send_token


async def resend_verify_service(email: str):
    """
    Resend a verification email to an unverified user.
    If user is already verified, raise 400.
    If user not found, raise 404.    """

    async with get_db_session() as session:

        result = await session.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.verify:
            raise HTTPException(status_code=400, detail="User is already verified")

        verification_token = user.verification_token or str(uuid.uuid4())
        user.verification_token = verification_token
        await session.commit()

        backend_base_url = os.getenv("BACKEND_BASE_URL")
        redirect = f"{backend_base_url}/auth/verify/{verification_token}"

        return await send_token(email.lower(), "Verification email", redirect, "verification_email.html")
