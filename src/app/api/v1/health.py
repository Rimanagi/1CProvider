from fastapi import APIRouter

from src.app.schema.health import HealthCheck

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/", response_model=HealthCheck)
async def get_health():
    status = HealthCheck()
    return status
