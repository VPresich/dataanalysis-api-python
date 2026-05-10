import bcrypt
import uuid
from app.models import User, ThemeEnum
from app.utils.constants import PATH_DEF_AVATAR


async def create_user(db_session, *, name="Real User", password="secret_password", verify=True):

    email = f"user_{uuid.uuid4().hex[:6]}@test.com"
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(
        name=name,
        email=email,
        password=hashed_password,
        verify=verify,
        theme=ThemeEnum.default,
        avatar_url=PATH_DEF_AVATAR
    )

    db_session.add(user)
    await db_session.commit()

    return user, password
