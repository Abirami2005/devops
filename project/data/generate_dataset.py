import pandas as pd
import random
import json
from datetime import datetime, timedelta


body_parts = ["knee", "shoulder", "hip", "ankle", "wrist", "elbow", "back", "neck"]

conditions_by_part = {
    "knee": ["Osteoarthritis", "Meniscus Tear", "ACL Tear", "Patellar Tendinitis", "Bursitis"],
    "shoulder": ["Rotator Cuff Tear", "Frozen Shoulder", "Shoulder Impingement", "Bursitis", "Arthritis"],
    "back": ["Herniated Disc", "Spinal Stenosis", "Sciatica", "Muscle Strain", "Spondylolisthesis"],
    "hip": ["Hip Osteoarthritis", "Hip Bursitis", "Hip Labral Tear", "Hip Fracture", "Avascular Necrosis"],
    "ankle": ["Ankle Sprain", "Achilles Tendinitis", "Ankle Fracture", "Arthritis", "Tarsal Tunnel Syndrome"],
    "wrist": ["Carpal Tunnel Syndrome", "Wrist Fracture", "Tendinitis", "Arthritis", "De Quervain's Tenosynovitis"],
    "elbow": ["Tennis Elbow", "Golfer's Elbow", "Elbow Bursitis", "Elbow Fracture", "Arthritis"],
    "neck": ["Cervical Spondylosis", "Herniated Cervical Disc", "Whiplash", "Muscle Strain", "Cervical Radiculopathy"]
}

symptom_templates = [
    "I have {intensity} pain in my {side} {body_part} for the past {duration}. The pain is {pain_level} out of 10. {additional}",
    "My {side} {body_part} has been hurting for {duration}. Pain level is around {pain_level}/10. {additional}",
    "Experiencing {intensity} {body_part} pain ({pain_level}/10) since {duration}. {additional}",
    "{intensity} discomfort in {side} {body_part}, started {duration} ago. Pain intensity: {pain_level}/10. {additional}",
    "I've had {intensity} pain in my {body_part} for {duration}. It's about {pain_level} out of 10. {additional}"
]

intensities = ["sharp", "dull", "throbbing", "aching", "burning", "stabbing", "constant", "intermittent"]
sides = ["left", "right", ""]
durations = ["2 days", "1 week", "2 weeks", "3 weeks", "1 month", "2 months", "3 months", "6 months", "1 year"]
additional_symptoms = [
    "There is swelling.",
    "I have difficulty moving it.",
    "There is numbness.",
    "I feel weakness in the area.",
    "Movement is limited.",
    "There is stiffness in the morning.",
    "I cannot bear weight on it.",
    "It's affecting my daily activities.",
    ""
]


def generate_patient_data(num_patients=500):
    patients = []

    for i in range(num_patients):
        patient_id = f"P{str(i+1).zfill(6)}"
        age = random.randint(18, 85)
        gender = random.choice(["Male", "Female", "Other"])

        body_part = random.choice(body_parts)
        condition = random.choice(conditions_by_part[body_part])

        pain_level = random.randint(1, 10)

        if pain_level >= 8:
            severity = "High"
        elif pain_level >= 5:
            severity = "Medium"
        else:
            severity = "Low"

        intensity = random.choice(intensities)
        side = random.choice(sides)
        duration = random.choice(durations)
        additional = random.choice(additional_symptoms)

        template = random.choice(symptom_templates)
        symptom_text = template.format(
            intensity=intensity,
            side=side if side else "",
            body_part=body_part,
            duration=duration,
            pain_level=pain_level,
            additional=additional
        ).replace("  ", " ").strip()

        patients.append({
            "patient_id": patient_id,
            "age": age,
            "gender": gender,
            "symptom_text": symptom_text,
            "affected_body_part": body_part,
            "pain_level": pain_level,
            "duration": duration,
            "predicted_condition": condition,
            "severity": severity,
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat()
        })

    return patients


def save_dataset(patients, filename="orthopaedic_dataset.csv"):
    df = pd.DataFrame(patients)
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}")
    print(f"Total records: {len(patients)}")
    print(f"\nDataset Statistics:")
    print(f"Severity Distribution:\n{df['severity'].value_counts()}")
    print(f"\nBody Part Distribution:\n{df['affected_body_part'].value_counts()}")
    print(f"\nAge Statistics:\n{df['age'].describe()}")


def save_json_dataset(patients, filename="orthopaedic_dataset.json"):
    with open(filename, 'w') as f:
        json.dump(patients, f, indent=2)
    print(f"JSON dataset saved to {filename}")


if __name__ == "__main__":
    print("Generating synthetic orthopaedic dataset...")

    patients = generate_patient_data(num_patients=500)

    save_dataset(patients, "orthopaedic_dataset.csv")
    save_json_dataset(patients, "orthopaedic_dataset.json")

    print("\nSample records:")
    for i in range(3):
        print(f"\nPatient {i+1}:")
        print(f"  Symptom: {patients[i]['symptom_text']}")
        print(f"  Condition: {patients[i]['predicted_condition']}")
        print(f"  Severity: {patients[i]['severity']}")
