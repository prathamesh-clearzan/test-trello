from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from trello.dbConnection import get_session
from trello.models import Task, Project
from trello.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/projects/{project_id}", response_model=TaskRead)
def create_task(project_id: int, task: TaskCreate, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = Task(**task.dict(), project_id=project_id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.get("/projects/{project_id}", response_model=list[TaskRead])
def get_tasks(project_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Task).where(Task.project_id == project_id)).all()


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_data: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
