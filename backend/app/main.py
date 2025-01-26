from fastapi import FastAPI

from .db.session import engine
from .models.base import Base
from .routes import todo_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="todoly", version="1.0")
app.include_router(todo_router.router, prefix="/todos", tags=["To-Dos"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"message" : "Welcome to ToDoly :) You have to use /docs for now."}
