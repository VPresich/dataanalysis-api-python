from fastapi import HTTPException
from app.utils.constants import DEF_THEME
from app.utils.fake_data import fake_users_db


async def login_service(email: str, password: str):
    """
    Fake login service.
    Simulates database lookup and token generation.
    """

    user = fake_users_db.get(email.lower())
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Email or password is wrong")

    # Simulate token generation (real implementation would use JWT)
    token = "fake-jwt-token"

    # Return a fake user payload, identical to old backend structure
    return {
        "token": token,
        "user": {
            "name": user["name"],
            "email": user["email"],
            "avatarURL": user["avatarURL"],
            "theme": user.get("theme", DEF_THEME),
        },
    }
