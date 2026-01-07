import uuid
import json
from datetime import datetime

AUDIT_FILE = "audit_log.jsonl"

def get_input(prompt):
    return input(prompt).strip()

def audit_patient_data():
    flags = []
    warnings = []


    audit_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    patient_name = get_input("Enter patient name: ")

    age = get_input("Enter age: ")
    heart_rate = get_input("Enter heart rate (bpm): ")
    systolic = get_input("Enter systolic BP: ")
    diastolic = get_input("Enter diastolic BP: ")
    allergy = get_input("Allergy (yes/no): ").lower()


    if not age.isdigit() or not (0 <= int(age) <= 120):
        flags.append("Invalid age (must be 0–120)")


    if not heart_rate.isdigit():
        flags.append("Heart rate must be numeric")


    if not systolic.isdigit() or not diastolic.isdigit():
        flags.append("Blood pressure values must be numeric")


    if systolic.isdigit() and diastolic.isdigit():
        if int(systolic) <= int(diastolic):
            flags.append("Systolic BP must be greater than Diastolic BP")

    if allergy not in ["yes", "no"]:
        flags.append("Allergy field must be yes or no")



    if heart_rate.isdigit():
        hr = int(heart_rate)
        if hr < 40 or hr > 180:
            warnings.append("Heart rate outside safe range (40–180 bpm)")

    if systolic.isdigit():
        sys = int(systolic)
        if sys < 70 or sys > 200:
            warnings.append("Systolic BP outside safe range (70–200)")

    if diastolic.isdigit():
        dia = int(diastolic)
        if dia < 40 or dia > 130:
            warnings.append("Diastolic BP outside safe range (40–130)")


    if flags:
        status = "FAIL"
    elif warnings:
        status = "REVIEW"
    else:
        status = "PASS"


    audit_record = {
        "audit_id": audit_id,
        "timestamp": timestamp,
        "patient_name": patient_name,
        "status": status,
        "flags": flags,
        "warnings": warnings
    }


    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(audit_record) + "\n")

 
    print("\n" + "=" * 39)
    print("CLINICAL DATA AUDIT REPORT")
    print("=" * 39)
    print(f"Audit ID     : {audit_id}")
    print(f"Timestamp    : {timestamp}")
    print(f"Patient Name : {patient_name}")
    print(f"Audit Status : {status}")

    print("\nFlags:")
    if flags:
        for f in flags:
            print(f" - {f}")
    else:
        print(" None")

    print("\nWarnings:")
    if warnings:
        for w in warnings:
            print(f" - {w}")
    else:
        print(" None")

    print("\nDISCLAIMER:")
    print("This is a non-diagnostic audit report only.")
    print("Not medically certified. No medical advice provided.")
    print("=" * 39)


if __name__ == "__main__":
    audit_patient_data()