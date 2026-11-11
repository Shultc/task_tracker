import pytest
from app.schemas.user import UserCreate

@pytest.mark.asyncio
async def test_create_user_success(client):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    response = await client.post("/users/", json=user_data)  # ← слеш!
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert "id" in data
