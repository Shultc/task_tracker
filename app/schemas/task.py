from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    status: str = "new"

class TaskUpdate(BaseModel):
    # project_id убрали: перенос задачи между проектами — отдельная логика
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    project_id: int
    status: str

    model_config = {"extra": "ignore"}
