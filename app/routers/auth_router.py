# auth_router.py
from fastapi import APIRouter, Depends, Request
from app.controllers.auth import register_controller, login_controller, logout_controller
from app.middleware import authenticate


auth_router = APIRouter()


@auth_router.post("/register")
async def register(request: Request):
    data = await request.json()
    return await register_controller(data)


@auth_router.post("/login")
async def login(request: Request):
    data = await request.json()
    return await login_controller(data)


@auth_router.post("/logout")
async def logout(current_user: dict = Depends(authenticate)):
    return await logout_controller(current_user)
