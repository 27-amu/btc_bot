from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    name = Column(String(200), nullable=False)
    generic_name = Column(String(200))
    dosage = Column(String(100))
    frequency = Column(String(100))
    route = Column(String(50))  # oral, IV, topical, etc.
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    prescribed_by = Column(String(150))
    indication = Column(String(300))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="medications")
