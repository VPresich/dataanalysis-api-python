import asyncio
import os
from pathlib import Path
from app.config.paths import UPLOAD_DIR
from app.config.urls import APP_DOMAIN


async def save_file_to_uploaddir(file_path: str) -> str:
    """
    Moves a file from TEMP upload dir to PERMANENT UPLOAD_DIR
    and returns public URL.

    :param file_path: Full path to the saved temp file
    :return: Public URL to access the file
    """

    source = Path(file_path)
    filename = source.name
    destination = Path(UPLOAD_DIR) / filename

    # Move file (async via thread)
    await asyncio.to_thread(os.rename, source, destination)

    return f"{APP_DOMAIN}/uploads/{filename}"
