from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_async_session
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

async def get_task_repo(session: AsyncSession = Depends(get_async_session)):
    return TaskRepository(session)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    repo: TaskRepository = Depends(get_task_repo),
):
    try:
        return await repo.create_task(task_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter by status (new/open/in_progress/done)"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    repo: TaskRepository = Depends(get_task_repo),
):
    offset = (page - 1) * size
    tasks = await repo.list_tasks(status=status, offset=offset, limit=size)
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    repo: TaskRepository = Depends(get_task_repo),
):
    task = await repo.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    repo: TaskRepository = Depends(get_task_repo),
):
    updated = await repo.update_task(
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        status=task_update.status,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        id=updated.id,
        title=updated.title,
        description=updated.description,
        project_id=updated.project_id,
        status=updated.status,
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    repo: TaskRepository = Depends(get_task_repo),
):
    deleted = await repo.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
