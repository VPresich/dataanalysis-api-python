from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.config.urls import BACKEND_BASE_URL
from app.config.google import GOOGLE_CLIENT_ID


@ctrl_wrapper
async def google_auth_controller():
    """
    Google OAuth Controller for FastAPI.

    This controller redirects the user to Google's OAuth 2.0 authorization page.
    It constructs the URL with all required parameters including:
      - client_id: Google application's client ID
      - redirect_uri: backend endpoint to receive the authorization code
      - scope: permissions requested (email and profile)
      - response_type: 'code', so Google returns an authorization code
      - access_type: 'offline', to allow issuing refresh tokens
      - prompt: 'consent', to force showing consent screen every time

    After successful authorization, Google will redirect the user back
    to /auth/google-redirect with the authorization code.
    """
    # Construct the redirect URI for Google to call after authorization
    redirect_uri = f"{BACKEND_BASE_URL}/auth/google-redirect"

    # Prepare query parameters for Google OAuth URL
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    }

    # Build the full Google OAuth URL
    google_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

    # Redirect the user to Google's OAuth consent page
    return RedirectResponse(url=google_url)
