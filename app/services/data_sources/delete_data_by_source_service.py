from fastapi import HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models.data_source import DataSource
from app.schemas import DataSourceSchema
from uuid import UUID


async def delete_data_by_source_service(*, user_id: str, source_number: int) -> dict:
    """
    Deletes a DataSource and all related Data using ORM cascade.
    Returns the deleted DataSource object.
    """
    async with get_db_session() as session:

        # Find the source
        result = await session.execute(
            select(DataSource).where(
                (DataSource.id_user == UUID(user_id))
                & (DataSource.source_number == source_number)
            )
        )
        source = result.scalar_one_or_none()

        if not source:
            raise HTTPException(404, f"Source with number {source_number} not found")

        # Convert to schema BEFORE deletion
        deleted_source = DataSourceSchema.model_validate(source).model_dump()

        # Delete source (cascade will remove related Data)
        await session.delete(source)
        await session.commit()

        return {
            "message": f"Source {source_number} and all related data have been successfully deleted.",
            "deletedSource": deleted_source
        }
