from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users import update_profile_service


@ctrl_wrapper
async def update_profile_controller(user: dict, data: dict):
    """
    Controller to update user's information.
    """
    name = data.get("name")
    theme = data.get("theme")
    password = data.get("password")

    updated_user = await update_profile_service(user["id"], name, password, theme)

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
