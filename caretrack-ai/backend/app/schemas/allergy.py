from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AllergyBase(BaseModel):
    allergen: str
    allergen_type: Optional[str] = None
    reaction: Optional[str] = None
    severity: Optional[str] = None
    onset_date: Optional[datetime] = None
    notes: Optional[str] = None


class AllergyCreate(AllergyBase):
    patient_id: int


class AllergyOut(AllergyBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
