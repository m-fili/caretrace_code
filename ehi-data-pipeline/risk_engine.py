import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================
# 1. Base Classes for Modules
# ============================================================
class RiskFactor:
    def __init__(self, name: str, description: str, required_vars: List[str], weight: float = 1.0):
        self.name = name
        self.description = description
        self.required_vars = required_vars
        self.weight = weight

class RiskModule:
    def __init__(self, module_id: str, name: str, description: str):
        self.module_id = module_id
        self.name = name
        self.description = description
        self.risk_factors: List[RiskFactor] = []
    
    def add_risk_factor(self, factor: RiskFactor):
        self.risk_factors.append(factor)
    
    def get_required_vars(self) -> List[str]:
        vars_set = set()
        for factor in self.risk_factors:
            vars_set.update(factor.required_vars)
        return list(vars_set)
    
    def calculate(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement calculate()")

# ============================================================
# 2. Alzheimer's Disease Module (AD)
# ============================================================
class AlzheimerModule(RiskModule):
    def __init__(self):
        super().__init__(
            module_id="AD",
            name="Alzheimer's Disease",
            description="Risk assessment for Alzheimer's Disease based on clinical and genetic factors."
        )
        # Define risk factors
        self.add_risk_factor(RiskFactor(
            name="Age",
            description="Age is the strongest known risk factor for Alzheimer's disease.",
            required_vars=["age"],
            weight=1.0
        ))
        self.add_risk_factor(RiskFactor(
            name="Family History",
            description="Family history of Alzheimer's or dementia increases risk.",
            required_vars=["family_history_ad"],
            weight=1.5
        ))
        self.add_risk_factor(RiskFactor(
            name="APOE-e4 Genotype",
            description="APOE-e4 is the strongest genetic risk factor for late-onset Alzheimer's.",
            required_vars=["apoe_e4_carrier"],
            weight=2.0
        ))
        self.add_risk_factor(RiskFactor(
            name="Cardiovascular Health",
            description="Poor cardiovascular health (hypertension, diabetes) increases AD risk.",
            required_vars=["has_hypertension", "has_diabetes"],
            weight=1.2
        ))
        self.add_risk_factor(RiskFactor(
            name="Cognitive Test Score",
            description="Lower scores on cognitive tests (like MoCA) indicate higher risk.",
            required_vars=["moca_score"],
            weight=1.0
        ))
    
    def calculate(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        
        # 1. Age
        age = patient_data.get("age", 0)
        if age >= 65:
            score += (age - 60) * 0.5
        
        # 2. Family history
        if patient_data.get("family_history_ad", False):
            score += 15
        
        # 3. APOE-e4 gene
        if patient_data.get("apoe_e4_carrier", False):
            score += 20
        
        # 4. Cardiovascular diseases
        if patient_data.get("has_hypertension", False):
            score += 8
        if patient_data.get("has_diabetes", False):
            score += 10
        
        # 5. Cognitive test score
        moca = patient_data.get("moca_score", 30)
        if moca < 24:
            score += (24 - moca) * 1.5
        
        score = min(score, 100)
        
        # Determine risk level
        if score < 20:
            risk_level = "Low"
            interpretation = "Low risk of Alzheimer's Disease."
        elif score < 40:
            risk_level = "Moderate"
            interpretation = "Moderate risk. Consider lifestyle interventions and regular cognitive screening."
        elif score < 60:
            risk_level = "High"
            interpretation = "High risk. Please consult with a neurologist for further evaluation."
        else:
            risk_level = "Very High"
            interpretation = "Very high risk. Immediate consultation with a specialist is recommended."
        
        return {
            "module_id": self.module_id,
            "module_name": self.name,
            "score": round(score, 2),
            "risk_level": risk_level,
            "interpretation": interpretation,
            "risk_factors": self._get_factor_details(patient_data),
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_factor_details(self, patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        details = []
        for factor in self.risk_factors:
            values = [patient_data.get(var, None) for var in factor.required_vars]
            details.append({
                "name": factor.name,
                "value": values[0] if len(values) == 1 else values,
                "description": factor.description
            })
        return details

# ============================================================
# 3. Cardiovascular Disease Module (CVD)
# ============================================================
class CardiovascularModule(RiskModule):
    def __init__(self):
        super().__init__(
            module_id="CVD",
            name="Cardiovascular Disease",
            description="Risk assessment for Cardiovascular Disease based on established clinical guidelines."
        )
        self.add_risk_factor(RiskFactor(
            name="Age",
            description="Age is a major risk factor for cardiovascular disease.",
            required_vars=["age"],
            weight=1.0
        ))
        self.add_risk_factor(RiskFactor(
            name="Hypertension",
            description="High blood pressure is a leading cause of CVD.",
            required_vars=["has_hypertension"],
            weight=1.5
        ))
        self.add_risk_factor(RiskFactor(
            name="Smoking",
            description="Smoking significantly increases the risk of CVD.",
            required_vars=["is_smoker"],
            weight=2.0
        ))
        self.add_risk_factor(RiskFactor(
            name="Diabetes",
            description="Diabetes increases the risk of CVD by 2-4 times.",
            required_vars=["has_diabetes"],
            weight=1.8
        ))
        self.add_risk_factor(RiskFactor(
            name="Cholesterol",
            description="High LDL and low HDL cholesterol are risk factors.",
            required_vars=["ldl_cholesterol", "hdl_cholesterol"],
            weight=1.2
        ))
        self.add_risk_factor(RiskFactor(
            name="BMI",
            description="Obesity and overweight increase CVD risk.",
            required_vars=["bmi"],
            weight=1.0
        ))
    
    def calculate(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        
        # 1. Age
        age = patient_data.get("age", 0)
        if age >= 50:
            score += (age - 45) * 0.5
        
        # 2. Hypertension
        if patient_data.get("has_hypertension", False):
            score += 12
        
        # 3. Smoking
        if patient_data.get("is_smoker", False):
            score += 18
        
        # 4. Diabetes
        if patient_data.get("has_diabetes", False):
            score += 10
        
        # 5. Cholesterol
        ldl = patient_data.get("ldl_cholesterol", 100)
        if ldl > 130:
            score += (ldl - 130) * 0.2
        hdl = patient_data.get("hdl_cholesterol", 50)
        if hdl < 40:
            score += (40 - hdl) * 0.5
        
        # 6. BMI
        bmi = patient_data.get("bmi", 22)
        if bmi > 25:
            score += (bmi - 25) * 0.8
        
        score = min(score, 100)
        
        if score < 15:
            risk_level = "Low"
            interpretation = "Low risk of Cardiovascular Disease."
        elif score < 30:
            risk_level = "Moderate"
            interpretation = "Moderate risk. Consider lifestyle modifications and regular check-ups."
        elif score < 50:
            risk_level = "High"
            interpretation = "High risk. Please consult with a cardiologist."
        else:
            risk_level = "Very High"
            interpretation = "Very high risk. Immediate consultation with a specialist is recommended."
        
        return {
            "module_id": self.module_id,
            "module_name": self.name,
            "score": round(score, 2),
            "risk_level": risk_level,
            "interpretation": interpretation,
            "risk_factors": self._get_factor_details(patient_data),
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_factor_details(self, patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        details = []
        for factor in self.risk_factors:
            values = [patient_data.get(var, None) for var in factor.required_vars]
            details.append({
                "name": factor.name,
                "value": values[0] if len(values) == 1 else values,
                "description": factor.description
            })
        return details

# ============================================================
# 4. Main Risk Engine
# ============================================================
class RiskEngine:
    def __init__(self):
        self.modules: Dict[str, RiskModule] = {}
        self._register_default_modules()
    
    def _register_default_modules(self):
        self.register_module(AlzheimerModule())
        self.register_module(CardiovascularModule())
    
    def register_module(self, module: RiskModule):
        self.modules[module.module_id] = module
    
    def get_module(self, module_id: str) -> Optional[RiskModule]:
        return self.modules.get(module_id)
    
    def get_all_modules(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": module.module_id,
                "name": module.name,
                "description": module.description,
                "required_variables": module.get_required_vars()
            }
            for module in self.modules.values()
        ]
    
    def calculate_risk(self, patient_data: Dict[str, Any], module_id: Optional[str] = None) -> Dict[str, Any]:
        if module_id:
            module = self.get_module(module_id)
            if module:
                return {module_id: module.calculate(patient_data)}
            raise ValueError(f"Module '{module_id}' not found.")
        else:
            results = {}
            for module_id, module in self.modules.items():
                results[module_id] = module.calculate(patient_data)
            return results
    
    def save_results(self, patient_data: Dict[str, Any], filename: str = "risk_scores.json"):
        results = self.calculate_risk(patient_data)
        with open(filename, "w") as f:
            json.dump(results, f, indent=2, default=str)
        return results

# ============================================================
# 5. Execution and Testing
# ============================================================
if __name__ == "__main__":
    engine = RiskEngine()
    
    # Sample patient data
    patient_data = {
        "age": 72,
        "family_history_ad": True,
        "apoe_e4_carrier": True,
        "has_hypertension": True,
        "has_diabetes": True,
        "moca_score": 22,
        "is_smoker": False,
        "ldl_cholesterol": 145,
        "hdl_cholesterol": 38,
        "bmi": 28.5
    }
    
    print("🧬 Risk Engine Results")
    print("=" * 50)
    
    results = engine.calculate_risk(patient_data)
    
    for module_id, result in results.items():
        print(f"\n📌 {result['module_name']}:")
        print(f"   Score: {result['score']}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Interpretation: {result['interpretation']}")
    
    # Save to JSON
    engine.save_results(patient_data)
    print("\n✅ Results saved to 'risk_scores.json'")