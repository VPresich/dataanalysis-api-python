# auth_router.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session
from fastapi import APIRouter, Depends, Request
from app.controllers.auth import (
    register_controller,
    login_controller,
    logout_controller,
    google_auth_controller,
    google_redirect_controller,
    verify_email_controller,
    resend_verify_controller,
    request_reset_pwd_controller,
    reset_pwd_controller
)

from app.dependencies import authenticate
from app.validation import (
    RegisterValidation,
    LoginValidation,
    EmailValidation,
    ResetPasswordValidation)

auth_router = APIRouter()


@auth_router.post("/register")
async def register(data: RegisterValidation, db: AsyncSession = Depends(get_db_session)):
    return await register_controller(data.model_dump(), db=db)


@auth_router.post("/login")
async def login(data: LoginValidation, db: AsyncSession = Depends(get_db_session)):
    return await login_controller(data.model_dump(), db=db)


@auth_router.post("/logout")
async def logout(current_user: dict = Depends(authenticate), db: AsyncSession = Depends(get_db_session)):
    return await logout_controller(current_user, db=db)


@auth_router.get("/google")
async def google_auth():
    return await google_auth_controller()


@auth_router.get("/google-redirect")
async def google_redirect(request: Request, db: AsyncSession = Depends(get_db_session)):
    return await google_redirect_controller(request, db=db)


@auth_router.post("/request-reset-pwd")
async def request_reset_pwd(data: EmailValidation, db: AsyncSession = Depends(get_db_session)):
    return await request_reset_pwd_controller(data.model_dump(), db=db)


@auth_router.post("/reset-pwd")
async def reset_pwd(data: ResetPasswordValidation, db: AsyncSession = Depends(get_db_session)):
    return await reset_pwd_controller(data.model_dump(), db=db)


@auth_router.post("/resend-verify")
async def resend_verify(data: EmailValidation, db: AsyncSession = Depends(get_db_session)):
    return await resend_verify_controller(data.model_dump(), db=db)


@auth_router.get("/verify/{verification_token}")
async def verify(verification_token: str, db: AsyncSession = Depends(get_db_session)):
    return await verify_email_controller(verification_token, db=db)
