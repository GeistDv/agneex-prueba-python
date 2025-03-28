import pytest
from httpx import AsyncClient
from src.main import app
from src.config import settings

@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json={"microservice": "test_ms", "password": "test_password"},
        )
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_failure():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json={"microservice": "wrong_ms", "password": "wrong_password"},
        )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}