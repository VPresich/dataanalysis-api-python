from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users.update_theme_service import update_theme_service


@ctrl_wrapper
async def update_theme_controller(user: dict, data):
    """
    Controller to update user's theme.
    """

    updated_theme = await update_theme_service(user, data.color)
    if not updated_theme:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(status_code=200, content=updated_theme)
