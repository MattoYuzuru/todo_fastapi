from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.session import engine
from .models.base import Base
from .routes import todo_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="todoly", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # http://localhost:8080 *
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router.router, tags=["To-Dos"])
app.include_router(user_router.router, tags=["Users"])


@app.get("/")
def read_root():
    return {"message" : "Welcome to Todoly."}
