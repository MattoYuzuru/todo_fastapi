import json
from datetime import datetime, timezone

import redis
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import TIME_ZONE, REDIS_HOST, REDIS_PORT
from ..crud.user_crud import get_current_user
from ..models import TodoItem
from ..models.user import User
from ..schemas.todo_schemas import TodoItemCreate, TodoItemUpdate

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)


def create_todo_item(db: Session, todo_data: TodoItemCreate, current_user: User = Depends(get_current_user)):
    db_todo = TodoItem(user_id=current_user.id, **todo_data.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo_item(db: Session, todo_id: int):
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()


def get_user_todo_items(db: Session, current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 10):
    all_todos = db.query(TodoItem).filter(TodoItem.user_id == current_user.id).offset(skip).limit(limit).all()
    return all_todos


def get_completed_tasks(db: Session, current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 10):
    completed_todos = db.query(TodoItem).filter(TodoItem.user_id == current_user.id,
                                                TodoItem.status == "Completed").offset(skip).limit(limit).all()
    return completed_todos


def update_todo_item(db: Session, todo_id: int, todo_data: TodoItemUpdate,
                     current_user: User = Depends(get_current_user)):
    todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()

    if not todo:
        return None

    for key, value in todo_data.model_dump(exclude_unset=True).items():
        setattr(todo, key, value)

    if todo.status == "Completed" and todo.completed_at is None:
        todo.completed_at = datetime.now(TIME_ZONE)

    db.commit()
    db.refresh(todo)
    return todo


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

    key = f"pomodoro:{current_user.id}:{todo_id}"
    session_data = redis_client.get(key)

    start_time = datetime.now(timezone.utc).isoformat()
    accumulated_time = 0

    if session_data:
        session = json.loads(session_data)
        accumulated_time = session.get("accumulated_time", 0)

    redis_client.set(key, json.dumps({"start_time": start_time, "accumulated_time": accumulated_time}), ex=60 * 120)

    return {"message": "Pomodoro started", "start_time": start_time, "accumulated_time": accumulated_time}


def pause_pomodoro(db: Session, todo_id: int, current_user: User = Depends(get_current_user)):
    key = f"pomodoro:{current_user.id}:{todo_id}"
    session_data = redis_client.get(key)
    if not session_data:
        raise HTTPException(status_code=400, detail="No active pomodoro session for this task")

    session = json.loads(session_data)
    elapsed_time = (datetime.now(timezone.utc) - datetime.fromisoformat(session["start_time"])).total_seconds()

    todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    accumulated_time = session.get("accumulated_time", 0) + elapsed_time

    redis_client.set(key, json.dumps({"accumulated_time": accumulated_time}), ex=60 * 120)

    db.commit()
    db.refresh(todo)
    return {"message": "Pomodoro paused", "elapsed_time": accumulated_time}


def finish_pomodoro(db: Session, todo_id: int, current_user: User = Depends(get_current_user)):
    key = f"pomodoro:{current_user.id}:{todo_id}"
    session_data = redis_client.get(key)
    if not session_data:
        raise HTTPException(status_code=400, detail="No active pomodoro session for this task")

    session = json.loads(session_data)
    elapsed_time = (datetime.now(timezone.utc) - datetime.fromisoformat(session["start_time"])).total_seconds()

    todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    accumulated_time = session.get("accumulated_time", 0) + elapsed_time

    todo.total_time_spent = (todo.total_time_spent or 0) + int(accumulated_time)
    todo.pomodoro_sessions += 1
    current_user.pomodoro_sessions += 1

    redis_client.delete(key)
    db.commit()
    db.refresh(todo)
    return {"message": "Pomodoro finished", "elapsed_time": accumulated_time, "total_pomodoros": todo.pomodoro_sessions}


def get_pomodoro(todo_id: int, current_user: User = Depends(get_current_user)):
    key = f"pomodoro:{current_user.id}:{todo_id}"
    session_data = redis_client.get(key)

    if not session_data:
        return {"elapsed_time": 0, "is_running": False, "accumulated_time": 0}

    session = json.loads(session_data)
    if "start_time" in session:
        elapsed_time = (datetime.now(timezone.utc) - datetime.fromisoformat(session["start_time"])).total_seconds()
        accumulated_time = session.get("accumulated_time", 0)
        return {"elapsed_time": int(accumulated_time + elapsed_time), "is_running": True,
                "accumulated_time": accumulated_time}
    else:
        return {"elapsed_time": session.get("accumulated_time", 0), "is_running": False,
                "accumulated_time": session.get("accumulated_time", 0)}


def mark_task_as_completed(db: Session, todo_id: int, current_user: User = Depends(get_current_user)):
    todo = db.query(TodoItem).filter(TodoItem.id == todo_id, TodoItem.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")

    if todo.completed_at:
        raise HTTPException(status_code=400, detail="Task is already completed")

    todo.status = "Completed"
    current_user.tasks_completed += 1
    todo.completed_at = datetime.now(TIME_ZONE)
    db.commit()
    db.refresh(todo)
    return todo
