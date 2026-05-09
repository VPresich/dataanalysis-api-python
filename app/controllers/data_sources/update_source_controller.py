from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.data_sources import update_source_service


@ctrl_wrapper
async def update_source_controller(user: dict, source_number: int, data: dict, db: AsyncSession):
    """
    Controller to update data source.
    """
    result = await update_source_service(
        user_id=user["id"],
        source_number=source_number,
        source_name=data.get("source_name"),
        file_name=data.get("file_name"),
        comment=data.get("comment"),
        session = db
    )

    return result
