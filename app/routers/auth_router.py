# auth_router.py
from fastapi import APIRouter, Depends, Request
from app.controllers.auth import (
    register_controller,
    login_controller,
    logout_controller,
    google_auth_controller,
    google_redirect_controller
)

from app.dependencies import authenticate
from app.validation import RegisterValidation, LoginValidation

auth_router = APIRouter()


@auth_router.post("/register")
async def register(data: RegisterValidation):
    return await register_controller(data.model_dump())


@auth_router.post("/login")
async def login(data: LoginValidation):
    return await login_controller(data.model_dump())


@auth_router.post("/logout")
async def logout(current_user: dict = Depends(authenticate)):
    return await logout_controller(current_user)


@auth_router.get("/google")
async def google_auth():
    return await google_auth_controller()


@auth_router.get("/google-redirect")
async def google_redirect(request: Request):
    return await google_redirect_controller(request)
