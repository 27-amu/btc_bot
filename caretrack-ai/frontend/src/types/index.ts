export interface Patient {
  id: number;
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone?: string;
  email?: string;
  address?: string;
  primary_diagnosis?: string;
  primary_physician?: string;
  insurance_id?: string;
  created_at: string;
  updated_at?: string;
}

export interface PatientList {
  id: number;
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  primary_diagnosis?: string;
  primary_physician?: string;
}

export interface Visit {
  id: number;
  patient_id: number;
  visit_date: string;
  visit_type: string;
  chief_complaint?: string;
  diagnosis?: string;
  notes?: string;
  physician?: string;
  facility?: string;
  created_at: string;
}

export interface LabResult {
  id: number;
  patient_id: number;
  test_name: string;
  test_date: string;
  value: number;
  unit?: string;
  reference_min?: number;
  reference_max?: number;
  is_abnormal: boolean;
  notes?: string;
  ordered_by?: string;
  created_at: string;
}

export interface Vital {
  id: number;
  patient_id: number;
  recorded_date: string;
  systolic_bp?: number;
  diastolic_bp?: number;
  heart_rate?: number;
  temperature?: number;
  weight_kg?: number;
  height_cm?: number;
  bmi?: number;
  oxygen_saturation?: number;
  respiratory_rate?: number;
  recorded_by?: string;
  created_at: string;
}

export interface Medication {
  id: number;
  patient_id: number;
  name: string;
  generic_name?: string;
  dosage?: string;
  frequency?: string;
  route?: string;
  start_date?: string;
  end_date?: string;
  is_active: boolean;
  prescribed_by?: string;
  indication?: string;
  created_at: string;
}

export interface Allergy {
  id: number;
  patient_id: number;
  allergen: string;
  allergen_type?: string;
  reaction?: string;
  severity?: string;
  onset_date?: string;
  notes?: string;
  created_at: string;
}

export interface Reminder {
  id: number;
  patient_id: number;
  reminder_type: string;
  due_date: string;
  description?: string;
  is_completed: boolean;
  completed_at?: string;
  priority: string;
  assigned_to?: string;
  created_at: string;
}

export interface RiskAssessment {
  id: number;
  patient_id: number;
  assessed_at: string;
  risk_score: number;
  risk_level: "low" | "medium" | "high";
  reasons: string[];
  recommended_actions: string[];
  assessed_by: string;
}

export interface PatientSummary {
  patient_id: number;
  generated_at: string;
  source: string;
  summary: {
    overview: string;
    key_diagnoses: string[];
    latest_vitals: string;
    lab_trends: string;
    medications: string;
    allergies: string;
    risk_alerts: string;
    visit_history: string;
    suggested_follow_up_actions: string[];
    pending_follow_ups: string;
  };
  structured: {
    patient_name: string;
    age: number;
    gender: string;
    primary_diagnosis?: string;
    recent_vitals: any[];
    recent_labs: any[];
    active_medications: string[];
    allergies: string[];
    risk_level: string;
    risk_score: number;
    risk_reasons: string[];
    pending_reminders: any[];
    recent_visits: any[];
  };
}
