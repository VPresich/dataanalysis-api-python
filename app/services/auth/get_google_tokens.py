import httpx
import os
from fastapi import HTTPException


async def get_google_tokens(code: str, redirect_uri: str):
    """Exchange authorization code for access token and ID token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to fetch tokens from Google")
        return response.json()
