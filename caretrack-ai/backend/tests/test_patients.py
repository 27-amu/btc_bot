from datetime import date


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_patient(client):
    data = {
        "mrn": "PT-0001",
        "first_name": "Alice",
        "last_name": "Smith",
        "date_of_birth": "1980-06-15",
        "gender": "Female",
        "primary_diagnosis": "Type 2 Diabetes",
        "primary_physician": "Dr. Johnson",
    }
    resp = client.post("/api/v1/patients/", json=data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["mrn"] == "PT-0001"
    assert body["first_name"] == "Alice"


def test_create_patient_duplicate_mrn(client, sample_patient):
    data = {
        "mrn": "TEST-001",
        "first_name": "Bob",
        "last_name": "Jones",
        "date_of_birth": "1975-03-20",
        "gender": "Male",
    }
    resp = client.post("/api/v1/patients/", json=data)
    assert resp.status_code == 409


def test_get_patient(client, sample_patient):
    pid = sample_patient["id"]
    resp = client.get(f"/api/v1/patients/{pid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == pid


def test_get_patient_not_found(client):
    resp = client.get("/api/v1/patients/99999")
    assert resp.status_code == 404


def test_list_patients(client, sample_patient):
    resp = client.get("/api/v1/patients/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_search_patients(client, sample_patient):
    resp = client.get("/api/v1/patients/?search=Doe")
    assert resp.status_code == 200
    results = resp.json()
    assert any(p["last_name"] == "Doe" for p in results)


def test_update_patient(client, sample_patient):
    pid = sample_patient["id"]
    resp = client.patch(f"/api/v1/patients/{pid}", json={"phone": "555-9999"})
    assert resp.status_code == 200
    assert resp.json()["phone"] == "555-9999"


def test_create_visit(client, sample_patient):
    pid = sample_patient["id"]
    data = {
        "patient_id": pid,
        "visit_date": "2024-03-15",
        "visit_type": "routine",
        "chief_complaint": "Annual checkup",
        "diagnosis": "Hypertension, controlled",
        "physician": "Dr. Test",
    }
    resp = client.post("/api/v1/visits/", json=data)
    assert resp.status_code == 201
    assert resp.json()["visit_type"] == "routine"


def test_get_patient_visits(client, sample_patient):
    pid = sample_patient["id"]
    client.post("/api/v1/visits/", json={
        "patient_id": pid, "visit_date": "2024-06-01",
        "visit_type": "follow-up", "physician": "Dr. Test",
    })
    resp = client.get(f"/api/v1/visits/patient/{pid}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_create_lab_result(client, sample_patient):
    pid = sample_patient["id"]
    data = {
        "patient_id": pid,
        "test_name": "HbA1c",
        "test_date": "2024-04-01",
        "value": 8.2,
        "unit": "%",
        "reference_min": 4.0,
        "reference_max": 5.6,
    }
    resp = client.post("/api/v1/labs/", json=data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["test_name"] == "HbA1c"
    assert body["is_abnormal"] is True


def test_create_vital(client, sample_patient):
    pid = sample_patient["id"]
    data = {
        "patient_id": pid,
        "recorded_date": "2024-04-01",
        "systolic_bp": 145.0,
        "diastolic_bp": 92.0,
        "heart_rate": 78.0,
        "weight_kg": 85.0,
        "height_cm": 175.0,
    }
    resp = client.post("/api/v1/vitals/", json=data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["bmi"] is not None


def test_medication_crud(client, sample_patient):
    pid = sample_patient["id"]
    data = {
        "patient_id": pid,
        "name": "Metformin",
        "generic_name": "metformin hcl",
        "dosage": "500mg",
        "frequency": "twice daily",
        "route": "oral",
        "is_active": True,
        "indication": "Type 2 Diabetes",
    }
    resp = client.post("/api/v1/medications/", json=data)
    assert resp.status_code == 201
    mid = resp.json()["id"]

    resp = client.get(f"/api/v1/medications/patient/{pid}")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.patch(f"/api/v1/medications/{mid}", json={"dosage": "1000mg"})
    assert resp.status_code == 200
    assert resp.json()["dosage"] == "1000mg"


def test_allergy_crud(client, sample_patient):
    pid = sample_patient["id"]
    data = {
        "patient_id": pid,
        "allergen": "Penicillin",
        "allergen_type": "drug",
        "reaction": "Rash",
        "severity": "moderate",
    }
    resp = client.post("/api/v1/allergies/", json=data)
    assert resp.status_code == 201

    resp = client.get(f"/api/v1/allergies/patient/{pid}")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_reminder_crud(client, sample_patient):
    pid = sample_patient["id"]
    data = {
        "patient_id": pid,
        "reminder_type": "follow-up",
        "due_date": "2024-09-01",
        "description": "Quarterly diabetes review",
        "priority": "high",
    }
    resp = client.post("/api/v1/reminders/", json=data)
    assert resp.status_code == 201
    rid = resp.json()["id"]

    resp = client.patch(f"/api/v1/reminders/{rid}", json={"is_completed": True})
    assert resp.status_code == 200
    assert resp.json()["is_completed"] is True
