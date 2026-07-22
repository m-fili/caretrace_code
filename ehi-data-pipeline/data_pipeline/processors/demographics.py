from datetime import datetime
from typing import Dict, Any, List

from ..core.base_processor import BaseProcessor
from ..utils.date_utils import calculate_age, get_age_group


class DemographicsProcessor(BaseProcessor):
    """Processes patient demographic information."""

    def __init__(self):
        super().__init__(
            name="Demographics Processor",
            description=(
                "Processes patient demographic data, including age, "
                "gender, and location."
            ),
        )

    def can_process(self, data: Dict[str, Any]) -> bool:
        """Check whether the required demographic fields are available."""
        required = self.get_required_fields()
        return any(field in data for field in required)

    def get_required_fields(self) -> List[str]:
        """Return the required fields for demographic processing."""
        return ["age", "gender", "date_of_birth", "dob"]

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient demographic data."""
        try:
            # Extract data
            age = data.get("age", 0)
            dob = data.get("date_of_birth") or data.get("dob")
            gender = data.get("gender", "Unknown")

            # Calculate age from date of birth if necessary
            if dob and not age:
                age = calculate_age(dob)

            result = {
                "age": age,
                "gender": gender,
                "date_of_birth": dob,
                "calculated_age": (
                    age if age else calculate_age(dob) if dob else None
                ),
                "age_group": get_age_group(age),
            }

            # Additional demographic information
            if "address" in data:
                result["address"] = data["address"]

            if "ethnicity" in data:
                result["ethnicity"] = data["ethnicity"]

            if "race" in data:
                result["race"] = data["race"]

            self.processed_data = result
            return result

        except Exception as e:
            self.add_error(f"Error processing demographics: {str(e)}")
            return {}