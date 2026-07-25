from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from risk_engine import RiskEngine
from data_pipeline import DataPipeline
import json
import os

app = Flask(__name__)
CORS(app)


risk_engine = RiskEngine()
data_pipeline = DataPipeline()

print("🧬 Risk Engine and Data Pipeline initialized successfully!")
print(f"📋 Available processors: {data_pipeline.get_all_processors()}")


@app.route('/')
def index():
    return send_from_directory('.', 'risk-scores.html')


@app.route('/api/pipeline/process', methods=['POST'])
def process_data_with_pipeline():
    """
    Process raw data using the Data Pipeline.

    Input:
        Raw healthcare data (e.g., Epic EHI Tables)

    Output:
        Processed healthcare data
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        
        results = data_pipeline.process(data)
        
       
        processed_data = data_pipeline.get_all_processed_data()
        
        return jsonify({
            "status": "success",
            "processed_data": processed_data,
            "pipeline_status": data_pipeline.get_pipeline_status(),
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/pipeline/risk', methods=['POST'])
def process_and_calculate_risk():
    """
    Process healthcare data through the Data Pipeline
    and calculate patient risk scores.

    Input:
        Raw healthcare data (e.g., Epic EHI Tables)

    Output:
        Risk scores and processed data
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        
        pipeline_results = data_pipeline.process(data)
        processed_data = data_pipeline.get_all_processed_data()
        
        
        patient_data = {}
        
        
        if "Demographics Processor" in processed_data and processed_data["Demographics Processor"]:
            demo = processed_data["Demographics Processor"]
            patient_data["age"] = demo.get("age", 50)
            patient_data["gender"] = demo.get("gender", "M")
        
        
        if "Labs Processor" in processed_data and processed_data["Labs Processor"]:
            labs = processed_data["Labs Processor"]
            lab_results = labs.get("lab_results", [])
            
            for lab in lab_results:
                test = lab.get("test", "").lower()
                value = lab.get("value", 0)
                
                if "ldl" in test:
                    patient_data["ldl_cholesterol"] = value
                elif "hdl" in test:
                    patient_data["hdl_cholesterol"] = value
                elif "glucose" in test:
                    patient_data["glucose"] = value
                elif "a1c" in test:
                    patient_data["a1c"] = value
        
        
        if "Medications Processor" in processed_data and processed_data["Medications Processor"]:
            meds = processed_data["Medications Processor"]
            medications = meds.get("medications", [])
            patient_data["medications"] = medications
            
            
            for med in medications:
                name = med.get("name", "").lower()
                
                if "metformin" in name or "insulin" in name:
                    patient_data["has_diabetes"] = True
                
                if "lisinopril" in name or "amlodipine" in name:
                    patient_data["has_hypertension"] = True
        
        
        patient_data.setdefault("has_hypertension", False)
        patient_data.setdefault("has_diabetes", False)
        patient_data.setdefault("is_smoker", False)
        patient_data.setdefault("ldl_cholesterol", 120)
        patient_data.setdefault("hdl_cholesterol", 45)
        patient_data.setdefault("bmi", 24.5)
        patient_data.setdefault("family_history_ad", False)
        patient_data.setdefault("apoe_e4_carrier", False)
        patient_data.setdefault("moca_score", 28)
        
        
        risk_results = risk_engine.calculate_risk(patient_data)
        
        return jsonify({
            "status": "success",
            "patient_data": patient_data,
            "risk_results": risk_results,
            "processed_data": processed_data,
            "pipeline_status": data_pipeline.get_pipeline_status()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/system/status', methods=['GET'])
def system_status():
    """Return overall system status."""
    return jsonify({
        "status": "healthy",
        "risk_engine": {
            "modules": risk_engine.get_all_modules(),
            "version": "1.0.0"
        },
        "data_pipeline": {
            "processors": data_pipeline.get_all_processors(),
            "version": "1.0.0"
        }
    })

@app.route('/api/modules')
def get_modules():
    return jsonify(risk_engine.get_all_modules())


@app.route('/api/calculate', methods=['POST'])
def calculate_risk():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    patient_data = data.get('patient_data', {})
    module_id = data.get('module_id')
    
    try:
        results = risk_engine.calculate_risk(patient_data, module_id)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/risk/calculate', methods=['POST'])
def calculate_risk_api():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        results = risk_engine.calculate_risk(data)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/risk/batch', methods=['POST'])
def batch_risk_calculation():
    data = request.get_json()
    
    if not data or 'patients' not in data:
        return jsonify({"error": "No patients data provided"}), 400
    
    try:
        all_results = []
        
        for patient in data['patients']:
            results = risk_engine.calculate_risk(patient)
            all_results.append({
                "patient": patient,
                "results": results
            })
        
        return jsonify(all_results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/risk/health-check', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "modules": risk_engine.get_all_modules(),
        "version": "2.0.0"
    })



if __name__ == '__main__':
    app.run(debug=True, port=5000)