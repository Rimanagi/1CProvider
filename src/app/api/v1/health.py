from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.app.core.config import Settings
from src.app.schema.health import HealthCheck

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/", response_model=HealthCheck)
@inject
async def get_health(settings: FromDishka[Settings]) -> HealthCheck:
    status = HealthCheck(
        service=settings.app.name,
        version=settings.app.version
    )
    return status
