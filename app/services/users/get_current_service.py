async def get_current_service(user: dict):
    """
    Service for returning the current user's public info.
    :param user: dict returned из authenticate dependency
    :return: dict с публичными полями
    """
    if not user:
        raise ValueError("User data not found")

    return {
        "name": user.get("name"),
        "email": user.get("email"),
        "avatarURL": user.get("avatarUrl"),
        "theme": user.get("theme"),
    }
