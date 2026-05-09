from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from app.models import User


async def get_avatar_url_service(user_id: str, session: AsyncSession) -> str:
    """
    Service to get the avatar URL of a user by their ID.

    :param user_id: User's ID as string
    :return: Avatar URL
    :raises HTTPException 401: If user not found
    :raises HTTPException 404: If avatar URL is not set
    """

    result = await session.execute(select(User).where(User._id == UUID(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.avatar_url:
        raise HTTPException(status_code=404, detail="User avatar not found")

    return user.avatar_url
