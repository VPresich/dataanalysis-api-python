from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.auth import register_service


@ctrl_wrapper
async def register_controller(request_data: dict):
    """
    User registration controller.
    Returns JSON containing the authentication token and user data.
    Steps:
      1. Call the registration service to create a new user.
      2. Receive token and user info from the service.
      3. Return a JSONResponse with status code 201.
    """

    result = await register_service(request_data)
    return JSONResponse(status_code=201, content=result)
