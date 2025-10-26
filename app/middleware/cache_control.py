from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class CacheControl(BaseHTTPMiddleware):
    """
    Middleware that disables client-side caching.

    This middleware adds HTTP headers to every response to ensure
    that browsers and proxies do not cache the response.
    Useful for APIs where data is dynamic and must always be fetched fresh.
    """

    async def dispatch(self, request: Request, call_next):
        # Process the incoming request and get the response
        response = await call_next(request)

        # Add HTTP headers to prevent caching
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        # Return the modified response
        return response
