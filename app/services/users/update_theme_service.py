from fastapi import HTTPException
from uuid import UUID
from app.database import get_db_session
from app.models import User, ThemeEnum
from sqlalchemy import select


async def update_theme_service(id: str, theme: str):
    """
    Update user's theme in the users table.
    """
    async with get_db_session() as session:
        result = await session.execute(
            select(User).where(User._id == UUID(id))
        )
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate theme
        try:
            db_user.theme = ThemeEnum(theme)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid theme value")

        await session.commit()
        await session.refresh(db_user)

        return db_user.theme.name
