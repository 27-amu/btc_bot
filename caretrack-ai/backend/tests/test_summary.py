from datetime import date, timedelta


def test_patient_summary_empty(client, sample_patient):
    pid = sample_patient["id"]
    resp = client.get(f"/api/v1/summary/patient/{pid}")
    assert resp.status_code == 200
    body = resp.json()
    assert "summary" in body
    assert "overview" in body["summary"]
    assert body["source"] == "template"


def test_patient_summary_with_data(client):
    patient = client.post("/api/v1/patients/", json={
        "mrn": "SUM-001",
        "first_name": "Summary",
        "last_name": "Patient",
        "date_of_birth": "1965-05-10",
        "gender": "Female",
        "primary_diagnosis": "Type 2 Diabetes, Hypertension",
        "primary_physician": "Dr. Summary",
    }).json()
    pid = patient["id"]

    client.post("/api/v1/vitals/", json={
        "patient_id": pid,
        "recorded_date": str(date.today() - timedelta(days=10)),
        "systolic_bp": 135.0,
        "diastolic_bp": 85.0,
        "heart_rate": 72.0,
        "weight_kg": 70.0,
        "height_cm": 165.0,
    })

    client.post("/api/v1/labs/", json={
        "patient_id": pid,
        "test_name": "HbA1c",
        "test_date": str(date.today() - timedelta(days=15)),
        "value": 7.8,
        "unit": "%",
        "reference_min": 4.0,
        "reference_max": 5.6,
        "is_abnormal": True,
    })

    client.post("/api/v1/medications/", json={
        "patient_id": pid,
        "name": "Metformin",
        "dosage": "500mg",
        "frequency": "twice daily",
        "is_active": True,
        "indication": "Diabetes",
    })

    client.post("/api/v1/allergies/", json={
        "patient_id": pid,
        "allergen": "Penicillin",
        "allergen_type": "drug",
        "reaction": "Rash",
        "severity": "moderate",
    })

    resp = client.get(f"/api/v1/summary/patient/{pid}")
    assert resp.status_code == 200
    body = resp.json()

    summary = body["summary"]
    assert "Diabetes" in summary["overview"] or "diabetes" in summary["overview"].lower()
    assert "Metformin" in summary["medications"]
    assert "Penicillin" in summary["allergies"]
    assert "HbA1c" in summary["lab_trends"] or "abnormal" in summary["lab_trends"].lower()


def test_patient_summary_not_found(client):
    resp = client.get("/api/v1/summary/patient/99999")
    assert resp.status_code == 404


def test_summary_has_required_keys(client, sample_patient):
    pid = sample_patient["id"]
    resp = client.get(f"/api/v1/summary/patient/{pid}")
    assert resp.status_code == 200
    summary = resp.json()["summary"]
    required_keys = [
        "overview", "key_diagnoses", "latest_vitals", "lab_trends",
        "medications", "allergies", "risk_alerts", "visit_history",
        "suggested_follow_up_actions", "pending_follow_ups",
    ]
    for key in required_keys:
        assert key in summary, f"Missing key: {key}"
