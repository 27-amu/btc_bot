import React, { useEffect, useState, useCallback } from "react";
import { PatientList, RiskAssessment } from "../types";
import { patientsApi, riskApi } from "../api/client";
import PatientCard from "../components/PatientCard";
import AddPatientModal from "../components/AddPatientModal";

const RISK_FILTERS = ["all", "high", "medium", "low"] as const;
type RiskFilter = typeof RISK_FILTERS[number];

const Dashboard: React.FC = () => {
  const [patients, setPatients] = useState<PatientList[]>([]);
  const [risks, setRisks] = useState<Record<number, RiskAssessment>>({});
  const [search, setSearch] = useState("");
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [addOpen, setAddOpen] = useState(false);

  const loadPatients = useCallback(async (q?: string) => {
    setLoading(true);
    setError(null);
    try {
      const resp = await patientsApi.list(q || undefined);
      setPatients(resp.data);
    } catch {
      setError("Failed to load patients. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadPatients();
  }, [loadPatients]);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => loadPatients(search), 300);
    return () => clearTimeout(timer);
  }, [search, loadPatients]);

  // Load risk assessments
  useEffect(() => {
    const fetchRisks = async () => {
      const entries = await Promise.allSettled(
        patients.map(async (p) => {
          try {
            const resp = await riskApi.getLatest(p.id);
            return [p.id, resp.data] as [number, RiskAssessment];
          } catch {
            return null;
          }
        })
      );
      const map: Record<number, RiskAssessment> = {};
      entries.forEach((result) => {
        if (result.status === "fulfilled" && result.value) {
          const [id, risk] = result.value;
          map[id] = risk;
        }
      });
      setRisks(map);
    };
    if (patients.length > 0) fetchRisks();
  }, [patients]);

  const filtered = patients.filter((p) =>
    riskFilter === "all" ? true : risks[p.id]?.risk_level === riskFilter
  );

  const stats = {
    total: patients.length,
    high: Object.values(risks).filter((r) => r.risk_level === "high").length,
    medium: Object.values(risks).filter((r) => r.risk_level === "medium").length,
    low: Object.values(risks).filter((r) => r.risk_level === "low").length,
  };

  return (
    <div>
      {addOpen && (
        <AddPatientModal onClose={() => setAddOpen(false)} onCreated={() => loadPatients(search)} />
      )}

      {/* Page Header */}
      <div style={{ marginBottom: 24, display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <h1 style={{ margin: "0 0 4px", fontSize: 26, fontWeight: 700, color: "#1e293b" }}>
            Patient Dashboard
          </h1>
          <p style={{ margin: 0, color: "#64748b", fontSize: 14 }}>
            Longitudinal monitoring • Risk assessment • Follow-up tracking
          </p>
        </div>
        <button
          onClick={() => setAddOpen(true)}
          style={{
            padding: "9px 18px", borderRadius: 8, border: "none",
            background: "#1e3a5f", color: "#fff", fontSize: 14,
            fontWeight: 600, cursor: "pointer",
          }}
        >
          + Add Patient
        </button>
      </div>

      {/* Stats Bar */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 24 }}>
        <StatCard label="Total Patients" value={stats.total} color="#1e3a5f" bg="#eff6ff" />
        <StatCard label="High Risk" value={stats.high} color="#dc2626" bg="#fef2f2" onClick={() => setRiskFilter("high")} />
        <StatCard label="Medium Risk" value={stats.medium} color="#d97706" bg="#fffbeb" onClick={() => setRiskFilter("medium")} />
        <StatCard label="Low Risk" value={stats.low} color="#16a34a" bg="#f0fdf4" onClick={() => setRiskFilter("low")} />
      </div>

      {/* Search + Filter */}
      <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap" }}>
        <input
          type="text"
          placeholder="Search by name, MRN, or diagnosis..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            flex: 1,
            minWidth: 280,
            padding: "10px 16px",
            borderRadius: 8,
            border: "1px solid #e2e8f0",
            fontSize: 14,
            outline: "none",
            boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
          }}
        />
        <div style={{ display: "flex", gap: 6 }}>
          {RISK_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setRiskFilter(f)}
              style={{
                padding: "8px 16px",
                borderRadius: 8,
                border: riskFilter === f ? "2px solid #1e3a5f" : "1px solid #e2e8f0",
                background: riskFilter === f ? "#1e3a5f" : "#fff",
                color: riskFilter === f ? "#fff" : "#64748b",
                fontSize: 13,
                fontWeight: riskFilter === f ? 600 : 400,
                cursor: "pointer",
                textTransform: "capitalize",
              }}
            >
              {f === "all" ? "All" : `${f.charAt(0).toUpperCase() + f.slice(1)} Risk`}
            </button>
          ))}
        </div>
      </div>

      {/* Patient List */}
      {loading ? (
        <LoadingState />
      ) : error ? (
        <ErrorState message={error} />
      ) : filtered.length === 0 ? (
        <EmptyState search={search} />
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <p style={{ margin: "0 0 8px", fontSize: 13, color: "#94a3b8" }}>
            Showing {filtered.length} patient{filtered.length !== 1 ? "s" : ""}
          </p>
          {filtered.map((p) => (
            <PatientCard key={p.id} patient={p} risk={risks[p.id]} />
          ))}
        </div>
      )}
    </div>
  );
};

const StatCard: React.FC<{
  label: string; value: number; color: string; bg: string; onClick?: () => void
}> = ({ label, value, color, bg, onClick }) => (
  <div
    onClick={onClick}
    style={{
      background: bg,
      border: `1px solid ${color}25`,
      borderRadius: 12,
      padding: "16px 20px",
      cursor: onClick ? "pointer" : "default",
      transition: "transform 0.15s",
    }}
    onMouseEnter={(e) => { if (onClick) (e.currentTarget as HTMLDivElement).style.transform = "translateY(-2px)"; }}
    onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.transform = "none"; }}
  >
    <div style={{ fontSize: 32, fontWeight: 700, color, lineHeight: 1 }}>{value}</div>
    <div style={{ fontSize: 13, color, opacity: 0.8, marginTop: 4 }}>{label}</div>
  </div>
);

const LoadingState = () => (
  <div style={{ textAlign: "center", padding: "60px 0", color: "#94a3b8" }}>
    <div style={{ fontSize: 32, marginBottom: 12 }}>⏳</div>
    Loading patients...
  </div>
);

const ErrorState: React.FC<{ message: string }> = ({ message }) => (
  <div style={{
    background: "#fef2f2",
    border: "1px solid #fecaca",
    borderRadius: 10,
    padding: "24px",
    textAlign: "center",
    color: "#dc2626",
  }}>
    <div style={{ fontSize: 24, marginBottom: 8 }}>⚠️</div>
    <p style={{ margin: 0 }}>{message}</p>
  </div>
);

const EmptyState: React.FC<{ search: string }> = ({ search }) => (
  <div style={{ textAlign: "center", padding: "60px 0", color: "#94a3b8" }}>
    <div style={{ fontSize: 32, marginBottom: 12 }}>🔍</div>
    {search ? `No patients matching "${search}"` : "No patients found."}
  </div>
);

export default Dashboard;
