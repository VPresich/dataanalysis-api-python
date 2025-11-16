from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users import update_avatar_service


@ctrl_wrapper
async def update_avatar_controller(user: dict, source_path: str, required: bool = True):
    """
        Controller to update user's avatar.
    """
    if required and not source_path:
        raise HTTPException(status_code=400, detail="File is required")

    if not source_path:
        return JSONResponse(status_code=200, content={"avatarURL": user.get("avatarURL")})

    upload_avatar_url = await update_avatar_service(user["id"], source_path)

    return JSONResponse(status_code=200, content={"avatarURL": upload_avatar_url})
