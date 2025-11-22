from fastapi import HTTPException
from sqlalchemy import select
from app.database import get_db_session
from app.models.user import User
from app.models import DataSource
from app.schemas import DataSourceSchema
from uuid import UUID


async def update_source_service(
    *,
    user_id: str,
    source_number: int,
    source_name: str | None = None,
    file_name: str | None = None,
    comment: str | None = None
) -> dict:

    async with get_db_session() as session:

        result = await session.execute(
            select(User).where(User._id == UUID(user_id))
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(404, "User not found")

        result = await session.execute(
            select(DataSource).where(
                (DataSource.id_user == UUID(user_id))
                & (DataSource.source_number == source_number)
            )
        )
        source = result.scalar_one_or_none()
        if not source:
            raise HTTPException(404, "Source with this number does not exist")

        if source_name is not None:
            source.source_name = source_name
        if file_name is not None:
            source.file_name = file_name
        if comment is not None:
            source.comment = comment

        await session.commit()
        await session.refresh(source)

        updated_source = DataSourceSchema.model_validate(source).model_dump(by_alias=True)

        return {
            "message": f"Source {source_number} has been successfully updated.",
            "updatedSource": updated_source,
        }
