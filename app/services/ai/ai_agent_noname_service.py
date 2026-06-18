import os
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models import DataSource, User
from app.schemas.ai_schema import AIChatRequest
from .execute_ai_analysis_workflow import run_ai_analysis


async def ai_agent_noname(payload: AIChatRequest, session: AsyncSession) -> dict:
    """
    Service: Bypasses authentication headers for public/anonymous dashboard sessions,
    resolving the static 'noname user' account profile to authorize data fetching.
    """
    result = await session.execute(select(User).where(User.name == "noname user"))
    noname_user = result.scalar_one_or_none()
    if not noname_user:
        raise HTTPException(404, "Not found user")

    result = await session.execute(
        select(DataSource).where(
            (DataSource.id_user == noname_user._id)
            & (DataSource._id == UUID(payload.id_source))
        )
    )
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(404, "Source not found for this user")

    # Delegate core data formatting and LLM querying to the helper function
    return await run_ai_analysis(source._id, payload.TrackNum, session)
