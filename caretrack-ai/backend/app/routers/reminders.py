from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..database import get_db
from ..models import Reminder, Patient
from ..schemas import ReminderCreate, ReminderUpdate, ReminderOut

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.get("/patient/{patient_id}", response_model=List[ReminderOut])
def get_patient_reminders(
    patient_id: int,
    pending_only: bool = False,
    overdue_only: bool = False,
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    query = db.query(Reminder).filter(Reminder.patient_id == patient_id)
    if pending_only:
        query = query.filter(Reminder.is_completed == False)
    if overdue_only:
        query = query.filter(Reminder.due_date < date.today(), Reminder.is_completed == False)
    return query.order_by(Reminder.due_date).all()


@router.post("/", response_model=ReminderOut, status_code=201)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == reminder.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_reminder = Reminder(**reminder.model_dump())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


@router.patch("/{reminder_id}", response_model=ReminderOut)
def update_reminder(reminder_id: int, update: ReminderUpdate, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    for field, value in update.model_dump(exclude_none=True).items():
        setattr(reminder, field, value)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.delete("/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    db.delete(reminder)
    db.commit()
