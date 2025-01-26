from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import TIME_ZONE
from ..crud.user_crud import get_current_user
from ..models import TodoItem
from ..models.user import User
from ..schemas.todo_schemas import TodoItemCreate, TodoItemUpdate

active_pomodoros = {}


def create_todo_item(db: Session, todo_data: TodoItemCreate, current_user: User = Depends(get_current_user)):
    db_todo = TodoItem(user_id=current_user.id, **todo_data.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo_item(db: Session, todo_id: int):
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()


def get_user_todo_items(db: Session, current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 10):
    return db.query(TodoItem).filter(TodoItem.user_id == current_user.id).offset(skip).limit(limit).all()


def update_todo_item(db: Session, todo_id: int, todo_data: TodoItemUpdate,
                     current_user: User = Depends(get_current_user)):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()
    if not db_todo:
        return None
    for key, value in todo_data.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo_item(db: Session, todo_id: int, current_user: User = Depends(get_current_user)):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo


def start_pomodoro(db: Session, todo_id: int, current_user: User = Depends(get_current_user)):
    todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.id in active_pomodoros:
        raise HTTPException(status_code=400, detail="Pomodoro already active for this task")

    active_pomodoros[todo_id] = {
        "start_time": datetime.now(TIME_ZONE),
    }
    return {"message": "Pomodoro started"}


def pause_pomodoro(db: Session, todo_id: int, current_user: User = Depends(get_current_user)):
    if todo_id not in active_pomodoros:
        raise HTTPException(status_code=400, detail="No active pomodoro session for this task")

    session = active_pomodoros.pop(todo_id)
    elapsed_time = (datetime.now(TIME_ZONE) - session["start_time"]).total_seconds()

    todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.total_time_spent is None:
        todo.total_time_spent = 0

    todo.total_time_spent += int(elapsed_time)
    db.commit()
    db.refresh(todo)
    return {"message": "Pomodoro paused", "elapsed_time": elapsed_time}


def finish_pomodoro(db: Session, todo_id: int, current_user: User = Depends(get_current_user)):
    if todo_id not in active_pomodoros:
        raise HTTPException(status_code=400, detail="No active pomodoro session for this task")

    session = active_pomodoros.pop(todo_id)
    elapsed_time = (datetime.now(TIME_ZONE) - session["start_time"]).total_seconds()

    todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.total_time_spent is None:
        todo.total_time_spent = 0

    todo.total_time_spent += int(elapsed_time)
    todo.pomodoro_sessions += 1
    current_user.pomodoro_sessions += 1
    db.commit()
    db.refresh(todo)
    return {"message": "Pomodoro finished", "elapsed_time": elapsed_time, "total_pomodoros": todo.pomodoro_sessions}
