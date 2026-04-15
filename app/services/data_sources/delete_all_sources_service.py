from app.models.data_source import DataSource
from app.database import get_db_session
from uuid import UUID
from sqlalchemy import select, delete
from fastapi import HTTPException


async def delete_all_sources_service(*, user_id: str) -> dict:
    """
    Deletes all data sources and all related Data for a given user.
    """
    user_uuid = UUID(user_id)

    async with get_db_session() as session:
        try:
            # Fetch all source IDs for this user
            result = await session.execute(
                select(DataSource._id).where(DataSource.id_user == user_uuid)
            )
            source_ids = result.scalars().all()

            # If no sources exist, return 0 counts
            if not source_ids:
                return {
                    "deletedSources": 0,
                    "deletedData": 0,
                }

            # Delete all sources
            # Related Data objects will be deleted automatically via cascade
            source_result = await session.execute(
                delete(DataSource).where(DataSource._id.in_(source_ids))
            )

            # Commit the transaction
            await session.commit()

            return {
                "message": "Sources and related data successfully deleted",
                "deletedSources": source_result.rowcount,
                "deletedData": "all related Data deleted via cascade",
            }

        except Exception as exc:
            # Rollback the transaction if anything goes wrong
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete sources and related data: {exc}",
            )
