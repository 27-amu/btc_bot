import React, { useState } from "react";
import { Patient } from "../types";
import { patientsApi } from "../api/client";

interface Props {
  patient: Patient;
  onClose: () => void;
  onSaved: (updated: Patient) => void;
}

const FIELDS: { key: keyof Patient; label: string; type?: string }[] = [
  { key: "first_name", label: "First Name" },
  { key: "last_name", label: "Last Name" },
  { key: "date_of_birth", label: "Date of Birth", type: "date" },
  { key: "gender", label: "Gender" },
  { key: "phone", label: "Phone" },
  { key: "email", label: "Email", type: "email" },
  { key: "address", label: "Address" },
  { key: "primary_diagnosis", label: "Primary Diagnosis" },
  { key: "primary_physician", label: "Primary Physician" },
  { key: "insurance_id", label: "Insurance ID" },
];

const EditPatientModal: React.FC<Props> = ({ patient, onClose, onSaved }) => {
  const [form, setForm] = useState<Partial<Patient>>({
    first_name: patient.first_name,
    last_name: patient.last_name,
    date_of_birth: patient.date_of_birth,
    gender: patient.gender,
    phone: patient.phone ?? "",
    email: patient.email ?? "",
    address: patient.address ?? "",
    primary_diagnosis: patient.primary_diagnosis ?? "",
    primary_physician: patient.primary_physician ?? "",
    insurance_id: patient.insurance_id ?? "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (key: keyof Patient, value: string) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      const resp = await patientsApi.update(patient.id, form);
      onSaved(resp.data);
      onClose();
    } catch {
      setError("Failed to save changes. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      style={{
        position: "fixed", inset: 0, zIndex: 1000,
        background: "rgba(0,0,0,0.45)",
        display: "flex", alignItems: "center", justifyContent: "center",
      }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div style={{
        background: "#fff", borderRadius: 14, width: "100%", maxWidth: 560,
        maxHeight: "90vh", display: "flex", flexDirection: "column",
        boxShadow: "0 20px 60px rgba(0,0,0,0.2)",
      }}>
        {/* Header */}
        <div style={{
          padding: "18px 24px", borderBottom: "1px solid #e2e8f0",
          display: "flex", justifyContent: "space-between", alignItems: "center",
        }}>
          <div>
            <div style={{ fontWeight: 700, fontSize: 16, color: "#1e293b" }}>Edit Patient</div>
            <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 2 }}>MRN: {patient.mrn}</div>
          </div>
          <button
            onClick={onClose}
            style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#94a3b8", lineHeight: 1 }}
          >
            ×
          </button>
        </div>

        {/* Form */}
        <div style={{ padding: "20px 24px", overflowY: "auto", flex: 1 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "14px 16px" }}>
            {FIELDS.map(({ key, label, type }) => (
              <div key={key} style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                <label style={{ fontSize: 12, fontWeight: 600, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.04em" }}>
                  {label}
                </label>
                <input
                  type={type || "text"}
                  value={(form[key] as string) ?? ""}
                  onChange={(e) => handleChange(key, e.target.value)}
                  style={{
                    padding: "8px 12px", borderRadius: 8,
                    border: "1px solid #e2e8f0", fontSize: 14,
                    color: "#1e293b", outline: "none",
                    background: "#f8fafc",
                  }}
                  onFocus={(e) => { e.currentTarget.style.borderColor = "#3b82f6"; e.currentTarget.style.background = "#fff"; }}
                  onBlur={(e) => { e.currentTarget.style.borderColor = "#e2e8f0"; e.currentTarget.style.background = "#f8fafc"; }}
                />
              </div>
            ))}
          </div>

          {error && (
            <div style={{
              marginTop: 16, padding: "10px 14px",
              background: "#fef2f2", border: "1px solid #fecaca",
              borderRadius: 8, color: "#dc2626", fontSize: 13,
            }}>
              {error}
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{
          padding: "14px 24px", borderTop: "1px solid #e2e8f0",
          display: "flex", justifyContent: "flex-end", gap: 10,
        }}>
          <button
            onClick={onClose}
            style={{
              padding: "8px 20px", borderRadius: 8,
              border: "1px solid #e2e8f0", background: "#fff",
              color: "#64748b", fontSize: 14, cursor: "pointer", fontWeight: 500,
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            style={{
              padding: "8px 20px", borderRadius: 8, border: "none",
              background: saving ? "#93c5fd" : "#1e3a5f",
              color: "#fff", fontSize: 14, cursor: saving ? "not-allowed" : "pointer",
              fontWeight: 600,
            }}
          >
            {saving ? "Saving…" : "Save Changes"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditPatientModal;
