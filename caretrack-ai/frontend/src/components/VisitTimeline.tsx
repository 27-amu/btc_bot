import React, { useState } from "react";
import { Visit } from "../types";
import { formatDate } from "../utils";

interface Props {
  visits: Visit[];
}

const TYPE_COLORS: Record<string, string> = {
  routine: "#3b82f6",
  "follow-up": "#8b5cf6",
  urgent: "#ef4444",
  emergency: "#dc2626",
  telehealth: "#06b6d4",
};

const VisitTimeline: React.FC<Props> = ({ visits }) => {
  const [selectedYear, setSelectedYear] = useState<number | "all">("all");

  const years = Array.from(new Set(visits.map((v) => new Date(v.visit_date).getFullYear()))).sort((a, b) => b - a);

  const filtered = selectedYear === "all"
    ? visits
    : visits.filter((v) => new Date(v.visit_date).getFullYear() === selectedYear);

  const sorted = [...filtered].sort((a, b) => new Date(b.visit_date).getTime() - new Date(a.visit_date).getTime());

  return (
    <div>
      {/* Year filter */}
      <div style={{ display: "flex", gap: 8, marginBottom: 20, flexWrap: "wrap" }}>
        <FilterBtn label="All" active={selectedYear === "all"} onClick={() => setSelectedYear("all")} />
        {years.map((y) => (
          <FilterBtn key={y} label={String(y)} active={selectedYear === y} onClick={() => setSelectedYear(y)} />
        ))}
      </div>

      {sorted.length === 0 ? (
        <p style={{ color: "#94a3b8", fontSize: 14 }}>No visits found for selected period.</p>
      ) : (
        <div style={{ position: "relative" }}>
          {/* Vertical line */}
          <div style={{
            position: "absolute",
            left: 20,
            top: 0,
            bottom: 0,
            width: 2,
            background: "#e2e8f0",
            borderRadius: 1,
          }} />

          <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
            {sorted.map((visit, idx) => {
              const color = TYPE_COLORS[visit.visit_type] || "#6b7280";
              return (
                <div key={visit.id} style={{ display: "flex", gap: 20, paddingBottom: idx === sorted.length - 1 ? 0 : 24 }}>
                  {/* Dot */}
                  <div style={{
                    width: 42,
                    flexShrink: 0,
                    display: "flex",
                    justifyContent: "center",
                  }}>
                    <div style={{
                      width: 14,
                      height: 14,
                      borderRadius: "50%",
                      background: color,
                      border: "3px solid #fff",
                      boxShadow: `0 0 0 2px ${color}`,
                      marginTop: 4,
                    }} />
                  </div>

                  {/* Content */}
                  <div style={{
                    flex: 1,
                    background: "#f8fafc",
                    borderRadius: 8,
                    padding: "12px 16px",
                    border: "1px solid #e2e8f0",
                  }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                        <span style={{
                          fontSize: 11,
                          fontWeight: 600,
                          textTransform: "uppercase",
                          color,
                          background: `${color}18`,
                          padding: "2px 8px",
                          borderRadius: 10,
                        }}>
                          {visit.visit_type}
                        </span>
                        <span style={{ fontSize: 13, fontWeight: 500, color: "#334155" }}>
                          {formatDate(visit.visit_date)}
                        </span>
                      </div>
                      {visit.physician && (
                        <span style={{ fontSize: 12, color: "#94a3b8" }}>{visit.physician}</span>
                      )}
                    </div>

                    {visit.chief_complaint && (
                      <p style={{ margin: "0 0 4px", fontSize: 13, color: "#475569" }}>
                        <strong>Chief Complaint:</strong> {visit.chief_complaint}
                      </p>
                    )}
                    {visit.diagnosis && (
                      <p style={{ margin: "0 0 4px", fontSize: 13, color: "#475569" }}>
                        <strong>Diagnosis:</strong> {visit.diagnosis}
                      </p>
                    )}
                    {visit.facility && (
                      <p style={{ margin: 0, fontSize: 12, color: "#94a3b8" }}>{visit.facility}</p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

const FilterBtn: React.FC<{ label: string; active: boolean; onClick: () => void }> = ({ label, active, onClick }) => (
  <button
    onClick={onClick}
    style={{
      padding: "5px 14px",
      borderRadius: 20,
      border: active ? "1px solid #1e3a5f" : "1px solid #e2e8f0",
      background: active ? "#1e3a5f" : "#fff",
      color: active ? "#fff" : "#64748b",
      fontSize: 13,
      fontWeight: active ? 600 : 400,
      cursor: "pointer",
      transition: "all 0.15s",
    }}
  >
    {label}
  </button>
);

export default VisitTimeline;
