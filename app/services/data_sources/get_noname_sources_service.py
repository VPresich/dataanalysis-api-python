from sqlalchemy import select
from app.database import get_db_session
from app.models import User
from app.models import DataSource


async def get_noname_sources_service():
    """
    Service: Retrieves demo sources for the "noname user".
    This service provides example data for users who are not registered or not logged in.
    It fetches the default ("noname") user's sources from the database.

    1. Finds the "noname user" in the users table.
    2. Retrieves all sources associated with this user, sorted by creation date (newest first).
    3. Returns the list of sources.

    If the "noname user" does not exist, or the user has no sources,
    the function returns an empty list instead of throwing an error.

    :return: List of DataSource ORM objects (may be empty)
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

        return noname_sources
