DO $$
DECLARE
  constraint_record RECORD;
BEGIN
  FOR constraint_record IN
    SELECT conrelid::regclass AS table_name, conname AS constraint_name
    FROM pg_constraint
    WHERE contype = 'f'
      AND connamespace = 'public'::regnamespace
  LOOP
    EXECUTE format(
      'ALTER TABLE %s DROP CONSTRAINT IF EXISTS %I',
      constraint_record.table_name,
      constraint_record.constraint_name
    );
  END LOOP;
END $$;

ALTER TABLE users ALTER COLUMN id TYPE VARCHAR USING id::text;
ALTER TABLE patients ALTER COLUMN id TYPE VARCHAR USING id::text;
ALTER TABLE patients ALTER COLUMN created_by TYPE VARCHAR USING created_by::text;
ALTER TABLE triage_records ALTER COLUMN id TYPE VARCHAR USING id::text;
ALTER TABLE triage_records ALTER COLUMN patient_id TYPE VARCHAR USING patient_id::text;
ALTER TABLE triage_records ALTER COLUMN created_by TYPE VARCHAR USING created_by::text;
ALTER TABLE triage_records ALTER COLUMN reviewed_by TYPE VARCHAR USING reviewed_by::text;
ALTER TABLE reviews ALTER COLUMN id TYPE VARCHAR USING id::text;
ALTER TABLE reviews ALTER COLUMN created_by TYPE VARCHAR USING created_by::text;
ALTER TABLE patient_progress ALTER COLUMN id TYPE VARCHAR USING id::text;
ALTER TABLE patient_progress ALTER COLUMN patient_id TYPE VARCHAR USING patient_id::text;
ALTER TABLE patient_progress ALTER COLUMN created_by TYPE VARCHAR USING created_by::text;

ALTER TABLE patient_progress ADD COLUMN IF NOT EXISTS referred BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE patients
  ADD CONSTRAINT patients_created_by_fkey
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE triage_records
  ADD CONSTRAINT triage_records_patient_id_fkey
  FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE SET NULL;

ALTER TABLE triage_records
  ADD CONSTRAINT triage_records_created_by_fkey
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE triage_records
  ADD CONSTRAINT triage_records_reviewed_by_fkey
  FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE reviews
  ADD CONSTRAINT reviews_created_by_fkey
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE patient_progress
  ADD CONSTRAINT patient_progress_patient_id_fkey
  FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE;

ALTER TABLE patient_progress
  ADD CONSTRAINT patient_progress_created_by_fkey
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
