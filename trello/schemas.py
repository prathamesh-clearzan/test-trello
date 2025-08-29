
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(ProjectBase):
    id: int
    owner_id: int
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

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    role: Optional[str] = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
