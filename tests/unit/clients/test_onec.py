from uuid import UUID

import httpx
import pytest
from pydantic import ValidationError

from src.app.clients.onec import OneCClient


async def test_get_typical_defects_returns_models() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path.endswith("/TypicalDefects")
        return httpx.Response(
            status_code=200,
            request=request,
            json=[
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
        assert request.url.path.endswith("/CausesDefects")
        return httpx.Response(
            status_code=200,
            request=request,
            json=[
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
        return httpx.Response(
            status_code=200,
            request=request,
            json=[
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


@pytest.