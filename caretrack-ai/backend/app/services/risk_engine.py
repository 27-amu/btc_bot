from datetime import date, timedelta
from typing import List, Tuple
from sqlalchemy.orm import Session
from ..models import Patient, LabResult, Vital, Medication, Allergy, Reminder, RiskAssessment


KNOWN_ALLERGY_CONFLICTS = {
    "penicillin": ["amoxicillin", "ampicillin", "augmentin"],
    "sulfa": ["sulfamethoxazole", "trimethoprim-sulfamethoxazole", "bactrim"],
    "aspirin": ["ibuprofen", "naproxen", "celecoxib"],
    "latex": [],
}

BP_HIGH_THRESHOLD = {"systolic": 140, "diastolic": 90}
BP_CRISIS_THRESHOLD = {"systolic": 180, "diastolic": 120}
HBBA1C_WORSENING_THRESHOLD = 7.5
HBBA1C_CRITICAL = 9.0
FOLLOWUP_OVERDUE_DAYS = 90
GFR_LOW = 60.0
CREATININE_HIGH = 1.3


def compute_risk(patient_id: int, db: Session) -> dict:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return None

    reasons: List[str] = []
    actions: List[str] = []
    score = 0.0

    labs = (
        db.query(LabResult)
        .filter(LabResult.patient_id == patient_id)
        .order_by(LabResult.test_date.desc())
        .all()
    )

    vitals = (
        db.query(Vital)
        .filter(Vital.patient_id == patient_id)
        .order_by(Vital.recorded_date.desc())
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
        .all()
    )

    # Rule 1: Missed follow-up
    today = date.today()
    overdue = [
        r for r in reminders
        if r.due_date < today and (today - r.due_date).days > FOLLOWUP_OVERDUE_DAYS
    ]
    if overdue:
        score += 20
        reasons.append(f"{len(overdue)} follow-up(s) overdue by more than 90 days")
        actions.append("Schedule urgent follow-up appointment")

    pending_near = [
        r for r in reminders
        if r.due_date < today and r.due_date >= today - timedelta(days=FOLLOWUP_OVERDUE_DAYS)
    ]
    if pending_near:
        score += 10
        reasons.append(f"{len(pending_near)} follow-up(s) pending")
        actions.append("Review and complete pending reminders")

    # Rule 2: Worsening HbA1c
    hba1c_results = sorted(
        [l for l in labs if "hba1c" in l.test_name.lower() or "hemoglobin a1c" in l.test_name.lower()],
        key=lambda x: x.test_date,
    )
    if hba1c_results:
        latest_hba1c = hba1c_results[-1].value
        if latest_hba1c >= HBBA1C_CRITICAL:
            score += 30
            reasons.append(f"Critical HbA1c: {latest_hba1c}% (>=9.0%)")
            actions.append("Immediate diabetes management review; consider endocrinology referral")
        elif latest_hba1c >= HBBA1C_WORSENING_THRESHOLD:
            score += 15
            reasons.append(f"Elevated HbA1c: {latest_hba1c}%")
            actions.append("Review diabetes medication and dietary compliance")
        if len(hba1c_results) >= 2:
            prev = hba1c_results[-2].value
            if latest_hba1c - prev >= 0.5:
                score += 10
                reasons.append(f"HbA1c worsening trend: {prev}% -> {latest_hba1c}%")
                actions.append("Evaluate treatment plan adjustments")

    # Rule 3: High blood pressure trend
    recent_vitals = vitals[:6]
    high_bp_count = sum(
        1 for v in recent_vitals
        if v.systolic_bp and v.diastolic_bp
        and (v.systolic_bp >= BP_HIGH_THRESHOLD["systolic"] or v.diastolic_bp >= BP_HIGH_THRESHOLD["diastolic"])
    )
    crisis_bp = any(
        v for v in recent_vitals
        if v.systolic_bp and v.diastolic_bp
        and (v.systolic_bp >= BP_CRISIS_THRESHOLD["systolic"] or v.diastolic_bp >= BP_CRISIS_THRESHOLD["diastolic"])
    )
    if crisis_bp:
        score += 35
        reasons.append("Hypertensive crisis level blood pressure recorded")
        actions.append("Immediate blood pressure management; consider emergency evaluation")
    elif high_bp_count >= 3:
        score += 20
        reasons.append(f"Persistently elevated BP in {high_bp_count} of last 6 readings")
        actions.append("Intensify antihypertensive therapy and lifestyle counseling")
    elif high_bp_count >= 1:
        score += 8
        reasons.append("Elevated blood pressure noted in recent readings")
        actions.append("Monitor blood pressure; review current antihypertensive regimen")

    # Rule 4: Abnormal kidney markers
    creatinine_results = sorted(
        [l for l in labs if "creatinine" in l.test_name.lower()],
        key=lambda x: x.test_date,
    )
    gfr_results = sorted(
        [l for l in labs if "gfr" in l.test_name.lower() or "egfr" in l.test_name.lower()],
        key=lambda x: x.test_date,
    )
    if creatinine_results:
        latest_cr = creatinine_results[-1].value
        if latest_cr > CREATININE_HIGH:
            score += 20
            reasons.append(f"Elevated creatinine: {latest_cr} mg/dL")
            actions.append("Nephrology referral; review nephrotoxic medications")
    if gfr_results:
        latest_gfr = gfr_results[-1].value
        if latest_gfr < GFR_LOW:
            score += 25
            reasons.append(f"Low eGFR: {latest_gfr} mL/min/1.73m² (CKD indicator)")
            actions.append("Nephrology consult; adjust renally-cleared medications")

    # Rule 5: Medication-allergy conflict
    allergy_names = {a.allergen.lower() for a in allergies}
    med_names = {m.name.lower() for m in medications}
    med_generic = {m.generic_name.lower() for m in medications if m.generic_name}
    all_med_names = med_names | med_generic

    for allergen, cross_reactive in KNOWN_ALLERGY_CONFLICTS.items():
        if allergen in allergy_names:
            conflicts = [m for m in all_med_names if allergen in m or any(cr in m for cr in cross_reactive)]
            if conflicts:
                score += 40
                reasons.append(f"Allergy conflict: patient allergic to {allergen} but prescribed {', '.join(conflicts)}")
                actions.append(f"URGENT: Review and discontinue contraindicated medications for {allergen} allergy")

    # Rule 6: Multiple abnormal labs
    abnormal_labs = [l for l in labs if l.is_abnormal]
    recent_abnormal = [l for l in abnormal_labs if (today - l.test_date).days <= 180]
    if len(recent_abnormal) >= 5:
        score += 20
        reasons.append(f"{len(recent_abnormal)} abnormal lab values in last 6 months")
        actions.append("Comprehensive metabolic panel review; consider specialist referral")
    elif len(recent_abnormal) >= 3:
        score += 10
        reasons.append(f"{len(recent_abnormal)} abnormal lab values in last 6 months")
        actions.append("Review abnormal lab trends and adjust treatment plan")

    # Normalize score to 0-100
    score = min(score, 100.0)

    if score >= 60:
        risk_level = "high"
    elif score >= 30:
        risk_level = "medium"
    else:
        risk_level = "low"

    if not reasons:
        reasons.append("No significant risk factors identified")
        actions.append("Continue routine monitoring and preventive care")

    return {
        "patient_id": patient_id,
        "risk_score": round(score, 1),
        "risk_level": risk_level,
        "reasons": reasons,
        "recommended_actions": actions,
        "assessed_by": "system",
    }


def save_risk_assessment(patient_id: int, db: Session) -> RiskAssessment:
    result = compute_risk(patient_id, db)
    if not result:
        return None
    assessment = RiskAssessment(**result)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment
