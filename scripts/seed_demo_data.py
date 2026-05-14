import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import psycopg2
from psycopg2.extras import Json


DATABASE_URL = os.environ["DATABASE_URL"]


def iso_days_ago(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


def main() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT id, employee_id FROM users")
    users = {employee_id: user_id for user_id, employee_id in cur.fetchall()}
    required = ["ASHA001", "ASHA002", "THO001", "THO002"]
    missing = [employee_id for employee_id in required if employee_id not in users]
    if missing:
        raise RuntimeError(f"Missing users: {', '.join(missing)}")

    patients = [
        {
            "id": str(uuid4()),
            "name": "Lakshmi Devi",
            "age": 28,
            "gender": "Female",
            "village": "Nandi",
            "tehsil": "Chikballapur",
            "district": "Chikkaballapur",
            "pregnant": True,
            "abha_id": "91-2345-6789-1234",
            "created_by": users["ASHA001"],
            "created_at": iso_days_ago(6),
        },
        {
            "id": str(uuid4()),
            "name": "Ramesh Gowda",
            "age": 42,
            "gender": "Male",
            "village": "Bagepalli",
            "tehsil": "Bagepalli",
            "district": "Chikkaballapur",
            "pregnant": False,
            "abha_id": "82-9981-2234-1100",
            "created_by": users["ASHA002"],
            "created_at": iso_days_ago(5),
        },
        {
            "id": str(uuid4()),
            "name": "Ayesha Khan",
            "age": 9,
            "gender": "Female",
            "village": "Sidlaghatta",
            "tehsil": "Sidlaghatta",
            "district": "Chikkaballapur",
            "pregnant": False,
            "abha_id": None,
            "created_by": users["ASHA001"],
            "created_at": iso_days_ago(3),
        },
        {
            "id": str(uuid4()),
            "name": "Manjunath R",
            "age": 67,
            "gender": "Male",
            "village": "Gauribidanur",
            "tehsil": "Gauribidanur",
            "district": "Chikkaballapur",
            "pregnant": False,
            "abha_id": "77-5555-1010-9090",
            "created_by": users["ASHA002"],
            "created_at": iso_days_ago(2),
        },
    ]

    for patient in patients:
        cur.execute(
            """
            INSERT INTO patients (
              id, name, age, gender, village, tehsil, district, pregnant,
              abha_id, created_by, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (
                patient["id"],
                patient["name"],
                patient["age"],
                patient["gender"],
                patient["village"],
                patient["tehsil"],
                patient["district"],
                patient["pregnant"],
                patient["abha_id"],
                patient["created_by"],
                patient["created_at"],
            ),
        )

    triage_records = [
        {
            "patient": patients[0],
            "symptoms": ["fever", "dizziness", "pregnancy risk"],
            "severity": "red",
            "sickle_cell_risk": False,
            "brief": "Pregnant patient with high fever and dizziness. Immediate PHC referral advised.",
            "ai_suggestion": "Check temperature, hydration, blood pressure, and refer urgently if persistent fever or weakness continues.",
            "reviewed": True,
            "created_by": users["ASHA001"],
            "reviewed_by": users["THO001"],
            "days_ago": 5,
        },
        {
            "patient": patients[1],
            "symptoms": ["cough", "fever", "body ache"],
            "severity": "yellow",
            "sickle_cell_risk": False,
            "brief": "Adult male with fever and cough for two days. Monitor for respiratory distress.",
            "ai_suggestion": "Hydration, fever control, masking, and PHC visit if symptoms worsen.",
            "reviewed": False,
            "created_by": users["ASHA002"],
            "reviewed_by": None,
            "days_ago": 4,
        },
        {
            "patient": patients[2],
            "symptoms": ["diarrhea", "vomiting", "dehydration"],
            "severity": "red",
            "sickle_cell_risk": False,
            "brief": "Child with vomiting and dehydration signs. ORS started, urgent evaluation needed.",
            "ai_suggestion": "Continue ORS in small frequent sips and refer to nearest PHC immediately.",
            "reviewed": True,
            "created_by": users["ASHA001"],
            "reviewed_by": users["THO002"],
            "days_ago": 2,
        },
        {
            "patient": patients[3],
            "symptoms": ["joint pain", "fatigue"],
            "severity": "green",
            "sickle_cell_risk": True,
            "brief": "Elderly patient reports fatigue and joint pain with possible sickle-cell risk.",
            "ai_suggestion": "Schedule follow-up screening and monitor for pain crisis or fever.",
            "reviewed": False,
            "created_by": users["ASHA002"],
            "reviewed_by": None,
            "days_ago": 1,
        },
    ]

    for record in triage_records:
        patient = record["patient"]
        created_at = iso_days_ago(record["days_ago"])
        cur.execute(
            """
            INSERT INTO triage_records (
              id, patient_id, patient_name, symptoms, severity, sickle_cell_risk,
              brief, ai_suggestion, tehsil, district, latitude, longitude,
              reviewed, source, created_by, reviewed_by, reviewed_at, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                str(uuid4()),
                patient["id"],
                patient["name"],
                Json(record["symptoms"]),
                record["severity"],
                record["sickle_cell_risk"],
                record["brief"],
                record["ai_suggestion"],
                patient["tehsil"],
                patient["district"],
                13.43,
                77.72,
                record["reviewed"],
                "demo_seed",
                record["created_by"],
                record["reviewed_by"],
                created_at + timedelta(hours=6) if record["reviewed"] else None,
                created_at,
            ),
        )

    progress_updates = [
        (patients[0], "improving", ["fever reduced", "hydrated"], "Reviewed at PHC, follow-up tomorrow.", True, users["ASHA001"]),
        (patients[1], "stable", ["mild cough"], "No danger signs reported today.", False, users["ASHA002"]),
        (patients[2], "improving", ["vomiting reduced"], "ORS accepted, child more active.", True, users["ASHA001"]),
        (patients[3], "stable", ["joint pain"], "Sickle-cell screening camp referral shared.", False, users["ASHA002"]),
    ]

    for patient, status, symptoms, notes, referred, created_by in progress_updates:
        cur.execute(
            """
            INSERT INTO patient_progress (
              id, patient_id, status, symptoms, notes, referred, created_by, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (str(uuid4()), patient["id"], status, Json(symptoms), notes, referred, created_by, iso_days_ago(1)),
        )

    outbreaks = [
        (2026, 20, "Karnataka", "Chikkaballapur", "Dengue", 18, 0, "monitoring", 13.4355, 77.7315),
        (2026, 20, "Karnataka", "Chikkaballapur", "Acute Diarrheal Disease", 11, 0, "active", 13.3409, 77.1010),
        (2026, 19, "Karnataka", "Bengaluru Rural", "Influenza-like Illness", 27, 0, "watch", 13.2847, 77.6078),
    ]
    for outbreak in outbreaks:
        cur.execute(
            """
            INSERT INTO outbreaks (year, week, state, district, disease, cases, deaths, status, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            outbreak,
        )

    reviews = [
        ("asha", 5, {"usability": 5, "offline": 4, "triage": 5}, "Useful for field triage and patient follow-up.", "Kavya N", "ASHA Worker", "Nandi", "mobile"),
        ("asha", 4, {"usability": 4, "offline": 5, "triage": 4}, "Offline queue helps during village visits.", "Meena R", "ASHA Worker", "Bagepalli", "mobile"),
        ("tho", 5, {"dashboard": 5, "review": 5, "outbreaks": 4}, "Review queue makes high-risk cases visible quickly.", "Dr. Arjun S", "THO Officer", "District Health Office", "web"),
        ("tho", 4, {"dashboard": 4, "review": 5, "outbreaks": 5}, "Outbreak map is helpful for district monitoring.", "Dr. Nisha P", "THO Officer", "District Surveillance Unit", "web"),
    ]
    for review in reviews:
        cur.execute(
            """
            INSERT INTO reviews (id, role, overall, categories, comment, "userName", designation, location, source, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (str(uuid4()), review[0], review[1], Json(review[2]), review[3], review[4], review[5], review[6], review[7], datetime.now(timezone.utc)),
        )

    for table in ["users", "patients", "triage_records", "patient_progress", "outbreaks", "reviews"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cur.fetchone()[0]}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
