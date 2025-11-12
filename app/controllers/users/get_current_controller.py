from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper


@ctrl_wrapper
async def get_current_controller(current_user: dict):
    """
    Controller to get current authenticated user info.
    Returns JSON containing user data: name, email, avatarURL, theme.
    """

    return JSONResponse(status_code=200, content=current_user)
