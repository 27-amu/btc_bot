import React from "react";
import { Link, useLocation } from "react-router-dom";

interface Props {
  children: React.ReactNode;
}

const Layout: React.FC<Props> = ({ children }) => {
  const location = useLocation();

  return (
    <div style={{ minHeight: "100vh", background: "#f1f5f9", fontFamily: "'Inter', system-ui, sans-serif" }}>
      {/* Header */}
      <header style={{
        background: "#1e3a5f",
        color: "#fff",
        padding: "0 32px",
        height: 60,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}>
        <Link to="/" style={{ textDecoration: "none", color: "inherit", display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 22, fontWeight: 700, letterSpacing: "-0.5px" }}>
            &#9877; CareTrack AI
          </span>
          <span style={{
            fontSize: 10,
            background: "#ef4444",
            padding: "2px 6px",
            borderRadius: 4,
            fontWeight: 600,
            letterSpacing: "0.05em",
          }}>
            DEMO
          </span>
        </Link>
        <nav style={{ display: "flex", gap: 8 }}>
          <NavLink to="/" label="Dashboard" current={location.pathname === "/"} />
        </nav>
        <div style={{ fontSize: 12, opacity: 0.7, textAlign: "right" }}>
          Synthetic data only • Not for clinical use
        </div>
      </header>

      {/* Main */}
      <main style={{ maxWidth: 1400, margin: "0 auto", padding: "24px 24px" }}>
        {children}
      </main>

      {/* Footer */}
      <footer style={{
        textAlign: "center",
        padding: "16px",
        fontSize: 12,
        color: "#94a3b8",
        borderTop: "1px solid #e2e8f0",
        marginTop: 40,
        background: "#fff",
      }}>
        CareTrack AI — Portfolio Demo | All data is synthetic |{" "}
        <strong>NOT a certified medical device</strong> | Do not use with real PHI
      </footer>
    </div>
  );
};

const NavLink: React.FC<{ to: string; label: string; current: boolean }> = ({ to, label, current }) => (
  <Link
    to={to}
    style={{
      color: current ? "#fff" : "rgba(255,255,255,0.7)",
      textDecoration: "none",
      padding: "6px 14px",
      borderRadius: 6,
      fontSize: 14,
      fontWeight: current ? 600 : 400,
      background: current ? "rgba(255,255,255,0.15)" : "transparent",
    }}
  >
    {label}
  </Link>
);

export default Layout;
