# app/services/data_sources/parser_csv_chunked.py
import csv
import os
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models import Data
from .parser_csv import convert_value


async def parse_and_save_csv_chunked(
    file_path: str,
    data_source_id,
    session: AsyncSession,
) -> dict:
    """
    Optimized version: Parses a tab-separated CSV file and inserts data 
    into the database using memory-efficient chunking.
    """
    total_records = 0
    chunk_size = 2000
    chunk = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                cleaned_row = {k.strip(): convert_value(k.strip(), v) for k, v in row.items()}
                chunk.append({"id_source": data_source_id, **cleaned_row})

                if len(chunk) >= chunk_size:
                    await session.execute(Data.__table__.insert(), chunk)
                    total_records += len(chunk)
                    chunk = []

            if chunk:
                await session.execute(Data.__table__.insert(), chunk)
                total_records += len(chunk)

    except FileNotFoundError:
        raise HTTPException(400, f"CSV file not found: {file_path}")
    except csv.Error as e:
        raise HTTPException(400, f"CSV parsing error: {e}")
    except SQLAlchemyError as e:
        raise HTTPException(500, f"DB insert error: {e}")

    try:
        os.remove(file_path)
    except Exception:
        pass

    return {
        "message": "Data processed successfully using chunked stream",
        "totalRecords": total_records,
    }
