from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Allergy(Base):
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    allergen = Column(String(200), nullable=False)
    allergen_type = Column(String(50))  # drug, food, environmental
    reaction = Column(String(300))
    severity = Column(String(50))  # mild, moderate, severe, life-threatening
    onset_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="allergies")
