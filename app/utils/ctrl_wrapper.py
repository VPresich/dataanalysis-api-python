from functools import wraps


def ctrl_wrapper(func):
    """
    Wraps controller functions to catch unexpected errors
    and pass them to FastAPI's global exception handlers.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Errors are propagated upwards (they will be caught by the global error handler)
            raise e
    return wrapper
