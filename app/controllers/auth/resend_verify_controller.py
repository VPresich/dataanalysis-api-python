from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.auth import resend_verify_service


@ctrl_wrapper
async def resend_verify_controller(data: dict):
    """
    Public endpoint to resend a verification email.
    This route does not require authentication.
    """
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    await resend_verify_service(email)

    return JSONResponse(
        status_code=200,
        content={
            "message": "A verification email has been sent. Please check your inbox to verify your account."
        }
    )
