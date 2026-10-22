from dishka import Provider, Scope, provide

from src.app.core.config import Settings


class SettingsProvider(Provider):
    def __init__(self, settings: Settings):
        super().__init__()
        self._settings = settings

    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return self._settings
