from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ReminderBase(BaseModel):
    reminder_type: str
    due_date: date
    description: Optional[str] = None
    priority: str = "medium"
    assigned_to: Optional[str] = None


class ReminderCreate(ReminderBase):
    patient_id: int


class ReminderUpdate(BaseModel):
    due_date: Optional[date] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    priority: Optional[str] = None


class ReminderOut(ReminderBase):
    id: int
    patient_id: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
