from uuid import UUID
from app.models import User
from app.database import get_db_session
from sqlalchemy import select


async def get_theme_service(id: str):
    """
    Get the theme of a user by their ID from the users table.
    """
    async with get_db_session() as session:
        result = await session.execute(
            select(User).where(User._id == UUID(id))
        )
        user = result.scalar_one_or_none()

        return user.theme.name
