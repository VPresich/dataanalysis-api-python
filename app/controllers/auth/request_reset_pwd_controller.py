from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.auth import request_reset_pwd_service


@ctrl_wrapper
async def request_reset_pwd_controller(data: dict):
    """
    Public endpoint to request reset password.
    This route does not require authentication.
    """
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    await request_reset_pwd_service(email)

    return JSONResponse(
        status_code=200,
        content={
            "message": "If an account with this email exists, a password reset link has been sent. Please check your inbox and follow the instructions to reset your password."
        }
    )
