from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    current_streak: int = 0
    longest_streak: int = 0
    last_activity_date: Optional[date] = None
    pomodoro_sessions: int = 0
    tasks_completed: int = 0


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)


class UserStats(BaseModel):
    current_streak: int
    longest_streak: int
    pomodoro_sessions: int
    tasks_completed: int


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
