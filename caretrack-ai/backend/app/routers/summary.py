from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Patient
from ..services.summary_generator import generate_patient_summary

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/patient/{patient_id}")
def get_patient_summary(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    summary = generate_patient_summary(patient_id, db)
    if not summary:
        raise HTTPException(status_code=500, detail="Failed to generate summary")
    return summary
