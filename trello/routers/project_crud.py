from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from trello.dbConnection import get_session
from trello.models import Project

router = APIRouter()

@router.post("/createProject")
def create_project(project: Project, session: Session = Depends(get_session)):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.get("/projects")
def get_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return projects

@router.get("/projects/{id}")
def get_project(id: int, session: Session = Depends(get_session)):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/updateProject/{id}")
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

@router.delete("/deleteProject/{id}")
def delete_project(id: int, session: Session = Depends(get_session)):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"message": "Project deleted successfully"}
