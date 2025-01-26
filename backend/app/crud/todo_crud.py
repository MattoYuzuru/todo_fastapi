from fastapi import Depends
from sqlalchemy.orm import Session

from ..crud.user_crud import get_current_user
from ..models import TodoItem
from ..models.user import User
from ..schemas.todo_schemas import TodoItemCreate, TodoItemUpdate


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
