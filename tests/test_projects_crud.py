import pytest
from app.schemas.project import ProjectCreate

@pytest.mark.asyncio
async def test_create_project_success(client):
    project_data = ProjectCreate(
        title="Test Project",
        description="Project description",
        owner_id=1
    )
    response = await client.post("/projects/", json=project_data.model_dump())  # ← слеш!
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Project"
    assert "id" in data
