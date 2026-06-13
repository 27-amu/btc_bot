import React from "react";
import { Allergy } from "../types";
import { getSeverityColor } from "../utils";

interface Props {
  allergies: Allergy[];
}

const AllergySection: React.FC<Props> = ({ allergies }) => {
  if (allergies.length === 0) {
    return (
      <div style={{
        background: "#f0fdf4",
        border: "1px solid #bbf7d0",
        borderRadius: 8,
        padding: "12px 16px",
        color: "#16a34a",
        fontSize: 14,
      }}>
        ✓ No known allergies documented
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {allergies.map((allergy) => {
        const color = getSeverityColor(allergy.severity || "");
        const isSerious = ["life-threatening", "severe"].includes(allergy.severity?.toLowerCase() || "");

        return (
          <div
            key={allergy.id}
            style={{
              background: isSerious ? "#fef2f2" : "#fffbeb",
              border: `1px solid ${isSerious ? "#fecaca" : "#fde68a"}`,
              borderLeft: `4px solid ${color}`,
              borderRadius: 8,
              padding: "12px 16px",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                {isSerious && <span style={{ fontSize: 16 }}>⚠️</span>}
                <span style={{ fontWeight: 700, fontSize: 14, color: "#1e293b" }}>{allergy.allergen}</span>
                {allergy.allergen_type && (
                  <span style={{
                    fontSize: 11,
                    textTransform: "uppercase",
                    color: "#64748b",
                    background: "#f1f5f9",
                    padding: "1px 6px",
                    borderRadius: 10,
                  }}>
                    {allergy.allergen_type}
                  </span>
                )}
              </div>
              {allergy.severity && (
                <span style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color,
                  textTransform: "capitalize",
                }}>
                  {allergy.severity}
                </span>
              )}
            </div>
            {allergy.reaction && (
              <div style={{ marginTop: 4, fontSize: 13, color: "#475569" }}>
                Reaction: {allergy.reaction}
              </div>
            )}
            {allergy.notes && (
              <div style={{ marginTop: 2, fontSize: 12, color: "#64748b" }}>{allergy.notes}</div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default AllergySection;
