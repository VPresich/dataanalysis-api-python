import csv
import os
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models import Data
from app.database import get_db_session

# List of columns in the Data table that are of type String
STRING_FIELDS = [
    "CVpositive", "CVstable", "CApositive", "CAstable", "CTpositive", "CTstable",
    "Kde", "KdeWeighted", "Gaussian", "GaussianWeighted", "EvaluationNum",
    "IMMconsistentValue", "probability", "TrackConsistent", "VelocityConsistent",
    "IMMconsistent", "IMMpositive", "velocityOK", "speed"
]


def convert_value(key: str, value: str | None):
    """
    Converts a CSV value into the correct Python type.
    - For STRING_FIELDS, always converts to string.
    - For numeric columns, converts to float/int if possible.
    """
    if value is None:
        return "" if key in STRING_FIELDS else None

    trimmed = value.strip()

    if trimmed == "None":
        return "None" if key in STRING_FIELDS else None

    if trimmed == "":
        return "" if key in STRING_FIELDS else None

    # For text columns, convert everything to string
    if key in STRING_FIELDS:
        return str(trimmed)

    # Try to convert to a number for numeric columns
    try:
        num = float(trimmed)
        return int(num) if num.is_integer() else num
    except ValueError:
        # If not a number, leave as string
        return trimmed


async def parse_and_save_csv(
    file_path: str,
    data_source_id,
    session: Optional[AsyncSession] = None,
) -> dict:
    """
    Parses a tab-separated CSV file and inserts the data into the database.

    :param file_path: Path to the uploaded CSV file
    :param data_source_id: UUID of the DataSource entry
    :param session: Optional existing DB transaction session
    """
    results = []

    # --- CSV parsing ---
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                # Convert each value to the correct type based on the column
                cleaned_row = {k.strip(): convert_value(k.strip(), v) for k, v in row.items()}
                results.append({"id_source": data_source_id, **cleaned_row})
    except FileNotFoundError:
        raise HTTPException(400, f"CSV file not found: {file_path}")
    except csv.Error as e:
        raise HTTPException(400, f"CSV parsing error: {e}")

    if not results:
        raise HTTPException(400, "File is empty or not properly tab-delimited.")

    # --- Database insert ---
    async def _insert(sess: AsyncSession):
        try:
            await sess.execute(Data.__table__.insert(), results)
        except SQLAlchemyError as e:
            raise HTTPException(500, f"DB insert error: {e}")

    if session:
        await _insert(session)
    else:
        async with get_db_session() as new_session:
            await _insert(new_session)

    # --- File cleanup ---
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
    except OSError as e:
        print(f"Warning: could not delete file {file_path}: {e}")

    return {
        "message": "Data uploaded successfully",
        "totalRecords": len(results),
    }
