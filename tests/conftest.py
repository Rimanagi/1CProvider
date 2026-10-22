import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport

from src.app.core.config import App, LoggingSettings, OneCSettings, Settings
from src.app.factory import create_app

@pytest.fixture(scope="session")
def one_c_base_test_url():
    return "http://1c.test"

@pytest.fixture(scope="session")
def app_base_test_url():
    return "http://test"


@pytest.fixture(scope="session")
def settings(one_c_base_test_url):
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
        onec=OneCSettings(
            base_url=one_c_base_test_url,
            login="login",
            password="password",
            timeout_sec=20,
        )
    )


# def is_dev_mode(settings) -> bool:
#     return settings.mode == "TEST"


@pytest.fixture(scope="session")
def app(settings) -> FastAPI:
    return create_app(settings)


@pytest.fixture(scope="function")
async def cl(app, app_base_test_url):
    async with httpx.AsyncClient(base_url=app_base_test_url, transport=ASGITransport(app)) as cl:
        yield cl
