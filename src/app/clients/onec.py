import json
import httpx

from src.app.schema.onec import DefectCause, TypicalDefect


class OneCClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_typical_defects(self) -> list[TypicalDefect]:
        response = await self._client.get("TypicalDefects")
        response.raise_for_status()
        return [TypicalDefect.model_validate(item) for item in json.loads(response.content.decode("cp1251"))]

    async def get_defect_causes(self) -> list[DefectCause]:
        response = await self._client.get("CausesOfDefects")
        response.raise_for_status()
        return [DefectCause.model_validate(item) for item in json.loads(response.content.decode("cp1251"))]

