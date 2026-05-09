from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session
from typing import List, Optional
from app.dependencies import authenticate, valid_parameter, time_params
from app.schemas import DataSchema
from app.controllers.data import (
    data_by_source_controller,
    filtered_data_by_source_controller,
    noname_data_by_source_controller
)

data_router = APIRouter()


@data_router.get("/{source_number}/filter", response_model=List[DataSchema])
async def get_filtered_data(source_number: int = Depends(valid_parameter),
                            times: tuple[Optional[float], Optional[float]] = Depends(time_params),
                            current_user: dict = Depends(authenticate), db: AsyncSession = Depends(get_db_session)):
    return await filtered_data_by_source_controller(current_user, source_number, times, db=db)


@data_router.get("/{source_number}", response_model=List[DataSchema])
async def get_data(source_number: int = Depends(valid_parameter),
                   current_user: dict = Depends(authenticate), db: AsyncSession = Depends(get_db_session)):
    return await data_by_source_controller(current_user, source_number, db=db)


@data_router.get("/noname/data/{source_number}", response_model=List[DataSchema])
async def get_noneme_data(source_number: int = Depends(valid_parameter), db: AsyncSession = Depends(get_db_session)):
    return await noname_data_by_source_controller(source_number, db=db)
