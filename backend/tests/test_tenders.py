import httpx
import pytest


@pytest.mark.anyio
async def test_get_tenders():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.get("/api/tenders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_create_tender():
    new_tender = {
        "name": "Тендер 1",
        "description": "Описание тендера",
        "serviceType": "Construction",
        "status": "Open",
        "organizationId": 1,
        "creatorUsername": "user1"
    }
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.post("/api/tenders/new", json=new_tender)
    assert response.status_code == 200
    tender = response.json()
    assert tender["name"] == "Тендер 1"
    assert tender["description"] == "Описание тендера"

@pytest.mark.anyio
async def test_get_my_tenders():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.get("/api/tenders/my?username=user1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_edit_tender():
    updated_tender = {
        "name": "Обновленный Тендер 1",
        "description": "Обновленное описание"
    }
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.patch("/api/tenders/1/edit", json=updated_tender)
    assert response.status_code == 200
    tender = response.json()
    assert tender["name"] == "Обновленный Тендер 1"
    assert tender["description"] == "Обновленное описание"

@pytest.mark.anyio
async def test_rollback_tender():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        response = await client.put("/api/tenders/1/rollback/2")
    assert response.status_code == 200
    tender = response.json()
    assert tender["id"] == 1
    assert "версия 2" in tender["name"]
