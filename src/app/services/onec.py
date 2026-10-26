from src.app.clients.onec import OneCClient
from src.app.schema.onec import DefectCause, IdentifiedDefect, RepairFacility, TypicalDefect


class OneCService:
    def __init__(self, one_c_client: OneCClient) -> None:
        self._one_c_client = one_c_client

    async def get_typical_defects(self) -> list[TypicalDefect]:
        return await self._one_c_client.get_typical_defects()

    async def get_defect_causes(self) -> list[DefectCause]:
        return await self._one_c_client.get_defect_causes()

    async def get_repair_facilities(self) -> list[RepairFacility]:
        return await self._one_c_client.get_repair_facilities()

    async def post_identified_defect(self, defect: IdentifiedDefect) -> None:
        # TODO: Deduplicate transfers by idempotency_id after adding persistent storage.
        await self._one_c_client.post_identified_defect(defect)
