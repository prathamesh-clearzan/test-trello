from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task_name: str
    task_status: str

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_name: str
    project_description: str | None = None