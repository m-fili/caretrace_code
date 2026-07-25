from datetime import datetime
from typing import Dict, Any, List

from ..core.base_processor import BaseProcessor
from ..config import PIPELINE_CONFIG


class VitalsProcessor(BaseProcessor):
    """Processes patient vital signs."""

    def __init__(self):
        super().__init__(
            name="Vitals Processor",
            description=(
                "Processes patient vital signs, including blood pressure, "
                "heart rate, temperature, and other measurements."
            ),
        )
        self.normal_ranges = PIPELINE_CONFIG["processors"]["vitals"][
            "normal_ranges"
        ]

    def can_process(self, data: Dict[str, Any]) -> bool:
        """Check whether vital sign data is available."""
        vital_fields = [
            "vitals",
            "vital_signs",
            "observations",
            "measurements",
        ]
        return any(field in data for field in vital_fields)

    def get_required_fields(self) -> List[str]:
        """Return the required fields for vital signs processing."""
        return ["vitals"]

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient vital sign records."""
        try:
            vitals = (
                data.get("vitals", [])
                or data.get("vital_signs", [])
                or data.get("observations", [])
            )

            if not vitals:
                self.add_warning("No vital signs found.")
                return {"vitals": []}

            processed_vitals = []

            for vital in vitals:
                processed = self._process_single_vital(vital)
                if processed:
                    processed_vitals.append(processed)

            return {
                "vitals": processed_vitals,
                "total": len(processed_vitals),
                "abnormal_count": sum(
                    1
                    for vital in processed_vitals
                    if vital.get("is_abnormal", False)
                ),
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            self.add_error(f"Error processing vital signs: {str(e)}")
            return {}

    def _process_single_vital(
        self, vital: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a single vital sign record."""
        try:
            vital_type = vital.get(
                "type",
                vital.get("name", ""),
            ).lower()

            value = vital.get("value", 0)
            normal_range = self.normal_ranges.get(vital_type, {})

            return {
                "type": vital_type,
                "value": value,
                "unit": vital.get("unit", ""),
                "date": vital.get(
                    "date",
                    vital.get(
                        "recorded_date",
                        datetime.now().isoformat(),
                    ),
                ),
                "normal_range": (
                    f"{normal_range.get('min', 'N/A')} - "
                    f"{normal_range.get('max', 'N/A')}"
                ),
                "is_abnormal": self._is_abnormal(value, normal_range),
                "status": self._get_status(value, normal_range),
            }

        except Exception:
            return None

    def _is_abnormal(self, value: float, normal_range: Dict) -> bool:
        """Determine whether a vital sign value is outside the normal range."""
        if not normal_range:
            return False

        if value < normal_range.get("min", -float("inf")):
            return True

        if value > normal_range.get("max", float("inf")):
            return True

        return False

    def _get_status(self, value: float, normal_range: Dict) -> str:
        """Return the status of a vital sign measurement."""
        if not normal_range:
            return "Unknown"

        if value < normal_range.get("min", -float("inf")):
            return "Low"

        if value > normal_range.get("max", float("inf")):
            return "High"

        return "Normal"