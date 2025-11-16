from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users import get_theme_service


@ctrl_wrapper
async def get_theme_controller(user: dict):
    """
    Controller to get user's theme.
    """
    theme = await get_theme_service(user["id"])
    if not theme:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(status_code=200, content={"theme": theme})
