import logging
import time
from fastapi import Request


# Use the Uvicorn logger (so logs go to the same stream as FastAPI)
logger = logging.getLogger("uvicorn")


# ANSI colors for console output (works in VS Code terminal, PowerShell, etc.)
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


async def log_requests(request: Request, call_next):
    """
    Middleware that logs each HTTP request and response with execution time.

    Features:
      - Logs HTTP method, path, and status code
      - Calculates and displays request duration
      - Colors output based on response status:
          Green: 2xx (Success)
          Yellow: 4xx (Client error)
          Red: 5xx (Server error)
      - Adds X-Process-Time-ms header to the response
    """
    start_time = time.time()

    # Log incoming request
    logger.info(f"➡ {Colors.CYAN}{request.method} {request.url.path}{Colors.RESET}")

    try:
        response = await call_next(request)
    except Exception as e:
        # Log unexpected errors
        logger.error(
            f"{Colors.RED} Exception while processing request: {e}{Colors.RESET}"
        )
        raise

    process_time = (time.time() - start_time) * 1000  # ms
    duration = f"{process_time:.2f} ms"

    # Choose color based on response status
    status = response.status_code
    if status < 400:
        color = Colors.GREEN
    elif status < 500:
        color = Colors.YELLOW
    else:
        color = Colors.RED

    # Log result with color-coded status
    logger.info(
        f"⬅ {color}{status}{Colors.RESET} "
        f"{request.method} {request.url.path} "
        f"({duration})"
    )

    # Add duration header for visibility in Postman / browser devtools
    response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"

    return response
