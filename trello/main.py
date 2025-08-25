from fastapi import FastAPI
from sqlmodel import Session, select
from trello.dbConnection import engine, drop_tables, create_db_and_tables
from trello.routers import project_crud, task_crud, category_crud
from trello.models import Project, Category, Task

app = FastAPI(title="Trello Clone API")

@app.on_event("startup")
def on_startup():
   
    create_db_and_tables()

    with Session(engine) as session:
  
        if not session.exec(select(Project)).first():
            project1 = Project(name="FastAPI Project", description="Learning FastAPI")
            project2 = Project(name="Deployment Project", description="Preparing for deploy")
            session.add_all([project1, project2])
            session.commit()

      
        if not session.exec(select(Category)).first():
            categories = [
                Category(name="Development"),
                Category(name="Testing"),
                Category(name="Deployment"),
            ]
            session.add_all(categories)
            session.commit()

    
        if not session.exec(select(Task)).first():
            sample_task = Task(
                name="Setup Database",
                status="pending",
                description="Configure SQLModel with FastAPI",
                project_id=1,
                category_id=1,
            )
            session.add(sample_task)
            session.commit()

app.include_router(project_crud.router)
app.include_router(task_crud.router)
app.include_router(category_crud.router)
