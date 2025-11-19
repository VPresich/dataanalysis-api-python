from fastapi import Path
from app.validation import SourceNumberValidation


async def valid_parameter(
    source_number: int = Path(..., description="Number of the source to update")
) -> int:
    """
    Dependency to validate `source_number` from path using Pydantic model.
    Returns validated positive integer.
    """
    validated = SourceNumberValidation(source_number=source_number)
    return validated.source_number
