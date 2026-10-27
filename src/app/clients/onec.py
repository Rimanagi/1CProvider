import json
from csv import DictReader
from io import StringIO
from typing import Any

import httpx

from src.app.schema.onec import DefectCause, IdentifiedDefect, RepairFacility, TypicalDefect


class OneCClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_typical_defects(self) -> list[TypicalDefect]:
        response = await self._client.get("TypicalDefects")
        response.raise_for_status()
        return [
            TypicalDefect.model_validate(item)
            for item in self._parse_response_json(response)
        ]

    async def get_defect_causes(self) -> list[DefectCause]:
        response = await self._client.get("CausesOfDefects")
        response.raise_for_status()
        return [
            DefectCause.model_validate(item)
            for item in self._parse_response_json(response)
        ]

    async def get_repair_facilities(self) -> list[RepairFacility]:
        response = await self._client.post("RepairFacilities")
        print(response.text)
        response.raise_for_status()
        rows = DictReader(StringIO(response.content.decode("utf-8")), delimiter=";")
        return [RepairFacility.model_validate(row) for row in rows]

    async def post_identified_defect(self, defect: IdentifiedDefect) -> None:
        response = await self._client.post(
            "Identifieddefects",
            json=defect.model_dump(mode="json"),
        )
        print(response.text, response.status_code)
        response.raise_for_status()

    @staticmethod
    def _parse_response_json(response: httpx.Response) -> Any:
        return json.loads(response.content.decode("cp1251"))

