import httpx
import pytest


@pytest.mark.anyio
async def test_create_bid():
    new_bid = {
        "name": "Предложение 1",
        "description": "Описание предложения",
        "status": "Submitted",
        "tenderId": 1,
        "organizationId": 1,
        "creatorUsername": "user1"
    }
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.post("/api/bids/new", json=new_bid)
    assert response.status_code == 200
    bid = response.json()
    assert bid["name"] == "Предложение 1"

@pytest.mark.anyio
async def test_get_my_bids():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.get("/api/bids/my?username=user1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_get_bids_for_tender():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.get("/api/bids/1/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_edit_bid():
    updated_bid = {
        "name": "Обновленное Предложение 1",
        "description": "Обновленное описание"
    }
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.patch("/api/bids/1/edit", json=updated_bid)
    assert response.status_code == 200
    bid = response.json()
    assert bid["name"] == "Обновленное Предложение 1"

@pytest.mark.anyio
async def test_rollback_bid():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.put("/api/bids/1/rollback/2")
    assert response.status_code == 200
    bid = response.json()
    assert "версия 2" in bid["name"]
