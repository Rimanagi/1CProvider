import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport

from src.app.core.config import App, LoggingSettings, Settings
from src.app.factory import create_app


@pytest.fixture(scope="session")
def settings():
    app = App(
        title="1C Provider",
        name="1c-provider",
        version="0.1.0",
        host="127.0.0.1",
        port=8000,
    )
    mode = "TEST"
    return Settings(
        app=app,
        log=LoggingSettings(log_level="WARNING"),
        mode=mode,
    )


# def is_dev_mode(settings) -> bool:
#     return settings.mode == "TEST"


@pytest.fixture(scope="session")
def app(settings) -> FastAPI:
    return create_app(settings)


@pytest.fixture(scope="function")
async def cl(app):
    async with httpx.AsyncClient(base_url="http://test", transport=ASGITransport(app)) as cl:
        yield cl
