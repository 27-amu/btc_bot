from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Visit, Patient
from ..schemas import VisitCreate, VisitUpdate, VisitOut

router = APIRouter(prefix="/visits", tags=["visits"])


@router.get("/patient/{patient_id}", response_model=List[VisitOut])
def get_patient_visits(
    patient_id: int,
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    query = db.query(Visit).filter(Visit.patient_id == patient_id)
    if year:
        query = query.filter(Visit.visit_date >= f"{year}-01-01", Visit.visit_date <= f"{year}-12-31")
    return query.order_by(Visit.visit_date.desc()).all()


@router.get("/{visit_id}", response_model=VisitOut)
def get_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.post("/", response_model=VisitOut, status_code=201)
def create_visit(visit: VisitCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == visit.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_visit = Visit(**visit.model_dump())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit


@router.patch("/{visit_id}", response_model=VisitOut)
def update_visit(visit_id: int, update: VisitUpdate, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    for field, value in update.model_dump(exclude_none=True).items():
        setattr(visit, field, value)
    db.commit()
    db.refresh(visit)
    return visit
