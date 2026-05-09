from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.services.data_sources import get_all_sources_service
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def get_all_sources_controller(user: dict, db: AsyncSession):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    records = await get_all_sources_service(user["id"], session=db)
    result = jsonable_encoder(records)

    return JSONResponse(status_code=200, content=result)
