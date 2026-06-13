from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Patient, RiskAssessment
from ..schemas import RiskAssessmentOut
from ..services.risk_engine import compute_risk, save_risk_assessment

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/patient/{patient_id}/latest", response_model=RiskAssessmentOut)
def get_latest_risk(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    assessment = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.patient_id == patient_id)
        .order_by(RiskAssessment.assessed_at.desc())
        .first()
    )
    if not assessment:
        raise HTTPException(status_code=404, detail="No risk assessment found; call POST to generate one")
    return assessment


@router.get("/patient/{patient_id}/history", response_model=List[RiskAssessmentOut])
def get_risk_history(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return (
        db.query(RiskAssessment)
        .filter(RiskAssessment.patient_id == patient_id)
        .order_by(RiskAssessment.assessed_at.desc())
        .all()
    )


@router.post("/patient/{patient_id}/assess", response_model=RiskAssessmentOut, status_code=201)
def run_risk_assessment(patient_id: int, save: bool = True, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if save:
        assessment = save_risk_assessment(patient_id, db)
        return assessment
    else:
        result = compute_risk(patient_id, db)
        return {**result, "id": 0, "assessed_at": __import__("datetime").datetime.utcnow()}
