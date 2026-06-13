import React from "react";
import { Link } from "react-router-dom";
import { PatientList, RiskAssessment } from "../types";
import { calculateAge, formatDate } from "../utils";
import RiskBadge from "./RiskBadge";

interface Props {
  patient: PatientList;
  risk?: RiskAssessment;
}

const PatientCard: React.FC<Props> = ({ patient, risk }) => {
  const age = calculateAge(patient.date_of_birth);
  const initials = `${patient.first_name[0]}${patient.last_name[0]}`;

  return (
    <Link to={`/patients/${patient.id}`} style={{ textDecoration: "none" }}>
      <div
        style={{
          background: "#fff",
          borderRadius: 12,
          padding: "18px 20px",
          border: "1px solid #e2e8f0",
          cursor: "pointer",
          transition: "all 0.15s ease",
          display: "flex",
          alignItems: "center",
          gap: 16,
        }}
        onMouseEnter={(e) => {
          (e.currentTarget as HTMLDivElement).style.boxShadow = "0 4px 16px rgba(30,58,95,0.12)";
          (e.currentTarget as HTMLDivElement).style.borderColor = "#3b82f6";
          (e.currentTarget as HTMLDivElement).style.transform = "translateY(-1px)";
        }}
        onMouseLeave={(e) => {
          (e.currentTarget as HTMLDivElement).style.boxShadow = "none";
          (e.currentTarget as HTMLDivElement).style.borderColor = "#e2e8f0";
          (e.currentTarget as HTMLDivElement).style.transform = "none";
        }}
      >
        {/* Avatar */}
        <div style={{
          width: 48,
          height: 48,
          borderRadius: "50%",
          background: "#1e3a5f",
          color: "#fff",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 16,
          fontWeight: 700,
          flexShrink: 0,
        }}>
          {initials}
        </div>

        {/* Info */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
            <span style={{ fontWeight: 600, fontSize: 15, color: "#1e293b" }}>
              {patient.first_name} {patient.last_name}
            </span>
            <span style={{ fontSize: 12, color: "#94a3b8", fontFamily: "monospace" }}>
              {patient.mrn}
            </span>
          </div>
          <div style={{ fontSize: 13, color: "#64748b", marginBottom: 4 }}>
            {patient.gender} • {age} years • DOB: {formatDate(patient.date_of_birth)}
          </div>
          {patient.primary_diagnosis && (
            <div style={{
              fontSize: 12,
              color: "#475569",
              whiteSpace: "nowrap",
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}>
              Dx: {patient.primary_diagnosis}
            </div>
          )}
        </div>

        {/* Right side */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 6, flexShrink: 0 }}>
          {risk ? (
            <RiskBadge level={risk.risk_level} score={risk.risk_score} size="sm" />
          ) : (
            <span style={{ fontSize: 12, color: "#94a3b8" }}>No risk data</span>
          )}
          {patient.primary_physician && (
            <span style={{ fontSize: 12, color: "#64748b" }}>{patient.primary_physician}</span>
          )}
        </div>
      </div>
    </Link>
  );
};

export default PatientCard;
