from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.services.data_sources import get_all_sources_service
from app.schemas import DataSourceSchema
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def get_all_sources_controller(user: dict):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    records = await get_all_sources_service(user["id"])
    result = jsonable_encoder([DataSourceSchema.model_validate(r) for r in records])
    return JSONResponse(status_code=200, content=result)
