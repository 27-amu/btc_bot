from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import LabResult, Patient
from ..schemas import LabResultCreate, LabResultOut

router = APIRouter(prefix="/labs", tags=["labs"])


@router.get("/patient/{patient_id}", response_model=List[LabResultOut])
def get_patient_labs(
    patient_id: int,
    test_name: Optional[str] = Query(None),
    abnormal_only: bool = False,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    query = db.query(LabResult).filter(LabResult.patient_id == patient_id)
    if test_name:
        query = query.filter(LabResult.test_name.ilike(f"%{test_name}%"))
    if abnormal_only:
        query = query.filter(LabResult.is_abnormal == True)
    return query.order_by(LabResult.test_date.desc()).limit(limit).all()


@router.post("/", response_model=LabResultOut, status_code=201)
def create_lab(lab: LabResultCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == lab.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    # Auto-flag if outside reference range
    data = lab.model_dump()
    if data.get("reference_min") and data.get("reference_max"):
        data["is_abnormal"] = not (data["reference_min"] <= data["value"] <= data["reference_max"])
    db_lab = LabResult(**data)
    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)
    return db_lab


@router.delete("/{lab_id}", status_code=204)
def delete_lab(lab_id: int, db: Session = Depends(get_db)):
    lab = db.query(LabResult).filter(LabResult.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab result not found")
    db.delete(lab)
    db.commit()
