from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from .base import Base
from .associations import task_user_association

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()
    status: Mapped[str] = mapped_column(default="new")
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))

    # Связь многие-ко-многим: пользователи, назначенные на задачу
    assigned_users: Mapped[list["User"]] = relationship(
        "User",
        secondary=task_user_association,
        back_populates="assigned_tasks",
        lazy="selectin",
    )

    # Связь один-ко-многим: задача принадлежит проекту
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="tasks",
        lazy="selectin",
    )
