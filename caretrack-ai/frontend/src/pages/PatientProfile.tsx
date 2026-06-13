import React, { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import {
  Patient, Visit, LabResult, Vital,
  Medication, Allergy, Reminder, RiskAssessment, PatientSummary,
} from "../types";
import {
  patientsApi, visitsApi, labsApi, vitalsApi,
  medicationsApi, allergiesApi, remindersApi, riskApi, summaryApi,
} from "../api/client";
import { calculateAge, formatDate } from "../utils";
import RiskBadge from "../components/RiskBadge";
import VisitTimeline from "../components/VisitTimeline";
import LabChart from "../components/LabChart";
import VitalChart from "../components/VitalChart";
import MedicationSection from "../components/MedicationSection";
import AllergySection from "../components/AllergySection";
import RemindersPanel from "../components/RemindersPanel";
import DoctorSummary from "../components/DoctorSummary";
import EditPatientModal from "../components/EditPatientModal";
import AddReminderModal from "../components/AddReminderModal";

type TabKey = "overview" | "visits" | "labs" | "vitals" | "medications" | "summary";

const TABS: { key: TabKey; label: string }[] = [
  { key: "overview", label: "Overview" },
  { key: "visits", label: "Visits" },
  { key: "labs", label: "Labs" },
  { key: "vitals", label: "Vitals" },
  { key: "medications", label: "Medications & Allergies" },
  { key: "summary", label: "Doctor Summary" },
];

const PatientProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const patientId = Number(id);

  const [patient, setPatient] = useState<Patient | null>(null);
  const [visits, setVisits] = useState<Visit[]>([]);
  const [labs, setLabs] = useState<LabResult[]>([]);
  const [vitals, setVitals] = useState<Vital[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [allergies, setAllergies] = useState<Allergy[]>([]);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [risk, setRisk] = useState<RiskAssessment | null>(null);
  const [summary, setSummary] = useState<PatientSummary | null>(null);
  const [activeTab, setActiveTab] = useState<TabKey>("overview");
  const [loading, setLoading] = useState(true);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editOpen, setEditOpen] = useState(false);
  const [addReminderOpen, setAddReminderOpen] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        patientResp, visitsResp, labsResp, vitalsResp,
        medsResp, allergiesResp, remindersResp,
      ] = await Promise.all([
        patientsApi.get(patientId),
        visitsApi.getByPatient(patientId),
        labsApi.getByPatient(patientId),
        vitalsApi.getByPatient(patientId, 50),
        medicationsApi.getByPatient(patientId),
        allergiesApi.getByPatient(patientId),
        remindersApi.getByPatient(patientId),
      ]);

      setPatient(patientResp.data);
      setVisits(visitsResp.data);
      setLabs(labsResp.data);
      setVitals(vitalsResp.data);
      setMedications(medsResp.data);
      setAllergies(allergiesResp.data);
      setReminders(remindersResp.data);

      try {
        const riskResp = await riskApi.getLatest(patientId);
        setRisk(riskResp.data);
      } catch {
        // No risk assessment yet
      }
    } catch {
      setError("Failed to load patient data.");
    } finally {
      setLoading(false);
    }
  }, [patientId]);

  const loadSummary = useCallback(async () => {
    setSummaryLoading(true);
    try {
      const resp = await summaryApi.get(patientId);
      setSummary(resp.data);
    } catch {
      setSummary(null);
    } finally {
      setSummaryLoading(false);
    }
  }, [patientId]);

  const runRiskAssessment = async () => {
    try {
      const resp = await riskApi.assess(patientId);
      setRisk(resp.data);
    } catch (e) {
      console.error("Risk assessment failed", e);
    }
  };

  useEffect(() => {
    loadData();
    loadSummary();
  }, [loadData, loadSummary]);

  if (loading) return <div style={{ textAlign: "center", padding: "80px", color: "#94a3b8" }}>Loading patient...</div>;
  if (error) return <div style={{ textAlign: "center", padding: "80px", color: "#ef4444" }}>{error}</div>;
  if (!patient) return null;

  const age = calculateAge(patient.date_of_birth);
  const pendingReminders = reminders.filter((r) => !r.is_completed);
  const abnormalLabs = labs.filter((l) => l.is_abnormal);

  return (
    <div>
      {editOpen && (
        <EditPatientModal
          patient={patient}
          onClose={() => setEditOpen(false)}
          onSaved={(updated) => setPatient(updated)}
        />
      )}
      {addReminderOpen && (
        <AddReminderModal
          patientId={patientId}
          onClose={() => setAddReminderOpen(false)}
          onCreated={loadData}
        />
      )}

      {/* Breadcrumb */}
      <div style={{ marginBottom: 16, fontSize: 13, color: "#94a3b8" }}>
        <Link to="/" style={{ color: "#3b82f6", textDecoration: "none" }}>Dashboard</Link>
        {" / "}
        {patient.first_name} {patient.last_name}
      </div>

      {/* Patient Header */}
      <div style={{
        background: "#1e3a5f",
        borderRadius: 14,
        padding: "24px 28px",
        marginBottom: 24,
        color: "#fff",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        flexWrap: "wrap",
        gap: 16,
      }}>
        <div style={{ display: "flex", gap: 20, alignItems: "flex-start" }}>
          {/* Avatar */}
          <div style={{
            width: 64,
            height: 64,
            borderRadius: "50%",
            background: "rgba(255,255,255,0.15)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 24,
            fontWeight: 700,
            flexShrink: 0,
          }}>
            {patient.first_name[0]}{patient.last_name[0]}
          </div>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 4 }}>
              <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700 }}>
                {patient.first_name} {patient.last_name}
              </h1>
              <button
                onClick={() => setEditOpen(true)}
                style={{
                  padding: "4px 12px", borderRadius: 6,
                  border: "1px solid rgba(255,255,255,0.4)",
                  background: "rgba(255,255,255,0.15)",
                  color: "#fff", fontSize: 12, cursor: "pointer", fontWeight: 500,
                }}
              >
                Edit
              </button>
            </div>
            <div style={{ fontSize: 14, opacity: 0.8, marginBottom: 8 }}>
              {patient.gender} • {age} years • DOB: {formatDate(patient.date_of_birth)} • MRN: {patient.mrn}
            </div>
            {patient.primary_diagnosis && (
              <div style={{ fontSize: 13, opacity: 0.9, fontStyle: "italic" }}>
                Dx: {patient.primary_diagnosis}
              </div>
            )}
            {patient.primary_physician && (
              <div style={{ fontSize: 13, opacity: 0.7, marginTop: 4 }}>
                Physician: {patient.primary_physician}
              </div>
            )}
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 10, alignItems: "flex-end" }}>
          {risk ? (
            <div>
              <RiskBadge level={risk.risk_level} score={risk.risk_score} size="lg" />
            </div>
          ) : (
            <button
              onClick={runRiskAssessment}
              style={{
                background: "#fff",
                color: "#1e3a5f",
                border: "none",
                borderRadius: 8,
                padding: "8px 16px",
                cursor: "pointer",
                fontWeight: 600,
                fontSize: 13,
              }}
            >
              Run Risk Assessment
            </button>
          )}
          <div style={{ display: "flex", gap: 12, fontSize: 13, opacity: 0.8 }}>
            <span>{visits.length} visits</span>
            <span>{abnormalLabs.length} abnormal labs</span>
            <span>{pendingReminders.length} pending reminders</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 2, borderBottom: "2px solid #e2e8f0", marginBottom: 24 }}>
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              padding: "10px 18px",
              border: "none",
              background: "none",
              cursor: "pointer",
              fontSize: 14,
              fontWeight: activeTab === tab.key ? 600 : 400,
              color: activeTab === tab.key ? "#1e3a5f" : "#64748b",
              borderBottom: activeTab === tab.key ? "2px solid #1e3a5f" : "2px solid transparent",
              marginBottom: -2,
              transition: "all 0.15s",
            }}
          >
            {tab.label}
            {tab.key === "overview" && pendingReminders.length > 0 && (
              <span style={{
                marginLeft: 6, background: "#ef4444", color: "#fff",
                borderRadius: 10, padding: "1px 6px", fontSize: 11,
              }}>
                {pendingReminders.length}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === "overview" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          <Card title="Patient Information">
            <InfoRow label="Full Name" value={`${patient.first_name} ${patient.last_name}`} />
            <InfoRow label="MRN" value={patient.mrn} mono />
            <InfoRow label="Date of Birth" value={`${formatDate(patient.date_of_birth)} (Age ${age})`} />
            <InfoRow label="Gender" value={patient.gender} />
            {patient.phone && <InfoRow label="Phone" value={patient.phone} />}
            {patient.email && <InfoRow label="Email" value={patient.email} />}
            {patient.insurance_id && <InfoRow label="Insurance ID" value={patient.insurance_id} mono />}
            {patient.address && <InfoRow label="Address" value={patient.address} />}
            {patient.primary_physician && <InfoRow label="Primary Physician" value={patient.primary_physician} />}
          </Card>

          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            {risk && (
              <Card title="Risk Assessment">
                <div style={{ marginBottom: 12 }}>
                  <RiskBadge level={risk.risk_level} score={risk.risk_score} size="lg" />
                </div>
                <ul style={{ margin: 0, paddingLeft: 20 }}>
                  {risk.reasons.map((r, i) => (
                    <li key={i} style={{ fontSize: 13, color: "#475569", marginBottom: 4 }}>{r}</li>
                  ))}
                </ul>
                <button
                  onClick={runRiskAssessment}
                  style={{ marginTop: 12, fontSize: 12, color: "#3b82f6", background: "none", border: "none", cursor: "pointer", textDecoration: "underline" }}
                >
                  Re-assess risk
                </button>
              </Card>
            )}

            <Card title="Reminders" action={<button onClick={() => setAddReminderOpen(true)} style={{ padding: "4px 12px", borderRadius: 6, border: "1px solid #1e3a5f", background: "#fff", color: "#1e3a5f", fontSize: 12, fontWeight: 600, cursor: "pointer" }}>+ Add</button>}>
              <RemindersPanel reminders={reminders} onRefresh={loadData} />
            </Card>
          </div>
        </div>
      )}

      {activeTab === "visits" && (
        <Card title={`Visit Timeline (${visits.length} total)`}>
          <VisitTimeline visits={visits} />
        </Card>
      )}

      {activeTab === "labs" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <Card title="Lab Trends">
            <LabChart labs={labs} />
          </Card>
          <Card title={`Lab Results (${labs.length} total • ${abnormalLabs.length} abnormal)`}>
            <LabTable labs={labs} />
          </Card>
        </div>
      )}

      {activeTab === "vitals" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <Card title="Vitals Trends">
            <VitalChart vitals={vitals} />
          </Card>
          <Card title={`Vitals History (${vitals.length} records)`}>
            <VitalsTable vitals={vitals} />
          </Card>
        </div>
      )}

      {activeTab === "medications" && (
        <div style={{ display: "grid", gridTemplateColumns: "3fr 2fr", gap: 20 }}>
          <Card title="Medications">
            <MedicationSection medications={medications} />
          </Card>
          <Card title="Allergies">
            <AllergySection allergies={allergies} />
          </Card>
        </div>
      )}

      {activeTab === "summary" && (
        <Card title="AI-Ready Patient Summary">
          <DoctorSummary summary={summary} loading={summaryLoading} onRefresh={loadSummary} />
        </Card>
      )}
    </div>
  );
};

const Card: React.FC<{ title: string; children: React.ReactNode; action?: React.ReactNode }> = ({ title, children, action }) => (
  <div style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 12, overflow: "hidden" }}>
    <div style={{ padding: "14px 20px", borderBottom: "1px solid #f1f5f9", fontWeight: 600, fontSize: 15, color: "#1e293b", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      {title}
      {action}
    </div>
    <div style={{ padding: "18px 20px" }}>
      {children}
    </div>
  </div>
);

const InfoRow: React.FC<{ label: string; value: string; mono?: boolean }> = ({ label, value, mono }) => (
  <div style={{ display: "flex", justifyContent: "space-between", padding: "7px 0", borderBottom: "1px solid #f8fafc", fontSize: 13 }}>
    <span style={{ color: "#94a3b8" }}>{label}</span>
    <span style={{ color: "#334155", fontFamily: mono ? "monospace" : "inherit", fontWeight: 500 }}>{value}</span>
  </div>
);

const LabTable: React.FC<{ labs: LabResult[] }> = ({ labs }) => {
  const sorted = [...labs].sort((a, b) => new Date(b.test_date).getTime() - new Date(a.test_date).getTime());
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
        <thead>
          <tr style={{ background: "#f8fafc" }}>
            {["Date", "Test", "Value", "Unit", "Ref Range", "Status", "Ordered By"].map((h) => (
              <th key={h} style={{ padding: "8px 12px", textAlign: "left", color: "#64748b", fontWeight: 600, fontSize: 12 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((lab) => (
            <tr key={lab.id} style={{ borderBottom: "1px solid #f1f5f9" }}>
              <td style={{ padding: "8px 12px", color: "#475569" }}>{formatDate(lab.test_date)}</td>
              <td style={{ padding: "8px 12px", fontWeight: 500 }}>{lab.test_name}</td>
              <td style={{ padding: "8px 12px", color: lab.is_abnormal ? "#ef4444" : "#1e293b", fontWeight: lab.is_abnormal ? 700 : 400 }}>{lab.value}</td>
              <td style={{ padding: "8px 12px", color: "#94a3b8" }}>{lab.unit || "—"}</td>
              <td style={{ padding: "8px 12px", color: "#94a3b8" }}>
                {lab.reference_min !== undefined && lab.reference_max !== undefined
                  ? `${lab.reference_min} – ${lab.reference_max}`
                  : "—"}
              </td>
              <td style={{ padding: "8px 12px" }}>
                <span style={{
                  fontSize: 11,
                  fontWeight: 600,
                  color: lab.is_abnormal ? "#ef4444" : "#16a34a",
                  background: lab.is_abnormal ? "#fef2f2" : "#f0fdf4",
                  padding: "2px 8px",
                  borderRadius: 10,
                }}>
                  {lab.is_abnormal ? "Abnormal" : "Normal"}
                </span>
              </td>
              <td style={{ padding: "8px 12px", color: "#94a3b8" }}>{lab.ordered_by || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const VitalsTable: React.FC<{ vitals: Vital[] }> = ({ vitals }) => {
  const sorted = [...vitals].sort((a, b) => new Date(b.recorded_date).getTime() - new Date(a.recorded_date).getTime());
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
        <thead>
          <tr style={{ background: "#f8fafc" }}>
            {["Date", "BP", "HR", "Temp", "Weight", "BMI", "O₂ Sat", "RR"].map((h) => (
              <th key={h} style={{ padding: "8px 12px", textAlign: "left", color: "#64748b", fontWeight: 600, fontSize: 12 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((v) => {
            const bpHigh = v.systolic_bp && v.systolic_bp >= 140;
            return (
              <tr key={v.id} style={{ borderBottom: "1px solid #f1f5f9" }}>
                <td style={{ padding: "8px 12px", color: "#475569" }}>{formatDate(v.recorded_date)}</td>
                <td style={{ padding: "8px 12px", color: bpHigh ? "#ef4444" : "#1e293b", fontWeight: bpHigh ? 700 : 400 }}>
                  {v.systolic_bp && v.diastolic_bp ? `${v.systolic_bp}/${v.diastolic_bp}` : "—"}
                </td>
                <td style={{ padding: "8px 12px" }}>{v.heart_rate ? `${v.heart_rate} bpm` : "—"}</td>
                <td style={{ padding: "8px 12px" }}>{v.temperature ? `${v.temperature}°C` : "—"}</td>
                <td style={{ padding: "8px 12px" }}>{v.weight_kg ? `${v.weight_kg} kg` : "—"}</td>
                <td style={{ padding: "8px 12px" }}>{v.bmi || "—"}</td>
                <td style={{ padding: "8px 12px" }}>{v.oxygen_saturation ? `${v.oxygen_saturation}%` : "—"}</td>
                <td style={{ padding: "8px 12px" }}>{v.respiratory_rate ? `${v.respiratory_rate}/min` : "—"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default PatientProfile;
