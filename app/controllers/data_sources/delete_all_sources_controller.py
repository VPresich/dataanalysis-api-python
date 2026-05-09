from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.data_sources import delete_all_sources_service


@ctrl_wrapper
async def delete_all_sources_controller(user: dict, db: AsyncSession):
    """
    Controller to delete data by source.
    """
    result = await delete_all_sources_service(user_id=user["id"], session=db)

    return result
