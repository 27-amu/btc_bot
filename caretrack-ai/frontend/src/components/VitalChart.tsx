import React, { useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, ReferenceLine,
} from "recharts";
import { Vital } from "../types";
import { formatDate } from "../utils";

interface Props {
  vitals: Vital[];
}

type VitalKey = "bp" | "heart_rate" | "bmi" | "oxygen_saturation" | "weight_kg";

const VITAL_OPTIONS: { key: VitalKey; label: string; unit: string; color: string; refMin?: number; refMax?: number }[] = [
  { key: "bp", label: "Blood Pressure", unit: "mmHg", color: "#ef4444", refMin: 90, refMax: 140 },
  { key: "heart_rate", label: "Heart Rate", unit: "bpm", color: "#f59e0b", refMin: 60, refMax: 100 },
  { key: "bmi", label: "BMI", unit: "kg/m²", color: "#8b5cf6", refMin: 18.5, refMax: 24.9 },
  { key: "oxygen_saturation", label: "O₂ Saturation", unit: "%", color: "#06b6d4", refMin: 95, refMax: 100 },
  { key: "weight_kg", label: "Weight", unit: "kg", color: "#10b981" },
];

const VitalChart: React.FC<Props> = ({ vitals }) => {
  const [selected, setSelected] = useState<VitalKey>("bp");

  const sorted = [...vitals].sort(
    (a, b) => new Date(a.recorded_date).getTime() - new Date(b.recorded_date).getTime()
  );

  const option = VITAL_OPTIONS.find((o) => o.key === selected)!;

  const chartData = sorted.map((v) => {
    if (selected === "bp") {
      return {
        date: formatDate(v.recorded_date),
        systolic: v.systolic_bp,
        diastolic: v.diastolic_bp,
      };
    }
    return {
      date: formatDate(v.recorded_date),
      value: (v as any)[selected],
    };
  });

  return (
    <div>
      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        {VITAL_OPTIONS.map((opt) => (
          <button
            key={opt.key}
            onClick={() => setSelected(opt.key)}
            style={{
              padding: "5px 12px",
              borderRadius: 20,
              border: selected === opt.key ? `2px solid ${opt.color}` : "1px solid #e2e8f0",
              background: selected === opt.key ? `${opt.color}15` : "#fff",
              color: selected === opt.key ? opt.color : "#64748b",
              fontSize: 12,
              fontWeight: selected === opt.key ? 600 : 400,
              cursor: "pointer",
            }}
          >
            {opt.label}
          </button>
        ))}
      </div>

      <ResponsiveContainer width="100%" height={240}>
        <LineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey="date" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} unit={option.unit ? ` ${option.unit}` : ""} />
          <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8 }} />
          {option.refMax && <ReferenceLine y={option.refMax} stroke="#ef4444" strokeDasharray="4 2" />}
          {option.refMin && <ReferenceLine y={option.refMin} stroke="#10b981" strokeDasharray="4 2" />}

          {selected === "bp" ? (
            <>
              <Line type="monotone" dataKey="systolic" stroke="#ef4444" strokeWidth={2} dot={{ r: 4 }} name="Systolic" />
              <Line type="monotone" dataKey="diastolic" stroke="#f97316" strokeWidth={2} dot={{ r: 4 }} name="Diastolic" />
            </>
          ) : (
            <Line type="monotone" dataKey="value" stroke={option.color} strokeWidth={2} dot={{ r: 4 }} name={option.label} />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default VitalChart;
