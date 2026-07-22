from datetime import datetime
from typing import Dict, Any, List

from ..core.base_processor import BaseProcessor
from ..config import PIPELINE_CONFIG


class LabsProcessor(BaseProcessor):
    """Processes laboratory test results."""

    def __init__(self):
        super().__init__(
            name="Labs Processor",
            description=(
                "Processes laboratory results, including blood tests, "
                "biomarkers, and other clinical measurements."
            ),
        )
        self.reference_ranges = PIPELINE_CONFIG["processors"]["labs"][
            "reference_ranges"
        ]

    def can_process(self, data: Dict[str, Any]) -> bool:
        """Check whether laboratory data is available."""
        lab_fields = ["lab_results", "labs", "observations", "laboratory"]
        return any(field in data for field in lab_fields)

    def get_required_fields(self) -> List[str]:
        """Return the required fields for laboratory processing."""
        return ["lab_results"]

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process laboratory test results."""
        try:
            lab_data = (
                data.get("lab_results", [])
                or data.get("labs", [])
                or data.get("observations", [])
            )

            if not lab_data:
                self.add_warning("No laboratory data found.")
                return {"lab_results": []}

            processed_labs = []

            for lab in lab_data:
                processed = self._process_single_lab(lab)
                if processed:
                    processed_labs.append(processed)

            return {
                "lab_results": processed_labs,
                "summary": self._generate_summary(processed_labs),
                "abnormal_results": self._get_abnormal_results(processed_labs),
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            self.add_error(f"Error processing laboratory results: {str(e)}")
            return {}

    def _process_single_lab(self, lab: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single laboratory result."""
        try:
            test_name = lab.get("test", lab.get("name", "")).lower()
            value = lab.get("value", 0)
            ref_range = self.reference_ranges.get(test_name, {})

            return {
                "test": lab.get("test", lab.get("name", "Unknown")),
                "value": value,
                "unit": lab.get("unit", ref_range.get("unit", "")),
                "date": lab.get(
                    "date",
                    lab.get(
                        "performed_date",
                        datetime.now().isoformat(),
                    ),
                ),
                "reference_range": (
                    f"{ref_range.get('min', 'N/A')} - "
                    f"{ref_range.get('max', 'N/A')}"
                ),
                "is_abnormal": self._is_abnormal(value, ref_range),
                "status": self._get_status(value, ref_range),
            }

        except Exception:
            return None

    def _is_abnormal(self, value: float, ref_range: Dict) -> bool:
        """Determine whether a laboratory value is outside its reference range."""
        if not ref_range:
            return False

        if value < ref_range.get("min", -float("inf")):
            return True

        if value > ref_range.get("max", float("inf")):
            return True

        return False

    def _get_status(self, value: float, ref_range: Dict) -> str:
        """Return the clinical status of a laboratory value."""
        if not ref_range:
            return "Unknown"

        if value < ref_range.get("min", -float("inf")):
            return "Low"

        if value > ref_range.get("max", float("inf")):
            return "High"

        return "Normal"

    def _generate_summary(self, labs: List[Dict]) -> Dict:
        """Generate a summary of processed laboratory results."""
        if not labs:
            return {
                "total": 0,
                "abnormal": 0,
                "normal": 0,
            }

        total = len(labs)
        abnormal = sum(
            1 for lab in labs if lab.get("is_abnormal", False)
        )

        return {
            "total": total,
            "abnormal": abnormal,
            "normal": total - abnormal,
            "abnormal_percentage": (
                abnormal / total * 100 if total > 0 else 0
            ),
        }

    def _get_abnormal_results(self, labs: List[Dict]) -> List[Dict]:
        """Return only abnormal laboratory results."""
        return [
            lab
            for lab in labs
            if lab.get("is_abnormal", False)
        ]