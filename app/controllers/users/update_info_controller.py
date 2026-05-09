from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.users import update_info_service


@ctrl_wrapper
async def update_info_controller(user: dict, data: dict, db: AsyncSession):
    """
    Controller to update user's information.
    """
    name = data.get("name")
    theme = data.get("theme")
    password = data.get("password")

    updated_user = await update_info_service(user["id"], name, password, theme, db)

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
