import asyncio
import os
import aiofiles
from pathlib import Path
import cloudinary
import cloudinary.uploader
from app.config.cloudinary import CLOUD_NAME, API_KEY, API_SECRET


async def save_file_to_cloudinary(source_path: str, folder: str, size: int) -> str:
    """
    Uploads a file to Cloudinary and returns the secure URL of the uploaded image.

    :param file_path: Path to the local file to be uploaded.
    :param new_file_name: The name under which the file will be saved in Cloudinary.
    :param folder: The Cloudinary folder where the file will be stored.
    :param size: Desired width and height of the image after transformation.
    :return: A secure (HTTPS) URL of the uploaded image.
    """
    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=API_KEY,
        api_secret=API_SECRET,
        secure=True
    )

    try:
        result = cloudinary.uploader.upload(
            source_path,
            public_id=Path(source_path).name,
            folder=folder,
            allowed_formats=["jpg", "jpeg", "png"],
            transformation=[{"width": size, "height": size, "crop": "limit"}],
        )

        # Remove local file asynchronously
        try:
            # Just check if the file can be opened
            async with aiofiles.open(source_path, "rb"):
                pass
            # Delete file in a thread to avoid blocking
            await asyncio.to_thread(os.remove, source_path)
        except Exception as e:
            print(f"Warning: Failed to delete local file {source_path}: {e}")

        return result["secure_url"]

    except Exception as error:
        print("Error uploading file to Cloudinary:", error)
        raise
