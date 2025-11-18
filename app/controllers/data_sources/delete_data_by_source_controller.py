
from app.utils.ctrl_wrapper import ctrl_wrapper
from app.services.data_sources import delete_data_by_source_service


@ctrl_wrapper
async def delete_data_by_source_controller(user: dict, source_number: int):
    """
    Controller to delete data by source.
    """
    result = await delete_data_by_source_service(
        user_id=user["id"],
        source_number=source_number
    )

    return result
