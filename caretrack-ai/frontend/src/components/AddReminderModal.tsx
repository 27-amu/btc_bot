import React, { useState } from "react";
import { remindersApi } from "../api/client";

interface Props {
  patientId: number;
  onClose: () => void;
  onCreated: () => void;
}

const REMINDER_TYPES = ["follow-up", "lab", "medication", "screening", "other"];

const AddReminderModal: React.FC<Props> = ({ patientId, onClose, onCreated }) => {
  const today = new Date().toISOString().split("T")[0];
  const [form, setForm] = useState({
    reminder_type: "follow-up",
    due_date: today,
    description: "",
    priority: "medium",
    assigned_to: "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = (key: string, value: string) => setForm((f) => ({ ...f, [key]: value }));

  const handleSave = async () => {
    if (!form.due_date) {
      setError("Due date is required.");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      await remindersApi.create({ ...form, patient_id: patientId });
      onCreated();
      onClose();
    } catch (e: any) {
      const msg = e?.response?.data?.detail;
      setError(msg || "Failed to create reminder.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      style={{ position: "fixed", inset: 0, zIndex: 1000, background: "rgba(0,0,0,0.45)", display: "flex", alignItems: "center", justifyContent: "center" }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div style={{ background: "#fff", borderRadius: 14, width: "100%", maxWidth: 460, display: "flex", flexDirection: "column", boxShadow: "0 20px 60px rgba(0,0,0,0.2)" }}>
        {/* Header */}
        <div style={{ padding: "18px 24px", borderBottom: "1px solid #e2e8f0", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ fontWeight: 700, fontSize: 16, color: "#1e293b" }}>Add Reminder</div>
          <button onClick={onClose} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#94a3b8" }}>×</button>
        </div>

        {/* Form */}
        <div style={{ padding: "20px 24px", display: "flex", flexDirection: "column", gap: 14 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px 16px" }}>
            <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
              <label style={labelStyle}>Type</label>
              <select value={form.reminder_type} onChange={(e) => set("reminder_type", e.target.value)} style={inputStyle}>
                {REMINDER_TYPES.map((t) => (
                  <option key={t} value={t} style={{ textTransform: "capitalize" }}>{t}</option>
                ))}
              </select>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
              <label style={labelStyle}>Priority</label>
              <select value={form.priority} onChange={(e) => set("priority", e.target.value)} style={inputStyle}>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 4, gridColumn: "1 / -1" }}>
              <label style={labelStyle}>Due Date *</label>
              <input type="date" value={form.due_date} onChange={(e) => set("due_date", e.target.value)} style={inputStyle} />
            </div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            <label style={labelStyle}>Description</label>
            <textarea
              value={form.description}
              onChange={(e) => set("description", e.target.value)}
              placeholder="Optional notes about this reminder…"
              rows={3}
              style={{ ...inputStyle, resize: "vertical", fontFamily: "inherit" }}
            />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            <label style={labelStyle}>Assigned To</label>
            <input
              type="text"
              value={form.assigned_to}
              onChange={(e) => set("assigned_to", e.target.value)}
              placeholder="e.g. Dr. Sarah Chen"
              style={inputStyle}
            />
          </div>

          {error && (
            <div style={{ padding: "10px 14px", background: "#fef2f2", border: "1px solid #fecaca", borderRadius: 8, color: "#dc2626", fontSize: 13 }}>
              {error}
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ padding: "14px 24px", borderTop: "1px solid #e2e8f0", display: "flex", justifyContent: "flex-end", gap: 10 }}>
          <button onClick={onClose} style={secondaryBtn}>Cancel</button>
          <button onClick={handleSave} disabled={saving} style={primaryBtn(saving)}>
            {saving ? "Adding…" : "Add Reminder"}
          </button>
        </div>
      </div>
    </div>
  );
};

const labelStyle: React.CSSProperties = { fontSize: 12, fontWeight: 600, color: "#64748b", textTransform: "uppercase" as const, letterSpacing: "0.04em" };
const inputStyle: React.CSSProperties = { padding: "8px 12px", borderRadius: 8, border: "1px solid #e2e8f0", fontSize: 14, color: "#1e293b", background: "#f8fafc", width: "100%", boxSizing: "border-box" as const };
const secondaryBtn: React.CSSProperties = { padding: "8px 20px", borderRadius: 8, border: "1px solid #e2e8f0", background: "#fff", color: "#64748b", fontSize: 14, cursor: "pointer", fontWeight: 500 };
const primaryBtn = (disabled: boolean): React.CSSProperties => ({ padding: "8px 20px", borderRadius: 8, border: "none", background: disabled ? "#93c5fd" : "#1e3a5f", color: "#fff", fontSize: 14, cursor: disabled ? "not-allowed" : "pointer", fontWeight: 600 });

export default AddReminderModal;
