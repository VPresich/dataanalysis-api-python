from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.auth import logout_service


@ctrl_wrapper
async def logout_controller(user: dict):
    """
    Logout controller stub.
    Calls the logout service to perform logout logic.
    """
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # вызываем сервис, передаем необходимые данные (например, user_id)
    await logout_service(user_id=user["_id"])

    return JSONResponse(status_code=204, content=None)
