"""
Core components for PII anonymization system

This package contains the fundamental types, base classes, and exceptions
used throughout the PII anonymization system.
"""

from .types import (
    Language, DataType, ProcessingConfig,
    AnonymizationResult, DeanonymizationResult,
    EntityMatch, AnonymizedEntity
)
from .exceptions import (
    PIIAnonymizerError, UnsupportedLanguageError,
    UnsupportedDataTypeError, RecognizerInitializationError,
    ProcessingError, DeanonymizationError
)
from .base import BaseRecognizer, BaseProcessor, BaseAnonymizerEngine

__all__ = [
    # Types
    "Language", "DataType", "ProcessingConfig",
    "AnonymizationResult", "DeanonymizationResult", 
    "EntityMatch", "AnonymizedEntity",
    
    # Exceptions
    "PIIAnonymizerError", "UnsupportedLanguageError",
    "UnsupportedDataTypeError", "RecognizerInitializationError",
    "ProcessingError", "DeanonymizationError",
    
    # Base classes
    "BaseRecognizer", "BaseProcessor", "BaseAnonymizerEngine"
]
