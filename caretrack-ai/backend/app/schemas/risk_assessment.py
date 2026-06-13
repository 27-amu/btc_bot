from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class RiskAssessmentOut(BaseModel):
    id: int
    patient_id: int
    assessed_at: datetime
    risk_score: float
    risk_level: str
    reasons: List[str]
    recommended_actions: List[str]
    assessed_by: str

    class Config:
        from_attributes = True


class RiskAssessmentRequest(BaseModel):
    patient_id: int
    save: bool = True
