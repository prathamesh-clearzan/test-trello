from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    tasks: List["Task"] = Relationship(back_populates="project")


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    tasks: List["Task"] = Relationship(back_populates="category")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str
    description: Optional[str] = None

    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    project: Optional[Project] = Relationship(back_populates="tasks")

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="tasks")
