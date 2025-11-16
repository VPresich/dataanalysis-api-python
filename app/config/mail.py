import os

SMTP_FROM = os.getenv("SMTP_FROM")
SMTP_APIKEY = os.getenv("SMTP_APIKEY")

__all__ = ("SMTP_FROM", "SMTP_APIKEY")
