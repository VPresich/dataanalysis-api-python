import uuid
from app.utils.constants import DEF_THEME, PATH_DEF_LIGHT_AVATAR
from app.utils.fake_data import fake_users_db


async def register_service(request_data: dict):
    """
    Stub registration service.
    In a real implementation, this would:
      - Hash the password
      - Save the new user in the DB
      - Create a token
      - Initialize user theme and avatar
    """
    name = request_data.get("name")
    email = request_data.get("email", "").lower()
    password = request_data.get("password")

    # Check if user already exists
    if email in fake_users_db:
        raise ValueError("Email already exists")

    # Fake password hashing and token generation
    token = f"fake-jwt-{uuid.uuid4()}"
    fake_users_db[email] = {
        "name": name,
        "email": email,
        "password": password,  # (real impl. should hash)
        "avatarURL": PATH_DEF_LIGHT_AVATAR,
        "theme": DEF_THEME,
    }

    # Return response
    return {
        "token": token,
        "user": {
            "name": name,
            "email": email,
            "avatarURL": PATH_DEF_LIGHT_AVATAR,
            "theme": DEF_THEME,
        },
    }
