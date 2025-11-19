from sqlalchemy import select
from app.database import get_db_session
from app.models import User
from app.models import DataSource
from app.schemas import DataSourceSchema


async def get_noname_sources_service():
    """
    Retrieves sources that belong to the demo user ("noname user").
    Workflow:
    1. Looks up the user with name "noname user" in the users table.
    2. If such a user exists, retrieves all DataSource entries linked to this user,
       ordered by creation date (newest first).
    3. Converts ORM objects to Pydantic schemas and returns them.
    Notes:
    - If the "noname user" does not exist, an empty list is returned.
    - If the user exists but has no sources, an empty list is returned.
    :return: List[DataSourceSchema] — possibly empty.
    """
    async with get_db_session() as session:
        result = await session.execute(select(User).where(User.name == "noname user"))
        noname_user = result.scalar_one_or_none()

        if not noname_user:
            return []

        result = await session.execute(
            select(DataSource)
            .where(DataSource.id_user == noname_user._id)
            .order_by(DataSource.created_at.desc())
        )
        noname_sources = result.scalars().all()
        result = [DataSourceSchema.model_validate(r) for r in noname_sources]

        return result
