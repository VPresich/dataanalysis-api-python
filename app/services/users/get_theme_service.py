from fastapi import HTTPException
from uuid import UUID
from app.models import User
from app.database import get_db_session
from sqlalchemy import select


async def get_theme_service(user: dict):
    """
    Get the theme of a user by their ID from the users table.
    """
    async with get_db_session() as session:
        result = await session.execute(
            select(User).where(User._id == UUID(user["id"]))
        )
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if not db_user.theme:
            raise HTTPException(status_code=404, detail="Theme not set")

        return db_user.theme.name
