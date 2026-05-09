from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import ctrl_wrapper
from app.services.auth import verify_email_service
from app.config.urls import FRONTEND_BASE_URL


@ctrl_wrapper
async def verify_email_controller(verification_token: str, db: AsyncSession):
    """
    Controller to verify a user's email.
    - Calls verify_email_service to validate the token and update the user.
    - Redirects to success or error page depending on result.
    """
    try:
        await verify_email_service(verification_token, db)
        return RedirectResponse(
            url=f"{FRONTEND_BASE_URL}/verified-success", status_code=307)
    except Exception as exc:
        print(f"Verification failed: {exc}")  # Optional: log the exception
        return RedirectResponse(
            url=f"{FRONTEND_BASE_URL}/verified-error", status_code=307)
