from typing import Dict, List, Optional, Union, Any
import pandas as pd
from PIL import Image

from core.types import (
    Language, DataType, ProcessingConfig, AnonymizationResult, 
    DeanonymizationResult, AnonymizedEntity
)
from core.exceptions import PIIAnonymizerError, UnsupportedDataTypeError
from processors.factory import ProcessorFactory
from recognizers.factory import RecognizerFactory
from utils.file_io import FileIOHandler
from engines.anonymizer_engine import PIIAnonymizerEngine


class PIIAnonymizer:
    """
    Main PII Anonymization/Deanonymization System
    
    Supports English and German languages with comprehensive PII detection.
    Handles text, image OCR, CSV, and Excel files.
    """
    
    def __init__(self):
        """Initialize the PII anonymizer"""
        self.engine = PIIAnonymizerEngine()
        self._processors = {}  # Cache processors
    
    # =============================================================================
    # Main Anonymization Methods
    # =============================================================================
    
    def anonymize_text(
        self,
        text: str,
        language: Language = Language.ENGLISH,
        entities_to_anonymize: Optional[List[str]] = None,
        confidence_threshold: float = 0.5,
        custom_fake_generators: Optional[Dict[str, callable]] = None
    ) -> AnonymizationResult:
        """
        Anonymize text content
        
        Args:
            text: Text to anonymize
            language: Language to use for detection
            entities_to_anonymize: Specific entity types to anonymize (None for all)
            confidence_threshold: Minimum confidence for entity detection
            custom_fake_generators: Custom fake value generators by entity type
            
        Returns:
            AnonymizationResult with anonymized text and entity mapping
        """
        config = ProcessingConfig(
            language=language,
            entities_to_process=entities_to_anonymize,
            confidence_threshold=confidence_threshold,
            custom_fake_generators=custom_fake_generators
        )
        
        processor = self._get_processor(DataType.TEXT)
        return processor.anonymize(text, config)
    
    def anonymize_image_ocr(
        self,
        image_data: Union[str, bytes, Image.Image],
        language: Language = Language.ENGLISH,
        entities_to_anonymize: Optional[List[str]] = None,
        confidence_threshold: float = 0.5
    ) -> AnonymizationResult:
        """
        Extract text from image using OCR and anonymize it
        
        Args:
            image_data: Image data (base64 string, bytes, or PIL Image)
            language: Language for OCR and PII detection
            entities_to_anonymize: Specific entity types to anonymize
            confidence_threshold: Minimum confidence for entity detection
            
        Returns:
            AnonymizationResult with original and anonymized OCR text
        """
        config = ProcessingConfig(
            language=language,
            entities_to_process=entities_to_anonymize,
            confidence_threshold=confidence_threshold
        )
        
        processor = self._get_processor(DataType.IMAGE_OCR)
        return processor.anonymize(image_data, config)
    
    def anonymize_csv(
        self,
        csv_data: Union[str, pd.DataFrame],
        language: Language = Language.ENGLISH,
        entities_to_anonymize: Optional[List[str]] = None,
        text_columns: Optional[List[str]] = None,
        confidence_threshold: float = 0.5
    ) -> AnonymizationResult:
        """
        Anonymize CSV data
        
        Args:
            csv_data: CSV data as string or DataFrame
            language: Language for PII detection
            entities_to_anonymize: Specific entity types to anonymize
            text_columns: Columns to process (None for all text columns)
            confidence_threshold: Minimum confidence for entity detection
            
        Returns:
            AnonymizationResult with anonymized DataFrame
        """
        config = ProcessingConfig(
            language=language,
            entities_to_process=entities_to_anonymize,
            confidence_threshold=confidence_threshold
        )
        
        processor = self._get_processor(DataType.CSV)
        return processor.anonymize(csv_data, config, text_columns)
    
    def anonymize_excel(
        self,
        excel_data: Union[str, pd.ExcelFile, Dict[str, pd.DataFrame]],
        language: Language = Language.ENGLISH,
        entities_to_anonymize: Optional[List[str]] = None,
        sheets_to_process: Optional[List[str]] = None,
        text_columns: Optional[Dict[str, List[str]]] = None,
        confidence_threshold: float = 0.5
    ) -> AnonymizationResult:
        """
        Anonymize Excel data with multiple sheets support
        
        Args:
            excel_data: Excel data (file path, ExcelFile, or dict of DataFrames)
            language: Language for PII detection
            entities_to_anonymize: Specific entity types to anonymize
            sheets_to_process: Sheet names to process (None for all)
            text_columns: Text columns by sheet name
            confidence_threshold: Minimum confidence for entity detection
            
        Returns:
            AnonymizationResult with anonymized sheets dictionary
        """
        config = ProcessingConfig(
            language=language,
            entities_to_process=entities_to_anonymize,
            confidence_threshold=confidence_threshold
        )
        
        processor = self._get_processor(DataType.EXCEL)
        return processor.anonymize(
            excel_data, config, sheets_to_process, text_columns
        )
    
    # =============================================================================
    # Deanonymization Methods
    # =============================================================================
    
    def deanonymize_text(
        self,
        anonymized_text: str,
        entities_map: Dict[str, AnonymizedEntity]
    ) -> DeanonymizationResult:
        """
        Deanonymize text using the entities map
        
        Args:
            anonymized_text: Anonymized text
            entities_map: Entity mapping from anonymization result
            
        Returns:
            DeanonymizationResult with original text
        """
        processor = self._get_processor(DataType.TEXT)
        return processor.deanonymize(anonymized_text, entities_map)
    
    def deanonymize_csv(
        self,
        anonymized_df: pd.DataFrame,
        entities_map: Dict[str, AnonymizedEntity]
    ) -> DeanonymizationResult:
        """
        Deanonymize CSV data
        
        Args:
            anonymized_df: Anonymized DataFrame
            entities_map: Entity mapping from anonymization result
            
        Returns:
            DeanonymizationResult with original DataFrame
        """
        processor = self._get_processor(DataType.CSV)
        return processor.deanonymize(anonymized_df, entities_map)
    
    def deanonymize_excel(
        self,
        anonymized_sheets: Dict[str, pd.DataFrame],
        entities_map: Dict[str, AnonymizedEntity]
    ) -> DeanonymizationResult:
        """
        Deanonymize Excel data with multiple sheets
        
        Args:
            anonymized_sheets: Dictionary of anonymized DataFrames by sheet name
            entities_map: Entity mapping from anonymization result
            
        Returns:
            DeanonymizationResult with original sheets
        """
        processor = self._get_processor(DataType.EXCEL)
        return processor.deanonymize(anonymized_sheets, entities_map)
    
    # =============================================================================
    # Analysis Methods
    # =============================================================================
    
    def analyze_only(
        self,
        text: str,
        language: Language = Language.ENGLISH,
        entities_to_find: Optional[List[str]] = None,
        confidence_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Analyze text and return found entities without anonymization
        
        Args:
            text: Text to analyze
            language: Language for PII detection
            entities_to_find: Specific entity types to find
            confidence_threshold: Minimum confidence for entity detection
            
        Returns:
            List of detected entities with metadata
        """
        config = ProcessingConfig(
            language=language,
            entities_to_process=entities_to_find,
            confidence_threshold=confidence_threshold
        )
        
        entities = self.engine.analyze_only(text, config)
        return [entity.to_dict() for entity in entities]
    
    # =============================================================================
    # Utility Methods
    # =============================================================================
    
    def get_supported_entities(self, language: Language) -> List[str]:
        """Get list of supported entity types for a language"""
        return RecognizerFactory.get_all_supported_entities(language)
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return [lang.value for lang in RecognizerFactory.get_supported_languages()]
    
    def get_supported_data_types(self) -> List[str]:
        """Get list of supported data types"""
        return [dtype.value for dtype in ProcessorFactory.get_supported_data_types()]
    
    def save_entities_map(
        self, 
        entities_map: Dict[str, AnonymizedEntity], 
        filepath: str
    ) -> None:
        """Save entities mapping to file for later deanonymization"""
        FileIOHandler.save_entities_map(entities_map, filepath)
    
    def load_entities_map(self, filepath: str) -> Dict[str, AnonymizedEntity]:
        """Load entities mapping from file"""
        return FileIOHandler.load_entities_map(filepath)
    
    # =============================================================================
    # Private Methods
    # =============================================================================
    
    def _get_processor(self, data_type: DataType):
        """Get or create processor for data type"""
        if data_type not in self._processors:
            self._processors[data_type] = ProcessorFactory.create_processor(data_type)
        return self._processors[data_type]
