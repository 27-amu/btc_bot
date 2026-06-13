import React from "react";
import { getRiskColor, getRiskBg } from "../utils";

interface Props {
  level: string;
  score?: number;
  size?: "sm" | "md" | "lg";
}

const RiskBadge: React.FC<Props> = ({ level, score, size = "md" }) => {
  const color = getRiskColor(level);
  const bg = getRiskBg(level);

  const padding = size === "sm" ? "2px 8px" : size === "lg" ? "6px 16px" : "4px 12px";
  const fontSize = size === "sm" ? "11px" : size === "lg" ? "15px" : "13px";

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "4px",
        background: bg,
        color,
        border: `1px solid ${color}`,
        borderRadius: "20px",
        padding,
        fontSize,
        fontWeight: 600,
        letterSpacing: "0.02em",
        textTransform: "uppercase",
      }}
    >
      <span
        style={{
          width: size === "sm" ? 6 : 8,
          height: size === "sm" ? 6 : 8,
          borderRadius: "50%",
          background: color,
          display: "inline-block",
        }}
      />
      {level}
      {score !== undefined && (
        <span style={{ fontSize: "0.85em", opacity: 0.8, fontWeight: 400 }}>
          {" "}({score})
        </span>
      )}
    </span>
  );
};

export default RiskBadge;
