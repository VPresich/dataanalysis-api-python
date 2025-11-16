from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users import update_profile_service


@ctrl_wrapper
async def update_profile_controller(user: dict, data: dict, file_path: str):
    """
    Controller to update user's information.
    """
    user_id = user.get("id")
    name = data.get("name")
    theme = data.get("theme")
    password = data.get("password")

    if not any([name, password, theme, file_path]):
        return JSONResponse(status_code=200, content=user)

    updated_user = await update_profile_service(user_id, name, password, theme, file_path)

    return JSONResponse(
        status_code=200,
        content={
            "_id": str(updated_user._id),
            "name": updated_user.name,
            "email": updated_user.email,
            "theme": updated_user.theme.name,
            "avatarURL": updated_user.avatar_url,
        }
    )
