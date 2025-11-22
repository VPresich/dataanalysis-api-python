from fastapi import HTTPException
from app.models.data_source import DataSource
from app.models.user import User
from app.services.data_sources.parser_csv import parse_and_save_csv
from app.database import get_db_session
from app.schemas import DataSourceSchema


async def upload_data_service(
    *,
    id: str,
    source_number: int,
    source_name: str,
    file_name: str,
    comment: str | None,
    file_path: str,
) -> dict:
    """
    Service to upload data CSV and create a new DataSource.

    :param id: User ID
    :param source_number: Source number
    :param source_name: Name of the source
    :param file_name: Original file name
    :param comment: Optional comment
    :param file_path: Path to the uploaded CSV file
    :return: dict with parsing results and DataSource object
    """
    async with get_db_session() as session:  # Creates a transaction
        user = await session.get(User, id)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        existing_source = await session.execute(
            DataSource.__table__.select().where(
                (DataSource.id_user == id)
                & (DataSource.source_number == source_number)
            )
        )
        existing_source = existing_source.scalar_one_or_none()
        if existing_source:
            raise HTTPException(
                status_code=409, detail="Source with this number already exists"
            )

        # Create new DataSource
        data_source = DataSource(
            id_user=id,
            source_number=source_number,
            source_name=source_name,
            file_name=file_name,
            comment=comment,
        )
        session.add(data_source)
        await session.flush()  # Ensure `data_source` gets its ID

        # Parse CSV and save data
        try:
            result_parser = await parse_and_save_csv(file_path, data_source._id, session)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Error uploading CSV: {e}")

        await session.commit()

        return {
            **result_parser,
            "dataSource": DataSourceSchema.model_validate(data_source).model_dump(by_alias=True),
        }
