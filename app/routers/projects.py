from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])

async def get_project_repo(session: AsyncSession = Depends(get_async_session)):
    return ProjectRepository(session)

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    repo: ProjectRepository = Depends(get_project_repo),
):
    # owner_id уже внутри project_data
    return await repo.create_project(project_data)

@router.get("/", response_model=list[ProjectResponse])
async def list_projects(repo: ProjectRepository = Depends(get_project_repo)):
    projects = await repo.list_projects()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    repo: ProjectRepository = Depends(get_project_repo),
):
    project = await repo.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,  # используем схему вместо dict
    repo: ProjectRepository = Depends(get_project_repo),
):
    project = await repo.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Обновляем только те поля, которые пришли
    if project_update.title is not None:
        project.title = project_update.title
    if project_update.description is not None:
        project.description = project_update.description

    await repo.session.flush()
    await repo.session.commit()
    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        owner_id=project.owner_id,
    )

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    repo: ProjectRepository = Depends(get_project_repo),
):
    deleted = await repo.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
