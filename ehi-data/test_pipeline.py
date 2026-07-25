from data_pipeline import DataPipeline
import json
import random
from datetime import datetime, timedelta
from faker import Faker


fake = Faker()

def generate_random_patient():
    """Generate random data for a patient"""
    
    
    age = random.randint(18, 90)
    
    
    today = datetime.now()
    birth_year = today.year - age
    birth_date = fake.date_of_birth(minimum_age=age, maximum_age=age)
    
    
    gender = random.choice(["Male", "Female"])
    
    
    has_hypertension = random.random() < 0.35
    has_diabetes = random.random() < 0.25
    is_smoker = random.random() < 0.20
    family_history_ad = random.random() < 0.15
    apoe_e4_carrier = random.random() < 0.15
    
    
    lab_results = [
        {
            "test": "hemoglobin",
            "value": round(random.uniform(11, 17), 1),
            "unit": "g/dL",
            "date": fake.date_this_year().isoformat()
        },
        {
            "test": "a1c",
            "value": round(random.uniform(4.5, 8.0), 1),
            "unit": "%",
            "date": fake.date_this_year().isoformat()
        },
        {
            "test": "ldl",
            "value": random.randint(70, 200),
            "unit": "mg/dL",
            "date": fake.date_this_year().isoformat()
        },
        {
            "test": "hdl",
            "value": random.randint(30, 70),
            "unit": "mg/dL",
            "date": fake.date_this_year().isoformat()
        },
        {
            "test": "glucose",
            "value": random.randint(70, 140),
            "unit": "mg/dL",
            "date": fake.date_this_year().isoformat()
        },
        {
            "test": "creatinine",
            "value": round(random.uniform(0.6, 1.4), 2),
            "unit": "mg/dL",
            "date": fake.date_this_year().isoformat()
        }
    ]
    
    
    possible_meds = [
        {"name": "Metformin", "dosage": "500mg", "status": "Active"},
        {"name": "Lisinopril", "dosage": "10mg", "status": "Active"},
        {"name": "Atorvastatin", "dosage": "20mg", "status": "Active"},
        {"name": "Amlodipine", "dosage": "5mg", "status": "Active"},
        {"name": "Losartan", "dosage": "50mg", "status": "Active"},
        {"name": "Levothyroxine", "dosage": "100mcg", "status": "Active"}
    ]
    
    medications = []
    
    
    for _ in range(random.randint(1, 3)):
        med = random.choice(possible_meds)
        if med not in medications:
            medications.append(med)
    
    
    vitals = [
        {
            "type": "blood_pressure_systolic",
            "value": random.randint(100, 160),
            "unit": "mmHg",
            "date": fake.date_this_year().isoformat()
        },
        {
            "type": "blood_pressure_diastolic",
            "value": random.randint(60, 100),
            "unit": "mmHg",
            "date": fake.date_this_year().isoformat()
        },
        {
            "type": "heart_rate",
            "value": random.randint(60, 100),
            "unit": "bpm",
            "date": fake.date_this_year().isoformat()
        },
        {
            "type": "temperature",
            "value": round(random.uniform(36.0, 37.5), 1),
            "unit": "°C",
            "date": fake.date_this_year().isoformat()
        },
        {
            "type": "respiratory_rate",
            "value": random.randint(12, 20),
            "unit": "/min",
            "date": fake.date_this_year().isoformat()
        },
        {
            "type": "oxygen_saturation",
            "value": random.randint(95, 100),
            "unit": "%",
            "date": fake.date_this_year().isoformat()
        }
    ]
    
    
    visit_types = ["outpatient", "inpatient", "emergency", "telehealth"]
    encounters = []
    
    for _ in range(random.randint(1, 4)):
        encounters.append({
            "id": fake.uuid4()[:8].upper(),
            "type": random.choice(visit_types),
            "date": fake.date_this_year().isoformat(),
            "provider": fake.name(),
            "department": random.choice([
                "Cardiology",
                "Endocrinology",
                "Neurology",
                "Orthopedics",
                "Internal Medicine"
            ]),
            "diagnosis": random.choice([
                "Hypertension",
                "Diabetes Type 2",
                "Hyperlipidemia",
                "Arthritis",
                "Migraine",
                "GERD"
            ])
        })
    
    return {
        "age": age,
        "gender": gender,
        "date_of_birth": birth_date.strftime("%Y-%m-%d"),
        "address": fake.address().replace("\n", ", "),
        "ethnicity": random.choice(["Hispanic", "Non-Hispanic"]),
        "race": random.choice(["White", "Black", "Asian", "Other"]),
        "has_hypertension": has_hypertension,
        "has_diabetes": has_diabetes,
        "is_smoker": is_smoker,
        "family_history_ad": family_history_ad,
        "apoe_e4_carrier": apoe_e4_carrier,
        "lab_results": lab_results,
        "medications": medications,
        "encounters": encounters,
        "vitals": vitals
    }



def main():

    print("=" * 60)
    print("🧬 Data Pipeline Test - Dynamic Data")
    print("=" * 60)

   
    pipeline = DataPipeline()
    
    print("\n Available Processors:")
    for name in pipeline.get_all_processors():
        print(f"   - {name}")


    
    raw_data = generate_random_patient()
    
    print("\n📥 Input Data (Randomly Generated):")
    print(f"   Age: {raw_data['age']}")
    print(f"   Gender: {raw_data['gender']}")
    print(f"   Hypertension: {'✅' if raw_data['has_hypertension'] else '❌'}")
    print(f"   Diabetes: {'✅' if raw_data['has_diabetes'] else '❌'}")
    print(f"   Smoker: {'✅' if raw_data['is_smoker'] else '❌'}")
    print(f"   Family History of AD: {'✅' if raw_data['family_history_ad'] else '❌'}")
    print(f"   APOE-e4 Carrier: {'✅' if raw_data['apoe_e4_carrier'] else '❌'}")
    print(f"   Number of Lab Tests: {len(raw_data['lab_results'])}")
    print(f"   Number of Medications: {len(raw_data['medications'])}")
    print(f"   Number of Encounters: {len(raw_data['encounters'])}")
    print(f"   Number of Vital Signs: {len(raw_data['vitals'])}")


    
    print("\n" + "-" * 60)
    print("🔄 Processing Data...")
    print("-" * 60)

    results = pipeline.process(raw_data)


    
    print("\n📊 Processing Results:")

    for processor_name, data in results["results"].items():

        if data["result"] and data["result"] != {}:

            print(f"\n📌 {processor_name}:")
            result = data["result"]

            if "age_group" in result:
                print(f"   Age Group: {result['age_group']}")

            if "lab_results" in result:
                total = result.get("summary", {}).get("total", 0)
                abnormal = result.get("summary", {}).get("abnormal", 0)
                print(f"   Lab Tests: {total} (Abnormal: {abnormal})")

            if "medications" in result:
                print(
                    f"   Medications: {result.get('total', 0)} "
                    f"(Active: {result.get('active_count', 0)})"
                )

            if "encounters" in result:
                print(f"   Encounters: {result.get('total', 0)}")
                by_type = result.get("by_type", {})
                if by_type:
                    print(f"   Encounter Types: {by_type}")

            if "vitals" in result:
                print(f"   Vital Signs: {result.get('total', 0)}")
                print(f"   Abnormal: {result.get('abnormal_count', 0)}")


    
    filename = (
        f"test_processed_data_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    pipeline.save_results(filename)

    print(f"\n✅ Results saved to '{filename}'")


    
    status = pipeline.get_pipeline_status()

    print(f"\n📋 Pipeline Status: {status['status']}")
    print(f"   Started: {status['started_at']}")
    print(f"   Completed: {status['completed_at']}")

    if status.get("errors"):
        print(f"   ❌ Errors: {len(status['errors'])}")

    if status.get("warnings"):
        print(f"   ⚠️ Warnings: {len(status['warnings'])}")


    print("\n" + "=" * 60)
    print("✅ Pipeline Test Completed Successfully!")
    print("=" * 60)



if __name__ == "__main__":
    main()