from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class App(BaseModel):
    title: str = "1C Provider"
    name: str = "1c-provider"
    version: str = "0.1.0"
    host: str
    port: int

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class Settings(BaseSettings):
    app: App
    mode: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        # env_prefix= ""
    )
