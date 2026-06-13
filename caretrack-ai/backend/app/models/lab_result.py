from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class LabResult(Base):
    __tablename__ = "lab_results"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    test_name = Column(String(150), nullable=False)
    test_date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50))
    reference_min = Column(Float)
    reference_max = Column(Float)
    is_abnormal = Column(Boolean, default=False)
    notes = Column(String(500))
    ordered_by = Column(String(150))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="lab_results")
