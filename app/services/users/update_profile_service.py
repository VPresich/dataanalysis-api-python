from fastapi import HTTPException
import bcrypt
from uuid import UUID
from app.database import get_db_session
from app.models import User, ThemeEnum
from app.config.flags import USE_CLOUDINARY
from app.utils.constants import AVATAR_SIZE
from app.utils import save_file_to_cloudinary, save_file_to_uploaddir
from sqlalchemy import select


async def update_profile_service(
    id: str,
    name: str | None = None,
    password: str | None = None,
    theme: str | None = None,
    file_path: str | None = None
):
    """
    Update user's info in the users table.   """

    avatar_url = None
    if file_path is not None:
        if USE_CLOUDINARY:
            avatar_url = await save_file_to_cloudinary(file_path, "avatars", AVATAR_SIZE)
        else:
            avatar_url = await save_file_to_uploaddir(file_path)

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

        if avatar_url:
            user.avatar_url = avatar_url

        await session.commit()
        await session.refresh(user)

        return user
