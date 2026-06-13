from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Allergy, Patient
from ..schemas import AllergyCreate, AllergyOut

router = APIRouter(prefix="/allergies", tags=["allergies"])


@router.get("/patient/{patient_id}", response_model=List[AllergyOut])
def get_patient_allergies(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db.query(Allergy).filter(Allergy.patient_id == patient_id).all()


@router.post("/", response_model=AllergyOut, status_code=201)
def create_allergy(allergy: AllergyCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == allergy.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_allergy = Allergy(**allergy.model_dump())
    db.add(db_allergy)
    db.commit()
    db.refresh(db_allergy)
    return db_allergy


@router.delete("/{allergy_id}", status_code=204)
def delete_allergy(allergy_id: int, db: Session = Depends(get_db)):
    allergy = db.query(Allergy).filter(Allergy.id == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    db.delete(allergy)
    db.commit()
