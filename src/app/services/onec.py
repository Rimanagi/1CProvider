from src.app.clients.onec import OneCClient
from src.app.schema.onec import DefectCause, TypicalDefect


class OneCService:
    def __init__(self, one_c_client: OneCClient) -> None:
        self._one_c_client = one_c_client

    async def get_typical_defects(self) -> list[TypicalDefect]:
        return await self._one_c_client.get_typical_defects()

    async def get_defect_causes(self) -> list[DefectCause]:
        return await self._one_c_client.get_defect_causes()
