from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class VitalBase(BaseModel):
    recorded_date: date
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    heart_rate: Optional[float] = None
    temperature: Optional[float] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    bmi: Optional[float] = None
    oxygen_saturation: Optional[float] = None
    respiratory_rate: Optional[float] = None
    recorded_by: Optional[str] = None


class VitalCreate(VitalBase):
    patient_id: int


class VitalOut(VitalBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
