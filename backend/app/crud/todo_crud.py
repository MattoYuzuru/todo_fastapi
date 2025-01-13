from sqlalchemy.orm import Session

from ..models import TodoItem
from ..schemas.todo_schemas import TodoItemCreate, TodoItemUpdate


def create_todo_item(db: Session, user_id: int, todo_data: TodoItemCreate):
    db_todo = TodoItem(user_id=user_id, **todo_data.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo_item(db: Session, todo_id: int):
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()


def get_user_todo_items(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(TodoItem).filter(TodoItem.user_id == user_id).offset(skip).limit(limit).all()


def update_todo_item(db: Session, todo_id: int, todo_data: TodoItemUpdate):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not db_todo:
        return None
    for key, value in todo_data.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo_item(db: Session, todo_id: int):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
