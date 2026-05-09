from uuid import UUID
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_theme_service(id: str, session: AsyncSession):
    """
    Get the theme of a user by their ID from the users table.
    """
    result = await session.execute(
        select(User).where(User._id == UUID(id))
    )
    user = result.scalar_one_or_none()

    return user.theme.name
