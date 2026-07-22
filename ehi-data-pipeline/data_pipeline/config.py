"""
Configuration settings for the Data Pipeline
"""

PIPELINE_CONFIG = {
    "version": "1.0.0",
    "processors": {
        "demographics": {
            "enabled": True,
            "required_fields": ["age", "gender", "date_of_birth"]
        },
        "labs": {
            "enabled": True,
            "reference_ranges": {
                "hemoglobin": {"min": 12.0, "max": 16.0, "unit": "g/dL"},
                "a1c": {"min": 4.0, "max": 5.6, "unit": "%"},
                "ldl": {"min": 0, "max": 100, "unit": "mg/dL"},
                "hdl": {"min": 40, "max": 60, "unit": "mg/dL"},
                "glucose": {"min": 70, "max": 100, "unit": "mg/dL"},
                "creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL"},
                "egfr": {"min": 90, "max": 120, "unit": "mL/min/1.73m²"}
            }
        },
        "medications": {
            "enabled": True,
            "active_statuses": ["active", "current", "ongoing", "prescribed"]
        },
        "encounters": {
            "enabled": True,
            "visit_types": ["outpatient", "inpatient", "emergency", "telehealth"]
        },
        "vitals": {
            "enabled": True,
            "normal_ranges": {
                "blood_pressure_systolic": {"min": 90, "max": 140},
                "blood_pressure_diastolic": {"min": 60, "max": 90},
                "heart_rate": {"min": 60, "max": 100},
                "temperature": {"min": 36.0, "max": 37.5},
                "respiratory_rate": {"min": 12, "max": 20},
                "oxygen_saturation": {"min": 95, "max": 100}
            }
        }
    },
    "output": {
        "save_json": True,
        "json_filename": "processed_data.json"
    }
}