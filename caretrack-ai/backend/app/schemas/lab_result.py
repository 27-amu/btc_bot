from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class LabResultBase(BaseModel):
    test_name: str = Field(..., min_length=1, max_length=150)
    test_date: date
    value: float
    unit: Optional[str] = None
    reference_min: Optional[float] = None
    reference_max: Optional[float] = None
    is_abnormal: bool = False
    notes: Optional[str] = None
    ordered_by: Optional[str] = None


class LabResultCreate(LabResultBase):
    patient_id: int


class LabResultOut(LabResultBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
