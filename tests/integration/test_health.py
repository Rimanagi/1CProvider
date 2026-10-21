import httpx

from src.main import app

transport = httpx.ASGITransport(app)

async def test_health():
    async with httpx.AsyncClient(transport=transport) as cl:
        url = "http://test/api/v1/health/"
        response = await cl.get(url)
        assert response.status_code == 200