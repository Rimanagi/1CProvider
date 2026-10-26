import json
from typing import Any
from uuid import UUID

import httpx
import pytest
from pydantic import ValidationError

from src.app.clients.onec import OneCClient
from src.app.schema.onec import IdentifiedDefect


def cp1251_json_response(request: httpx.Request, payload: Any) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        request=request,
        content=json.dumps(payload, ensure_ascii=False).encode("cp1251"),
    )


async def test_get_typical_defects_returns_models() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path.endswith("/TypicalDefects")
        return cp1251_json_response(
            request,
            [
                {
                    "GUIDTypicalDefect": "43361236-1004-11ee-990c-2c6dc1726ced",
                    "Code": "000000001",
                    "TypicalDefect": "Аппаратный",
                },
            ],
        )

    async with httpx.AsyncClient(
        base_url="http://1c.test/",
        transport=httpx.MockTransport(handler),
    ) as http_client:
        client = OneCClient(http_client)
        defects = await client.get_typical_defects()

    assert len(defects) == 1
    assert defects[0].guid == UUID("43361236-1004-11ee-990c-2c6dc1726ced")
    assert defects[0].code == "000000001"
    assert defects[0].name == "Аппаратный"


async def test_get_defect_causes_returns_models() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path.endswith("/CausesOfDefects")
        return cp1251_json_response(
            request,
            [
                {
                    "GUIDTitle": "dc0b23d1-0b50-11ee-990a-2c6dc1726ced",
                    "Code": "000000001",
                    "TheCauseOfTheDefect": "Естественный износ",
                },
            ],
        )

    async with httpx.AsyncClient(
        base_url="http://1c.test/",
        transport=httpx.MockTransport(handler),
    ) as http_client:
        client = OneCClient(http_client)
        causes = await client.get_defect_causes()

    assert len(causes) == 1
    assert causes[0].guid == UUID("dc0b23d1-0b50-11ee-990a-2c6dc1726ced")
    assert causes[0].code == "000000001"
    assert causes[0].name == "Естественный износ"


async def test_get_typical_defects_raises_on_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=503, request=request)

    async with httpx.AsyncClient(
        base_url="http://1c.test/",
        transport=httpx.MockTransport(handler),
    ) as http_client:
        client = OneCClient(http_client)

        with pytest.raises(httpx.HTTPStatusError) as error:
            await client.get_typical_defects()

    assert error.value.response.status_code == 503


async def test_get_typical_defects_raises_on_invalid_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return cp1251_json_response(
            request,
            [
                {
                    "Code": "000000001",
                    "TypicalDefect": "Аппаратный",
                },
            ],
        )

    async with httpx.AsyncClient(
        base_url="http://1c.test/",
        transport=httpx.MockTransport(handler),
    ) as http_client:
        client = OneCClient(http_client)

        with pytest.raises(ValidationError):
            await client.get_typical_defects()


async def test_get_repair_facilities_returns_models() -> None:
    content = (
        "GUIDRepairObject;CodeRepairObject;RepairObject;GUIDParent;CodeParent;Parent\r\n"
        "e015e632-b5ac-11f1-8011-566f28370005;ГС-094415;Измерительный прибор;"
        "0a83ca4a-118e-11ee-990d-2c6dc1726ced;ГС-000024966;Датчик температуры\r\n"
    ).encode("utf-8")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path.endswith("/RepairFacilities")
        return httpx.Response(status_code=200, request=request, content=content)

    async with httpx.AsyncClient(
        base_url="http://1c.test/",
        transport=httpx.MockTransport(handler),
    ) as http_client:
        client = OneCClient(http_client)
        repair_facilities = await client.get_repair_facilities()

    assert len(repair_facilities) == 1
    assert repair_facilities[0].guid == UUID("e015e632-b5ac-11f1-8011-566f28370005")
    assert repair_facilities[0].code == "ГС-094415"
    assert repair_facilities[0].name == "Измерительный прибор"


async def test_post_identified_defect_sends_json() -> None:
    defect = IdentifiedDefect.model_validate(
        {
            "defect": {
                "defect_type_id": "43361236-1004-11ee-990c-2c6dc1726ced",
                "defect_reason_id": "dc0b23d1-0b50-11ee-990a-2c6dc1726ced",
                "equipment_id": "e015e632-b5ac-11f1-8011-566f28370005",
                "server_defect_id": "server-defect-1",
                "detected_at": "2026-10-26T12:00:00+03:00",
                "comment": "Тестовый дефект",
            },
            "users": {
                "walker": {
                    "person_number": "000123",
                    "full_name": "Иванов Иван Иванович",
                },
            },
            "transfer": {
                "idempotency_id": "transfer-1",
                "transferred_at": "2026-10-26T12:05:00+03:00",
                "payload_sha256": "a" * 64,
            },
        },
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path.endswith("/Identifieddefects")
        assert json.loads(request.content) == defect.model_dump(mode="json")
        return httpx.Response(status_code=200, request=request)

    async with httpx.AsyncClient(
        base_url="http://1c.test/",
        transport=httpx.MockTransport(handler),
    ) as http_client:
        client = OneCClient(http_client)
        await client.post_identified_defect(defect)

