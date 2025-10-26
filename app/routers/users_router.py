# users_router.py
from fastapi import APIRouter, Depends
from app.controllers.users import get_current_controller
from app.middleware import authenticate


users_router = APIRouter()


@users_router.get("/current")
async def current(current_user: dict = Depends(authenticate)):
    return await get_current_controller(current_user)
