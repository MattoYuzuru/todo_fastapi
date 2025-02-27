from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class TodoItemBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    status: str = Field(default="Pending", max_length=20)
    priority: Optional[str] = None
    due_date: Optional[date] = None
    collaborators: List[int] = None
    pomodoro_sessions: int = 0
    total_time_spent: int = 0
    current_streak: int = 0
    longest_streak: Optional[int] = 0
    last_activity_date: Optional[date] = None


class TodoItemCreate(TodoItemBase):
    pass


class TodoItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    collaborators: Optional[List[int]] = None
    pomodoro_sessions: Optional[int] = None
    total_time_spent: Optional[int] = None
    current_streak: Optional[int] = None
    longest_streak: Optional[int] = 0
    last_activity_date: Optional[date] = None


class TodoItemResponse(TodoItemBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TodoWithStreak(BaseModel):
    todo: TodoItemResponse
    current_streak: dict
