export function calculateAge(dob: string): number {
  const today = new Date();
  const birth = new Date(dob);
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
  return age;
}

export function formatDate(dateStr: string): string {
  if (!dateStr) return "N/A";
  return new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function formatDateTime(dateStr: string): string {
  if (!dateStr) return "N/A";
  return new Date(dateStr).toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function daysUntil(dateStr: string): number {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const target = new Date(dateStr);
  target.setHours(0, 0, 0, 0);
  return Math.round((target.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
}

export function getRiskColor(level: string): string {
  switch (level?.toLowerCase()) {
    case "high": return "#dc2626";
    case "medium": return "#d97706";
    case "low": return "#16a34a";
    default: return "#6b7280";
  }
}

export function getRiskBg(level: string): string {
  switch (level?.toLowerCase()) {
    case "high": return "#fef2f2";
    case "medium": return "#fffbeb";
    case "low": return "#f0fdf4";
    default: return "#f9fafb";
  }
}

export function getSeverityColor(severity: string): string {
  switch (severity?.toLowerCase()) {
    case "life-threatening": return "#7f1d1d";
    case "severe": return "#dc2626";
    case "moderate": return "#d97706";
    case "mild": return "#16a34a";
    default: return "#6b7280";
  }
}
