import os
from pathlib import Path

import psycopg2


DATABASE_URL = os.environ["DATABASE_URL"]


def main() -> None:
    sql = Path("scripts/patch_reviews_schema.sql").read_text(encoding="utf-8")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
        """,
        ("public", "reviews"),
    )
    print("reviews columns:")
    print("\n".join(row[0] for row in cur.fetchall()))
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
