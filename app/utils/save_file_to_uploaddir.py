import asyncio
import time
from pathlib import Path
from app.config.paths import UPLOAD_DIR
from app.config.urls import APP_DOMAIN


async def save_file_to_uploaddir(file_path: str, user_id: str) -> str:
    """
    Moves a file from TEMP upload dir to PERMANENT UPLOAD_DIR for a specific user,
    replacing any previous avatar, and returns public URL.

    :param file_path: Full path to the saved temp file
    :param user_id: User ID to form the filename
    :return: Public URL to access the file
    """
    source = Path(file_path)
    ext = source.suffix
    filename = f"{user_id}-avatar{ext}"
    destination = Path(UPLOAD_DIR) / filename

    # Move file (replace if exists)
    await asyncio.to_thread(source.replace, destination)

    version = int(time.time() * 1000)

    return f"{APP_DOMAIN}/uploads/{filename}?v={version}"
