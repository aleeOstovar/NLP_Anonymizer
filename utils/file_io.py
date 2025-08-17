import json
import pandas as pd
import io
import base64
from typing import Dict, Any, Union, List, Optional
from PIL import Image
from core.types import AnonymizedEntity, DeanonymizationResult
from core.exceptions import ProcessingError


class FileIOHandler:
    """Handles file I/O operations for the anonymizer"""
    
    @staticmethod
    def save_entities_map(entities_map: Dict[str, AnonymizedEntity], filepath: str) -> None:
        """Save entities mapping to JSON file"""
        try:
            # Convert entities to dictionary format
            serializable_map = {
                entity_id: entity.to_dict() 
                for entity_id, entity in entities_map.items()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(serializable_map, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            raise ProcessingError(f"Failed to save entities map: {str(e)}")
    
    @staticmethod
    def load_entities_map(filepath: str) -> Dict[str, AnonymizedEntity]:
        """Load entities mapping from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                entities_dict = json.load(f)
            
            return {
                entity_id: AnonymizedEntity(
                    entity_id=entity_id,
                    original_value=entity_data["original_value"],
                    entity_type=entity_data["entity_type"],
                    fake_value=entity_data["fake_value"],
                    confidence=entity_data["confidence"],
                    metadata=entity_data.get("metadata")
                )
                for entity_id, entity_data in entities_dict.items()
            }
        except Exception as e:
            raise ProcessingError(f"Failed to load entities map: {str(e)}")
    
    @staticmethod
    def process_image_input(image_data: Union[str, bytes, Image.Image]) -> Image.Image:
        """Process different image input formats"""
        try:
            if isinstance(image_data, str):
                # Assume base64 encoded image
                image_bytes = base64.b64decode(image_data)
                return Image.open(io.BytesIO(image_bytes))
            elif isinstance(image_data, bytes):
                return Image.open(io.BytesIO(image_data))
            elif isinstance(image_data, Image.Image):
                return image_data
            else:
                raise ValueError("Unsupported image format")
        except Exception as e:
            raise ProcessingError(f"Failed to process image input: {str(e)}")
    
    @staticmethod
    def load_csv_data(csv_data: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """Load CSV data from string or DataFrame"""
        try:
            if isinstance(csv_data, str):
                return pd.read_csv(io.StringIO(csv_data))
            elif isinstance(csv_data, pd.DataFrame):
                return csv_data.copy()
            else:
                raise ValueError("Unsupported CSV format")
        except Exception as e:
            raise ProcessingError(f"Failed to load CSV data: {str(e)}")
    
    @staticmethod
    def load_excel_data(
        excel_data: Union[str, pd.ExcelFile, Dict[str, pd.DataFrame]]
    ) -> Dict[str, pd.DataFrame]:
        """Load Excel data with multiple sheets support"""
        try:
            if isinstance(excel_data, str):
                excel_file = pd.ExcelFile(excel_data)
                return {sheet: excel_file.parse(sheet) for sheet in excel_file.sheet_names}
            elif isinstance(excel_data, pd.ExcelFile):
                return {sheet: excel_data.parse(sheet) for sheet in excel_data.sheet_names}
            elif isinstance(excel_data, dict):
                return excel_data
            else:
                raise ValueError("Unsupported Excel format")
        except Exception as e:
            raise ProcessingError(f"Failed to load Excel data: {str(e)}")
