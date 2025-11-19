from fastapi.responses import JSONResponse
from fastapi import HTTPException
from typing import Optional
from fastapi.encoders import jsonable_encoder
from app.services.data import filtered_data_by_source_service
from app.utils import ctrl_wrapper


@ctrl_wrapper
async def filtered_data_by_source_controller(user: dict, source_number,
                                             times: tuple[Optional[float], Optional[float]]):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    start_time, end_time = times

    records = await filtered_data_by_source_service(
        user_id=user["id"],
        source_number=source_number,
        start_time=start_time,
        end_time=end_time
    )

    result = jsonable_encoder(records)

    return JSONResponse(status_code=200, content=result)
