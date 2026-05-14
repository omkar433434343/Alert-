import os
from pathlib import Path

import psycopg2


DATABASE_URL = os.environ["DATABASE_URL"]


def main() -> None:
    sql = Path("scripts/patch_id_columns_for_backend.sql").read_text(encoding="utf-8")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute(
        """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name IN (%s, %s, %s, %s, %s)
          AND column_name IN (%s, %s, %s, %s)
        ORDER BY table_name, ordinal_position
        """,
        (
            "public",
            "users",
            "patients",
            "triage_records",
            "reviews",
            "patient_progress",
            "id",
            "patient_id",
            "created_by",
            "reviewed_by",
        ),
    )
    for table, column, data_type in cur.fetchall():
        print(f"{table}.{column}: {data_type}")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
