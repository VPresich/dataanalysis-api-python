from sqlalchemy import update
from app.database import get_db_session
from app.models import User
from uuid import UUID


async def logout_service(user_id: str):
    """
    Real logout service.
    Clears the token for the given user in the database.
    Steps:
      1. Find the user by ID.
      2. Set the token field to None.
      3. Commit the transaction.
    """
    async with get_db_session() as session:
        await session.execute(
            update(User)
            .where(User._id == UUID(user_id))
            .values(token=None)
        )
        await session.commit()
        return True
