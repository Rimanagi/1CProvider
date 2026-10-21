from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str = "OK"
    service: str
    version: str
