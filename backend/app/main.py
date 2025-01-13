from fastapi import FastAPI

from .db.session import engine
from .models.base import Base
from .routes import todo_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="todoly", version="1.0")
app.include_router(todo_router.router, prefix="/todos", tags=["To-Dos"])
