import os
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from app.services.auth import get_google_tokens, get_google_userinfo, google_login_service
from app.utils.ctrl_wrapper import ctrl_wrapper


@ctrl_wrapper
async def google_redirect_controller(request: Request):
    """
    Handles redirect from Google OAuth, retrieves tokens and user profile,
    passes them to the service, and redirects to frontend.
    If an error occurs, redirects to frontend with error query parameter.
    """
    frontend_base_url = os.getenv("FRONTEND_BASE_URL", "")

    try:
        code = request.query_params.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Missing authorization code")

        backend_base_url = os.getenv("BACKEND_BASE_URL")
        if not backend_base_url:
            raise RuntimeError("Environment variable BACKEND_BASE_URL is not set")

        redirect_uri = f"{backend_base_url}/auth/google-redirect"

        # Getting tokens
        tokens = await get_google_tokens(code, redirect_uri)
        access_token = tokens.get("access_token")
        if not access_token:
            raise HTTPException(status_code=401, detail="No access token received from Google")

        # Getting user profile
        userinfo = await get_google_userinfo(access_token)

        # Pass data to service
        data_to_service = {"userinfo": userinfo, "tokens": tokens}
        jwt_token = await google_login_service(data_to_service)

        # Successful redirect with JWT
        return RedirectResponse(f"{frontend_base_url}?token={jwt_token}")

    except Exception:
        # Redirect to frontend with generic error
        return RedirectResponse(f"{frontend_base_url}?error=google_login_failed")
