import bcrypt
import jwt
from fastapi import HTTPException
from sqlalchemy import select, update
from app.database import get_db_session
from app.models import User
from app.config.jwt import JWT_SECRET


async def reset_pwd_service(password: str, token: str):
    """
    Resets user password if the provided JWT reset token is valid and not expired.
    Token must contain the user's ID and be signed with the server secret.
    :param password: New password
    :param token: Reset token from email
    :raises HTTPException: 401 if token invalid, 404 if user not found
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        email = payload.get("email")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Reset token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    async with get_db_session() as session:
        result = await session.execute(
            select(User).where(User._id == user_id, User.email == email)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        await session.execute(
            update(User)
            .where(User._id == user._id)
            .values(password=hashed_password)
        )
        await session.commit()
