from fastapi import APIRouter, Depends, Body
from typing import List
from app.dependencies import authenticate, get_valid_parameter, upload_file
from app.schemas import DataSourceSchema
from app.dependencies import datasource_form

from app.controllers.data_sources import (
    get_all_sources_controller,
    get_noname_sources_controller,
    update_source_controller,
    upload_data_controller,
    delete_data_by_source_controller
)

from app.validation import (
    SourceUpdateValidation,
    DataSourceValidation,
)


sources_router = APIRouter()


@sources_router.get("/", response_model=List[DataSourceSchema])
async def get_sources(current_user: dict = Depends(authenticate)):
    return await get_all_sources_controller(current_user)


@sources_router.get("/noname/sources", response_model=List[DataSourceSchema])
async def get_noname_sources():
    return await get_noname_sources_controller()


@sources_router.post("/")
async def upload_data(
    data: DataSourceValidation = Depends(datasource_form),
    current_user: dict = Depends(authenticate),
    file_path: str = Depends(upload_file("datafile"))
):
    return await upload_data_controller(
        current_user,
        data.model_dump(),
        file_path
    )


@sources_router.patch("/{source_number}")
async def update_source(source_number: int = Depends(get_valid_parameter),
                        data: SourceUpdateValidation = Body(...),
                        current_user: dict = Depends(authenticate)
                        ):
    return await update_source_controller(
        current_user,
        source_number,
        data.model_dump()
    )


@sources_router.delete("/{source_number}")
async def delete_data_by_source(source_number: int = Depends(get_valid_parameter),
                                current_user: dict = Depends(authenticate)
                                ):
    return await delete_data_by_source_controller(current_user, source_number)
