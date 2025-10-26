from fastapi.responses import JSONResponse
from app.services.auth import login_service
from app.utils.ctrl_wrapper import ctrl_wrapper


@ctrl_wrapper
async def login_controller(request_data: dict):
    """
    User login controller.
    Returns JSON containing the authentication token and user data.

    Steps:
      1. Call the login service with request data.
      2. Receive token and user info from the service.
      3. Return a JSONResponse with status code 200.
    """
    result = await login_service(request_data)
    return JSONResponse(status_code=200, content=result)
