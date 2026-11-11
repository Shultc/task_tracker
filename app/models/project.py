from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base

class Project(Base):
    __tablename__ = 'projects'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)

    # Связь один-ко-многим: проект принадлежит одному пользователю
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped["User"] = relationship(back_populates='projects')

    # Связь один-ко-многим: у проекта много задач
    tasks: Mapped[list["Task"]] = relationship(back_populates='project')
