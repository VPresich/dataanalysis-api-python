from uuid import UUID
import jwt
from fastapi import Header, HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models import User
from app.config.jwt import JWT_SECRET


async def authenticate(authorization: str = Header(None)):
    """
    Middleware-style dependency to authenticate the user via JWT.
    Steps:
      1. Check for Authorization header.
      2. Split Bearer and token, validate type.
      3. Decode JWT and check expiration.
      4. Fetch user from DB and validate token match.
      5. Return user dict for controller usage.
    """

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        bearer, token = authorization.split(" ")
        if bearer.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")

        # Verify JWT and check expiration
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        async with get_db_session() as session:
            result = await session.execute(
                select(User).where(User._id == UUID(user_id))
            )
            user = result.scalar_one_or_none()
            if not user or user.token != token:
                raise HTTPException(status_code=401, detail="Token mismatch")

            # Return user info for controller usage
            return {
                "id": str(user._id),
                "name": user.name,
                "email": user.email,
                "avatarUrl": user.avatar_url,
                "theme": user.theme.name,
            }

    except jwt.ExpiredSignatureError:
        # Specific error for expired token
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        # Any other token-related error
        raise HTTPException(status_code=401, detail="Invalid token")
