import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

export const patientsApi = {
  list: (search?: string, physician?: string) =>
    api.get("/patients/", { params: { search, physician } }),
  get: (id: number) => api.get(`/patients/${id}`),
  create: (data: any) => api.post("/patients/", data),
  update: (id: number, data: any) => api.patch(`/patients/${id}`, data),
};

export const visitsApi = {
  getByPatient: (patientId: number, year?: number) =>
    api.get(`/visits/patient/${patientId}`, { params: { year } }),
};

export const labsApi = {
  getByPatient: (patientId: number, testName?: string, abnormalOnly?: boolean) =>
    api.get(`/labs/patient/${patientId}`, {
      params: { test_name: testName, abnormal_only: abnormalOnly },
    }),
};

export const vitalsApi = {
  getByPatient: (patientId: number, limit?: number) =>
    api.get(`/vitals/patient/${patientId}`, { params: { limit } }),
};

export const medicationsApi = {
  getByPatient: (patientId: number, activeOnly?: boolean) =>
    api.get(`/medications/patient/${patientId}`, { params: { active_only: activeOnly } }),
};

export const allergiesApi = {
  getByPatient: (patientId: number) => api.get(`/allergies/patient/${patientId}`),
};

export const remindersApi = {
  getByPatient: (patientId: number, pendingOnly?: boolean) =>
    api.get(`/reminders/patient/${patientId}`, { params: { pending_only: pendingOnly } }),
  create: (data: any) => api.post("/reminders/", data),
  update: (id: number, data: any) => api.patch(`/reminders/${id}`, data),
  delete: (id: number) => api.delete(`/reminders/${id}`),
};

export const riskApi = {
  getLatest: (patientId: number) => api.get(`/risk/patient/${patientId}/latest`),
  getHistory: (patientId: number) => api.get(`/risk/patient/${patientId}/history`),
  assess: (patientId: number) => api.post(`/risk/patient/${patientId}/assess`),
};

export const summaryApi = {
  get: (patientId: number) => api.get(`/summary/patient/${patientId}`),
};

export default api;
