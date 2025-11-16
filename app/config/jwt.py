import os

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", 86400))

__all__ = ("JWT_SECRET", "JWT_EXPIRES_IN")
