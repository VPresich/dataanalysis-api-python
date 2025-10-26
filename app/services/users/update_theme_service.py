from fastapi import HTTPException
from uuid import UUID
from app.database import get_db_session
from app.models import User, ThemeEnum
from sqlalchemy import select


async def update_theme_service(user: dict, color: str):
    """
    Update user's theme in the users table.
    """
    async with get_db_session() as session:
        result = await session.execute(
            select(User).where(User._id == UUID(user["id"]))
        )
        db_user = result.scalar_one_or_none()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.theme = ThemeEnum(color)
        await session.commit()
        await session.refresh(db_user)

        return {"theme": db_user.theme.name}
