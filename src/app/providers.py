from collections.abc import AsyncIterator

import httpx
from dishka import Provider, Scope, provide

from src.app.clients.onec import OneCClient
from src.app.core.config import Settings
from src.app.services.onec import OneCService


class SettingsProvider(Provider):
    def __init__(self, settings: Settings):
        super().__init__()
        self._settings = settings

    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return self._settings


class OneCProvider(Provider):
    @provide(scope=Scope.APP)
    async def client(self, settings: Settings) -> AsyncIterator[httpx.AsyncClient]:
        async with httpx.AsyncClient(
            auth=(settings.onec.login, settings.onec.password),
            base_url=str(settings.onec.base_url),
            timeout=settings.onec.timeout_sec,
        ) as cl:
            yield cl

    @provide(scope=Scope.APP)
    def one_c_client(self, client: httpx.AsyncClient) -> OneCClient:
        return OneCClient(client)

    @provide(scope=Scope.APP)
    def one_c_service(self, one_c_client: OneCClient) -> OneCService:
        return OneCService(one_c_client)
