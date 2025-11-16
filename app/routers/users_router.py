# users_router.py
from fastapi import APIRouter, Depends
from app.controllers.users import (
    get_current_controller,
    update_theme_controller,
    get_theme_controller,
    get_avatar_url_controller,
    update_info_controller,
    update_profile_controller,
    update_avatar_controller
)
from app.dependencies import authenticate, upload_file
from app.validation import ThemeValidation, ProfileValidation


users_router = APIRouter()


@users_router.get("/current")
async def current(current_user: dict = Depends(authenticate)):
    return await get_current_controller(current_user)


@users_router.patch("/")
async def update_info(data: ProfileValidation, current_user: dict = Depends(authenticate)):
    return await update_info_controller(current_user, data.model_dump())


@users_router.patch("/profile")
async def update_profile(data: ProfileValidation, current_user: dict = Depends(authenticate)):
    return await update_profile_controller(current_user, data.model_dump())


@users_router.get("/themes")
async def get_themes(current_user: dict = Depends(authenticate)):
    return await get_theme_controller(current_user)


@users_router.patch("/themes")
async def update_themes(data: ThemeValidation, current_user: dict = Depends(authenticate)):
    return await update_theme_controller(current_user, data.model_dump())


@users_router.get("/avatars")
async def get_avatar_url(current_user: dict = Depends(authenticate)):
    return await get_avatar_url_controller(current_user)


@users_router.patch("/avatars")
async def update_avatar(current_user: dict = Depends(authenticate), file_path: str = Depends(upload_file("avatar"))):
    return await update_avatar_controller(current_user, file_path)

# file_path: Optional[str] = Depends(upload_file("profile_picture", required=False))
