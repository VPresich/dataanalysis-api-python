from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users import update_theme_service


@ctrl_wrapper
async def update_theme_controller(user: dict, data: dict):
    """
    Controller to update user's theme.
    """
    theme = data.get("theme")
    user_id = user.get("id")
    updated_theme = await update_theme_service(user_id, theme)
    if not updated_theme:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(status_code=200, content={"theme": updated_theme})
