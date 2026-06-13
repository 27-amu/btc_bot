from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Vital, Patient
from ..schemas import VitalCreate, VitalOut

router = APIRouter(prefix="/vitals", tags=["vitals"])


@router.get("/patient/{patient_id}", response_model=List[VitalOut])
def get_patient_vitals(
    patient_id: int,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return (
        db.query(Vital)
        .filter(Vital.patient_id == patient_id)
        .order_by(Vital.recorded_date.desc())
        .limit(limit)
        .all()
    )


@router.post("/", response_model=VitalOut, status_code=201)
def create_vital(vital: VitalCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == vital.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    data = vital.model_dump()
    # Auto-compute BMI if weight and height provided
    if data.get("weight_kg") and data.get("height_cm") and not data.get("bmi"):
        h_m = data["height_cm"] / 100
        data["bmi"] = round(data["weight_kg"] / (h_m ** 2), 1)
    db_vital = Vital(**data)
    db.add(db_vital)
    db.commit()
    db.refresh(db_vital)
    return db_vital
