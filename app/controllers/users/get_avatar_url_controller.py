from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users import get_avatar_url_service


@ctrl_wrapper
async def get_avatar_url_controller(user: dict):
    """
    Controller to get current authenticated user info.
    Returns JSON containing user data: name, email, avatarURL, theme.
    """
    result = await get_avatar_url_service(user["id"])
    return JSONResponse(status_code=200, content={"avatarURL": result})
