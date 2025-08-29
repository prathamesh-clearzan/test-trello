
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from trello.dbConnection import get_session
from trello.models import Project, User
from trello.schemas import ProjectCreate, ProjectRead, ProjectUpdate
from trello.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectRead)
def create_project(project: ProjectCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_project = Project(**project.dict(), owner_id=current_user.id)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.get("/", response_model=list[ProjectRead])
def get_projects(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return session.exec(select(Project).where(Project.owner_id == current_user.id)).all()

@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, updated_data: ProjectUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    for k, v in updated_data.dict(exclude_unset=True).items():
        setattr(project, k, v)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"detail": "Project deleted successfully"}
