import functools
import logging
from fastapi import HTTPException

# Use the same logger as Uvicorn / FastAPI
logger = logging.getLogger("uvicorn")


def ctrl_wrapper(func):
    """
    Decorator for FastAPI route handlers (controllers) that:
      - Executes the async function
      - Catches any unexpected exceptions
      - Logs the error with traceback
      - Converts unexpected exceptions into HTTP 500 responses
      - Allows HTTPException to pass through unchanged
    """

    @functools.wraps(func)  # Preserve metadata (name, docstring) of the original function
    async def wrapper(*args, **kwargs):
        try:
            # Call the original async route handler
            return await func(*args, **kwargs)

        except HTTPException:
            # Already known HTTP errors (like 401, 404) are passed through
            raise

        except Exception as e:
            # Catch any unexpected exception
            logger.exception(f"Unhandled error in {func.__name__}: {e}")
            # Convert it to a generic 500 Internal Server Error response
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return wrapper
