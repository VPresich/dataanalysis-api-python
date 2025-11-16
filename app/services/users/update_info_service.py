from fastapi import HTTPException
import bcrypt
from uuid import UUID
from app.database import get_db_session
from app.models import User, ThemeEnum
from sqlalchemy import select


async def update_info_service(id: str, name: str, password: str, theme: str):
    """
    Update user's info in the users table.   """

    async with get_db_session() as session:
        result = await session.execute(
            select(User).where(User._id == UUID(id))
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if name:
            user.name = name

        if password:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user.password = hashed_password

        if theme:
            try:
                user.theme = ThemeEnum(theme)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid theme value")

        await session.commit()
        await session.refresh(user)

        return user
