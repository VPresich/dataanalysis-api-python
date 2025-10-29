import httpx
import os
from fastapi import HTTPException


async def get_google_tokens(code: str, redirect_uri: str):
    """
    Exchange Google OAuth 2.0 authorization code for access and ID tokens.

    This function sends a POST request to Google's token endpoint to exchange
    the temporary authorization code (received after user consent) for an access
    token and an ID token. The access token can be used to fetch user info,
    while the ID token contains identity claims about the user.
    Args:
        code (str): The authorization code returned by Google after user consent.
        redirect_uri (str): The redirect URI used in the OAuth flow.
    Returns:
        dict: A dictionary containing 'access_token', 'id_token', 'expires_in', etc.
    """
    # Create an asynchronous HTTP client
    async with httpx.AsyncClient() as client:
        # Send POST request to Google's OAuth token endpoint
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
            raise HTTPException(
                status_code=401,
                detail="Failed to fetch tokens from Google"
            )

        # Return the JSON response containing tokens
        return response.json()
