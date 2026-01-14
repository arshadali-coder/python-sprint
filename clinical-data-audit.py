import uuid
import json
from datetime import datetime

AUDIT_FILE = "audit_log.jsonl"


def get_input(prompt):
    return input(prompt).strip()


def safe_int(value):
    return int(value) if value.isdigit() else None


def audit_patient_data():
    flags = []
    warnings = []

    audit_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    patient_name = get_input("Enter patient name: ")
    if not patient_name:
        flags.append("Patient name cannot be empty")

    age = get_input("Enter age: ")
    heart_rate = get_input("Enter heart rate (bpm): ")
    systolic = get_input("Enter systolic BP: ")
    diastolic = get_input("Enter diastolic BP: ")
    allergy = get_input("Allergy (yes/no): ").lower()

    age_i = safe_int(age)
    hr_i = safe_int(heart_rate)
    sys_i = safe_int(systolic)
    dia_i = safe_int(diastolic)

    if age_i is None or not (0 <= age_i <= 120):
        flags.append("Invalid age (must be 0–120)")

    if hr_i is None:
        flags.append("Heart rate must be numeric")

    if sys_i is None or dia_i is None:
        flags.append("Blood pressure values must be numeric")
    elif sys_i <= dia_i:
        flags.append("Systolic BP must be greater than Diastolic BP")

    if allergy not in ["yes", "no"]:
        flags.append("Allergy field must be yes or no")

    if hr_i is not None and (hr_i < 40 or hr_i > 180):
        warnings.append("Heart rate outside safe range (40–180 bpm)")

    if sys_i is not None and (sys_i < 70 or sys_i > 200):
        warnings.append("Systolic BP outside safe range (70–200)")

    if dia_i is not None and (dia_i < 40 or dia_i > 130):
        warnings.append("Diastolic BP outside safe range (40–130)")

    derived_metrics = {}
    if sys_i is not None and dia_i is not None:
        derived_metrics["pulse_pressure"] = sys_i - dia_i
        derived_metrics["mean_arterial_pressure"] = round(
            (sys_i + 2 * dia_i) / 3, 2
        )

    severity_score = len(flags) * 10 + len(warnings) * 3

    if flags:
        status = "FAIL"
    elif warnings:
        status = "REVIEW"
    else:
        status = "PASS"

    audit_record = {
        "audit_id": audit_id,
        "correlation_id": correlation_id,
        "timestamp": timestamp,
        "input_data": {
            "patient_name": patient_name,
            "age": age_i,
            "heart_rate": hr_i,
            "blood_pressure": {
                "systolic": sys_i,
                "diastolic": dia_i
            },
            "allergy": allergy
        },
        "derived_metrics": derived_metrics,
        "audit_result": {
            "status": status,
            "severity_score": severity_score,
            "flags": flags,
            "warnings": warnings
        }
    }

    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(audit_record) + "\n")

    print("\n" + "=" * 45)
    print("CLINICAL DATA AUDIT REPORT")
    print("=" * 45)
    print(f"Audit ID        : {audit_id}")
    print(f"Correlation ID  : {correlation_id}")
    print(f"Timestamp       : {timestamp}")
    print(f"Patient Name    : {patient_name}")
    print(f"Audit Status    : {status}")
    print(f"Severity Score  : {severity_score}")

    print("\nDerived Metrics:")
    if derived_metrics:
        for k, v in derived_metrics.items():
            print(f" - {k}: {v}")
    else:
        print(" None")

    print("\nFlags:")
    print("\n".join(f" - {f}" for f in flags) if flags else " None")

    print("\nWarnings:")
    print("\n".join(f" - {w}" for w in warnings) if warnings else " None")

    print("\nDISCLAIMER:")
    print("Non-diagnostic audit system.")
    print("For software validation only. Not medical advice.")
    print("=" * 45)


if __name__ == "__main__":
    audit_patient_data()