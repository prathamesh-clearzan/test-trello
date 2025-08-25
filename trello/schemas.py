from pydantic import BaseModel
from typing import Optional, List



class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    class Config:
        from_attributes = True



class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    class Config:
        from_attributes = True



class TaskBase(BaseModel):
    name: str
    status: str
    description: Optional[str] = None
    category_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class TaskRead(TaskBase):
    id: int
    project_id: int
    class Config:
        from_attributes = True
