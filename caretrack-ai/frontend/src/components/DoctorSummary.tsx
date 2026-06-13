import React, { useState } from "react";
import { PatientSummary } from "../types";
import { getRiskColor, getRiskBg, formatDate } from "../utils";
import RiskBadge from "./RiskBadge";

interface Props {
  summary: PatientSummary | null;
  loading: boolean;
  onRefresh: () => void;
}

const DoctorSummary: React.FC<Props> = ({ summary, loading, onRefresh }) => {
  const [expanded, setExpanded] = useState(true);

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "32px 0", color: "#94a3b8" }}>
        Generating summary...
      </div>
    );
  }

  if (!summary) {
    return (
      <div style={{ textAlign: "center", padding: "32px 0" }}>
        <p style={{ color: "#94a3b8", marginBottom: 12 }}>Summary not available.</p>
        <button onClick={onRefresh} style={btnStyle}>Generate Summary</button>
      </div>
    );
  }

  const { summary: s, structured: st } = summary;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <RiskBadge level={st.risk_level} score={st.risk_score} />
          <span style={{ fontSize: 12, color: "#94a3b8" }}>
            Generated {formatDate(summary.generated_at)} • {summary.source === "llm" ? "AI-generated" : "Template-based"}
          </span>
        </div>
        <button onClick={onRefresh} style={{ ...btnStyle, padding: "4px 10px", fontSize: 12 }}>
          ↻ Refresh
        </button>
      </div>

      {/* Overview */}
      <Section title="Patient Overview" icon="👤">
        <p style={{ margin: 0, color: "#334155", lineHeight: 1.6 }}>{s.overview}</p>
        {s.key_diagnoses.length > 0 && (
          <div style={{ marginTop: 8, display: "flex", gap: 6, flexWrap: "wrap" }}>
            {s.key_diagnoses.map((dx, i) => (
              <span key={i} style={{
                background: "#eff6ff",
                color: "#1e40af",
                border: "1px solid #bfdbfe",
                borderRadius: 20,
                padding: "3px 10px",
                fontSize: 12,
                fontWeight: 500,
              }}>
                {dx}
              </span>
            ))}
          </div>
        )}
      </Section>

      {/* Risk Alerts */}
      {st.risk_reasons.length > 0 && (
        <Section title="Risk Alerts" icon="⚠️">
          <div style={{ background: getRiskBg(st.risk_level), border: `1px solid ${getRiskColor(st.risk_level)}30`, borderRadius: 8, padding: 12 }}>
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              {st.risk_reasons.map((r, i) => (
                <li key={i} style={{ fontSize: 13, color: "#334155", marginBottom: 4 }}>{r}</li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      {/* Vitals & Labs */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <Section title="Latest Vitals" icon="💓">
          <p style={{ margin: 0, fontSize: 13, color: "#475569", lineHeight: 1.6 }}>{s.latest_vitals}</p>
          {st.recent_vitals.slice(0, 2).map((v, i) => (
            <div key={i} style={{ marginTop: 8, padding: "8px 10px", background: "#f8fafc", borderRadius: 6, fontSize: 12, color: "#64748b" }}>
              <strong>{v.date}</strong> • BP: {v.bp} • HR: {v.hr} bpm • BMI: {v.bmi}
            </div>
          ))}
        </Section>

        <Section title="Lab Summary" icon="🧪">
          <p style={{ margin: 0, fontSize: 13, color: "#475569" }}>{s.lab_trends}</p>
          {st.recent_labs.slice(0, 4).map((l: any, i: number) => (
            <div key={i} style={{
              marginTop: 6,
              display: "flex",
              justifyContent: "space-between",
              fontSize: 12,
              padding: "4px 0",
              borderBottom: "1px solid #f1f5f9",
            }}>
              <span style={{ color: "#475569" }}>{l.test} ({l.date})</span>
              <span style={{ color: l.abnormal ? "#ef4444" : "#16a34a", fontWeight: 600 }}>
                {l.value} {l.unit}
              </span>
            </div>
          ))}
        </Section>
      </div>

      {/* Medications */}
      <Section title="Active Medications" icon="💊">
        {st.active_medications.length === 0 ? (
          <p style={{ margin: 0, color: "#94a3b8", fontSize: 13 }}>None documented</p>
        ) : (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {st.active_medications.map((m, i) => (
              <span key={i} style={{
                background: "#f0f9ff",
                color: "#0369a1",
                border: "1px solid #bae6fd",
                borderRadius: 6,
                padding: "3px 10px",
                fontSize: 12,
              }}>
                {m}
              </span>
            ))}
          </div>
        )}
      </Section>

      {/* Allergies */}
      <Section title="Allergies" icon="🚫">
        {st.allergies.length === 0 ? (
          <p style={{ margin: 0, color: "#16a34a", fontSize: 13 }}>No known allergies</p>
        ) : (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {st.allergies.map((a, i) => (
              <span key={i} style={{
                background: "#fef2f2",
                color: "#dc2626",
                border: "1px solid #fecaca",
                borderRadius: 6,
                padding: "3px 10px",
                fontSize: 12,
              }}>
                {a}
              </span>
            ))}
          </div>
        )}
      </Section>

      {/* Suggested Actions */}
      {s.suggested_follow_up_actions.length > 0 && (
        <Section title="Suggested Follow-up Actions" icon="✅">
          <ul style={{ margin: 0, paddingLeft: 20 }}>
            {s.suggested_follow_up_actions.map((action, i) => (
              <li key={i} style={{ fontSize: 13, color: "#334155", marginBottom: 4 }}>{action}</li>
            ))}
          </ul>
        </Section>
      )}
    </div>
  );
};

const Section: React.FC<{ title: string; icon: string; children: React.ReactNode }> = ({ title, icon, children }) => (
  <div style={{ marginBottom: 16, background: "#fff", border: "1px solid #e2e8f0", borderRadius: 10, overflow: "hidden" }}>
    <div style={{ padding: "10px 16px", background: "#f8fafc", borderBottom: "1px solid #e2e8f0", display: "flex", gap: 8, alignItems: "center" }}>
      <span>{icon}</span>
      <span style={{ fontWeight: 600, fontSize: 13, color: "#1e293b" }}>{title}</span>
    </div>
    <div style={{ padding: "12px 16px" }}>{children}</div>
  </div>
);

const btnStyle: React.CSSProperties = {
  padding: "7px 16px",
  background: "#1e3a5f",
  color: "#fff",
  border: "none",
  borderRadius: 6,
  cursor: "pointer",
  fontSize: 13,
  fontWeight: 500,
};

export default DoctorSummary;
