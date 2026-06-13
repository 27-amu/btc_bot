from datetime import date, timedelta


def setup_patient_with_data(client):
    patient = client.post("/api/v1/patients/", json={
        "mrn": "RISK-001",
        "first_name": "Risk",
        "last_name": "TestPatient",
        "date_of_birth": "1960-01-01",
        "gender": "Male",
        "primary_diagnosis": "Type 2 Diabetes, Hypertension",
        "primary_physician": "Dr. Risk",
    }).json()
    pid = patient["id"]

    # High HbA1c
    client.post("/api/v1/labs/", json={
        "patient_id": pid,
        "test_name": "HbA1c",
        "test_date": str(date.today() - timedelta(days=30)),
        "value": 9.5,
        "unit": "%",
        "reference_min": 4.0,
        "reference_max": 5.6,
        "is_abnormal": True,
    })

    # High BP vitals
    for i in range(4):
        client.post("/api/v1/vitals/", json={
            "patient_id": pid,
            "recorded_date": str(date.today() - timedelta(days=i * 20)),
            "systolic_bp": 158.0,
            "diastolic_bp": 98.0,
            "heart_rate": 78.0,
        })

    # Overdue reminder (>90 days ago)
    client.post("/api/v1/reminders/", json={
        "patient_id": pid,
        "reminder_type": "follow-up",
        "due_date": str(date.today() - timedelta(days=120)),
        "description": "Missed follow-up",
        "priority": "high",
    })

    return pid


def test_risk_assessment_high_risk(client):
    pid = setup_patient_with_data(client)
    resp = client.post(f"/api/v1/risk/patient/{pid}/assess")
    assert resp.status_code == 201
    body = resp.json()
    assert body["risk_level"] in ("medium", "high")
    assert body["risk_score"] > 20
    assert len(body["reasons"]) > 0
    assert len(body["recommended_actions"]) > 0


def test_risk_assessment_low_risk(client):
    patient = client.post("/api/v1/patients/", json={
        "mrn": "LOW-001",
        "first_name": "Healthy",
        "last_name": "Patient",
        "date_of_birth": "1990-01-01",
        "gender": "Female",
    }).json()
    pid = patient["id"]

    # Normal HbA1c
    client.post("/api/v1/labs/", json={
        "patient_id": pid,
        "test_name": "HbA1c",
        "test_date": str(date.today() - timedelta(days=15)),
        "value": 5.2,
        "unit": "%",
        "reference_min": 4.0,
        "reference_max": 5.6,
        "is_abnormal": False,
    })

    resp = client.post(f"/api/v1/risk/patient/{pid}/assess")
    assert resp.status_code == 201
    body = resp.json()
    assert body["risk_level"] == "low"
    assert body["risk_score"] < 30


def test_risk_history(client):
    pid = setup_patient_with_data(client)
    client.post(f"/api/v1/risk/patient/{pid}/assess")
    client.post(f"/api/v1/risk/patient/{pid}/assess")

    resp = client.get(f"/api/v1/risk/patient/{pid}/history")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


def test_get_latest_risk(client):
    pid = setup_patient_with_data(client)
    client.post(f"/api/v1/risk/patient/{pid}/assess")

    resp = client.get(f"/api/v1/risk/patient/{pid}/latest")
    assert resp.status_code == 200
    assert "risk_level" in resp.json()


def test_get_latest_risk_not_found(client, sample_patient):
    pid = sample_patient["id"]
    resp = client.get(f"/api/v1/risk/patient/{pid}/latest")
    assert resp.status_code == 404


def test_allergy_medication_conflict(client):
    patient = client.post("/api/v1/patients/", json={
        "mrn": "CONF-001",
        "first_name": "Conflict",
        "last_name": "Test",
        "date_of_birth": "1970-01-01",
        "gender": "Male",
    }).json()
    pid = patient["id"]

    # Penicillin allergy
    client.post("/api/v1/allergies/", json={
        "patient_id": pid,
        "allergen": "Penicillin",
        "allergen_type": "drug",
        "reaction": "Anaphylaxis",
        "severity": "life-threatening",
    })

    # Amoxicillin medication (cross-reactive with penicillin)
    client.post("/api/v1/medications/", json={
        "patient_id": pid,
        "name": "Amoxicillin",
        "dosage": "500mg",
        "frequency": "three times daily",
        "is_active": True,
    })

    resp = client.post(f"/api/v1/risk/patient/{pid}/assess")
    assert resp.status_code == 201
    body = resp.json()
    assert body["risk_level"] == "high"
    assert any("allergy" in r.lower() or "conflict" in r.lower() for r in body["reasons"])
