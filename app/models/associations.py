from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

task_user_association = Table(
    "task_user_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
)
