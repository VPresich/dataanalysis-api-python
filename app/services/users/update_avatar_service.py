from fastapi import HTTPException
from uuid import UUID
from app.database import get_db_session
from app.models import User
from app.utils.constants import AVATAR_SIZE
from app.config.flags import USE_CLOUDINARY
from app.utils import save_file_to_cloudinary, save_file_to_uploaddir
from sqlalchemy import select


async def update_avatar_service(user_id: str, source_path: str) -> str:
    """
    Uploads avatar and updates user's avatar_url in the database.
    Handles both Cloudinary and local upload depending on environment.

    :param user_id: ID of the user
    :param source_path: Path to uploaded file
    :return: New avatar URL
    :raises HTTPException: if file not provided or user not found
    """

    if USE_CLOUDINARY:
        avatar_url = await save_file_to_cloudinary(source_path, "avatars", AVATAR_SIZE)
    else:
        avatar_url = await save_file_to_uploaddir(source_path)

    # Update user in database
    async with get_db_session() as session:
        result = await session.execute(
            select(User).where(User._id == UUID(user_id))
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.avatar_url = avatar_url
        await session.commit()

    return avatar_url
