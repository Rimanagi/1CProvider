from pydantic import BaseModel

from src.app.core.config import settings as s


class HealthCheck(BaseModel):
    status: str = "OK"
    service: str = ""
    version: str = s.app.version
