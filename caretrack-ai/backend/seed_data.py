"""
Seed script for CareTrack AI demo data.
All data is completely synthetic — no real patient information.
"""

import sys
import os
import random
from datetime import date, timedelta, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import (
    Patient, Visit, LabResult, Vital,
    Medication, Allergy, Reminder, RiskAssessment
)
from app.services.risk_engine import compute_risk

Base.metadata.create_all(bind=engine)

random.seed(42)

PHYSICIANS = [
    "Dr. Sarah Chen", "Dr. Michael Torres", "Dr. Priya Patel",
    "Dr. James Okafor", "Dr. Emily Nguyen",
]

FACILITIES = [
    "City General Hospital", "Metro Health Clinic",
    "Riverside Medical Center", "Lakeside Family Practice",
]

PATIENTS_DATA = [
    {
        "mrn": "CT-000001", "first_name": "Robert", "last_name": "Hargrove",
        "date_of_birth": date(1958, 3, 12), "gender": "Male",
        "phone": "555-0101", "email": "r.hargrove@demo.test",
        "address": "123 Maple St, Springfield", "primary_diagnosis": "Type 2 Diabetes, Hypertension",
        "primary_physician": "Dr. Sarah Chen", "insurance_id": "INS-001-DEMO",
    },
    {
        "mrn": "CT-000002", "first_name": "Linda", "last_name": "Vasquez",
        "date_of_birth": date(1965, 7, 22), "gender": "Female",
        "phone": "555-0102", "email": "l.vasquez@demo.test",
        "address": "456 Oak Ave, Riverside", "primary_diagnosis": "Chronic Kidney Disease Stage 3, Hypertension",
        "primary_physician": "Dr. Michael Torres", "insurance_id": "INS-002-DEMO",
    },
    {
        "mrn": "CT-000003", "first_name": "James", "last_name": "Whitfield",
        "date_of_birth": date(1945, 11, 5), "gender": "Male",
        "phone": "555-0103", "email": "j.whitfield@demo.test",
        "address": "789 Pine Rd, Lakeside", "primary_diagnosis": "COPD, Heart Failure",
        "primary_physician": "Dr. Priya Patel", "insurance_id": "INS-003-DEMO",
    },
    {
        "mrn": "CT-000004", "first_name": "Maria", "last_name": "Delgado",
        "date_of_birth": date(1972, 4, 18), "gender": "Female",
        "phone": "555-0104", "email": "m.delgado@demo.test",
        "address": "321 Elm St, Metro City", "primary_diagnosis": "Rheumatoid Arthritis, Hypothyroidism",
        "primary_physician": "Dr. James Okafor", "insurance_id": "INS-004-DEMO",
    },
    {
        "mrn": "CT-000005", "first_name": "Kevin", "last_name": "Park",
        "date_of_birth": date(1980, 9, 30), "gender": "Male",
        "phone": "555-0105", "email": "k.park@demo.test",
        "address": "654 Birch Blvd, Northtown", "primary_diagnosis": "Asthma, Allergic Rhinitis",
        "primary_physician": "Dr. Emily Nguyen", "insurance_id": "INS-005-DEMO",
    },
    {
        "mrn": "CT-000006", "first_name": "Patricia", "last_name": "Morrison",
        "date_of_birth": date(1952, 1, 14), "gender": "Female",
        "phone": "555-0106", "email": "p.morrison@demo.test",
        "address": "987 Cedar Lane, Eastside", "primary_diagnosis": "Osteoporosis, Type 2 Diabetes",
        "primary_physician": "Dr. Sarah Chen", "insurance_id": "INS-006-DEMO",
    },
    {
        "mrn": "CT-000007", "first_name": "Thomas", "last_name": "Nakamura",
        "date_of_birth": date(1963, 6, 8), "gender": "Male",
        "phone": "555-0107", "email": "t.nakamura@demo.test",
        "address": "147 Spruce Way, Westfield", "primary_diagnosis": "Coronary Artery Disease, Hyperlipidemia",
        "primary_physician": "Dr. Michael Torres", "insurance_id": "INS-007-DEMO",
    },
    {
        "mrn": "CT-000008", "first_name": "Angela", "last_name": "Brown",
        "date_of_birth": date(1988, 12, 25), "gender": "Female",
        "phone": "555-0108", "email": "a.brown@demo.test",
        "address": "258 Willow Court, Southgate", "primary_diagnosis": "Major Depressive Disorder, Anxiety",
        "primary_physician": "Dr. Priya Patel", "insurance_id": "INS-008-DEMO",
    },
    {
        "mrn": "CT-000009", "first_name": "Carlos", "last_name": "Reyes",
        "date_of_birth": date(1970, 8, 3), "gender": "Male",
        "phone": "555-0109", "email": "c.reyes@demo.test",
        "address": "369 Poplar Dr, Highland", "primary_diagnosis": "Hepatitis C, Liver Fibrosis",
        "primary_physician": "Dr. James Okafor", "insurance_id": "INS-009-DEMO",
    },
    {
        "mrn": "CT-000010", "first_name": "Susan", "last_name": "Fletcher",
        "date_of_birth": date(1957, 5, 19), "gender": "Female",
        "phone": "555-0110", "email": "s.fletcher@demo.test",
        "address": "741 Ash Street, Midvale", "primary_diagnosis": "Breast Cancer (remission), Osteoarthritis",
        "primary_physician": "Dr. Emily Nguyen", "insurance_id": "INS-010-DEMO",
    },
]

MEDICATIONS_DATA = {
    "CT-000001": [
        ("Metformin", "metformin hcl", "500mg", "twice daily", "oral", True, "Type 2 Diabetes"),
        ("Lisinopril", "lisinopril", "10mg", "once daily", "oral", True, "Hypertension"),
        ("Atorvastatin", "atorvastatin", "20mg", "once at bedtime", "oral", True, "Hyperlipidemia"),
        ("Aspirin", "aspirin", "81mg", "once daily", "oral", True, "Cardiovascular prevention"),
    ],
    "CT-000002": [
        ("Amlodipine", "amlodipine", "5mg", "once daily", "oral", True, "Hypertension"),
        ("Furosemide", "furosemide", "40mg", "once daily", "oral", True, "Edema"),
        ("Sodium Bicarbonate", "sodium bicarbonate", "650mg", "twice daily", "oral", True, "CKD acidosis"),
        ("Erythropoietin", "epoetin alfa", "4000 units", "3x weekly", "subcutaneous", True, "CKD anemia"),
    ],
    "CT-000003": [
        ("Tiotropium", "tiotropium bromide", "18mcg", "once daily", "inhaled", True, "COPD"),
        ("Albuterol", "albuterol sulfate", "90mcg", "as needed", "inhaled", True, "COPD/Asthma"),
        ("Carvedilol", "carvedilol", "6.25mg", "twice daily", "oral", True, "Heart Failure"),
        ("Spironolactone", "spironolactone", "25mg", "once daily", "oral", True, "Heart Failure"),
        ("Enalapril", "enalapril maleate", "10mg", "twice daily", "oral", True, "Heart Failure"),
    ],
    "CT-000004": [
        ("Methotrexate", "methotrexate", "15mg", "once weekly", "oral", True, "Rheumatoid Arthritis"),
        ("Folic Acid", "folic acid", "1mg", "once daily", "oral", True, "Methotrexate supplement"),
        ("Levothyroxine", "levothyroxine sodium", "75mcg", "once daily", "oral", True, "Hypothyroidism"),
        ("Prednisone", "prednisone", "5mg", "once daily", "oral", False, "RA flare (completed)"),
    ],
    "CT-000005": [
        ("Fluticasone", "fluticasone propionate", "110mcg", "twice daily", "inhaled", True, "Asthma"),
        ("Montelukast", "montelukast sodium", "10mg", "once daily", "oral", True, "Asthma/Allergic Rhinitis"),
        ("Cetirizine", "cetirizine hcl", "10mg", "once daily", "oral", True, "Allergic Rhinitis"),
        ("Albuterol", "albuterol sulfate", "90mcg", "as needed", "inhaled", True, "Asthma rescue"),
    ],
    "CT-000006": [
        ("Alendronate", "alendronate sodium", "70mg", "once weekly", "oral", True, "Osteoporosis"),
        ("Calcium Carbonate", "calcium carbonate", "1200mg", "twice daily", "oral", True, "Bone health"),
        ("Vitamin D3", "cholecalciferol", "2000 IU", "once daily", "oral", True, "Bone health"),
        ("Glipizide", "glipizide", "5mg", "once daily", "oral", True, "Type 2 Diabetes"),
        ("Metformin", "metformin hcl", "1000mg", "twice daily", "oral", True, "Type 2 Diabetes"),
    ],
    "CT-000007": [
        ("Atorvastatin", "atorvastatin", "80mg", "once at bedtime", "oral", True, "CAD/Hyperlipidemia"),
        ("Metoprolol", "metoprolol succinate", "50mg", "once daily", "oral", True, "CAD"),
        ("Clopidogrel", "clopidogrel bisulfate", "75mg", "once daily", "oral", True, "Antiplatelet"),
        ("Nitroglycerin", "nitroglycerin", "0.4mg", "as needed", "sublingual", True, "Angina rescue"),
        ("Aspirin", "aspirin", "81mg", "once daily", "oral", True, "Antiplatelet"),
    ],
    "CT-000008": [
        ("Sertraline", "sertraline hcl", "100mg", "once daily", "oral", True, "MDD"),
        ("Alprazolam", "alprazolam", "0.5mg", "as needed", "oral", True, "Anxiety"),
        ("Mirtazapine", "mirtazapine", "15mg", "once at bedtime", "oral", True, "MDD/Insomnia"),
    ],
    "CT-000009": [
        ("Sofosbuvir/Velpatasvir", "sofosbuvir/velpatasvir", "400/100mg", "once daily", "oral", False, "Hepatitis C (completed)"),
        ("Ribavirin", "ribavirin", "600mg", "twice daily", "oral", False, "Hepatitis C (completed)"),
        ("Propranolol", "propranolol hcl", "20mg", "twice daily", "oral", True, "Portal hypertension"),
        ("Lactulose", "lactulose", "30ml", "twice daily", "oral", True, "Hepatic encephalopathy prevention"),
    ],
    "CT-000010": [
        ("Anastrozole", "anastrozole", "1mg", "once daily", "oral", True, "Breast cancer (hormonal)"),
        ("Calcium Carbonate", "calcium carbonate", "600mg", "twice daily", "oral", True, "Bone health"),
        ("Naproxen", "naproxen sodium", "500mg", "as needed", "oral", True, "Osteoarthritis pain"),
        ("Omeprazole", "omeprazole", "20mg", "once daily", "oral", True, "GI protection"),
    ],
}

ALLERGIES_DATA = {
    "CT-000001": [("Penicillin", "drug", "Rash, hives", "moderate")],
    "CT-000002": [("Sulfa", "drug", "Stevens-Johnson syndrome", "severe"), ("Shellfish", "food", "Anaphylaxis", "life-threatening")],
    "CT-000003": [("Latex", "environmental", "Contact dermatitis", "mild")],
    "CT-000004": [("NSAIDs", "drug", "GI bleeding", "moderate")],
    "CT-000005": [("Peanuts", "food", "Anaphylaxis", "life-threatening"), ("Aspirin", "drug", "Bronchospasm", "severe")],
    "CT-000006": [("Codeine", "drug", "Nausea, vomiting, confusion", "moderate")],
    "CT-000007": [("Contrast dye", "drug", "Allergic reaction", "moderate")],
    "CT-000008": [("Penicillin", "drug", "Anaphylaxis", "life-threatening")],
    "CT-000009": [("Amoxicillin", "drug", "Rash", "mild")],
    "CT-000010": [("Sulfa", "drug", "Rash, photosensitivity", "mild"), ("Latex", "environmental", "Urticaria", "mild")],
}


def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def generate_visits(patient_id: int, mrn: str, physician: str, facility: str):
    visits = []
    start_2024 = date(2024, 1, 1)
    end_2024 = date(2024, 12, 31)
    start_2025 = date(2025, 1, 1)
    end_2025 = date(2025, 12, 31)

    visit_types = ["routine", "follow-up", "urgent", "telehealth"]
    diagnoses_map = {
        "CT-000001": "Type 2 Diabetes mellitus, uncontrolled; Essential Hypertension",
        "CT-000002": "CKD Stage 3; Hypertension, well-controlled",
        "CT-000003": "COPD exacerbation; Chronic Heart Failure, stable",
        "CT-000004": "Rheumatoid Arthritis, active; Hypothyroidism",
        "CT-000005": "Asthma, intermittent; Seasonal Allergic Rhinitis",
        "CT-000006": "Osteoporosis with low trauma fracture risk; T2DM",
        "CT-000007": "Stable Angina; Hyperlipidemia",
        "CT-000008": "Major Depressive Disorder, recurrent; Generalized Anxiety Disorder",
        "CT-000009": "Hepatitis C (SVR12 achieved); Liver Fibrosis F2",
        "CT-000010": "Breast Cancer Stage II (remission); Osteoarthritis, bilateral knees",
    }

    for _ in range(random.randint(4, 7)):
        visits.append({
            "patient_id": patient_id,
            "visit_date": random_date(start_2024, end_2024),
            "visit_type": random.choice(visit_types),
            "chief_complaint": random.choice(["Routine checkup", "Medication review", "Worsening symptoms", "Lab follow-up"]),
            "diagnosis": diagnoses_map.get(mrn, "Chronic condition management"),
            "notes": "Synthetic demo visit — not real clinical data.",
            "physician": physician,
            "facility": facility,
        })

    for _ in range(random.randint(3, 6)):
        visits.append({
            "patient_id": patient_id,
            "visit_date": random_date(start_2025, end_2025),
            "visit_type": random.choice(visit_types),
            "chief_complaint": random.choice(["Follow-up visit", "Symptom review", "Lab results discussion", "Medication adjustment"]),
            "diagnosis": diagnoses_map.get(mrn, "Chronic condition management"),
            "notes": "Synthetic demo visit — not real clinical data.",
            "physician": physician,
            "facility": facility,
        })

    return visits


def generate_labs(patient_id: int, mrn: str, physician: str):
    labs = []
    base_date = date(2024, 1, 15)

    # Common panels
    common_tests = [
        ("HbA1c", 4.0, 5.6, "%"),
        ("Fasting Glucose", 70, 99, "mg/dL"),
        ("Creatinine", 0.6, 1.2, "mg/dL"),
        ("eGFR", 60, 120, "mL/min/1.73m²"),
        ("Potassium", 3.5, 5.0, "mEq/L"),
        ("Sodium", 136, 145, "mEq/L"),
        ("ALT", 7, 56, "U/L"),
        ("AST", 10, 40, "U/L"),
        ("Total Cholesterol", 0, 200, "mg/dL"),
        ("LDL Cholesterol", 0, 100, "mg/dL"),
        ("HDL Cholesterol", 40, 60, "mg/dL"),
        ("Hemoglobin", 12.0, 17.5, "g/dL"),
    ]

    # Patient-specific overrides to create realistic abnormalities
    overrides = {
        "CT-000001": {"HbA1c": [(7.8, True), (8.1, True), (8.5, True)], "Fasting Glucose": [(165, True), (178, True)]},
        "CT-000002": {"Creatinine": [(1.6, True), (1.7, True)], "eGFR": [(48, True), (45, True), (43, True)]},
        "CT-000003": {"Hemoglobin": [(10.2, True), (10.8, True)]},
        "CT-000006": {"HbA1c": [(7.2, True), (7.6, True)]},
        "CT-000007": {"LDL Cholesterol": [(148, True), (135, True)], "Total Cholesterol": [(245, True), (230, True)]},
        "CT-000009": {"ALT": [(78, True), (65, True)], "AST": [(62, True), (55, True)]},
    }

    for i, (test_name, ref_min, ref_max, unit) in enumerate(common_tests):
        patient_overrides = overrides.get(mrn, {}).get(test_name, [])
        num_results = random.randint(3, 5)

        for j in range(num_results):
            test_date = base_date + timedelta(days=j * 90 + i * 3)
            if test_date > date.today():
                break

            if patient_overrides and j < len(patient_overrides):
                value, is_abnormal = patient_overrides[j]
            else:
                spread = (ref_max - ref_min) * 0.3
                value = round(random.uniform(ref_min - spread * 0.2, ref_max + spread * 0.2), 2)
                is_abnormal = not (ref_min <= value <= ref_max)

            labs.append({
                "patient_id": patient_id,
                "test_name": test_name,
                "test_date": test_date,
                "value": value,
                "unit": unit,
                "reference_min": ref_min,
                "reference_max": ref_max,
                "is_abnormal": is_abnormal,
                "ordered_by": physician,
            })

    return labs


def generate_vitals(patient_id: int, mrn: str):
    vitals = []
    base_date = date(2024, 1, 10)

    # Baseline by patient
    bp_profiles = {
        "CT-000001": (150, 95),
        "CT-000002": (148, 92),
        "CT-000003": (130, 82),
        "CT-000004": (118, 76),
        "CT-000005": (115, 72),
        "CT-000006": (138, 86),
        "CT-000007": (145, 90),
        "CT-000008": (110, 70),
        "CT-000009": (120, 78),
        "CT-000010": (125, 80),
    }

    base_sys, base_dia = bp_profiles.get(mrn, (120, 78))

    weights = {
        "CT-000001": 98.5, "CT-000002": 72.3, "CT-000003": 68.0,
        "CT-000004": 65.4, "CT-000005": 78.2, "CT-000006": 61.8,
        "CT-000007": 82.1, "CT-000008": 58.9, "CT-000009": 70.5, "CT-000010": 67.3,
    }
    heights = {
        "CT-000001": 177, "CT-000002": 163, "CT-000003": 171, "CT-000004": 162,
        "CT-000005": 180, "CT-000006": 158, "CT-000007": 174, "CT-000008": 165,
        "CT-000009": 170, "CT-000010": 160,
    }

    weight = weights.get(mrn, 70.0)
    height = heights.get(mrn, 170.0)

    for i in range(12):
        v_date = base_date + timedelta(days=i * 60)
        if v_date > date.today():
            break
        sys_bp = base_sys + random.randint(-10, 12)
        dia_bp = base_dia + random.randint(-8, 10)
        w = weight + random.uniform(-1.5, 1.5)
        h_m = height / 100
        bmi = round(w / (h_m ** 2), 1)

        vitals.append({
            "patient_id": patient_id,
            "recorded_date": v_date,
            "systolic_bp": float(sys_bp),
            "diastolic_bp": float(dia_bp),
            "heart_rate": float(random.randint(62, 88)),
            "temperature": round(random.uniform(36.4, 37.2), 1),
            "weight_kg": round(w, 1),
            "height_cm": float(height),
            "bmi": bmi,
            "oxygen_saturation": float(random.randint(95, 99)),
            "respiratory_rate": float(random.randint(14, 20)),
            "recorded_by": "Nursing Staff",
        })

    return vitals


def generate_reminders(patient_id: int, physician: str):
    today = date.today()
    reminder_templates = [
        ("follow-up", -120, "Quarterly diabetes follow-up overdue", "high"),
        ("lab", -60, "HbA1c recheck needed", "high"),
        ("screening", 30, "Annual eye exam for diabetic retinopathy", "medium"),
        ("follow-up", 14, "Post-medication-change check", "medium"),
        ("lab", -200, "Lipid panel — severely overdue", "high"),
        ("screening", 45, "Annual flu vaccination", "low"),
        ("follow-up", 7, "Nephrology referral follow-up", "high"),
        ("medication", -90, "Medication reconciliation overdue", "medium"),
    ]

    reminders = []
    selected = random.sample(reminder_templates, random.randint(3, 5))
    for rtype, days_offset, desc, priority in selected:
        due = today + timedelta(days=days_offset)
        reminders.append({
            "patient_id": patient_id,
            "reminder_type": rtype,
            "due_date": due,
            "description": desc,
            "is_completed": False,
            "priority": priority,
            "assigned_to": physician,
        })
    return reminders


def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(Patient).count() > 0:
            print("Database already seeded. Skipping.")
            return

        print("Seeding CareTrack AI demo data...")

        for i, pdata in enumerate(PATIENTS_DATA):
            patient = Patient(**pdata)
            db.add(patient)
            db.flush()

            mrn = pdata["mrn"]
            physician = pdata["primary_physician"]
            facility = random.choice(FACILITIES)

            for vdata in generate_visits(patient.id, mrn, physician, facility):
                db.add(Visit(**vdata))

            for ldata in generate_labs(patient.id, mrn, physician):
                db.add(LabResult(**ldata))

            for vital in generate_vitals(patient.id, mrn):
                db.add(Vital(**vital))

            for med in MEDICATIONS_DATA.get(mrn, []):
                name, generic, dosage, freq, route, is_active, indication = med
                start = date(2023, random.randint(1, 12), random.randint(1, 28))
                db.add(Medication(
                    patient_id=patient.id,
                    name=name, generic_name=generic, dosage=dosage,
                    frequency=freq, route=route, is_active=is_active,
                    start_date=start, prescribed_by=physician,
                    indication=indication,
                ))

            for allergy in ALLERGIES_DATA.get(mrn, []):
                allergen, atype, reaction, severity = allergy
                db.add(Allergy(
                    patient_id=patient.id,
                    allergen=allergen, allergen_type=atype,
                    reaction=reaction, severity=severity,
                ))

            for rdata in generate_reminders(patient.id, physician):
                db.add(Reminder(**rdata))

            print(f"  Added patient {i+1}/10: {pdata['first_name']} {pdata['last_name']}")

        db.commit()
        print("Seed data committed. Running risk assessments...")

        patients = db.query(Patient).all()
        for patient in patients:
            result = compute_risk(patient.id, db)
            if result:
                assessment = RiskAssessment(**result)
                db.add(assessment)

        db.commit()
        print(f"Risk assessments complete.")
        print("\nCareTrack AI seeded successfully!")
        print("REMINDER: All data is synthetic — for demonstration only.")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
