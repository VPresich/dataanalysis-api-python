import os
from datetime import datetime, timedelta, timezone
import jwt


def generate_jwt(user_id: str, expires_in: int = None, email: str | None = None) -> str:
    """
    Generates a JWT for a user with a specified expiration time.
    Includes email only if provided.

    :param user_id: User ID
    :param expires_in: Token lifetime in seconds (default is taken from env)
    :param email: Optional user email to include in the token
    :return: JWT token (str)
    """
    if expires_in is None:
        expires_in = int(os.getenv("JWT_EXPIRES_IN", 86400))

    expire_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    payload = {"id": str(user_id), "exp": expire_at}

    if email:
        payload["email"] = email

    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")
    return token
