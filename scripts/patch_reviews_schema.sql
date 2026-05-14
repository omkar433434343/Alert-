ALTER TABLE reviews ADD COLUMN IF NOT EXISTS categories JSONB DEFAULT '{}'::jsonb;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS "userName" VARCHAR;
ALTER TABLE reviews ADD COLUMN IF NOT EXISTS source VARCHAR;

DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'reviews'
      AND column_name = 'user_name'
  ) THEN
    UPDATE reviews SET "userName" = COALESCE("userName", user_name);
  END IF;
END $$;
