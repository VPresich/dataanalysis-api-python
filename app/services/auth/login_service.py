import bcrypt
from fastapi import HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models import User
from app.utils import generate_jwt


async def login_service(request_data: dict):
    """
    User login service.

    Steps:
      1. Extract email and password from request data.
      2. Find user by email in the users table.
      3. Raise 401 if user does not exist or password is wrong.
      4. Optionally, check user.verify if needed (commented out).
      5. Generate JWT token and save it in user.token.
      6. Commit changes and return token + user info.
    """
    email = request_data.get("email", "").lower()
    password = request_data.get("password")

    async with get_db_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="Email or password is wrong")

        # Uncomment if account verification is required
        # if not user.verify:
        #     raise HTTPException(status_code=401, detail="Your account is not verified")

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise HTTPException(status_code=401, detail="Email or password is wrong")

        # Generate JWT token
        user_token = generate_jwt(str(user._id))

        # Save token in user table
        user.token = user_token
        await session.commit()

        return {
            "token": user_token,
            "user": {
                "name": user.name,
                "email": user.email,
                "avatarURL": user.avatar_url,
                "theme": user.theme.name,
            },
        }
