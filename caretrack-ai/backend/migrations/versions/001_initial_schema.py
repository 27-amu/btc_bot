"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mrn", sa.String(20), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", sa.String(20), nullable=False),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("email", sa.String(150), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("primary_diagnosis", sa.String(200), nullable=True),
        sa.Column("primary_physician", sa.String(150), nullable=True),
        sa.Column("insurance_id", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_patients_id", "patients", ["id"])
    op.create_index("ix_patients_mrn", "patients", ["mrn"], unique=True)

    op.create_table(
        "visits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("visit_date", sa.Date(), nullable=False),
        sa.Column("visit_type", sa.String(50), nullable=False),
        sa.Column("chief_complaint", sa.Text(), nullable=True),
        sa.Column("diagnosis", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("physician", sa.String(150), nullable=True),
        sa.Column("facility", sa.String(200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_visits_id", "visits", ["id"])

    op.create_table(
        "lab_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("test_name", sa.String(150), nullable=False),
        sa.Column("test_date", sa.Date(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(50), nullable=True),
        sa.Column("reference_min", sa.Float(), nullable=True),
        sa.Column("reference_max", sa.Float(), nullable=True),
        sa.Column("is_abnormal", sa.Boolean(), nullable=True),
        sa.Column("notes", sa.String(500), nullable=True),
        sa.Column("ordered_by", sa.String(150), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_lab_results_id", "lab_results", ["id"])

    op.create_table(
        "vitals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("recorded_date", sa.Date(), nullable=False),
        sa.Column("systolic_bp", sa.Float(), nullable=True),
        sa.Column("diastolic_bp", sa.Float(), nullable=True),
        sa.Column("heart_rate", sa.Float(), nullable=True),
        sa.Column("temperature", sa.Float(), nullable=True),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("bmi", sa.Float(), nullable=True),
        sa.Column("oxygen_saturation", sa.Float(), nullable=True),
        sa.Column("respiratory_rate", sa.Float(), nullable=True),
        sa.Column("recorded_by", sa.String(150), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_vitals_id", "vitals", ["id"])

    op.create_table(
        "medications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("generic_name", sa.String(200), nullable=True),
        sa.Column("dosage", sa.String(100), nullable=True),
        sa.Column("frequency", sa.String(100), nullable=True),
        sa.Column("route", sa.String(50), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("prescribed_by", sa.String(150), nullable=True),
        sa.Column("indication", sa.String(300), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_medications_id", "medications", ["id"])

    op.create_table(
        "allergies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("allergen", sa.String(200), nullable=False),
        sa.Column("allergen_type", sa.String(50), nullable=True),
        sa.Column("reaction", sa.String(300), nullable=True),
        sa.Column("severity", sa.String(50), nullable=True),
        sa.Column("onset_date", sa.DateTime(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_allergies_id", "allergies", ["id"])

    op.create_table(
        "reminders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("reminder_type", sa.String(100), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("priority", sa.String(20), nullable=True),
        sa.Column("assigned_to", sa.String(150), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reminders_id", "reminders", ["id"])

    op.create_table(
        "risk_assessments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("assessed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.String(20), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=True),
        sa.Column("recommended_actions", sa.JSON(), nullable=True),
        sa.Column("assessed_by", sa.String(50), nullable=True),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_risk_assessments_id", "risk_assessments", ["id"])


def downgrade() -> None:
    op.drop_table("risk_assessments")
    op.drop_table("reminders")
    op.drop_table("allergies")
    op.drop_table("medications")
    op.drop_table("vitals")
    op.drop_table("lab_results")
    op.drop_table("visits")
    op.drop_table("patients")
