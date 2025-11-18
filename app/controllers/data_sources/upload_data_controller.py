from fastapi import HTTPException
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.data_sources import upload_data_service
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@ctrl_wrapper
async def upload_data_controller(user: dict, data: dict, file_path: str):
    """
    Upload CSV file and create a new data source.
    """
    if not user.get("id"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not file_path:
        raise HTTPException(status_code=400, detail="File is required")

    result = await upload_data_service(
        id=user["id"],
        source_number=data.get("source_number"),
        source_name=data.get("source_name"),
        file_name=data.get("file_name"),
        comment=data.get("comment"),
        file_path=file_path
    )

    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(result)
    )
