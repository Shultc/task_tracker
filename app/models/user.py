from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base
from .associations import task_user_association

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Связь один-ко-многим: у пользователя много проектов
    projects: Mapped[list["Project"]] = relationship(back_populates='owner')

    # Связь многие-ко-многим: задачи, назначенные пользователю
    assigned_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary=task_user_association,
        back_populates="assigned_users",
        lazy="selectin",
    )
