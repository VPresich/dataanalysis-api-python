async def get_current_service(user: dict):
    """
    Service to return current user info.
    """
    return {
        "name": user["name"],
        "email": user["email"],
        "avatarURL": user["avatarURL"],
        "theme": user.get("theme")
    }
