from datetime import datetime
from typing import Dict, Any, List

from ..core.base_processor import BaseProcessor
from ..config import PIPELINE_CONFIG


class MedicationsProcessor(BaseProcessor):
    """Processes patient medication records."""

    def __init__(self):
        super().__init__(
            name="Medications Processor",
            description=(
                "Processes patient medications, including current and "
                "historical prescriptions."
            ),
        )
        self.active_statuses = PIPELINE_CONFIG["processors"]["medications"][
            "active_statuses"
        ]

    def can_process(self, data: Dict[str, Any]) -> bool:
        """Check whether medication data is available."""
        medication_fields = [
            "medications",
            "prescriptions",
            "current_medications",
            "drugs",
        ]
        return any(field in data for field in medication_fields)

    def get_required_fields(self) -> List[str]:
        """Return the required fields for medication processing."""
        return ["medications"]

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient medication data."""
        try:
            medications = (
                data.get("medications", [])
                or data.get("prescriptions", [])
                or data.get("current_medications", [])
            )

            if not medications:
                self.add_warning("No medication data found.")
                return {"medications": []}

            processed_medications = []

            for medication in medications:
                processed = self._process_single_medication(medication)
                if processed:
                    processed_medications.append(processed)

            return {
                "medications": processed_medications,
                "total": len(processed_medications),
                "active_count": sum(
                    1
                    for medication in processed_medications
                    if medication.get("is_active", False)
                ),
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            self.add_error(f"Error processing medications: {str(e)}")
            return {}

    def _process_single_medication(
        self, medication: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a single medication record."""
        try:
            status = medication.get("status", "Active")

            return {
                "name": medication.get(
                    "name",
                    medication.get("drug_name", "Unknown"),
                ),
                "dosage": medication.get("dosage", ""),
                "frequency": medication.get("frequency", ""),
                "route": medication.get("route", ""),
                "start_date": medication.get(
                    "start_date",
                    medication.get("prescribed_date", ""),
                ),
                "end_date": medication.get(
                    "end_date",
                    medication.get("discontinued_date", ""),
                ),
                "status": status,
                "is_active": status.lower() in self.active_statuses,
                "prescriber": medication.get(
                    "prescriber",
                    medication.get("doctor", ""),
                ),
                "notes": medication.get("notes", ""),
            }

        except Exception:
            return None