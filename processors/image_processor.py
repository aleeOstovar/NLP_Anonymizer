import pytesseract
from PIL import Image
from typing import Dict, Union
from core.types import (
    DataType, AnonymizationResult, DeanonymizationResult,
    ProcessingConfig, AnonymizedEntity, Language
)
from core.base import BaseProcessor
from core.exceptions import ProcessingError
from utils.file_io import FileIOHandler
from engines.anonymizer_engine import PIIAnonymizerEngine


class ImageOCRProcessor(BaseProcessor):
    """Processes images using OCR and anonymizes extracted text"""
    
    def __init__(self):
        self.engine = PIIAnonymizerEngine()
    
    def anonymize(
        self, 
        data: Union[str, bytes, Image.Image], 
        config: ProcessingConfig
    ) -> AnonymizationResult:
        """Extract text from image using OCR and anonymize it"""
        try:
            # Process image input
            image = FileIOHandler.process_image_input(data)
            
            # Extract text using OCR
            ocr_language = 'deu' if config.language == Language.GERMAN else 'eng'
            extracted_text = pytesseract.image_to_string(image, lang=ocr_language)
            
            if not extracted_text.strip():
                return AnonymizationResult(
                    anonymized_data={
                        "original_text": "",
                        "anonymized_text": "",
                        "message": "No text detected in image"
                    },
                    entities_map={},
                    metadata={
                        "data_type": DataType.IMAGE_OCR.value,
                        "ocr_language": ocr_language,
                        "entities_found": 0
                    }
                )
            
            # Anonymize the extracted text
            text_result = self.engine.anonymize_text(extracted_text, config)
            
            return AnonymizationResult(
                anonymized_data={
                    "original_text": extracted_text,
                    "anonymized_text": text_result.anonymized_data
                },
                entities_map=text_result.entities_map,
                metadata={
                    **text_result.metadata,
                    "data_type": DataType.IMAGE_OCR.value,
                    "ocr_language": ocr_language
                }
            )
            
        except Exception as e:
            raise ProcessingError(f"Image OCR processing failed: {str(e)}")
    
    def deanonymize(
        self, 
        anonymized_data: Dict[str, str], 
        entities_map: Dict[str, AnonymizedEntity]
    ) -> DeanonymizationResult:
        """Deanonymize OCR extracted text"""
        try:
            if "anonymized_text" not in anonymized_data:
                return DeanonymizationResult(
                    original_data=anonymized_data,
                    success=False,
                    errors=["No anonymized text found in data"]
                )
            
            original_text = self.engine.deanonymize_text(
                anonymized_data["anonymized_text"], 
                entities_map
            )
            
            result_data = anonymized_data.copy()
            result_data["deanonymized_text"] = original_text
            
            return DeanonymizationResult(
                original_data=result_data,
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
        return DataType.IMAGE_OCR