import React, { useState } from "react";
import { patientsApi } from "../api/client";

interface Props {
  onClose: () => void;
  onCreated: () => void;
}

const GENDER_OPTIONS = ["Male", "Female", "Other", "Unknown"];

const AddPatientModal: React.FC<Props> = ({ onClose, onCreated }) => {
  const [form, setForm] = useState({
    mrn: "",
    first_name: "",
    last_name: "",
    date_of_birth: "",
    gender: "Male",
    phone: "",
    email: "",
    address: "",
    primary_diagnosis: "",
    primary_physician: "",
    insurance_id: "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = (key: string, value: string) =>
    setForm((f) => ({ ...f, [key]: value }));

  const handleSave = async () => {
    if (!form.mrn || !form.first_name || !form.last_name || !form.date_of_birth) {
      setError("MRN, first name, last name, and date of birth are required.");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      await patientsApi.create(form);
      onCreated();
      onClose();
    } catch (e: any) {
      const msg = e?.response?.data?.detail;
      setError(msg || "Failed to create patient. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      style={{ position: "fixed", inset: 0, zIndex: 1000, background: "rgba(0,0,0,0.45)", display: "flex", alignItems: "center", justifyContent: "center" }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div style={{ background: "#fff", borderRadius: 14, width: "100%", maxWidth: 580, maxHeight: "90vh", display: "flex", flexDirection: "column", boxShadow: "0 20px 60px rgba(0,0,0,0.2)" }}>
        {/* Header */}
        <div style={{ padding: "18px 24px", borderBottom: "1px solid #e2e8f0", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div style={{ fontWeight: 700, fontSize: 16, color: "#1e293b" }}>Add New Patient</div>
            <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 2 }}>Fields marked * are required</div>
          </div>
          <button onClick={onClose} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#94a3b8" }}>×</button>
        </div>

        {/* Form */}
        <div style={{ padding: "20px 24px", overflowY: "auto", flex: 1 }}>
          <Section title="Identity">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px 16px" }}>
              <Field label="MRN *" value={form.mrn} onChange={(v) => set("mrn", v)} placeholder="e.g. CT-000011" />
              <div />
              <Field label="First Name *" value={form.first_name} onChange={(v) => set("first_name", v)} />
              <Field label="Last Name *" value={form.last_name} onChange={(v) => set("last_name", v)} />
              <Field label="Date of Birth *" type="date" value={form.date_of_birth} onChange={(v) => set("date_of_birth", v)} />
              <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                <label style={labelStyle}>Gender *</label>
                <select value={form.gender} onChange={(e) => set("gender", e.target.value)} style={inputStyle}>
                  {GENDER_OPTIONS.map((g) => <option key={g} value={g}>{g}</option>)}
                </select>
              </div>
            </div>
          </Section>

          <Section title="Contact">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px 16px" }}>
              <Field label="Phone" value={form.phone} onChange={(v) => set("phone", v)} placeholder="+1 (555) 000-0000" />
              <Field label="Email" type="email" value={form.email} onChange={(v) => set("email", v)} />
              <div style={{ gridColumn: "1 / -1" }}>
                <Field label="Address" value={form.address} onChange={(v) => set("address", v)} />
              </div>
            </div>
          </Section>

          <Section title="Clinical">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px 16px" }}>
              <div style={{ gridColumn: "1 / -1" }}>
                <Field label="Primary Diagnosis" value={form.primary_diagnosis} onChange={(v) => set("primary_diagnosis", v)} placeholder="e.g. Type 2 Diabetes, Hypertension" />
              </div>
              <Field label="Primary Physician" value={form.primary_physician} onChange={(v) => set("primary_physician", v)} placeholder="e.g. Dr. Sarah Chen" />
              <Field label="Insurance ID" value={form.insurance_id} onChange={(v) => set("insurance_id", v)} />
            </div>
          </Section>

          {error && (
            <div style={{ marginTop: 8, padding: "10px 14px", background: "#fef2f2", border: "1px solid #fecaca", borderRadius: 8, color: "#dc2626", fontSize: 13 }}>
              {error}
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ padding: "14px 24px", borderTop: "1px solid #e2e8f0", display: "flex", justifyContent: "flex-end", gap: 10 }}>
          <button onClick={onClose} style={secondaryBtn}>Cancel</button>
          <button onClick={handleSave} disabled={saving} style={primaryBtn(saving)}>
            {saving ? "Creating…" : "Create Patient"}
          </button>
        </div>
      </div>
    </div>
  );
};

const Section: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <div style={{ marginBottom: 20 }}>
    <div style={{ fontSize: 11, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 10 }}>{title}</div>
    {children}
  </div>
);

const Field: React.FC<{ label: string; value: string; onChange: (v: string) => void; type?: string; placeholder?: string }> = ({ label, value, onChange, type, placeholder }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
    <label style={labelStyle}>{label}</label>
    <input
      type={type || "text"}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      style={inputStyle}
      onFocus={(e) => { e.currentTarget.style.borderColor = "#3b82f6"; e.currentTarget.style.background = "#fff"; }}
      onBlur={(e) => { e.currentTarget.style.borderColor = "#e2e8f0"; e.currentTarget.style.background = "#f8fafc"; }}
    />
  </div>
);

const labelStyle: React.CSSProperties = { fontSize: 12, fontWeight: 600, color: "#64748b", textTransform: "uppercase" as const, letterSpacing: "0.04em" };
const inputStyle: React.CSSProperties = { padding: "8px 12px", borderRadius: 8, border: "1px solid #e2e8f0", fontSize: 14, color: "#1e293b", background: "#f8fafc", width: "100%", boxSizing: "border-box" as const };
const secondaryBtn: React.CSSProperties = { padding: "8px 20px", borderRadius: 8, border: "1px solid #e2e8f0", background: "#fff", color: "#64748b", fontSize: 14, cursor: "pointer", fontWeight: 500 };
const primaryBtn = (disabled: boolean): React.CSSProperties => ({ padding: "8px 20px", borderRadius: 8, border: "none", background: disabled ? "#93c5fd" : "#1e3a5f", color: "#fff", fontSize: 14, cursor: disabled ? "not-allowed" : "pointer", fontWeight: 600 });

export default AddPatientModal;
