from fastapi import HTTPException
from sqlalchemy import select, and_
from uuid import UUID
from app.database import get_db_session
from app.models import DataSource, Data
from app.schemas import DataSchema
from typing import Optional, List, Union


async def filtered_data_by_source_service(
    *,
    user_id: str,
    source_number: Union[int, str],
    start_time: Optional[float] = None,
    end_time: Optional[float] = None
) -> List[dict]:
    """
    Fetch user data filtered by source number and optional time range.

    :param user_id: UUID of the current user
    :param source_number: Source number to filter
    :param start_time: Optional start time filter
    :param end_time: Optional end time filter
    :return: List of data records (as dicts)
    """
    async with get_db_session() as session:
        # Get the source
        result = await session.execute(
            select(DataSource).where(
                and_(
                    DataSource.id_user == UUID(user_id),
                    DataSource.source_number == int(source_number)
                )
            )
        )
        source = result.scalar_one_or_none()
        if not source:
            raise HTTPException(404, detail="Source not found for this user")

        # Build query for Data
        query = select(Data).where(Data.id_source == source._id)

        if start_time is not None:
            query = query.where(Data.Time >= start_time)
        if end_time is not None:
            query = query.where(Data.Time <= end_time)

        data_result = await session.execute(query)
        records = data_result.scalars().all()

        result = [DataSchema.model_validate(r).model_dump(by_alias=True) for r in records]

        return result
