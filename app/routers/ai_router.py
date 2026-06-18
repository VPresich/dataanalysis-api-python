from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session
from app.dependencies import authenticate
from app.schemas import AIChatRequest
from app.controllers.ai import (
    ai_agent_user_ctrl,
    ai_agent_noname_ctrl,
)

ai_router = APIRouter()


@ai_router.post("/user-evaluate")
async def evaluate_user_track_consistency(
    payload: AIChatRequest,
    current_user: dict = Depends(authenticate),
    db: AsyncSession = Depends(get_db_session)
):
    return await ai_agent_user_ctrl(current_user, payload, db=db)


@ai_router.post("/noname-evaluate")
async def evaluate_noname_track_consistency(
    payload: AIChatRequest,
    db: AsyncSession = Depends(get_db_session)
):
    return await ai_agent_noname_ctrl(payload, db=db)
