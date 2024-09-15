import httpx
import pytest


@pytest.mark.anyio
async def test_ping():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.get("/api/ping")
    assert response.status_code == 200
    assert response.text == "ok"
