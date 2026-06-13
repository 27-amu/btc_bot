from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    mrn = Column(String(20), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    phone = Column(String(20))
    email = Column(String(150))
    address = Column(Text)
    primary_diagnosis = Column(String(200))
    primary_physician = Column(String(150))
    insurance_id = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")
    lab_results = relationship("LabResult", back_populates="patient", cascade="all, delete-orphan")
    vitals = relationship("Vital", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    allergies = relationship("Allergy", back_populates="patient", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="patient", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="patient", cascade="all, delete-orphan")
