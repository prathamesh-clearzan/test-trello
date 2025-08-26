from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from trello.dbConnection import get_session
from trello.models import Project
from trello.schemas import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["Projects"])



@router.post("/", response_model=ProjectRead)
def create_project(project: ProjectCreate, session: Session = Depends(get_session)):
    new_project = Project(**project.dict())
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project



@router.get("/", response_model=list[ProjectRead])
def get_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project)).all()



@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project



@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, updated_data: ProjectCreate, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in updated_data.dict().items():
        setattr(project, key, value)

    session.add(project)
    session.commit()
    session.refresh(project)
    return project



@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    session.delete(project)
    session.commit()
    return {"detail": "Project deleted successfully"}
