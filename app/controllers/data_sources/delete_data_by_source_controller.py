from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.data_sources import delete_data_by_source_service


@ctrl_wrapper
async def delete_data_by_source_controller(user: dict, source_number: int, db: AsyncSession):
    """
    Controller to delete data by source.
    """
    result = await delete_data_by_source_service(user_id=user["id"],
                                                 source_number=source_number,
                                                 session=db
                                                 )

    return result
