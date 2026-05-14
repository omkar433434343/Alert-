-- Alert+ baseline PostgreSQL schema
-- Safe to run multiple times (uses IF NOT EXISTS)

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  employee_id VARCHAR(64) NOT NULL UNIQUE,
  role VARCHAR(16) NOT NULL CHECK (role IN ('asha', 'tho')),
  password_hash TEXT NOT NULL,
  full_name TEXT,
  location TEXT,
  district TEXT,
  avatar_b64 TEXT,
  banner_b64 TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  age INTEGER,
  gender VARCHAR(16),
  village TEXT,
  tehsil TEXT,
  district TEXT,
  pregnant BOOLEAN NOT NULL DEFAULT FALSE,
  abha_id TEXT,
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS triage_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID REFERENCES patients(id) ON DELETE SET NULL,
  patient_name TEXT NOT NULL,
  symptoms JSONB NOT NULL DEFAULT '[]'::jsonb,
  severity VARCHAR(16) NOT NULL DEFAULT 'yellow' CHECK (severity IN ('green', 'yellow', 'red')),
  sickle_cell_risk BOOLEAN NOT NULL DEFAULT FALSE,
  brief TEXT NOT NULL DEFAULT '',
  ai_suggestion TEXT,
  tehsil TEXT,
  district TEXT,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  reviewed BOOLEAN NOT NULL DEFAULT FALSE,
  transcript TEXT,
  source TEXT,
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  reviewed_by UUID REFERENCES users(id) ON DELETE SET NULL,
  reviewed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS outbreaks (
  id BIGSERIAL PRIMARY KEY,
  year INTEGER,
  week INTEGER,
  state TEXT,
  district TEXT,
  disease TEXT,
  cases INTEGER,
  deaths INTEGER,
  status TEXT,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  role VARCHAR(16) NOT NULL CHECK (role IN ('asha', 'tho')),
  overall INTEGER NOT NULL CHECK (overall BETWEEN 1 AND 5),
  comment TEXT,
  user_name TEXT,
  designation TEXT,
  location TEXT,
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS patient_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
  status TEXT NOT NULL DEFAULT 'stable',
  symptoms JSONB NOT NULL DEFAULT '[]'::jsonb,
  notes TEXT,
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_patients_district ON patients(district);
CREATE INDEX IF NOT EXISTS idx_patients_created_by ON patients(created_by);
CREATE INDEX IF NOT EXISTS idx_triage_patient_id ON triage_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_triage_reviewed ON triage_records(reviewed);
CREATE INDEX IF NOT EXISTS idx_triage_created_at ON triage_records(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_triage_severity ON triage_records(severity);
CREATE INDEX IF NOT EXISTS idx_triage_symptoms_gin ON triage_records USING GIN (symptoms);
CREATE INDEX IF NOT EXISTS idx_outbreaks_district ON outbreaks(district);
CREATE INDEX IF NOT EXISTS idx_outbreaks_disease ON outbreaks(disease);
CREATE INDEX IF NOT EXISTS idx_reviews_role ON reviews(role);
CREATE INDEX IF NOT EXISTS idx_patient_progress_patient_id ON patient_progress(patient_id);
CREATE INDEX IF NOT EXISTS idx_patient_progress_created_at ON patient_progress(created_at DESC);

DROP TRIGGER IF EXISTS trg_users_updated_at ON users;
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_patients_updated_at ON patients;
CREATE TRIGGER trg_patients_updated_at
BEFORE UPDATE ON patients
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_triage_records_updated_at ON triage_records;
CREATE TRIGGER trg_triage_records_updated_at
BEFORE UPDATE ON triage_records
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_outbreaks_updated_at ON outbreaks;
CREATE TRIGGER trg_outbreaks_updated_at
BEFORE UPDATE ON outbreaks
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
