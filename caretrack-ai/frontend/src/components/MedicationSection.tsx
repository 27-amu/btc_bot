import React, { useState } from "react";
import { Medication } from "../types";
import { formatDate } from "../utils";

interface Props {
  medications: Medication[];
}

const MedicationSection: React.FC<Props> = ({ medications }) => {
  const [showAll, setShowAll] = useState(false);

  const active = medications.filter((m) => m.is_active);
  const inactive = medications.filter((m) => !m.is_active);
  const displayed = showAll ? medications : active;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div style={{ fontSize: 13, color: "#64748b" }}>
          {active.length} active • {inactive.length} discontinued
        </div>
        {inactive.length > 0 && (
          <button
            onClick={() => setShowAll(!showAll)}
            style={{
              fontSize: 12,
              color: "#3b82f6",
              background: "none",
              border: "none",
              cursor: "pointer",
              textDecoration: "underline",
            }}
          >
            {showAll ? "Show active only" : "Show all"}
          </button>
        )}
      </div>

      {displayed.length === 0 ? (
        <p style={{ color: "#94a3b8", fontSize: 14 }}>No medications documented.</p>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {displayed.map((med) => (
            <div
              key={med.id}
              style={{
                background: med.is_active ? "#f0f9ff" : "#f8fafc",
                border: `1px solid ${med.is_active ? "#bae6fd" : "#e2e8f0"}`,
                borderRadius: 8,
                padding: "12px 16px",
                opacity: med.is_active ? 1 : 0.7,
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <div>
                  <span style={{ fontWeight: 600, fontSize: 14, color: "#1e293b" }}>{med.name}</span>
                  {med.generic_name && (
                    <span style={{ fontSize: 12, color: "#94a3b8", marginLeft: 6 }}>({med.generic_name})</span>
                  )}
                  {!med.is_active && (
                    <span style={{
                      marginLeft: 8,
                      fontSize: 11,
                      background: "#f1f5f9",
                      color: "#94a3b8",
                      padding: "1px 6px",
                      borderRadius: 10,
                      fontWeight: 500,
                    }}>
                      discontinued
                    </span>
                  )}
                </div>
                {med.route && (
                  <span style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase" }}>{med.route}</span>
                )}
              </div>
              <div style={{ marginTop: 4, fontSize: 13, color: "#475569" }}>
                {[med.dosage, med.frequency].filter(Boolean).join(" • ")}
              </div>
              {med.indication && (
                <div style={{ marginTop: 2, fontSize: 12, color: "#64748b" }}>
                  Indication: {med.indication}
                </div>
              )}
              <div style={{ marginTop: 4, fontSize: 11, color: "#94a3b8", display: "flex", gap: 12 }}>
                {med.start_date && <span>Started: {formatDate(med.start_date)}</span>}
                {med.end_date && <span>Ended: {formatDate(med.end_date)}</span>}
                {med.prescribed_by && <span>By: {med.prescribed_by}</span>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MedicationSection;
