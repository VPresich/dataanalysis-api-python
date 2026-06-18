import os
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .execute_ai_analysis_workflow import run_ai_analysis
from uuid import UUID
from app.models import DataSource
from app.schemas.ai_schema import AIChatRequest


async def ai_agent_user(user_id: str, payload: AIChatRequest, session: AsyncSession) -> dict:
    """
    Service: Verifies authenticated user access ownership to the source data 
    and triggers the core AI trajectory processing workflow.
    """
    result = await session.execute(
        select(DataSource).where(
            (DataSource.id_user == UUID(user_id))
            & (DataSource._id == UUID(payload.id_source))
        )
    )
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(404, "Source not found for this user")

    # Delegate core data formatting and LLM querying to the helper function
    return await run_ai_analysis(source._id, payload.TrackNum, session)
