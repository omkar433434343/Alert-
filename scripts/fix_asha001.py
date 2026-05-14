import json
import os
import urllib.error
import urllib.request

import psycopg2


DATABASE_URL = os.environ["DATABASE_URL"]
BASE_URL = "https://alert-backend-wdln.onrender.com"


def post(path: str, payload: dict) -> tuple[int, str]:
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="ignore")


def main() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT id, employee_id, role FROM users ORDER BY employee_id")
    print("before:", cur.fetchall())
    cur.execute("DELETE FROM users WHERE employee_id = %s", ("ASHA001",))
    print("deleted:", cur.rowcount)
    cur.close()
    conn.close()

    user = {
        "employee_id": "ASHA001",
        "password": "Asha@123",
        "role": "asha",
        "full_name": "Kavya N",
        "location": "Chikaballapur PHC Cluster",
        "district": "Chikkaballapur",
    }
    print("register:", post("/api/v1/auth/register", user))
    print(
        "login:",
        post(
            "/api/v1/auth/login",
            {"employee_id": "ASHA001", "password": "Asha@123", "role": "asha"},
        )[0],
    )

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, employee_id, role FROM users ORDER BY employee_id")
    print("after:", cur.fetchall())
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
