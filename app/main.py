from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import init_server, init_db
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context.
    Runs once at startup and shutdown.

    On startup: tests DB connection.
    On shutdown: logs message (optional cleanup logic can go here).
    """
    # Startup: check DB connection
    await init_db()
    print("Database connection verified. Application is starting...")

    yield  # <-- this yields control to FastAPI to start serving requests

    # Shutdown: optional cleanup
    print("Application is shutting down...")


# Initialize the FastAPI app with lifespan
app: FastAPI = init_server(lifespan=lifespan)


if __name__ == "__main__":
    # Run the server with auto-reload (similar to nodemon)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
