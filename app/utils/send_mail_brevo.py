import httpx
from app.config.mail import SMTP_APIKEY, SMTP_FROM


async def send_mail(to: str, subject: str, html: str):
    """
    Send an email via Brevo (SMTP API).
    """
    url = "https://api.brevo.com/v3/smtp/email"
    payload = {
        "sender": {
            "name": "DataAnalysis",
            "email": SMTP_FROM
        },
        "to": [{"email": to}],
        "subject": subject,
        "htmlContent": html
    }
    headers = {
        "api-key": SMTP_APIKEY,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()  # raise HTTPError if status >= 400
            return response.json()
    except httpx.HTTPStatusError as err:
        # API returned error status code
        print(f"HTTP error: {err.response.status_code} - {err.response.text}")
        raise
    except httpx.RequestError as err:
        # Network error or timeout
        print(f"Request error: {err}")
        raise
