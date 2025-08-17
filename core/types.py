from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass


class DataType(Enum):
    """Supported data types for anonymization"""
    TEXT = "text"
    IMAGE_OCR = "image_ocr"
    CSV = "csv"
    EXCEL = "excel"


class Language(Enum):
    """Supported languages"""
    ENGLISH = "en"
    GERMAN = "de"


@dataclass
class EntityMatch:
    """Represents a detected PII entity"""
    entity_type: str
    start: int
    end: int
    text: str
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "confidence": self.confidence
        }


@dataclass
class AnonymizedEntity:
    """Represents an anonymized entity with mapping info"""
    entity_id: str
    original_value: str
    entity_type: str
    fake_value: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_value": self.original_value,
            "entity_type": self.entity_type,
            "fake_value": self.fake_value,
            "confidence": self.confidence,
            "metadata": self.metadata or {}
        }


@dataclass
class AnonymizationResult:
    """Result of anonymization operation"""
    anonymized_data: Any
    entities_map: Dict[str, AnonymizedEntity]
    metadata: Dict[str, Any]
    
    def get_entities_dict(self) -> Dict[str, Dict[str, Any]]:
        """Convert entities map to dictionary format"""
        return {
            entity_id: entity.to_dict() 
            for entity_id, entity in self.entities_map.items()
        }


@dataclass
class DeanonymizationResult:
    """Result of deanonymization operation"""
    original_data: Any
    success: bool
    errors: List[str]
    
    def add_error(self, error: str) -> None:
        """Add an error to the result"""
        self.errors.append(error)
        self.success = False


@dataclass
class ProcessingConfig:
    """Configuration for anonymization processing"""
    language: Language = Language.ENGLISH
    entities_to_process: Optional[List[str]] = None
    confidence_threshold: float = 0.5
    preserve_format: bool = True
    custom_fake_generators: Optional[Dict[str, callable]] = None