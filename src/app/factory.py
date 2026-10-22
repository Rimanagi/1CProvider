from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.app.api import router as api_router
from src.app.core.config import Settings
from src.app.providers import OneCProvider, SettingsProvider

log = structlog.get_logger(__name__)


def create_app(settings: Settings) -> FastAPI:
    async_container = make_async_container(
        SettingsProvider(settings),
        OneCProvider(),
    )

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        log.info(
            "app_started",
            service=settings.app.name,
            version=settings.app.version,
            mode=settings.mode,
        )
        yield
        await async_container.close()
        log.info(
            "app_stopped",
            service=settings.app.name,
            version=settings.app.version,
            mode=settings.mode,
        )

    app = FastAPI(
        title=settings.app.title,
        lifespan=lifespan,
        version=settings.app.version,
    )

    setup_dishka(async_container, app)

    app.include_router(api_router)

    return app
