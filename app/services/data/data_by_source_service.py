from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID
from app.database import get_db_session
from app.models import DataSource
from app.models import Data
from app.schemas import DataSchema
from typing import List


async def data_by_source_service(user_id: str, source_number: int) -> List[dict]:
    """
    Service: Retrieves data for a specific user by source number.

    :param user_id: ID of the authenticated user
    :param source_number: The source number
    :return: List of data records (dict)
    """
    async with get_db_session() as session:

        result = await session.execute(
            select(DataSource).where(
                (DataSource.id_user == UUID(user_id))
                & (DataSource.source_number == source_number)
            )
        )
        source = result.scalar_one_or_none()

        if not source:
            raise HTTPException(404, "Source not found for this user")

        data_result = await session.execute(
            select(Data).where(Data.id_source == source._id)
        )
        records = data_result.scalars().all()
        result = [DataSchema.model_validate(r).model_dump(by_alias=True) for r in records]

        return result
