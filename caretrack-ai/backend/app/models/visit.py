from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_date = Column(Date, nullable=False)
    visit_type = Column(String(50), nullable=False)  # routine, urgent, follow-up
    chief_complaint = Column(Text)
    diagnosis = Column(Text)
    notes = Column(Text)
    physician = Column(String(150))
    facility = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="visits")
