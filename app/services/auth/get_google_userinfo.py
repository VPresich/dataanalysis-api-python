import httpx
from fastapi import HTTPException


async def get_google_userinfo(access_token: str):
    """Get user info from Google using access token."""

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to fetch user info from Google")
        return response.json()
