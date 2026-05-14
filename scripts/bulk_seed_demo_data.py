import os
import random
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import psycopg2
from psycopg2.extras import Json


DATABASE_URL = os.environ["DATABASE_URL"]


random.seed(42)

FIRST_NAMES = [
    "Anitha", "Bhavya", "Chandra", "Deepa", "Farida", "Geetha", "Harish", "Imran",
    "Jaya", "Kiran", "Lakshmi", "Mahesh", "Nandini", "Omkar", "Pooja", "Rafiq",
    "Savitha", "Tanvi", "Umesh", "Vani", "Yashoda", "Zarina", "Ramesh", "Suresh",
    "Ayesha", "Meena", "Kavitha", "Prakash", "Roopa", "Shankar", "Divya", "Naveen",
]
LAST_NAMES = ["Gowda", "R", "Khan", "Naik", "Shetty", "P", "N", "S", "Devi", "Bai", "Rao", "Kumar"]
VILLAGES = [
    ("Nandi", "Chikballapur"),
    ("Bagepalli", "Bagepalli"),
    ("Sidlaghatta", "Sidlaghatta"),
    ("Gauribidanur", "Gauribidanur"),
    ("Chintamani", "Chintamani"),
    ("Gudibanda", "Gudibanda"),
    ("Peresandra", "Chikballapur"),
    ("Mandikal", "Chikballapur"),
    ("Chelur", "Bagepalli"),
    ("Manchenahalli", "Gauribidanur"),
]
SYMPTOM_SETS = [
    ["fever", "headache", "body ache"],
    ["cough", "fever", "sore throat"],
    ["diarrhea", "vomiting", "dehydration"],
    ["fatigue", "joint pain"],
    ["breathlessness", "chest discomfort", "cough"],
    ["skin rash", "fever"],
    ["abdominal pain", "nausea"],
    ["dizziness", "weakness"],
    ["leg swelling", "fatigue", "pregnancy risk"],
    ["high fever", "chills", "body ache"],
]
DISEASES = [
    "Dengue", "Acute Diarrheal Disease", "Influenza-like Illness", "Malaria",
    "Chikungunya", "Typhoid", "Measles", "Food Poisoning", "Viral Fever",
]


def days_ago(max_days: int = 45) -> datetime:
    return datetime.now(timezone.utc) - timedelta(
        days=random.randint(0, max_days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )


def severity_for(symptoms: list[str]) -> str:
    red_words = {"breathlessness", "dehydration", "high fever", "pregnancy risk", "chest discomfort"}
    if any(symptom in red_words for symptom in symptoms):
        return random.choices(["red", "yellow"], weights=[70, 30])[0]
    return random.choices(["green", "yellow", "red"], weights=[45, 45, 10])[0]


def main() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT id, employee_id FROM users")
    users = {employee_id: user_id for user_id, employee_id in cur.fetchall()}
    for employee_id in ["ASHA001", "ASHA002", "THO001", "THO002"]:
        if employee_id not in users:
            raise RuntimeError(f"Missing required user {employee_id}")

    patient_rows = []
    for i in range(80):
        village, tehsil = random.choice(VILLAGES)
        gender = random.choice(["Male", "Female", "Other"])
        age = random.randint(1, 82)
        pregnant = gender == "Female" and 18 <= age <= 42 and random.random() < 0.18
        patient_rows.append(
            {
                "id": str(uuid4()),
                "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                "age": age,
                "gender": gender,
                "village": village,
                "tehsil": tehsil,
                "district": "Chikkaballapur",
                "pregnant": pregnant,
                "abha_id": f"{random.randint(10, 99)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
                if random.random() < 0.65
                else None,
                "created_by": users["ASHA001" if i % 2 == 0 else "ASHA002"],
                "created_at": days_ago(),
            }
        )

    for patient in patient_rows:
        cur.execute(
            """
            INSERT INTO patients (
              id, name, age, gender, village, tehsil, district, pregnant,
              abha_id, created_by, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                patient["id"], patient["name"], patient["age"], patient["gender"],
                patient["village"], patient["tehsil"], patient["district"], patient["pregnant"],
                patient["abha_id"], patient["created_by"], patient["created_at"],
            ),
        )

    for i in range(180):
        patient = random.choice(patient_rows)
        symptoms = random.choice(SYMPTOM_SETS).copy()
        if patient["pregnant"] and "pregnancy risk" not in symptoms and random.random() < 0.35:
            symptoms.append("pregnancy risk")
        severity = severity_for(symptoms)
        reviewed = random.random() < 0.62
        created_at = days_ago()
        reviewed_by = random.choice([users["THO001"], users["THO002"]]) if reviewed else None
        cur.execute(
            """
            INSERT INTO triage_records (
              id, patient_id, patient_name, symptoms, severity, sickle_cell_risk,
              brief, ai_suggestion, tehsil, district, latitude, longitude,
              reviewed, source, created_by, reviewed_by, reviewed_at, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                str(uuid4()), patient["id"], patient["name"], Json(symptoms), severity,
                random.random() < 0.14,
                f"{patient['name']} reported {', '.join(symptoms)}. Severity marked {severity}.",
                "Monitor danger signs, maintain hydration, and refer to PHC if symptoms worsen.",
                patient["tehsil"], patient["district"],
                13.25 + random.random() * 0.45,
                77.35 + random.random() * 0.55,
                reviewed, "bulk_demo_seed", patient["created_by"], reviewed_by,
                created_at + timedelta(hours=random.randint(1, 12)) if reviewed else None,
                created_at,
            ),
        )

    for i in range(140):
        patient = random.choice(patient_rows)
        status = random.choices(["improving", "stable", "worsening"], weights=[40, 45, 15])[0]
        symptoms = random.choice(SYMPTOM_SETS)[: random.randint(1, 3)]
        cur.execute(
            """
            INSERT INTO patient_progress (
              id, patient_id, status, symptoms, notes, referred, created_by, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                str(uuid4()), patient["id"], status, Json(symptoms),
                f"Follow-up update: patient is {status}; symptoms tracked by ASHA worker.",
                status == "worsening" or random.random() < 0.18,
                patient["created_by"], days_ago(20),
            ),
        )

    for _ in range(30):
        village, tehsil = random.choice(VILLAGES)
        disease = random.choice(DISEASES)
        cases = random.randint(3, 65)
        deaths = random.choices([0, 1, 2], weights=[85, 12, 3])[0]
        cur.execute(
            """
            INSERT INTO outbreaks (year, week, state, district, disease, cases, deaths, status, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                2026, random.randint(1, 22), "Karnataka", "Chikkaballapur", disease,
                cases, deaths, random.choice(["active", "monitoring", "watch", "contained"]),
                13.25 + random.random() * 0.45, 77.35 + random.random() * 0.55,
            ),
        )

    review_people = [
        ("asha", "Kavya N", "ASHA Worker", "Nandi", "mobile"),
        ("asha", "Meena R", "ASHA Worker", "Bagepalli", "mobile"),
        ("tho", "Dr. Arjun S", "THO Officer", "District Health Office", "web"),
        ("tho", "Dr. Nisha P", "THO Officer", "District Surveillance Unit", "web"),
    ]
    for role, user_name, designation, location, source in review_people * 8:
        cur.execute(
            """
            INSERT INTO reviews (id, role, overall, categories, comment, "userName", designation, location, source, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                str(uuid4()), role, random.randint(4, 5),
                Json({"usability": random.randint(4, 5), "speed": random.randint(3, 5), "workflow": random.randint(4, 5)}),
                "Demo feedback for populated workflow testing.",
                user_name, designation, location, source, days_ago(30),
            ),
        )

    for table in ["users", "patients", "triage_records", "patient_progress", "outbreaks", "reviews"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cur.fetchone()[0]}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
