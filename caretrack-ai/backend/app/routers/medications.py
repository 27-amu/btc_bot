from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Medication, Patient
from ..schemas import MedicationCreate, MedicationUpdate, MedicationOut

router = APIRouter(prefix="/medications", tags=["medications"])


@router.get("/patient/{patient_id}", response_model=List[MedicationOut])
def get_patient_medications(
    patient_id: int,
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    query = db.query(Medication).filter(Medication.patient_id == patient_id)
    if active_only:
        query = query.filter(Medication.is_active == True)
    return query.order_by(Medication.start_date.desc()).all()


@router.post("/", response_model=MedicationOut, status_code=201)
def create_medication(med: MedicationCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == med.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_med = Medication(**med.model_dump())
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med


@router.patch("/{med_id}", response_model=MedicationOut)
def update_medication(med_id: int, update: MedicationUpdate, db: Session = Depends(get_db)):
    med = db.query(Medication).filter(Medication.id == med_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    for field, value in update.model_dump(exclude_none=True).items():
        setattr(med, field, value)
    db.commit()
    db.refresh(med)
    return med


@router.delete("/{med_id}", status_code=204)
def delete_medication(med_id: int, db: Session = Depends(get_db)):
    med = db.query(Medication).filter(Medication.id == med_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    db.delete(med)
    db.commit()
