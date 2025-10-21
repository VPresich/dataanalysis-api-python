from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging_middleware import log_requests
from app.middleware.cache_control import CacheControlMiddleware
from fastapi import HTTPException
from app.exceptions import (
    CustomException,
    custom_exception_handler,
    http_exception_handler,
    generic_exception_handler,
)


def init_server(lifespan=None) -> FastAPI:
    """
    Creates and returns a FastAPI application instance
    with CORS and request logging middleware enabled.
    """
    app = FastAPI(title="Data Analysis API", lifespan=lifespan)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change to specific domains in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Cache-Control middleware
    app.add_middleware(CacheControlMiddleware)

    # Logging middleware (runs before and after every request)
    app.middleware("http")(log_requests)

    # Define a simple root endpoint
    @app.get("/")
    async def root():
        return {"message": "Server is working"}

    # Exception Handlers
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    return app
