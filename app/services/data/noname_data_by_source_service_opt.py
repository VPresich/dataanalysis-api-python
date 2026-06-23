from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import DataSource, User, Data
from typing import List


async def noname_data_by_source_service_optimized(source_number: int, session: AsyncSession) -> List[dict]:
    """
    Optimized Service: Retrieves data for noname user by source number using a SINGLE query.
    Bypasses heavy ORM object mapping and leverages composite database indices.

    :param source_number: The source number
    :return: List of data records (dict), empty list if not found
    """

    query = (
        select(Data.__table__)
        .join(DataSource, Data.id_source == DataSource._id)
        .join(User, DataSource.id_user == User._id)
        .where(
            (User.name == "noname user")
            & (DataSource.source_number == source_number)
        )
        .order_by(Data.Time.asc())
    )

    try:
        result = await session.execute(query)
        records = result.mappings().all()

        return [dict(row) for row in records]

    except Exception as e:
        print(f"Error fetching demo data for noname user: {e}")
        return []
