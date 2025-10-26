# from fastapi import HTTPException


async def authenticate():
    """
    Stub authentication middleware.
    Returns a fake user dict for testing.
    """
    fake_user = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Test User",
        "email": "user@example.com",
        "avatarURL": "https://example.com/avatar.jpg",
        "theme": "yellow",
    }
    return fake_user
