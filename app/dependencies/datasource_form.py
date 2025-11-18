from fastapi import Form
from typing import Optional
from app.validation import DataSourceValidation


async def datasource_form(
    source_number: int = Form(...),
    source_name: Optional[str] = Form(None),
    file_name: Optional[str] = Form(None),
    comment: Optional[str] | None = Form(None)
) -> DataSourceValidation:
    return DataSourceValidation(
        source_number=source_number,
        source_name=source_name,
        file_name=file_name,
        comment=comment
    )
