from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.services.ai import ai_agent_user
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def ai_agent_user_ctrl(user: dict, payload, db: AsyncSession):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    analysis_result = await ai_agent_user(user["id"], payload, session=db)
    result = jsonable_encoder(analysis_result)

    return JSONResponse(status_code=200, content=result)
