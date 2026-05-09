from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import DataSource, User
from app.models import Data
from app.schemas import DataSchema
from typing import List


async def noname_data_by_source_service(source_number: int, session: AsyncSession,) -> List[dict]:
    """
    Service: Retrieves data for noname user by source number.

    :param source_number: The source number
    :return: List of data records (dict), empty list if not found
    """
    result = await session.execute(select(User).where(User.name == "noname user"))
    noname_user = result.scalar_one_or_none()

    if not noname_user:
        return []

    result = await session.execute(
        select(DataSource).where(
            (DataSource.id_user == noname_user._id)
            & (DataSource.source_number == source_number)
        )
    )
    source = result.scalar_one_or_none()

    if not source:
        return []

    data_result = await session.execute(
        select(Data).where(Data.id_source == source._id)
    )
    records = data_result.scalars().all()
    result = [DataSchema.model_validate(r).model_dump(by_alias=True) for r in records]

    return result
