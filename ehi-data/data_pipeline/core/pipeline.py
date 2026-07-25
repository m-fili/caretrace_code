from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .base_processor import BaseProcessor
from ..processors.demographics import DemographicsProcessor
from ..processors.labs import LabsProcessor
from ..processors.medications import MedicationsProcessor
from ..processors.encounters import EncountersProcessor
from ..processors.vitals import VitalsProcessor
from ..config import PIPELINE_CONFIG


class DataPipeline:
    """
    Core pipeline for processing EHI data.
    Manages all processors and coordinates data processing.
    """

    def __init__(self):
        self.processors: Dict[str, BaseProcessor] = {}
        self.results = {}
        self.pipeline_status = {
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "status": "initialized",
            "errors": [],
            "warnings": [],
            "config": PIPELINE_CONFIG,
        }
        self._register_default_processors()

    def _register_default_processors(self):
        """Register the default processors."""
        self.register_processor(DemographicsProcessor())
        self.register_processor(LabsProcessor())
        self.register_processor(MedicationsProcessor())
        self.register_processor(EncountersProcessor())
        self.register_processor(VitalsProcessor())

    def register_processor(self, processor: BaseProcessor):
        """Register a new processor."""
        self.processors[processor.name] = processor

    def get_processor(self, name: str) -> Optional[BaseProcessor]:
        """Retrieve a processor by name."""
        return self.processors.get(name)

    def get_all_processors(self) -> List[str]:
        """Return a list of all registered processor names."""
        return list(self.processors.keys())

    def process(
        self,
        raw_data: Dict[str, Any],
        processor_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Process raw EHI data.

        Args:
            raw_data: Raw input data (can originate from an EHI export or an API).
            processor_names: List of processor names to execute.
                If None, all registered processors will be executed.

        Returns:
            Processing results.
        """
        self.pipeline_status["status"] = "running"
        self.results = {}
        self.pipeline_status["errors"] = []
        self.pipeline_status["warnings"] = []

        # Select processors
        if processor_names:
            selected_processors = {
                name: self.processors[name]
                for name in processor_names
                if name in self.processors
            }
        else:
            selected_processors = self.processors

        if not selected_processors:
            self.pipeline_status["status"] = "failed"
            self.pipeline_status["errors"].append("No processors available")
            return {"error": "No processors available"}

        # Execute processors
        for name, processor in selected_processors.items():
            try:
                if processor.can_process(raw_data):
                    result = processor.process(raw_data)
                    self.results[name] = {
                        "result": result,
                        "status": processor.get_status(),
                    }
                else:
                    self.results[name] = {
                        "result": None,
                        "status": {
                            "processor": name,
                            "errors": [],
                            "warnings": [
                                f"Processor '{name}' cannot process the provided data."
                            ],
                            "processed_at": datetime.now().isoformat(),
                        },
                    }

            except Exception as e:
                self.pipeline_status["errors"].append(
                    f"Error in processor '{name}': {str(e)}"
                )
                self.results[name] = {
                    "result": None,
                    "status": {
                        "processor": name,
                        "errors": [str(e)],
                        "warnings": [],
                        "processed_at": datetime.now().isoformat(),
                    },
                }

        self.pipeline_status["completed_at"] = datetime.now().isoformat()
        self.pipeline_status["status"] = (
            "completed"
            if not self.pipeline_status["errors"]
            else "completed_with_errors"
        )

        return {
            "results": self.results,
            "pipeline_status": self.pipeline_status,
        }

    def get_processed_data(self, processor_name: str) -> Optional[Dict]:
        """Retrieve processed data from a specific processor."""
        if processor_name in self.results:
            return self.results[processor_name].get("result")
        return None

    def get_all_processed_data(self) -> Dict:
        """Retrieve all processed data."""
        result = {}
        for name, data in self.results.items():
            result[name] = data.get("result")
        return result

    def get_pipeline_status(self) -> Dict:
        """Return the current pipeline status."""
        return self.pipeline_status

    def save_results(self, filename: str = "processed_data.json"):
        """Save processing results to a JSON file."""
        output = {
            "results": self.results,
            "pipeline_status": self.pipeline_status,
            "timestamp": datetime.now().isoformat(),
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, default=str)

        return output

    def to_dict(self) -> Dict:
        """Convert pipeline results to a dictionary."""
        return {
            "results": self.results,
            "pipeline_status": self.pipeline_status,
        }