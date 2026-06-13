"""
Template-based patient summary generator.

To integrate an LLM (e.g., Claude or GPT), replace the `_generate_with_llm` stub
below with an actual API call and set USE_LLM=true in your environment.
The structured `context` dict passed to the stub contains all patient data
already assembled — feed it as a prompt or structured message to the LLM.
"""

import os
from datetime import date
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from ..models import Patient, Visit, LabResult, Vital, Medication, Allergy, Reminder, RiskAssessment
from .risk_engine import compute_risk


USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"


def _calculate_age(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def _format_bp(vital: Vital) -> str:
    if vital.systolic_bp and vital.diastolic_bp:
        return f"{int(vital.systolic_bp)}/{int(vital.diastolic_bp)} mmHg"
    return "N/A"


def _generate_with_llm(context: Dict[str, Any]) -> Optional[str]:
    """
    PLACEHOLDER: Replace this function body with an LLM API call.

    Example using Anthropic Claude:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        message = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            messages=[{"role": "user", "content": build_prompt(context)}]
        )
        return message.content[0].text

    The `context` dict contains:
        - patient_name, age, gender, primary_diagnosis
        - recent_vitals (list of dicts)
        - recent_labs (list of dicts)
        - active_medications (list)
        - allergies (list)
        - risk_level, risk_score, risk_reasons
        - pending_reminders (list)
        - recent_visits (list)
    """
    return None  # Return None to fall through to template-based generation


def generate_patient_summary(patient_id: int, db: Session) -> Dict[str, Any]:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return None

    today = date.today()

    visits = (
        db.query(Visit)
        .filter(Visit.patient_id == patient_id)
        .order_by(Visit.visit_date.desc())
        .all()
    )

    labs = (
        db.query(LabResult)
        .filter(LabResult.patient_id == patient_id)
        .order_by(LabResult.test_date.desc())
        .limit(20)
        .all()
    )

    vitals = (
        db.query(Vital)
        .filter(Vital.patient_id == patient_id)
        .order_by(Vital.recorded_date.desc())
        .limit(10)
        .all()
    )

    medications = (
        db.query(Medication)
        .filter(Medication.patient_id == patient_id, Medication.is_active == True)
        .all()
    )

    allergies = db.query(Allergy).filter(Allergy.patient_id == patient_id).all()

    reminders = (
        db.query(Reminder)
        .filter(Reminder.patient_id == patient_id, Reminder.is_completed == False)
        .order_by(Reminder.due_date)
        .all()
    )

    risk = compute_risk(patient_id, db)

    # Build context for optional LLM call
    latest_vital = vitals[0] if vitals else None
    context = {
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "age": _calculate_age(patient.date_of_birth),
        "gender": patient.gender,
        "primary_diagnosis": patient.primary_diagnosis,
        "recent_vitals": [
            {
                "date": str(v.recorded_date),
                "bp": _format_bp(v),
                "hr": v.heart_rate,
                "weight_kg": v.weight_kg,
                "bmi": v.bmi,
                "o2_sat": v.oxygen_saturation,
            }
            for v in vitals[:3]
        ],
        "recent_labs": [
            {
                "test": l.test_name,
                "date": str(l.test_date),
                "value": l.value,
                "unit": l.unit,
                "abnormal": l.is_abnormal,
            }
            for l in labs[:10]
        ],
        "active_medications": [
            f"{m.name} {m.dosage or ''} {m.frequency or ''}".strip()
            for m in medications
        ],
        "allergies": [
            f"{a.allergen} ({a.severity or 'unknown severity'}) - {a.reaction or 'reaction not documented'}"
            for a in allergies
        ],
        "risk_level": risk["risk_level"] if risk else "unknown",
        "risk_score": risk["risk_score"] if risk else 0,
        "risk_reasons": risk["reasons"] if risk else [],
        "pending_reminders": [
            {"type": r.reminder_type, "due": str(r.due_date), "description": r.description}
            for r in reminders
        ],
        "recent_visits": [
            {"date": str(v.visit_date), "type": v.visit_type, "diagnosis": v.diagnosis}
            for v in visits[:5]
        ],
    }

    # Try LLM-based generation first
    if USE_LLM:
        llm_text = _generate_with_llm(context)
        if llm_text:
            return {
                "patient_id": patient_id,
                "generated_at": str(today),
                "source": "llm",
                "summary_text": llm_text,
                "structured": context,
            }

    # Template-based summary
    age = context["age"]
    name = context["patient_name"]
    diagnosis = patient.primary_diagnosis or "not documented"
    physician = patient.primary_physician or "not assigned"

    overview = (
        f"{name} is a {age}-year-old {patient.gender.lower()} patient "
        f"with a primary diagnosis of {diagnosis}, under the care of {physician}."
    )

    vitals_summary = "No recent vitals on record."
    if latest_vital:
        vitals_summary = (
            f"Most recent vitals ({latest_vital.recorded_date}): "
            f"BP {_format_bp(latest_vital)}, "
            f"HR {latest_vital.heart_rate or 'N/A'} bpm, "
            f"Weight {latest_vital.weight_kg or 'N/A'} kg, "
            f"BMI {latest_vital.bmi or 'N/A'}, "
            f"O2 Sat {latest_vital.oxygen_saturation or 'N/A'}%."
        )

    abnormal_labs = [l for l in labs if l.is_abnormal]
    lab_summary = (
        f"Latest labs include {len(labs)} results; {len(abnormal_labs)} flagged as abnormal."
        if labs
        else "No lab results on record."
    )

    med_summary = (
        f"Currently on {len(medications)} active medication(s): "
        + (", ".join(m.name for m in medications[:5]) + ("..." if len(medications) > 5 else ""))
        if medications
        else "No active medications documented."
    )

    allergy_summary = (
        f"Documented allergies: " + "; ".join(a.allergen for a in allergies)
        if allergies
        else "No known allergies documented."
    )

    risk_summary = (
        f"Risk assessment: {risk['risk_level'].upper()} risk (score {risk['risk_score']}/100). "
        f"Key concerns: {'; '.join(risk['reasons'][:3])}."
        if risk
        else "Risk assessment not available."
    )

    followup_summary = (
        f"{len(reminders)} follow-up action(s) pending. "
        f"Next due: {reminders[0].reminder_type} on {reminders[0].due_date}."
        if reminders
        else "No pending follow-ups."
    )

    visit_summary = (
        f"Total of {len(visits)} visits on record. "
        f"Most recent: {visits[0].visit_type} visit on {visits[0].visit_date}."
        if visits
        else "No visits on record."
    )

    suggested_actions = risk["recommended_actions"] if risk else ["Continue routine monitoring"]

    return {
        "patient_id": patient_id,
        "generated_at": str(today),
        "source": "template",
        "summary": {
            "overview": overview,
            "key_diagnoses": [d.strip() for d in (patient.primary_diagnosis or "").split(",") if d.strip()],
            "latest_vitals": vitals_summary,
            "lab_trends": lab_summary,
            "medications": med_summary,
            "allergies": allergy_summary,
            "risk_alerts": risk_summary,
            "visit_history": visit_summary,
            "suggested_follow_up_actions": suggested_actions,
            "pending_follow_ups": followup_summary,
        },
        "structured": context,
    }
