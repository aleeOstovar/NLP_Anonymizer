"""
PII Anonymization/Deanonymization System

A comprehensive system for detecting and anonymizing Personally Identifiable Information (PII)
in text, images (OCR), CSV, and Excel files. Supports English and German languages with 
extensive pattern recognition for country-specific identification numbers and formats.

Main Classes:
    PIIAnonymizer: Main interface for anonymization operations
    Language: Enum for supported languages (ENGLISH, GERMAN)
    DataType: Enum for supported data types (TEXT, IMAGE_OCR, CSV, EXCEL)
    
Usage:
    from pii_anonymizer import PIIAnonymizer, Language
    
    anonymizer = PIIAnonymizer()
    result = anonymizer.anonymize_text("John Doe's phone is +1-555-123-4567", Language.ENGLISH)
"""

from .main import PIIAnonymizer
from .core.types import (
    Language, DataType, ProcessingConfig, 
    AnonymizationResult, DeanonymizationResult,
    EntityMatch, AnonymizedEntity
)
from .core.exceptions import (
    PIIAnonymizerError, UnsupportedLanguageError, 
    UnsupportedDataTypeError, ProcessingError,
    DeanonymizationError
)

__version__ = "1.0.0"
__author__ = "PII Anonymizer Team"
__email__ = "info@pii-anonymizer.com"

__all__ = [
    # Main class
    "PIIAnonymizer",
    
    # Core types
    "Language",
    "DataType", 
    "ProcessingConfig",
    "AnonymizationResult",
    "DeanonymizationResult",
    "EntityMatch",
    "AnonymizedEntity",
    
    # Exceptions
    "PIIAnonymizerError",
    "UnsupportedLanguageError",
    "UnsupportedDataTypeError",
    "ProcessingError",
    "DeanonymizationError",
]