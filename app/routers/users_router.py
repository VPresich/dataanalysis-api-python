# users_router.py
from fastapi import APIRouter, Depends
from app.controllers.users import (
    get_current_controller,
    update_theme_controller,
    get_theme_controller
)

from app.dependencies import authenticate
from app.validation import ThemeValidation


users_router = APIRouter()


@users_router.get("/current")
async def current(current_user: dict = Depends(authenticate)):
    return await get_current_controller(current_user)


@users_router.patch("/themes")
async def update_themes(data: ThemeValidation, current_user: dict = Depends(authenticate)):
    return await update_theme_controller(current_user, data)


@users_router.get("/themes")
async def get_themes(current_user: dict = Depends(authenticate)):
    return await get_theme_controller(current_user)
