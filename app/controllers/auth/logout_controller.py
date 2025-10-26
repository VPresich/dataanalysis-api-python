from fastapi import Response
from fastapi import HTTPException
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.auth import logout_service


@ctrl_wrapper
async def logout_controller(user: dict):
    """
    Logout controller.

    Steps:
      1. Check if user exists in the request (from authentication dependency).
      2. Call the logout service to clear the user's token in the database.
      3. Return HTTP 204 No Content on success.
    """

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await logout_service(user_id=user["id"])
    return Response(status_code=204)
