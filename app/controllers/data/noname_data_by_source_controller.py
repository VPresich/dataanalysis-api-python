from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.data import noname_data_by_source_service
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def noname_data_by_source_controller(source_number):

    records = await noname_data_by_source_service(source_number)
    result = jsonable_encoder(records)

    return JSONResponse(status_code=200, content=result)
