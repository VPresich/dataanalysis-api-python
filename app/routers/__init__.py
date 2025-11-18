from fastapi import APIRouter
from .auth_router import auth_router
from .users_router import users_router
from .sources_router import sources_router


routers = APIRouter()
routers.include_router(auth_router, prefix="/auth", tags=["auth"])
routers.include_router(users_router, prefix="/users", tags=["users"])
routers.include_router(sources_router, prefix="/sources", tags=["sources"])
