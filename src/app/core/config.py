from typing import Annotated, Literal

from pydantic import AnyHttpUrl, BaseModel, Field
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


class LoggingSettings(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


class OneCSettings(BaseModel):
    base_url: AnyHttpUrl
    login: str
    password: Annotated[str, Field(..., min_length=8)]
    timeout_sec: int = 20


class Settings(BaseSettings):
    app: App
    log: LoggingSettings
    onec: OneCSettings
    mode: Literal["DEV", "TEST", "PROD"]
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
    )
