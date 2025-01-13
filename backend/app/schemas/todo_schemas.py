from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class TodoItemBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    status: str = Field(default="Pending", max_length=20)
    priority: Optional[str] = None
    due_date: Optional[date] = None
    collaborators: List[int] = None
    pomodoro_sessions: int = 0


class TodoItemCreate(TodoItemBase):
    pass


class TodoItemUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=20)
    priority: Optional[str] = None
    due_date: Optional[date] = None
    collaborators: Optional[List[int]] = None
    pomodoro_sessions: Optional[int] = None


class TodoItemResponse(TodoItemBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
