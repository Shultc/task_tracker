from sqlalchemy import select
from typing import List, Optional

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from .base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session):
        super().__init__(session)

    async def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        db_project = Project(
            title=project_data.title,
            description=project_data.description,
            owner_id=project_data.owner_id,
        )
        await self.create(db_project)
        await self.session.commit()
        await self.session.refresh(db_project)

        return ProjectResponse(
            id=db_project.id,
            title=db_project.title,
            description=db_project.description,
            owner_id=db_project.owner_id,
        )

    async def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return await self.get_by_id(project_id, Project)

    async def list_projects(self) -> List[Project]:
        return await self.list_all(Project)

    async def update_project(self, project_id: int, **kwargs) -> Optional[Project]:
        project = await self.get_by_id(project_id, Project)
        if not project:
            return None

        if "title" in kwargs:
            project.title = kwargs["title"]
        if "description" in kwargs:
            project.description = kwargs["description"]

        await self.session.flush()
        await self.session.commit()
        return project

    async def delete_project(self, project_id: int) -> bool:
        project = await self.get_by_id(project_id, Project)
        if not project:
            return False
        await self.session.delete(project)
        await self.session.commit()
        return True
