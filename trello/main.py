

from fastapi import FastAPI
from trello.dbConnection import create_db_and_tables , drop_tables
from trello.routers import project_crud, task_crud, category_crud, auth as auth_router

app = FastAPI(title="Trello Clone API")

@app.on_event("startup")
def on_startup():
    
    create_db_and_tables()

app.include_router(auth_router.router)
app.include_router(project_crud.router)
app.include_router(task_crud.router)
app.include_router(category_crud.router)
