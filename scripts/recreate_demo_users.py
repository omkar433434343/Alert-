import json
import os
import urllib.error
import urllib.request

import psycopg2


DATABASE_URL = os.environ["DATABASE_URL"]
BASE_URL = "https://alert-backend-wdln.onrender.com"

USERS = [
    {
        "employee_id": "ASHA001",
        "password": "Asha@123",
        "role": "asha",
        "full_name": "Kavya N",
        "location": "Chikaballapur PHC Cluster",
        "district": "Chikkaballapur",
    },
    {
        "employee_id": "ASHA002",
        "password": "Asha@123",
        "role": "asha",
        "full_name": "Meena R",
        "location": "Bagepalli Subcenter",
        "district": "Chikkaballapur",
    },
    {
        "employee_id": "THO001",
        "password": "Tho@123",
        "role": "tho",
        "full_name": "Dr. Arjun S",
        "location": "District Health Office",
        "district": "Chikkaballapur",
    },
    {
        "employee_id": "THO002",
        "password": "Tho@123",
        "role": "tho",
        "full_name": "Dr. Nisha P",
        "location": "District Surveillance Unit",
        "district": "Chikkaballapur",
    },
]


def request_json(path: str, payload: dict) -> tuple[int, str]:
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
    cur.execute(
        "DELETE FROM users WHERE employee_id = ANY(%s)",
        ([user["employee_id"] for user in USERS],),
    )
    print(f"deleted {cur.rowcount} existing demo users")
    cur.close()
    conn.close()

    for user in USERS:
        status, body = request_json("/api/v1/auth/register", user)
        print(f"register {user['employee_id']}: {status} {body}")

    for user in USERS:
        status, body = request_json(
            "/api/v1/auth/login",
            {
                "employee_id": user["employee_id"],
                "password": user["password"],
                "role": user["role"],
            },
        )
        print(f"login {user['employee_id']}: {status}")
        print(body[:300])


if __name__ == "__main__":
    main()
