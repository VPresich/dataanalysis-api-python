from fastapi.responses import JSONResponse
from app.services.auth import login_service
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def login_controller(request_data: dict):
    """
    Controller for user login.
    Calls the service and returns an old-backend-compatible response.
    """
    email = request_data.get("email", "").lower()
    password = request_data.get("password")

    result = await login_service(email, password)

    return JSONResponse(status_code=200, content=result)
