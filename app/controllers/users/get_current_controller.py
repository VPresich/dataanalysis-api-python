from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users import get_current_service


@ctrl_wrapper
async def get_current_controller(current_user: dict):
    """
    Controller to get current authenticated user info.
    Returns JSON containing user data: name, email, avatarURL, theme.
    """
    user_data = await get_current_service(current_user)
    return JSONResponse(status_code=200, content=user_data)
