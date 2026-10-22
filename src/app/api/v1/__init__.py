from fastapi import APIRouter

from src.app.api.v1.health import router as health_router
from src.app.api.v1.one_c import router as one_c_router

router = APIRouter(
    tags=["v1"],
    prefix="/v1",
)
router.include_router(health_router)
router.include_router(one_c_router)
