from abc import ABC, abstractmethod
from typing import List, Dict, Any
# Use string annotations to avoid circular imports


class BaseRecognizer(ABC):
    """Base class for PII recognizers"""
    
    @abstractmethod
    def get_recognizers(self) -> List[Any]:
        """Return list of presidio recognizers"""
        pass
    
    @abstractmethod
    def get_supported_entities(self) -> List[str]:
        """Return list of supported entity types"""
        pass


class BaseProcessor(ABC):
    """Base class for data processors"""
    
    @abstractmethod
    def anonymize(
        self, 
        data: Any, 
        config: 'ProcessingConfig'
    ) -> 'AnonymizationResult':
        """Anonymize data"""
        pass
    
    @abstractmethod
    def deanonymize(
        self, 
        anonymized_data: Any, 
        entities_map: Dict[str, 'AnonymizedEntity']
    ) -> 'DeanonymizationResult':
        """Deanonymize data"""
        pass
    
    @abstractmethod
    def get_supported_data_type(self) -> 'DataType':
        """Return supported data type"""
        pass


class BaseAnonymizerEngine(ABC):
    """Base class for anonymizer engines"""
    
    @abstractmethod
    def analyze(
        self, 
        text: str, 
        language: 'Language', 
        entities: List[str]
    ) -> List['EntityMatch']:
        """Analyze text for PII entities"""
        pass
    
    @abstractmethod
    def anonymize_entities(
        self, 
        text: str, 
        entities: List['EntityMatch']
    ) -> 'AnonymizationResult':
        """Anonymize detected entities"""
        pass