from fastapi.responses import JSONResponse
from app.utils import ctrl_wrapper
from app.services.auth import reset_pwd_service


@ctrl_wrapper
async def reset_pwd_controller(request_data: dict):
    """
    Controller to reset user's password.
    """
    token = request_data.get("token")
    password = request_data.get("password")

    await reset_pwd_service(password, token)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Password changed successfully!",
            "data": {}
        }
    )
