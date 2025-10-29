import httpx
from fastapi import HTTPException


async def get_google_user_info(access_token: str):
    """
    Fetch user information from Google using an OAuth 2.0 access token.

    This function sends a GET request to the Google UserInfo endpoint with the
    provided access token. It retrieves basic user profile data such as email,
    name, and profile picture.
    """
    # Create an asynchronous HTTP client
    async with httpx.AsyncClient() as client:
        # Send GET request to Google UserInfo endpoint with Authorization header
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=401,
                detail="Failed to fetch user info from Google"
            )

        # Return the JSON response containing user info
        return response.json()
