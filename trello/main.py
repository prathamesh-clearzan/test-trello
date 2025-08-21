from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from trello.dbConnection import create_db_and_tables, get_session, engine
from trello.models import Task
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

def ifexists(task_name: str, session: Session) -> bool:
    existing_task = session.exec(
        select(Task).where(Task.task_name == task_name)
    ).first()
    return existing_task is not None

class taskCreate(BaseModel):
    task_name: Annotated[str, Field(..., description="Task Name", max_length=100)]
    task_status: Annotated[str, Field(..., description="Task Status", max_length=50)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    insert_initial_data()


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


@app.get("/tasks/{task_status}")
def getByStatus(task_status: str, session: Session = Depends(get_session)):
    tasks = session.exec(
        select(Task).where(Task.task_status == task_status)
    ).all()
    return tasks


@app.post("/create", response_model=Task)
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
