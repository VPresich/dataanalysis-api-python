from fastapi import Query, HTTPException


def time_params(
    start_time: str | None = Query(None),
    end_time: str | None = Query(None)
):
    """
    Validate start_time and end_time query parameters.

    Raises HTTPException if:
    - start_time or end_time is not a number
    - start_time > end_time
    """
    try:
        start = float(start_time) if start_time is not None else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid start_time. It must be a number.")

    try:
        end = float(end_time) if end_time is not None else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid end_time. It must be a number.")

    if start is not None and end is not None and start > end:
        raise HTTPException(status_code=400, detail="start_time must be less than or equal to end_time.")

    return start, end
