from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    assessed_at = Column(DateTime(timezone=True), server_default=func.now())
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)  # low, medium, high
    reasons = Column(JSON)  # list of reason strings
    recommended_actions = Column(JSON)  # list of action strings
    assessed_by = Column(String(50), default="system")  # system or physician name

    patient = relationship("Patient", back_populates="risk_assessments")
