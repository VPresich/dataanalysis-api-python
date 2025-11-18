from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.data_sources import get_noname_sources_service
from app.schemas import DataSourceSchema
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def get_noname_sources_controller():
    records = await get_noname_sources_service()
    result = jsonable_encoder([DataSourceSchema.model_validate(r) for r in records])
    return JSONResponse(status_code=200, content=result)
