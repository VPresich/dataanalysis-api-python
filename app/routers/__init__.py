from fastapi import APIRouter
from .auth_router import auth_router

routers = APIRouter()
routers.include_router(auth_router, prefix="/auth", tags=["auth"])
