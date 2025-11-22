# from fastapi import Query, HTTPException


# def time_params(
#     start_time: str | None = Query(None),
#     end_time: str | None = Query(None)
# ):
#     """
#     Validate start_time and end_time query parameters.

#     Raises HTTPException if:
#     - start_time or end_time is not a number
#     - start_time > end_time
#     """
#     try:
#         start = float(start_time) if start_time is not None else None
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid start_time. It must be a number.")

#     try:
#         end = float(end_time) if end_time is not None else None
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid end_time. It must be a number.")

#     if start is not None and end is not None and start > end:
#         raise HTTPException(status_code=400, detail="start_time must be less than or equal to end_time.")

#     return start, end


from fastapi import Query, HTTPException


def time_params(
    startTime: str | None = Query(None, alias="startTime"),
    endTime: str | None = Query(None, alias="endTime"),
):
    """
    Accepts camelCase query params exactly like Node backend:
    /filter?startTime=1.5&endTime=3.2
    """
    # Validate startTime
    if startTime is not None:
        try:
            start = float(startTime)
        except ValueError:
            raise HTTPException(400, "Invalid startTime. It must be a number.")
    else:
        start = None

    # Validate endTime
    if endTime is not None:
        try:
            end = float(endTime)
        except ValueError:
            raise HTTPException(400, "Invalid endTime. It must be a number.")
    else:
        end = None

    # Logical check
    if start is not None and end is not None and start > end:
        raise HTTPException(400, "startTime must be less than or equal to endTime.")

    return start, end
