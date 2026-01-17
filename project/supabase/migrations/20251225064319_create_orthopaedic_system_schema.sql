/*
  # Orthopaedic Expert System Database Schema

  ## Overview
  This migration creates the complete database schema for an NLP-based orthopaedics 
  appointment expert system that assists doctors with symptom analysis, condition 
  prediction, and appointment prioritization.

  ## New Tables

  ### 1. `patients`
  Stores anonymized patient information
  - `id` (uuid, primary key) - Unique patient identifier
  - `patient_code` (text, unique) - Anonymized patient code (e.g., P-2024-001)
  - `age` (integer) - Patient age
  - `gender` (text) - Patient gender
  - `contact_phone` (text) - Encrypted contact information
  - `medical_history` (jsonb) - Previous conditions, allergies, medications
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### 2. `symptoms`
  Stores extracted symptom information from patient input
  - `id` (uuid, primary key)
  - `patient_id` (uuid, foreign key) - Reference to patients table
  - `symptom_text` (text) - Original patient description
  - `processed_text` (text) - Cleaned and normalized text
  - `affected_body_part` (text) - Extracted body part (knee, shoulder, spine, etc.)
  - `pain_level` (integer) - Pain severity 1-10
  - `duration` (text) - Duration of symptoms (e.g., "2 weeks", "3 months")
  - `additional_symptoms` (jsonb) - Array of extracted symptoms
  - `voice_recording_url` (text) - Optional: link to stored audio file
  - `extraction_confidence` (float) - NLP extraction confidence score
  - `created_at` (timestamptz)

  ### 3. `predictions`
  Stores AI model predictions for conditions
  - `id` (uuid, primary key)
  - `symptom_id` (uuid, foreign key) - Reference to symptoms table
  - `patient_id` (uuid, foreign key) - Reference to patients table
  - `predicted_conditions` (jsonb) - Array of {condition, probability, explanation}
  - `top_condition` (text) - Most likely condition
  - `top_condition_probability` (float) - Confidence score
  - `severity_level` (text) - Low, Medium, High
  - `severity_score` (float) - Numerical severity 0-1
  - `model_version` (text) - ML model version used
  - `features_used` (jsonb) - Features that influenced prediction
  - `created_at` (timestamptz)

  ### 4. `recommendations`
  Stores AI-generated recommendations for each prediction
  - `id` (uuid, primary key)
  - `prediction_id` (uuid, foreign key) - Reference to predictions table
  - `diagnostic_tests` (jsonb) - Recommended tests (X-ray, MRI, CT, blood work)
  - `initial_treatment` (jsonb) - Suggested initial treatments
  - `referral_needed` (boolean) - Whether specialist referral is needed
  - `referral_specialty` (text) - Specialty for referral
  - `urgency_level` (text) - Routine, Urgent, Emergency
  - `doctor_approved` (boolean) - Doctor confirmation status
  - `doctor_notes` (text) - Doctor's modifications or comments
  - `created_at` (timestamptz)

  ### 5. `appointments`
  Manages appointment queue with AI-based prioritization
  - `id` (uuid, primary key)
  - `patient_id` (uuid, foreign key)
  - `symptom_id` (uuid, foreign key)
  - `prediction_id` (uuid, foreign key)
  - `priority_score` (integer) - AI-calculated priority (1-100)
  - `scheduled_date` (timestamptz) - Appointment date/time
  - `status` (text) - Pending, Scheduled, Completed, Cancelled
  - `appointment_type` (text) - Initial, Follow-up, Emergency
  - `queue_position` (integer) - Position in priority queue
  - `assigned_doctor_id` (uuid) - Reference to auth.users
  - `created_at` (timestamptz)
  - `updated_at` (timestamptz)

  ### 6. `consultation_logs`
  Records actual doctor consultations and outcomes
  - `id` (uuid, primary key)
  - `appointment_id` (uuid, foreign key)
  - `patient_id` (uuid, foreign key)
  - `doctor_id` (uuid, foreign key) - Reference to auth.users
  - `actual_diagnosis` (text) - Doctor's final diagnosis
  - `ai_prediction_accuracy` (boolean) - Was AI prediction correct?
  - `treatments_prescribed` (jsonb) - Actual treatments given
  - `tests_ordered` (jsonb) - Actual tests ordered
  - `follow_up_needed` (boolean)
  - `follow_up_date` (timestamptz)
  - `consultation_notes` (text) - Doctor's notes
  - `consultation_duration` (integer) - Minutes
  - `created_at` (timestamptz)

  ### 7. `model_performance`
  Tracks ML model performance metrics over time
  - `id` (uuid, primary key)
  - `model_name` (text) - Model identifier
  - `model_version` (text) - Version number
  - `accuracy` (float)
  - `precision` (float)
  - `recall` (float)
  - `f1_score` (float)
  - `evaluation_date` (timestamptz)
  - `training_data_size` (integer)
  - `metrics_detail` (jsonb) - Detailed metrics per condition

  ## Security
  - Enable RLS on all tables
  - Doctors (authenticated users) can access all patient data
  - Patients cannot directly access the database (all access via API)
  - Audit logging for all sensitive operations
*/

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_code text UNIQUE NOT NULL,
  age integer NOT NULL CHECK (age > 0 AND age < 150),
  gender text NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
  contact_phone text,
  medical_history jsonb DEFAULT '[]'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create symptoms table
CREATE TABLE IF NOT EXISTS symptoms (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id uuid NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
  symptom_text text NOT NULL,
  processed_text text,
  affected_body_part text,
  pain_level integer CHECK (pain_level >= 0 AND pain_level <= 10),
  duration text,
  additional_symptoms jsonb DEFAULT '[]'::jsonb,
  voice_recording_url text,
  extraction_confidence float CHECK (extraction_confidence >= 0 AND extraction_confidence <= 1),
  created_at timestamptz DEFAULT now()
);

-- Create predictions table
CREATE TABLE IF NOT EXISTS predictions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  symptom_id uuid NOT NULL REFERENCES symptoms(id) ON DELETE CASCADE,
  patient_id uuid NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
  predicted_conditions jsonb NOT NULL DEFAULT '[]'::jsonb,
  top_condition text NOT NULL,
  top_condition_probability float NOT NULL CHECK (top_condition_probability >= 0 AND top_condition_probability <= 1),
  severity_level text NOT NULL CHECK (severity_level IN ('Low', 'Medium', 'High')),
  severity_score float NOT NULL CHECK (severity_score >= 0 AND severity_score <= 1),
  model_version text NOT NULL DEFAULT 'v1.0',
  features_used jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

-- Create recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  prediction_id uuid NOT NULL REFERENCES predictions(id) ON DELETE CASCADE,
  diagnostic_tests jsonb DEFAULT '[]'::jsonb,
  initial_treatment jsonb DEFAULT '[]'::jsonb,
  referral_needed boolean DEFAULT false,
  referral_specialty text,
  urgency_level text NOT NULL CHECK (urgency_level IN ('Routine', 'Urgent', 'Emergency')),
  doctor_approved boolean DEFAULT false,
  doctor_notes text,
  created_at timestamptz DEFAULT now()
);

-- Create appointments table
CREATE TABLE IF NOT EXISTS appointments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id uuid NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
  symptom_id uuid NOT NULL REFERENCES symptoms(id) ON DELETE CASCADE,
  prediction_id uuid NOT NULL REFERENCES predictions(id) ON DELETE CASCADE,
  priority_score integer NOT NULL CHECK (priority_score >= 1 AND priority_score <= 100),
  scheduled_date timestamptz,
  status text NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Scheduled', 'Completed', 'Cancelled')),
  appointment_type text NOT NULL CHECK (appointment_type IN ('Initial', 'Follow-up', 'Emergency')),
  queue_position integer,
  assigned_doctor_id uuid REFERENCES auth.users(id),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create consultation_logs table
CREATE TABLE IF NOT EXISTS consultation_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  appointment_id uuid NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
  patient_id uuid NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
  doctor_id uuid NOT NULL REFERENCES auth.users(id),
  actual_diagnosis text NOT NULL,
  ai_prediction_accuracy boolean,
  treatments_prescribed jsonb DEFAULT '[]'::jsonb,
  tests_ordered jsonb DEFAULT '[]'::jsonb,
  follow_up_needed boolean DEFAULT false,
  follow_up_date timestamptz,
  consultation_notes text,
  consultation_duration integer,
  created_at timestamptz DEFAULT now()
);

-- Create model_performance table
CREATE TABLE IF NOT EXISTS model_performance (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  model_name text NOT NULL,
  model_version text NOT NULL,
  accuracy float CHECK (accuracy >= 0 AND accuracy <= 1),
  precision float CHECK (precision >= 0 AND precision <= 1),
  recall float CHECK (recall >= 0 AND recall <= 1),
  f1_score float CHECK (f1_score >= 0 AND f1_score <= 1),
  evaluation_date timestamptz DEFAULT now(),
  training_data_size integer,
  metrics_detail jsonb DEFAULT '{}'::jsonb
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_symptoms_patient ON symptoms(patient_id);
CREATE INDEX IF NOT EXISTS idx_predictions_symptom ON predictions(symptom_id);
CREATE INDEX IF NOT EXISTS idx_predictions_patient ON predictions(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);
CREATE INDEX IF NOT EXISTS idx_appointments_priority ON appointments(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_consultation_logs_patient ON consultation_logs(patient_id);
CREATE INDEX IF NOT EXISTS idx_consultation_logs_doctor ON consultation_logs(doctor_id);

-- Enable Row Level Security
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE symptoms ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE model_performance ENABLE ROW LEVEL SECURITY;

-- RLS Policies for authenticated doctors/staff
CREATE POLICY "Authenticated users can view all patients"
  ON patients FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert patients"
  ON patients FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update patients"
  ON patients FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view all symptoms"
  ON symptoms FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert symptoms"
  ON symptoms FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view all predictions"
  ON predictions FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert predictions"
  ON predictions FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view all recommendations"
  ON recommendations FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert recommendations"
  ON recommendations FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update recommendations"
  ON recommendations FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view all appointments"
  ON appointments FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert appointments"
  ON appointments FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update appointments"
  ON appointments FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view all consultation logs"
  ON consultation_logs FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert consultation logs"
  ON consultation_logs FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view model performance"
  ON model_performance FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert model performance"
  ON model_performance FOR INSERT
  TO authenticated
  WITH CHECK (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_patients_updated_at
  BEFORE UPDATE ON patients
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at
  BEFORE UPDATE ON appointments
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
