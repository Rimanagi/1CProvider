from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.api import router as api_router
from src.app.core.config import Settings


def create_app(settings: Settings) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        print("App loading")
        yield
        print("App Shutting down")

    app = FastAPI(
        title=settings.app.title,
        lifespan=lifespan,
        version=settings.app.version,
    )

    app.include_router(api_router)

    return app
