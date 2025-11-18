from uuid import UUID
from sqlalchemy import select
from app.database import get_db_session
from app.models import DataSource


async def get_all_sources_service(user_id: str):
    """
    Service to get all data sources for a specific user.
    :param user_id: ID of the user (string UUID)
    :return: List of DataSource records
    """
    async with get_db_session() as session:

        query = (
            select(DataSource)
            .where(DataSource.id_user == UUID(user_id))
            .order_by(DataSource.created_at.desc())
        )

        result = await session.execute(query)
        records = result.scalars().all()

        return records
