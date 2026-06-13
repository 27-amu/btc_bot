from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Vital(Base):
    __tablename__ = "vitals"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    recorded_date = Column(Date, nullable=False)
    systolic_bp = Column(Float)
    diastolic_bp = Column(Float)
    heart_rate = Column(Float)
    temperature = Column(Float)
    weight_kg = Column(Float)
    height_cm = Column(Float)
    bmi = Column(Float)
    oxygen_saturation = Column(Float)
    respiratory_rate = Column(Float)
    recorded_by = Column(String(150))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="vitals")
