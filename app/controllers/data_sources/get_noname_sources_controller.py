from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.services.data_sources import get_noname_sources_service
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def get_noname_sources_controller(db: AsyncSession):
    records = await get_noname_sources_service(db)
    result = jsonable_encoder(records)

    return JSONResponse(status_code=200, content=result)
