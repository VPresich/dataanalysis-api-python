from fastapi import UploadFile, File, HTTPException
import os
import uuid
from app.config.paths import TEMP_UPLOAD_DIR
from app.utils.constants import MAX_FILE_SIZE
from typing import Optional


def upload_file(field_name: str, required: bool = True):
    """
    Factory dependency: returns dependency for uploading a file from the given field_name.

    :param field_name: Name of the multipart/form-data field.
    :param required: Whether the file is required or optional.
    """
    default = ... if required else None

    async def _upload_file(file: Optional[UploadFile] = File(default, description="Upload file", alias=field_name)) -> Optional[str]:
        if not file:
            return None

        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE} limit")

        ext = os.path.splitext(file.filename)[1]
        base = os.path.splitext(file.filename)[0]
        suffix = uuid.uuid4().hex
        filename = f"{base}-{suffix}{ext}"
        file_path = os.path.join(TEMP_UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        return file_path

    return _upload_file
