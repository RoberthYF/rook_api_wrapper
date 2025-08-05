import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import collection
from app.auth import create_access_token


def get_test_token():
    return create_access_token({"sub": "admin"})


@pytest.mark.asyncio
async def test_get_dog_image_success():
    await asyncio.sleep(0)
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as ac:
        response = await ac.get("/dog/breed/beagle")
        assert response.status_code == 200

        data = response.json()
        assert "image_url" in data
        assert data["image_url"] is not None  # <- ahora importante
        assert "breed" in data
        assert data["breed"].lower() == "beagle"


@pytest.mark.asyncio
async def test_insert_failed_request():
    test_entry = {
        "breed": "not-a-real-breed",
        "image_url": None,
        "timestamp": "2025-08-01T00:00:00Z",
        "response_code": 404
    }
    insert_result = await collection.insert_one(test_entry)
    assert insert_result.inserted_id is not None

    found = await collection.find_one({"_id": insert_result.inserted_id})
    assert found is not None
    assert found["image_url"] is None
    assert found["response_code"] == 404
