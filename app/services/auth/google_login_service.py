import uuid
import secrets
import bcrypt
from app.models import User, ThemeEnum
from sqlalchemy import select
from app.database import get_db_session
from app.utils import generate_jwt
from fastapi import HTTPException
from app.utils.constants import DEF_THEME, PATH_DEF_AVATAR


async def google_login_service(data: dict) -> str:
    """
    Processes Google login data:
    - Saves or updates user in DB
    - Generates and stores JWT token
    """

    userinfo = data.get("userinfo", {})
    if not userinfo:
        raise HTTPException(status_code=400, detail="Google user information is missing")

    email = userinfo.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    async with get_db_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user:
            # Update existing user
            user.name = userinfo.get("name", user.name)
            user.google_id = userinfo.get("id", user.google_id)
        else:
            # Create a new user with a random secure password
            random_password = secrets.token_urlsafe(16)
            hashed_password = bcrypt.hashpw(random_password.encode(), bcrypt.gensalt()).decode()

            user = User(
                name=userinfo.get("name", ""),
                email=email,
                password=hashed_password,
                googleId=userinfo.get("id"),
                avatar_url=PATH_DEF_AVATAR,
                theme=ThemeEnum(DEF_THEME),
                verification_token=str(uuid.uuid4()),
                verify=False
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        # Generate and assign JWT token
        jwt_token = generate_jwt(str(user._id))
        user.token = jwt_token
        await session.commit()

        return jwt_token
