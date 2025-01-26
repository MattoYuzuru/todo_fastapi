from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud.todo_crud import (create_todo_item,
                              get_todo_item,
                              get_user_todo_items,
                              update_todo_item,
                              delete_todo_item)
from ..crud.user_crud import get_current_user
from ..db.session import get_db
from ..models.user import User
from ..schemas.todo_schemas import TodoItemCreate, TodoItemUpdate, TodoItemResponse

router = APIRouter()


@router.post("/", response_model=TodoItemResponse)
def create_task(todo: TodoItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_todo_item(db, todo, current_user)


@router.get("/{todo_id}", response_model=TodoItemResponse)
def read_task(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = get_todo_item(db, todo_id)
    if not task or task.used_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=list[TodoItemResponse])
def read_user_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_todo_items(db, current_user, skip, limit)


@router.put("/{todo_id}", response_model=TodoItemResponse)
def update_task(todo_id: int, todo: TodoItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_task = update_todo_item(db, todo_id, todo, current_user)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{todo_id}")
def delete_task(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_task = delete_todo_item(db, todo_id, current_user)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
