import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth import create_access_token


def get_test_token():
    return create_access_token({"sub": "admin"})


@pytest.mark.asyncio
async def test_breed_endpoint_success():
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as ac:
        response = await ac.get("/dog/breed/husky")

    assert response.status_code == 200
    assert "breed" in response.json()
    assert "image_url" in response.json()
