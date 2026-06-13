import React, { useState } from "react";
import { Reminder } from "../types";
import { formatDate, daysUntil } from "../utils";
import { remindersApi } from "../api/client";

interface Props {
  reminders: Reminder[];
  onRefresh: () => void;
}

const PRIORITY_COLORS: Record<string, string> = {
  high: "#ef4444",
  medium: "#f59e0b",
  low: "#10b981",
};

const TYPE_ICONS: Record<string, string> = {
  "follow-up": "📅",
  lab: "🧪",
  medication: "💊",
  screening: "🔍",
};

interface EditState {
  due_date: string;
  description: string;
  priority: string;
}

const RemindersPanel: React.FC<Props> = ({ reminders, onRefresh }) => {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<EditState>({ due_date: "", description: "", priority: "medium" });
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const pending = reminders.filter((r) => !r.is_completed);
  const completed = reminders.filter((r) => r.is_completed);
  const overdue = pending.filter((r) => daysUntil(r.due_date) < 0);
  const upcoming = pending.filter((r) => daysUntil(r.due_date) >= 0);

  const handleComplete = async (id: number) => {
    try {
      await remindersApi.update(id, { is_completed: true, completed_at: new Date().toISOString() });
      onRefresh();
    } catch (e) {
      console.error("Failed to mark reminder complete", e);
    }
  };

  const handleDelete = async (id: number) => {
    setDeletingId(id);
    try {
      await remindersApi.delete(id);
      onRefresh();
    } catch (e) {
      console.error("Failed to delete reminder", e);
    } finally {
      setDeletingId(null);
    }
  };

  const openEdit = (r: Reminder) => {
    setEditingId(r.id);
    setEditForm({
      due_date: r.due_date,
      description: r.description ?? "",
      priority: r.priority,
    });
  };

  const handleSave = async (id: number) => {
    setSaving(true);
    try {
      await remindersApi.update(id, {
        due_date: editForm.due_date,
        description: editForm.description || null,
        priority: editForm.priority,
      });
      setEditingId(null);
      onRefresh();
    } catch (e) {
      console.error("Failed to update reminder", e);
    } finally {
      setSaving(false);
    }
  };

  const ReminderItem = (r: Reminder) => {
    const days = daysUntil(r.due_date);
    const isOverdue = days < 0;
    const priorityColor = PRIORITY_COLORS[r.priority] || "#6b7280";
    const isEditing = editingId === r.id;
    const isDeleting = deletingId === r.id;

    return (
      <div
        key={r.id}
        style={{
          background: r.is_completed ? "#f8fafc" : isOverdue ? "#fef2f2" : "#f8fafc",
          border: `1px solid ${r.is_completed ? "#e2e8f0" : isOverdue ? "#fecaca" : "#e2e8f0"}`,
          borderLeft: `3px solid ${r.is_completed ? "#cbd5e1" : priorityColor}`,
          borderRadius: 8,
          padding: "10px 14px",
          opacity: r.is_completed ? 0.7 : 1,
        }}
      >
        {/* Main row */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
          <div style={{ flex: 1 }}>
            <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 4 }}>
              <span style={{ fontSize: 14 }}>{TYPE_ICONS[r.reminder_type] || "📋"}</span>
              <span style={{ fontWeight: 600, fontSize: 13, color: "#1e293b", textTransform: "capitalize" }}>
                {r.reminder_type}
              </span>
              <span style={{ fontSize: 11, fontWeight: 600, color: r.is_completed ? "#94a3b8" : priorityColor, textTransform: "uppercase" }}>
                {r.priority}
              </span>
            </div>
            {!isEditing && r.description && (
              <p style={{ margin: "0 0 4px", fontSize: 12, color: "#475569" }}>{r.description}</p>
            )}
            {!isEditing && (
              <div style={{ fontSize: 12, color: r.is_completed ? "#94a3b8" : isOverdue ? "#ef4444" : "#64748b", fontWeight: isOverdue && !r.is_completed ? 600 : 400 }}>
                {r.is_completed
                  ? `Completed • was due ${formatDate(r.due_date)}`
                  : isOverdue
                  ? `Overdue by ${Math.abs(days)} days (due ${formatDate(r.due_date)})`
                  : `Due ${formatDate(r.due_date)} (in ${days} days)`}
              </div>
            )}
          </div>

          {/* Action buttons */}
          <div style={{ display: "flex", gap: 6, flexShrink: 0 }}>
            {!r.is_completed && !isEditing && (
              <>
                <button
                  onClick={() => handleComplete(r.id)}
                  title="Mark as completed"
                  style={btnStyle("#10b981", "#f0fdf4")}
                >
                  ✓ Done
                </button>
                <button
                  onClick={() => openEdit(r)}
                  title="Edit reminder"
                  style={btnStyle("#3b82f6", "#eff6ff")}
                >
                  Edit
                </button>
              </>
            )}
            <button
              onClick={() => handleDelete(r.id)}
              disabled={isDeleting}
              title="Delete reminder"
              style={btnStyle("#ef4444", "#fef2f2")}
            >
              {isDeleting ? "…" : "Delete"}
            </button>
          </div>
        </div>

        {/* Inline edit form */}
        {isEditing && (
          <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid #e2e8f0", display: "flex", flexDirection: "column", gap: 10 }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
              <div>
                <label style={labelStyle}>Due Date</label>
                <input
                  type="date"
                  value={editForm.due_date}
                  onChange={(e) => setEditForm((f) => ({ ...f, due_date: e.target.value }))}
                  style={inputStyle}
                />
              </div>
              <div>
                <label style={labelStyle}>Priority</label>
                <select
                  value={editForm.priority}
                  onChange={(e) => setEditForm((f) => ({ ...f, priority: e.target.value }))}
                  style={inputStyle}
                >
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>
            </div>
            <div>
              <label style={labelStyle}>Description</label>
              <input
                type="text"
                value={editForm.description}
                onChange={(e) => setEditForm((f) => ({ ...f, description: e.target.value }))}
                placeholder="Optional description"
                style={{ ...inputStyle, width: "100%" }}
              />
            </div>
            <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
              <button onClick={() => setEditingId(null)} style={btnStyle("#64748b", "#f1f5f9")}>Cancel</button>
              <button
                onClick={() => handleSave(r.id)}
                disabled={saving}
                style={{ ...btnStyle("#fff", "#1e3a5f"), color: "#fff", border: "none" }}
              >
                {saving ? "Saving…" : "Save"}
              </button>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div>
      {pending.length === 0 && completed.length === 0 ? (
        <div style={{ background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: 8, padding: 16, textAlign: "center", color: "#16a34a", fontSize: 14 }}>
          ✓ No reminders
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {overdue.length > 0 && (
            <div>
              <h4 style={{ margin: "0 0 8px", fontSize: 13, color: "#ef4444", fontWeight: 600, textTransform: "uppercase" }}>
                ⚠ Overdue ({overdue.length})
              </h4>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {overdue.map((r) => <ReminderItem key={r.id} {...r} />)}
              </div>
            </div>
          )}

          {upcoming.length > 0 && (
            <div>
              {overdue.length > 0 && (
                <h4 style={{ margin: "0 0 8px", fontSize: 13, color: "#475569", fontWeight: 600, textTransform: "uppercase" }}>
                  Upcoming ({upcoming.length})
                </h4>
              )}
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {upcoming.map((r) => <ReminderItem key={r.id} {...r} />)}
              </div>
            </div>
          )}

          {completed.length > 0 && (
            <details>
              <summary style={{ fontSize: 13, color: "#94a3b8", cursor: "pointer", userSelect: "none", marginBottom: 8 }}>
                Completed ({completed.length})
              </summary>
              <div style={{ display: "flex", flexDirection: "column", gap: 8, marginTop: 8 }}>
                {completed.map((r) => <ReminderItem key={r.id} {...r} />)}
              </div>
            </details>
          )}
        </div>
      )}
    </div>
  );
};

const btnStyle = (color: string, bg: string): React.CSSProperties => ({
  padding: "5px 10px",
  borderRadius: 6,
  border: `1px solid ${color}40`,
  background: bg,
  color: color,
  fontSize: 12,
  fontWeight: 500,
  cursor: "pointer",
  flexShrink: 0,
});

const labelStyle: React.CSSProperties = {
  display: "block",
  fontSize: 11,
  fontWeight: 600,
  color: "#64748b",
  textTransform: "uppercase",
  letterSpacing: "0.04em",
  marginBottom: 4,
};

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "6px 10px",
  borderRadius: 6,
  border: "1px solid #e2e8f0",
  fontSize: 13,
  color: "#1e293b",
  background: "#f8fafc",
  boxSizing: "border-box",
};

export default RemindersPanel;
