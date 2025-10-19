from fastapi import FastAPI


def init_server() -> FastAPI:
    """
    Creates and returns a FastAPI application instance.
    """
    app = FastAPI(title="Data Analysis API")

    # Define a simple root endpoint
    @app.get("/")
    async def root():
        return {"message": "Server is working"}

    return app
