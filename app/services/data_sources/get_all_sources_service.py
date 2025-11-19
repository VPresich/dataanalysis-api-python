from uuid import UUID
from sqlalchemy import select
from app.database import get_db_session
from app.models import DataSource
from app.schemas import DataSourceSchema


async def get_all_sources_service(user_id: str):
    """
    Retrieves all data sources that belong to a specific user.
    1. Converts the provided user_id (string) to a UUID.
    2. Selects all DataSource records where `id_user` matches this UUID.
    3. Sorts the records by creation date in descending order (newest first).
    4. Converts ORM objects into Pydantic schemas for safe API output.
    :param user_id: User ID as a string UUID.
    :return: List of DataSourceSchema objects.
    """
    async with get_db_session() as session:

        query = (
            select(DataSource)
            .where(DataSource.id_user == UUID(user_id))
            .order_by(DataSource.created_at.desc())
        )

        result = await session.execute(query)
        records = result.scalars().all()
        result = [DataSourceSchema.model_validate(r) for r in records]

        return result
