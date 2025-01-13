from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud.todo_crud import (create_todo_item,
                              get_todo_item,
                              get_user_todo_items,
                              update_todo_item,
                              delete_todo_item)
from ..db.session import get_db
from ..schemas.todo_schemas import TodoItemCreate, TodoItemUpdate, TodoItemResponse

router = APIRouter()


@router.post("/", response_model=TodoItemResponse)
def create_task(user_id: int, todo: TodoItemCreate, db: Session = Depends(get_db)):
    return create_todo_item(db, user_id, todo)


@router.get("/{todo_id}", response_model=TodoItemResponse)
def read_task(todo_id: int, db: Session = Depends(get_db)):
    task = get_todo_item(db, todo_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=list[TodoItemResponse])
def read_user_tasks(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_user_todo_items(db, user_id, skip, limit)


@router.put("/{todo_id}", response_model=TodoItemResponse)
def update_task(todo_id: int, todo: TodoItemUpdate, db: Session = Depends(get_db)):
    updated_task = update_todo_item(db, todo_id, todo)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{todo_id}")
def delete_task(todo_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_todo_item(db, todo_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
