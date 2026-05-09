from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User


async def verify_email_service(verification_token: str, session: AsyncSession):
    """
    Service to verify a user's email using a verification token.

    Steps:
      1. Find the user by verification token.
      2. Raise 404 if token is invalid or expired.
      3. Raise 400 if user is already verified.
      4. Set user.verify = True and clear verification_token.
      5. Commit changes and return user.
    """

    stmt = select(User).where(User.verification_token == verification_token)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid or expired verification token")

    if user.verify:
        raise HTTPException(status_code=400, detail="User already verified")

    # Update user
    user.verify = True
    user.verification_token = None
    await session.commit()
    return
