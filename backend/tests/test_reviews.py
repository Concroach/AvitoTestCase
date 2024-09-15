import httpx
import pytest


@pytest.mark.anyio
async def test_get_reviews_for_bid():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.get("/api/bids/1/reviews?authorUsername=user2&organizationId=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
