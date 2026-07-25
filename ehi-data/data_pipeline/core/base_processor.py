from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime


class BaseProcessor(ABC):
    """
    Base class for all data processors.
    Every processor must inherit from this class.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.processed_data = {}
        self.errors = []
        self.warnings = []

    @abstractmethod
    def can_process(self, data: Dict[str, Any]) -> bool:
        """
        Determine whether this processor can process the input data.
        """
        pass

    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and return the result.
        """
        pass

    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """
        Return the list of required fields needed for processing.
        """
        pass

    def add_error(self, error: str):
        """Record a processing error."""
        self.errors.append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": error,
            }
        )

    def add_warning(self, warning: str):
        """Record a processing warning."""
        self.warnings.append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": warning,
            }
        )

    def get_status(self) -> Dict[str, Any]:
        """Return the current processor status."""
        return {
            "processor": self.name,
            "errors": self.errors,
            "warnings": self.warnings,
            "processed_at": datetime.now().isoformat(),
        }