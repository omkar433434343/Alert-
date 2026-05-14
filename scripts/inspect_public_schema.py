import os

import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
for table in ["users", "patients", "triage_records", "reviews", "patient_progress"]:
    cur.execute(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
        """,
        ("public", table),
    )
    print(f"[{table}]")
    for name, data_type in cur.fetchall():
        print(f"{name}: {data_type}")
cur.close()
conn.close()
