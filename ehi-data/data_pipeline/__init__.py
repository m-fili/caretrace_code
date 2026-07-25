"""
Data Pipeline for CareTracer
A modular pipeline for processing EHI data from various sources
"""

from .core.pipeline import DataPipeline
from .core.base_processor import BaseProcessor
from .processors.demographics import DemographicsProcessor
from .processors.labs import LabsProcessor
from .processors.medications import MedicationsProcessor
from .processors.encounters import EncountersProcessor
from .processors.vitals import VitalsProcessor

__version__ = "1.0.0"
__all__ = [
    'DataPipeline',
    'BaseProcessor',
    'DemographicsProcessor',
    'LabsProcessor',
    'MedicationsProcessor',
    'EncountersProcessor',
    'VitalsProcessor'
]