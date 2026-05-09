from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.services.data import data_by_source_service
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def data_by_source_controller(user: dict, source_number, db: AsyncSession):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    records = await data_by_source_service(user["id"], source_number, session=db)
    result = jsonable_encoder(records)

    return JSONResponse(status_code=200, content=result)
