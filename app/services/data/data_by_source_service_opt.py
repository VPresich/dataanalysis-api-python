from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models import DataSource, Data
from typing import List


async def data_by_source_service_optimized(user_id: str, source_number: int, session: AsyncSession) -> List[dict]:
    """
    Optimized Service: Retrieves data for a specific user by source number using a SINGLE query.
    Bypasses heavy ORM object mapping for high performance.
    """

    query = (
        select(Data.__table__)
        .join(DataSource, Data.id_source == DataSource._id)
        .where(
            (DataSource.id_user == UUID(user_id))
            & (DataSource.source_number == source_number)
        )
        .order_by(Data.Time.asc())
    )

    try:
        result = await session.execute(query)
        records = result.mappings().all()

        if not records:
            source_exists = await session.execute(
                select(DataSource._id).where(
                    (DataSource.id_user == UUID(user_id)) & (DataSource.source_number == source_number)
                )
            )
            if not source_exists.scalar_one_or_none():
                raise HTTPException(404, "Source not found for this user")

        return [dict(row) for row in records]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error fetching tracking data: {e}")
