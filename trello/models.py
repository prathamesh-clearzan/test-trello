
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Task

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="users.id")
    tasks: List["Task"] = Relationship(back_populates="project")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    tasks: List["Task"] = Relationship(back_populates="category")

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, sa_column_kwargs={"unique": True})
    email: Optional[str] = Field(default=None, sa_column_kwargs={"unique": True})
    hashed_password: str
    role: Optional[str] = Field(default="member")
    tasks_assigned: List["Task"] = Relationship(back_populates="assigned_user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str
    description: Optional[str] = None
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    project: Optional[Project] = Relationship(back_populates="tasks")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="tasks")
    assigned_to: Optional[int] = Field(default=None, foreign_key="users.id")
    assigned_user: Optional[User] = Relationship(back_populates="tasks_assigned")
