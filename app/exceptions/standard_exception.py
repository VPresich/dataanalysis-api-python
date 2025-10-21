from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


# Exception handler for HTTPExceptions
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle standard FastAPI HTTPExceptions and return a consistent JSON response.
    Catches all built-in HTTP errors like 400, 401, 404, 422, etc.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail,
            "data": None,
        },
    )
