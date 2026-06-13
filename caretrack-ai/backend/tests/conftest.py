import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_patient(client):
    data = {
        "mrn": "TEST-001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1970-01-01",
        "gender": "Male",
        "primary_diagnosis": "Hypertension",
        "primary_physician": "Dr. Test",
    }
    resp = client.post("/api/v1/patients/", json=data)
    assert resp.status_code == 201
    return resp.json()
