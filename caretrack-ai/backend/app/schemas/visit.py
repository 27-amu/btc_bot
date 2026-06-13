from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class VisitBase(BaseModel):
    visit_date: date
    visit_type: str = Field(..., pattern="^(routine|urgent|follow-up|emergency|telehealth)$")
    chief_complaint: Optional[str] = None
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    physician: Optional[str] = None
    facility: Optional[str] = None


class VisitCreate(VisitBase):
    patient_id: int


class VisitUpdate(BaseModel):
    visit_type: Optional[str] = None
    chief_complaint: Optional[str] = None
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    physician: Optional[str] = None


class VisitOut(VisitBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
