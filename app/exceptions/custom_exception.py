from fastapi import Request
from fastapi.responses import JSONResponse


# Example custom exception
# This class can be raised anywhere in your application when a specific error occurs.
class CustomException(Exception):
    """
    Initialize the custom exception with a descriptive name.
    :param name: a short description of the error
    """

    def __init__(self, name: str, status_code: int = 400):
        self.name = name
        self.status_code = status_code


# Exception handler for FastAPI
# This function will be registered in FastAPI to handle CustomException globally.
# It returns a JSON response with status code 400 and a descriptive error message.
async def custom_exception_handler(request: Request, exc: CustomException):
    """
    Handle CustomException and return a structured JSON response.
    :param request: FastAPI request object
    :param exc: instance of CustomException
    :return: JSONResponse with error details
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": f"Custom error occurred: {exc.name}",
            "data": None,
        },
    )
