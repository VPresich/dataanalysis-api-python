import os
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from app.utils.ctrl_wrapper import ctrl_wrapper


@ctrl_wrapper
async def google_auth_controller():
    """
    Controller for redirecting the user to the Google OAuth authorization page.
    """
    redirect_uri = f"{os.getenv('BACKEND_BASE_URL')}/auth/google-redirect"

    params = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": redirect_uri,
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    }

    google_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url=google_url)
