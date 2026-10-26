from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Response, status

from src.app.schema.onec import DefectCause, IdentifiedDefect, RepairFacility, TypicalDefect
from src.app.services.onec import OneCService

router = APIRouter(
    prefix="/1c",
    tags=["1c"],
)


@router.get("/typical-defects", response_model=list[TypicalDefect])
@inject
async def get_typical_defects(
    service: FromDishka[OneCService],
) -> list[TypicalDefect]:
    return await service.get_typical_defects()


@router.get("/defect-causes", response_model=list[DefectCause])
@inject
async def get_defect_causes(
    service: FromDishka[OneCService],
) -> list[DefectCause]:
    return await service.get_defect_causes()


@router.get("/repair-facilities", response_model=list[RepairFacility])
@inject
async def get_repair_facilities(
    service: FromDishka[OneCService],
) -> list[RepairFacility]:
    return await service.get_repair_facilities()


@router.post("/identified-defects", status_code=status.HTTP_200_OK)
@inject
async def post_identified_defect(
    defect: IdentifiedDefect,
    service: FromDishka[OneCService],
) -> Response:
    await service.post_identified_defect(defect)
    return Response(status_code=status.HTTP_200_OK)
