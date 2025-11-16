import os

REQUIRE_EMAIL_VERIFICATION = (
    os.getenv("REQUIRE_EMAIL_VERIFICATION", "true").lower() == "true"
)

USE_CLOUDINARY = (os.getenv("ENABLE_CLOUDINARY") == "true")

__all__ = ("REQUIRE_EMAIL_VERIFICATION", "USE_CLOUDINARY")
