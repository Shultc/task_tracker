from sqlalchemy import select, func
from typing import List, Optional

from app.models.task import Task
from app.models.project import Project
from app.schemas.task import TaskCreate, TaskResponse
from .base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, session):
        super().__init__(session)

    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        # Проверка существования проекта
        project_exists = await self.session.scalar(
            select(func.count()).where(Project.id == task_data.project_id)
        )
        if not project_exists:
            raise ValueError(f"Project with id {task_data.project_id} does not exist")

        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            project_id=task_data.project_id,
            status=task_data.status,
        )

        await self.create(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        return TaskResponse(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            project_id=db_task.project_id,
            status=db_task.status,
        )

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return await self.get_by_id(task_id, Task)

    async def list_tasks(
        self,
        status: Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> List[Task]:
        query = select(Task)

        if status is not None:
            query = query.where(Task.status == status)

        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars())

    async def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[Task]:
        task = await self.get_by_id(task_id, Task)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status

        await self.session.flush()
        await self.session.commit()
        return task

    async def delete_task(self, task_id: int) -> bool:
        task = await self.get_by_id(task_id, Task)
        if not task:
            return False
        await self.session.delete(task)
        await self.session.commit()
        return True
