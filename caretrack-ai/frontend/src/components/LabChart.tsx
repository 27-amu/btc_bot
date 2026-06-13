import React, { useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, ReferenceLine, Legend,
} from "recharts";
import { LabResult } from "../types";
import { formatDate } from "../utils";

interface Props {
  labs: LabResult[];
}

const CHART_TESTS = [
  "HbA1c", "Fasting Glucose", "Creatinine", "eGFR",
  "Total Cholesterol", "LDL Cholesterol", "HDL Cholesterol",
  "Hemoglobin", "ALT", "AST",
];

const COLORS = [
  "#3b82f6", "#ef4444", "#10b981", "#f59e0b",
  "#8b5cf6", "#06b6d4", "#84cc16", "#f97316",
];

const LabChart: React.FC<Props> = ({ labs }) => {
  const available = Array.from(new Set(labs.map((l) => l.test_name)))
    .filter((name) => CHART_TESTS.includes(name) || labs.filter((l) => l.test_name === name).length >= 2)
    .slice(0, 8);

  const [selected, setSelected] = useState<string>(available[0] || "");

  const testLabs = labs
    .filter((l) => l.test_name === selected)
    .sort((a, b) => new Date(a.test_date).getTime() - new Date(b.test_date).getTime());

  const chartData = testLabs.map((l) => ({
    date: formatDate(l.test_date),
    value: l.value,
    unit: l.unit,
    abnormal: l.is_abnormal,
    refMin: l.reference_min,
    refMax: l.reference_max,
  }));

  const refMin = testLabs[0]?.reference_min;
  const refMax = testLabs[0]?.reference_max;
  const unit = testLabs[0]?.unit || "";

  const CustomDot = (props: any) => {
    const { cx, cy, payload } = props;
    if (!cx || !cy) return null;
    return (
      <circle
        cx={cx}
        cy={cy}
        r={5}
        fill={payload.abnormal ? "#ef4444" : "#3b82f6"}
        stroke="#fff"
        strokeWidth={2}
      />
    );
  };

  return (
    <div>
      {/* Test selector */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        {available.map((name, i) => (
          <button
            key={name}
            onClick={() => setSelected(name)}
            style={{
              padding: "5px 12px",
              borderRadius: 20,
              border: selected === name ? `2px solid ${COLORS[i % COLORS.length]}` : "1px solid #e2e8f0",
              background: selected === name ? `${COLORS[i % COLORS.length]}15` : "#fff",
              color: selected === name ? COLORS[i % COLORS.length] : "#64748b",
              fontSize: 12,
              fontWeight: selected === name ? 600 : 400,
              cursor: "pointer",
            }}
          >
            {name}
          </button>
        ))}
      </div>

      {chartData.length < 2 ? (
        <div style={{ textAlign: "center", color: "#94a3b8", padding: "40px 0", fontSize: 14 }}>
          Not enough data points to chart {selected || "this test"}.
        </div>
      ) : (
        <>
          <div style={{ display: "flex", gap: 16, marginBottom: 8, fontSize: 12, color: "#64748b" }}>
            {refMin !== undefined && refMax !== undefined && (
              <span>Reference range: {refMin} – {refMax} {unit}</span>
            )}
            <span style={{ display: "flex", gap: 4, alignItems: "center" }}>
              <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#ef4444", display: "inline-block" }} />
              Abnormal
            </span>
            <span style={{ display: "flex", gap: 4, alignItems: "center" }}>
              <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#3b82f6", display: "inline-block" }} />
              Normal
            </span>
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} unit={unit ? ` ${unit}` : ""} />
              <Tooltip
                formatter={(value: number) => [`${value} ${unit}`, selected]}
                contentStyle={{ fontSize: 12, borderRadius: 8 }}
              />
              {refMin !== undefined && (
                <ReferenceLine y={refMin} stroke="#10b981" strokeDasharray="4 2" label={{ value: "Min", fontSize: 10, fill: "#10b981" }} />
              )}
              {refMax !== undefined && (
                <ReferenceLine y={refMax} stroke="#f59e0b" strokeDasharray="4 2" label={{ value: "Max", fontSize: 10, fill: "#f59e0b" }} />
              )}
              <Line
                type="monotone"
                dataKey="value"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={<CustomDot />}
                activeDot={{ r: 7 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
};

export default LabChart;
