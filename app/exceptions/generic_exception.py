from fastapi import Request
from fastapi.responses import JSONResponse


# Exception handler for unexpected exceptions
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unexpected exceptions.
    Returns a safe 500 Internal Server Error response to the client
    without exposing sensitive server details.
    """
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "message": "Internal server error",  # Safe message for the client
            "data": None,
        },
    )
