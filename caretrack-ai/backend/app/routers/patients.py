from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Patient
from ..schemas import PatientCreate, PatientUpdate, PatientOut, PatientList

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/", response_model=List[PatientList])
def list_patients(
    search: Optional[str] = Query(None, description="Search by name, MRN, or diagnosis"),
    physician: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Patient)
    if search:
        term = f"%{search}%"
        query = query.filter(
            Patient.first_name.ilike(term)
            | Patient.last_name.ilike(term)
            | Patient.mrn.ilike(term)
            | Patient.primary_diagnosis.ilike(term)
        )
    if physician:
        query = query.filter(Patient.primary_physician.ilike(f"%{physician}%"))
    return query.offset(skip).limit(limit).all()


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", response_model=PatientOut, status_code=201)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    existing = db.query(Patient).filter(Patient.mrn == patient.mrn).first()
    if existing:
        raise HTTPException(status_code=409, detail="Patient with this MRN already exists")
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.patch("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, update: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for field, value in update.model_dump(exclude_none=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
