from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, func, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from .base import Base


class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="Pending")
    priority = Column(String(10), nullable=True)
    due_date = Column(Date, nullable=True)
    collaborators = Column(ARRAY(Integer), default=[])
    completed_at = Column(TIMESTAMP, nullable=True)
    pomodoro_sessions = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="todos")
