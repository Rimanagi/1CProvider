from collections.abc import AsyncIterator

import httpx
from dishka import Provider, Scope, provide

from src.app.clients.onec import OneCClient
from src.app.core.config import Settings


class SettingsProvider(Provider):
    def __init__(self, settings: Settings):
        super().__init__()
        self._settings = settings

    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return self._settings


class OneCProvider(Provider):

    @provide(scope=Scope.APP)
    async def client(self, _settings: Settings) -> AsyncIterator[httpx.AsyncClient]:
        async with httpx.AsyncClient(
            auth=(_settings.onec.login, _settings.onec.password),
            base_url=str(_settings.onec.base_url),
            timeout=_settings.onec.timeout_sec,
        ) as cl:
            yield cl

    @provide(scope=Scope.APP)
    def one_c_client(self, client: httpx.AsyncClient) -> OneCClient:
        return OneCClient(client)
