from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from trello.dbConnection import create_db_and_tables, get_session, engine
from trello.models import Task, Project
from pydantic import BaseModel, Field
from typing import Annotated, Optional

app = FastAPI()


#Check if task with same name exists
def ifexists(task_name: str, session: Session) -> bool:
    existing_task = session.exec(
        select(Task).where(Task.task_name == task_name)
    ).first()
    return existing_task is not None

def taskExistsById(task_id: int, session: Session) -> bool:
    existing_task = session.get(Task, task_id)
    return existing_task is not None

#Task Schema for Create and Update operations
class taskCreate(BaseModel):
    id: int
    task_name: Annotated[str, Field(..., description="Task Name", max_length=100)]
    task_status: Annotated[str, Field(..., description="Task Status", max_length=50)]

class taskUpdate(BaseModel):
    task_name: Annotated[Optional[str], Field(description="Task Name", max_length=100, default=None)]
    task_status: Annotated[Optional[str], Field(description="Task Status", max_length=50, default=None)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # insert_initial_data()

#Task CRUD Operations
def insert_initial_data():
    with Session(engine) as session:
        count = session.exec(select(Task)).all()
        if len(count) == 0:
            tasks = [
                Task(task_name="Learn FastAPI", task_status="pending"),
                Task(task_name="Set up Database", task_status="done"),
                Task(task_name="Build CRUD APIs", task_status="in-progress"),
                Task(task_name="Test Endpoints", task_status="pending"),
                Task(task_name="Deploy to Server", task_status="pending"),
            ]
            session.add_all(tasks)
            session.commit()


@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks


@app.get("/tasks/status/{task_status}")
def getByStatus(task_status: str, session: Session = Depends(get_session)):
    tasks = session.exec(
        select(Task).where(Task.task_status == task_status)
    ).all()
    return tasks

@app.get("/tasks/id/{task_id}")
def getById(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

@app.post("/createTask", response_model=Task)
def create(task: taskCreate, session: Session = Depends(get_session)):

    if ifexists(task.task_name, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task '{task.task_name}' already exists!"
        )

    new_task = Task(**task.dict())
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

@app.put("/updateTask/{task_id}", response_model=Task)
def update(task_id: int, task: taskUpdate, session: Session = Depends(get_session)):

    existing_task = session.get(Task, task_id)  
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    for key, value in task.dict(exclude_unset=True).items():
        setattr(existing_task, key, value)

    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task


@app.delete("/deleteTask/{task_id}")
def delete(task_id: int, session: Session = Depends(get_session)):
    existing_task = session.get(Task, task_id) 
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    session.delete(existing_task)
    session.commit()
    return {"message": "Task deleted successfully"}

@app.post("/createProject")
def create_project(project: Project, session: Session = Depends(get_session)):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.get("/projects")
def get_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return projects


@app.get("/projects/{id}")
def get_project(id: int, session: Session = Depends(get_session)):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/updateProject/{id}")
def update_project(id: int, updated: Project, session: Session = Depends(get_session)):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.project_name = updated.project_name
    project.project_description = updated.project_description
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.delete("/deleteProject/{id}")
def delete_project(id: int, session: Session = Depends(get_session)):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    session.delete(project)
    session.commit()
    return {"message": "Project deleted successfully"}