from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    reminder_type = Column(String(100), nullable=False)  # follow-up, lab, medication, screening
    due_date = Column(Date, nullable=False)
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    priority = Column(String(20), default="medium")  # low, medium, high
    assigned_to = Column(String(150))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="reminders")
