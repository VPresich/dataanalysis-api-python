import json
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.services.data import noname_data_by_source_service_optimized
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def noname_data_by_source_controller(source_number, db: AsyncSession):

    records = await noname_data_by_source_service_optimized(source_number, session=db)
    # result = jsonable_encoder(records)
    fast_json_string = json.dumps(records, default=str)
    result = json.loads(fast_json_string)

    return JSONResponse(status_code=200, content=result)
