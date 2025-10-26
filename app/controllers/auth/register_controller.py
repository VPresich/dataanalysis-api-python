from fastapi.responses import JSONResponse
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.auth import register_service


@ctrl_wrapper
async def register_controller(request_data: dict):
    """
    Controller for user registration (stub version).
    Returns a response compatible with the old Node.js backend:
    {
      "token": "...",
      "user": {
        "name": "...",
        "email": "...",
        "avatarURL": "...",
        "theme": "..."
      }
    }
    """
    result = await register_service(request_data)
    return JSONResponse(status_code=201, content=result)
