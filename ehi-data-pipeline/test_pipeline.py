from data_pipeline import DataPipeline
import json


def main():
    print("=" * 60)
    print("🧬 Data Pipeline Test")
    print("=" * 60)

    # ============================================================
    # 1. Create Pipeline Instance
    # ============================================================
    pipeline = DataPipeline()

    print("\n📋 Available Processors:")
    for name in pipeline.get_all_processors():
        print(f"   - {name}")

    # ============================================================
    # 2. Sample Input Data
    # ============================================================
    raw_data = {
        "age": 72,
        "gender": "Male",
        "date_of_birth": "1952-06-11",
        "address": "123 Main St, Boston, MA",
        "ethnicity": "Hispanic",
        "race": "White",

        # Laboratory data
        "lab_results": [
            {
                "test": "hemoglobin",
                "value": 14.5,
                "unit": "g/dL",
                "date": "2024-06-11",
            },
            {
                "test": "a1c",
                "value": 6.2,
                "unit": "%",
                "date": "2024-06-11",
            },
            {
                "test": "ldl",
                "value": 145,
                "unit": "mg/dL",
                "date": "2024-06-11",
            },
            {
                "test": "hdl",
                "value": 38,
                "unit": "mg/dL",
                "date": "2024-06-11",
            },
            {
                "test": "glucose",
                "value": 110,
                "unit": "mg/dL",
                "date": "2024-06-11",
            },
            {
                "test": "creatinine",
                "value": 1.0,
                "unit": "mg/dL",
                "date": "2024-06-11",
            },
        ],

        # Medication data
        "medications": [
            {
                "name": "Metformin",
                "dosage": "500mg",
                "frequency": "twice daily",
                "status": "Active",
            },
            {
                "name": "Lisinopril",
                "dosage": "10mg",
                "frequency": "once daily",
                "status": "Active",
            },
            {
                "name": "Atorvastatin",
                "dosage": "20mg",
                "frequency": "once daily",
                "status": "Active",
            },
        ],

        # Encounter data
        "encounters": [
            {
                "id": "ENC001",
                "type": "outpatient",
                "date": "2024-06-11",
                "provider": "Dr. Smith",
                "department": "Cardiology",
                "diagnosis": "Hypertension",
            },
            {
                "id": "ENC002",
                "type": "telehealth",
                "date": "2024-05-15",
                "provider": "Dr. Jones",
                "department": "Endocrinology",
                "diagnosis": "Type 2 Diabetes",
            },
        ],

        # Vital signs data
        "vitals": [
            {
                "type": "blood_pressure_systolic",
                "value": 135,
                "unit": "mmHg",
                "date": "2024-06-11",
            },
            {
                "type": "blood_pressure_diastolic",
                "value": 85,
                "unit": "mmHg",
                "date": "2024-06-11",
            },
            {
                "type": "heart_rate",
                "value": 72,
                "unit": "bpm",
                "date": "2024-06-11",
            },
            {
                "type": "temperature",
                "value": 36.8,
                "unit": "°C",
                "date": "2024-06-11",
            },
            {
                "type": "respiratory_rate",
                "value": 16,
                "unit": "/min",
                "date": "2024-06-11",
            },
            {
                "type": "oxygen_saturation",
                "value": 98,
                "unit": "%",
                "date": "2024-06-11",
            },
        ],
    }

    print("\n📥 Input Data:")
    print(f"   Age: {raw_data['age']}")
    print(f"   Gender: {raw_data['gender']}")
    print(f"   Number of laboratory tests: {len(raw_data['lab_results'])}")
    print(f"   Number of medications: {len(raw_data['medications'])}")
    print(f"   Number of encounters: {len(raw_data['encounters'])}")
    print(f"   Number of vital signs: {len(raw_data['vitals'])}")

    # ============================================================
    # 3. Execute Pipeline Processing
    # ============================================================
    print("\n" + "-" * 60)
    print("🔄 Processing data...")
    print("-" * 60)

    results = pipeline.process(raw_data)

    # ============================================================
    # 4. Display Processing Results
    # ============================================================
    print("\n📊 Processing Results:")

    for processor_name, data in results["results"].items():
        if data["result"] and data["result"] != {}:
            print(f"\n📌 {processor_name}:")

            result = data["result"]

            if "age_group" in result:
                print(f"   Age group: {result['age_group']}")

            if "lab_results" in result:
                total = result.get("summary", {}).get("total", 0)
                abnormal = result.get("summary", {}).get("abnormal", 0)
                print(
                    f"   Laboratory tests: {total} "
                    f"(Abnormal: {abnormal})"
                )

            if "medications" in result:
                print(
                    f"   Medications: {result.get('total', 0)} "
                    f"(Active: {result.get('active_count', 0)})"
                )

            if "encounters" in result:
                print(
                    f"   Encounters: {result.get('total', 0)}"
                )

                by_type = result.get("by_type", {})
                if by_type:
                    print(f"   Encounter types: {by_type}")

            if "vitals" in result:
                print(
                    f"   Vital signs: {result.get('total', 0)}"
                )
                print(
                    f"   Abnormal values: "
                    f"{result.get('abnormal_count', 0)}"
                )

    # ============================================================
    # 5. Save Results
    # ============================================================
    pipeline.save_results("test_processed_data.json")

    print("\n✅ Results saved to 'test_processed_data.json'.")

    # ============================================================
    # 6. Display Pipeline Status Summary
    # ============================================================
    status = pipeline.get_pipeline_status()

    print(f"\n📋 Pipeline Status: {status['status']}")
    print(f"   Started: {status['started_at']}")
    print(f"   Completed: {status['completed_at']}")

    if status.get("errors"):
        print(f"   ❌ Errors: {len(status['errors'])}")

    if status.get("warnings"):
        print(f"   ⚠️ Warnings: {len(status['warnings'])}")

    print("\n" + "=" * 60)
    print("✅ Pipeline test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()