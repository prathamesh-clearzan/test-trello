from fastapi import FastAPI
from trello.dbConnection import create_db_and_tables
from trello.routers import task_crud, project_crud

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(task_crud.router)
app.include_router(project_crud.router)
