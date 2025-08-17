from typing import Dict
from core.types import (
    DataType, AnonymizationResult, DeanonymizationResult, 
    ProcessingConfig, AnonymizedEntity
)
from core.base import BaseProcessor
from engines.anonymizer_engine import PIIAnonymizerEngine


class TextProcessor(BaseProcessor):
    """Processes plain text data"""
    
    def __init__(self):
        self.engine = PIIAnonymizerEngine()
    
    def anonymize(self, data: str, config: ProcessingConfig) -> AnonymizationResult:
        """Anonymize plain text"""
        return self.engine.anonymize_text(data, config)
    
    def deanonymize(
        self, 
        anonymized_data: str, 
        entities_map: Dict[str, AnonymizedEntity]
    ) -> DeanonymizationResult:
        """Deanonymize plain text"""
        try:
            original_text = self.engine.deanonymize_text(anonymized_data, entities_map)
            return DeanonymizationResult(
                original_data=original_text,
                success=True,
                errors=[]
            )
        except Exception as e:
            return DeanonymizationResult(
                original_data=anonymized_data,
                success=False,
                errors=[str(e)]
            )
    
    def get_supported_data_type(self) -> DataType:
        """Return supported data type"""
        return DataType.TEXT
