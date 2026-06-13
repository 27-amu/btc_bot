from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional


class PatientBase(BaseModel):
    mrn: str = Field(..., min_length=1, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: str = Field(..., pattern="^(Male|Female|Other|Unknown)$")
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    primary_diagnosis: Optional[str] = None
    primary_physician: Optional[str] = None
    insurance_id: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    primary_diagnosis: Optional[str] = None
    primary_physician: Optional[str] = None
    insurance_id: Optional[str] = None


class PatientOut(PatientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PatientList(BaseModel):
    id: int
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    primary_diagnosis: Optional[str] = None
    primary_physician: Optional[str] = None

    class Config:
        from_attributes = True
