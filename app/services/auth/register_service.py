import uuid
import bcrypt
from fastapi import HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models import User, ThemeEnum
from app.utils.constants import DEF_THEME, PATH_DEF_LIGHT_AVATAR
from app.utils import generate_jwt


async def register_service(data: dict):
    """
    User registration service.

    Steps:
      1. Check if a user with the given email already exists.
      2. Hash the user's password securely using bcrypt.
      3. Create a new User record in the database.
      4. Commit and refresh to get the database-generated _id.
      5. Generate a JWT token for the user.
      6. Update the user record with the token.
      7. Return a JSON-compatible dictionary with token and user info.
    """
    name = data.get("name")
    email = data.get("email", "").lower()
    password = data.get("password")

    async with get_db_session() as session:

        # Check if email is already registered
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=409, detail="Email in use")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # -----------------------------
        # Create a new User object
        # Store verification_token to enable email verification later
        # -----------------------------
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            avatar_url=PATH_DEF_LIGHT_AVATAR,
            theme=ThemeEnum(DEF_THEME),  # default theme
            verification_token=str(uuid.uuid4()),  # token for email verification
            verify=False  # user not verified yet
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        # -----------------------------
        # Generate JWT token
        # This token is stored in the user record (like MongoDB)
        # -----------------------------
        user_token = generate_jwt(str(new_user._id))
        new_user.token = user_token
        await session.commit()

        # -----------------------------
        # Optional: send verification email
        # Example: await send_verification_email(email, new_user.verification_token)
        # -----------------------------

        # Prepare response for frontend
        return {
            "token": user_token,
            "user": {
                "name": new_user.name,
                "email": new_user.email,
                "avatarURL": new_user.avatar_url,
                "theme": new_user.theme.name
            },
        }
