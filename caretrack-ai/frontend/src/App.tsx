import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import PatientProfile from "./pages/PatientProfile";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/patients/:id" element={<PatientProfile />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;
