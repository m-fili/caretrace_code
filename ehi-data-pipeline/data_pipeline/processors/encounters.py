from datetime import datetime
from typing import Dict, Any, List

from ..core.base_processor import BaseProcessor
from ..config import PIPELINE_CONFIG


class EncountersProcessor(BaseProcessor):
    """Processes patient encounters and medical visits."""

    def __init__(self):
        super().__init__(
            name="Encounters Processor",
            description=(
                "Processes patient encounters, including visits, "
                "hospital admissions, and appointments."
            ),
        )
        self.visit_types = PIPELINE_CONFIG["processors"]["encounters"][
            "visit_types"
        ]

    def can_process(self, data: Dict[str, Any]) -> bool:
        """Check whether encounter data is available."""
        encounter_fields = [
            "encounters",
            "visits",
            "appointments",
            "admissions",
        ]
        return any(field in data for field in encounter_fields)

    def get_required_fields(self) -> List[str]:
        """Return the required fields for encounter processing."""
        return ["encounters"]

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient encounter records."""
        try:
            encounters = (
                data.get("encounters", [])
                or data.get("visits", [])
                or data.get("appointments", [])
            )

            if not encounters:
                self.add_warning("No encounter data found.")
                return {"encounters": []}

            processed_encounters = []

            for encounter in encounters:
                processed = self._process_single_encounter(encounter)
                if processed:
                    processed_encounters.append(processed)

            return {
                "encounters": processed_encounters,
                "total": len(processed_encounters),
                "by_type": self._group_by_type(processed_encounters),
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            self.add_error(f"Error processing encounters: {str(e)}")
            return {}

    def _process_single_encounter(
        self, encounter: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a single patient encounter record."""
        try:
            return {
                "id": encounter.get(
                    "id",
                    encounter.get("encounter_id", ""),
                ),
                "type": encounter.get(
                    "type",
                    encounter.get("visit_type", "Unknown"),
                ),
                "date": encounter.get(
                    "date",
                    encounter.get(
                        "visit_date",
                        datetime.now().isoformat(),
                    ),
                ),
                "provider": encounter.get(
                    "provider",
                    encounter.get("doctor", ""),
                ),
                "department": encounter.get(
                    "department",
                    encounter.get("facility", ""),
                ),
                "diagnosis": encounter.get(
                    "diagnosis",
                    encounter.get("primary_diagnosis", ""),
                ),
                "notes": encounter.get("notes", ""),
            }

        except Exception:
            return None

    def _group_by_type(self, encounters: List[Dict]) -> Dict:
        """Group encounters by visit type."""
        result = {}

        for encounter in encounters:
            encounter_type = encounter.get("type", "Unknown")
            result[encounter_type] = result.get(encounter_type, 0) + 1

        return result