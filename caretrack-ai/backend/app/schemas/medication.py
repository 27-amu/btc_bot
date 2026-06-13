from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class MedicationBase(BaseModel):
    name: str
    generic_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True
    prescribed_by: Optional[str] = None
    indication: Optional[str] = None


class MedicationCreate(MedicationBase):
    patient_id: int


class MedicationUpdate(BaseModel):
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None
    indication: Optional[str] = None


class MedicationOut(MedicationBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
