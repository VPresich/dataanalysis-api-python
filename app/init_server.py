import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware import log_requests
from app.middleware import CacheControl
from fastapi import HTTPException
from app.exceptions import (
    CustomException,
    custom_exception_handler,
    http_exception_handler,
    generic_exception_handler,
)
from app.routers import routers
from fastapi.staticfiles import StaticFiles
from app.config.paths import UPLOAD_DIR, TEMP_UPLOAD_DIR


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
    app.add_middleware(CacheControl)

    # Create folders for upload files
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

    # Logging middleware (runs before and after every request)
    app.middleware("http")(log_requests)

    app.include_router(routers, prefix="/api")

    # Exception Handlers
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    return app
