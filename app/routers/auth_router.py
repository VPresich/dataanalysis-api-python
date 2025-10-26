# auth_router.py
from fastapi import APIRouter, Depends
from app.controllers.auth import register_controller, login_controller, logout_controller
from app.middleware import authenticate
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
