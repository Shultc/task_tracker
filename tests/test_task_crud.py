import pytest
from app.schemas.task import TaskCreate

@pytest.mark.asyncio
async def test_create_task_success(client):
    # Сначала создаём проект
    project_response = await client.post("/projects/", json={
        "title": "Test Project",
        "owner_id": 1
    })
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]


    # Теперь создаём задачу
    task_data = TaskCreate(
        title="Test Task",
        project_id=project_id,
        status="new"
    )
    response = await client.post("/tasks/", json=task_data.model_dump())  # ← слеш!
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
