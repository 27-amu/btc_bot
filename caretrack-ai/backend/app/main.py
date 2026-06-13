"""
CareTrack AI - Longitudinal Patient Monitoring System

DISCLAIMER: This is a demonstration system using synthetic data only.
It is NOT a certified medical device and must NOT be used for real patient care.
Do not input real PHI (Protected Health Information) into this system.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import engine, Base
from .routers import patients, visits, labs, vitals, medications, allergies, reminders, risk, summary

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareTrack AI",
    description=(
        "Longitudinal patient monitoring and risk-alert system. "
        "**DEMO ONLY** — uses synthetic data. Not a certified medical device."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = settings.api_prefix
app.include_router(patients.router, prefix=prefix)
app.include_router(visits.router, prefix=prefix)
app.include_router(labs.router, prefix=prefix)
app.include_router(vitals.router, prefix=prefix)
app.include_router(medications.router, prefix=prefix)
app.include_router(allergies.router, prefix=prefix)
app.include_router(reminders.router, prefix=prefix)
app.include_router(risk.router, prefix=prefix)
app.include_router(summary.router, prefix=prefix)


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "service": "CareTrack AI", "version": "1.0.0"}


@app.get("/", tags=["system"])
def root():
    return {
        "message": "CareTrack AI API",
        "docs": "/docs",
        "health": "/health",
        "disclaimer": "Demo system with synthetic data only. Not for clinical use.",
    }
