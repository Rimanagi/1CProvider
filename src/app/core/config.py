from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class App(BaseModel):
    title: str = "1C Provider"
    host: str
    port: int


class Settings(BaseSettings):
    app: App
    model_config = SettingsConfigDict(
        env_file= ".env",
        env_nested_delimiter="__",
        # env_prefix= ""
    )

settings = Settings() # pyright: ignore[reportCallIssue]
