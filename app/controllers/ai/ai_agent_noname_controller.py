from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.services.ai import ai_agent_noname
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def ai_agent_noname_ctrl(payload, db: AsyncSession):

    analysis_result = await ai_agent_noname(payload, session=db)
    result = jsonable_encoder(analysis_result)

    return JSONResponse(status_code=200, content=result)
