# CareTrack AI

> Longitudinal Patient Monitoring & Risk-Alert System — Portfolio Demo

**DISCLAIMER: This is a demonstration system using 100% synthetic data. It is NOT a certified medical device and must NOT be used for real patient care or with real PHI (Protected Health Information).**

---

## Overview

CareTrack AI is a full-stack healthcare monitoring system that helps clinicians track patients over multiple years, identify missed follow-ups, monitor lab/vital trends, flag medication-allergy risks, and generate AI-ready patient summaries.

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Recharts, React Router |
| Backend | FastAPI, Python 3.11, Pydantic v2 |
| Database | PostgreSQL 16, SQLAlchemy 2, Alembic |
| Deployment | Docker, Docker Compose, Nginx |

---

## Quick Start (Docker)

```bash
# 1. Clone the repo
git clone <repo-url> && cd caretrack-ai

# 2. Copy environment config
cp .env.example .env

# 3. Build and run everything
docker compose up --build
```

**That's it.** The startup sequence:
1. PostgreSQL starts and becomes healthy
2. Backend runs Alembic migrations
3. Seed script creates 10 synthetic demo patients
4. Frontend builds and serves via Nginx

| Service | URL |
|---------|-----|
| Frontend | http://localhost:80 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## Local Development (without Docker)

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL (or use Docker just for DB)
docker run -d --name caretrack_db \
  -e POSTGRES_USER=caretrack \
  -e POSTGRES_PASSWORD=caretrack \
  -e POSTGRES_DB=caretrack_db \
  -p 5432:5432 postgres:16-alpine

# Run migrations
export DATABASE_URL=postgresql://caretrack:caretrack@localhost:5432/caretrack_db
alembic upgrade head

# Seed demo data
python seed_data.py

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
REACT_APP_API_URL=http://localhost:8000/api/v1 npm start
```

---

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

Tests use SQLite in-memory (no PostgreSQL needed). Coverage includes:
- Patient CRUD operations
- Visit, lab, vital, medication, allergy, reminder APIs
- Risk engine rules (high/low risk, allergy conflicts)
- Summary generation

---

## Project Structure

```
caretrack-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models/              # ORM models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   └── services/
│   │       ├── risk_engine.py   # Rule-based risk scoring
│   │       └── summary_generator.py  # AI-ready summaries
│   ├── migrations/              # Alembic migrations
│   ├── tests/                   # Pytest test suite
│   ├── seed_data.py             # Synthetic demo data
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api/client.ts        # Axios API client
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Dashboard & PatientProfile
│   │   ├── types/               # TypeScript interfaces
│   │   └── utils/               # Helper functions
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Features

### Patient Dashboard
- Patient list with search (name, MRN, diagnosis)
- Risk-level filter (All / High / Medium / Low)
- Stats bar: total, high, medium, low risk counts
- Risk badge on each patient card

### Patient Profile
- **Overview**: Demographics, risk assessment, pending reminders
- **Visits**: Year-filterable timeline with visit type, diagnosis, physician
- **Labs**: Line charts per test with reference range lines; abnormal flagging; full results table
- **Vitals**: Charts for BP, HR, BMI, O₂ sat, weight; tabular history
- **Medications & Allergies**: Active/discontinued medications; severity-colored allergy list
- **Doctor Summary**: Structured patient summary (template-based, LLM-ready)

### Risk Engine
Rule-based scoring across 6 risk dimensions:
| Rule | Trigger |
|------|---------|
| Missed follow-up | Reminders overdue > 90 days |
| Worsening HbA1c | HbA1c ≥ 7.5% or rising trend |
| High BP trend | ≥ 3 of last 6 readings elevated |
| Kidney markers | Creatinine > 1.3 or eGFR < 60 |
| Allergy conflict | Active medication cross-reacts with documented allergy |
| Multiple abnormal labs | ≥ 3 abnormal labs in last 6 months |

### AI Summary
Template-based structured summary with LLM integration stub in [backend/app/services/summary_generator.py](backend/app/services/summary_generator.py). To enable Claude:
```python
# In summary_generator.py _generate_with_llm():
import anthropic
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
message = client.messages.create(model="claude-opus-4-8", ...)
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/patients/` | List patients (search, filter) |
| GET | `/api/v1/patients/{id}` | Get patient details |
| POST | `/api/v1/patients/` | Create patient |
| GET | `/api/v1/visits/patient/{id}` | Patient visits (filterable by year) |
| GET | `/api/v1/labs/patient/{id}` | Lab results |
| GET | `/api/v1/vitals/patient/{id}` | Vital signs |
| GET | `/api/v1/medications/patient/{id}` | Medications |
| GET | `/api/v1/allergies/patient/{id}` | Allergies |
| GET | `/api/v1/reminders/patient/{id}` | Reminders |
| POST | `/api/v1/risk/patient/{id}/assess` | Run risk assessment |
| GET | `/api/v1/risk/patient/{id}/latest` | Latest risk score |
| GET | `/api/v1/summary/patient/{id}` | Patient summary |
| GET | `/health` | Health check |

Full interactive docs at http://localhost:8000/docs

---

## Security & Compliance Notes

- **Not a medical device**: This system has not been cleared or approved by any regulatory body (FDA, CE, etc.)
- **Synthetic data only**: All demo patients are fictitious. No real PHI is stored.
- **Input validation**: All API inputs validated with Pydantic
- **Safe error messages**: Internal errors are caught and return generic messages
- **Audit-friendly structure**: Timestamps on all records; assessed_by field on risk assessments
- **No real credentials in code**: All secrets via environment variables (see `.env.example`)

---

## License

MIT — Free for educational and portfolio use.
