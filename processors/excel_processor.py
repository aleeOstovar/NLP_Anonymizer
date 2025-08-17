import pandas as pd
from typing import Dict, Union, List, Optional
from core.types import (
    DataType, AnonymizationResult, DeanonymizationResult,
    ProcessingConfig, AnonymizedEntity
)
from core.base import BaseProcessor
from core.exceptions import ProcessingError
from utils.file_io import FileIOHandler
from utils.helpers import DataFrameHelper, EntityMappingHelper
from .csv_processor import CSVProcessor


class ExcelProcessor(BaseProcessor):
    """Processes Excel data with multiple sheets support"""
    
    def __init__(self):
        self.csv_processor = CSVProcessor()
    
    def anonymize(
        self,
        data: Union[str, pd.ExcelFile, Dict[str, pd.DataFrame]],
        config: ProcessingConfig,
        sheets_to_process: Optional[List[str]] = None,
        text_columns: Optional[Dict[str, List[str]]] = None
    ) -> AnonymizationResult:
        """Anonymize Excel data with multiple sheets support"""
        try:
            # Load Excel data
            sheets_dict = FileIOHandler.load_excel_data(data)
            
            # Validate and get sheets to process
            sheets_to_process = DataFrameHelper.validate_sheet_names(
                list(sheets_dict.keys()), sheets_to_process
            )
            
            anonymized_sheets = {}
            combined_entities_map = {}
            total_entities = 0
            
            for sheet_name in sheets_to_process:
                if sheet_name not in sheets_dict:
                    continue
                
                df = sheets_dict[sheet_name]
                
                # Get text columns for this sheet
                sheet_text_columns = None
                if text_columns and sheet_name in text_columns:
                    sheet_text_columns = text_columns[sheet_name]
                
                # Anonymize this sheet using CSV processor
                sheet_result = self.csv_processor.anonymize(
                    df, config, sheet_text_columns
                )
                
                anonymized_sheets[sheet_name] = sheet_result.anonymized_data
                
                # Add sheet prefix to entity mappings
                for entity_id, entity in sheet_result.entities_map.items():
                    sheet_entity_id = f"{sheet_name}_{entity_id}"
                    enhanced_entity = EntityMappingHelper.add_location_metadata(
                        entity, sheet=sheet_name
                    )
                    combined_entities_map[sheet_entity_id] = enhanced_entity
                
                total_entities += sheet_result.metadata.get("total_entities", 0)
            
            # Create overall statistics
            stats = EntityMappingHelper.create_entity_statistics(combined_entities_map)
            
            return AnonymizationResult(
                anonymized_data=anonymized_sheets,
                entities_map=combined_entities_map,
                metadata={
                    "data_type": DataType.EXCEL.value,
                    "language": config.language.value,
                    "sheets_processed": sheets_to_process,
                    "total_sheets": len(sheets_to_process),
                    **stats
                }
            )
            
        except Exception as e:
            raise ProcessingError(f"Excel processing failed: {str(e)}")
    
    def deanonymize(
        self,
        anonymized_data: Dict[str, pd.DataFrame],
        entities_map: Dict[str, AnonymizedEntity]
    ) -> DeanonymizationResult:
        """Deanonymize Excel data with multiple sheets"""
        try:
            original_sheets = {}
            all_errors = []
            
            # Group entities by sheet
            entities_by_sheet = self._group_entities_by_sheet(entities_map)
            
            # Deanonymize each sheet
            for sheet_name, df in anonymized_data.items():
                if sheet_name in entities_by_sheet:
                    sheet_entities = entities_by_sheet[sheet_name]
                    sheet_result = self.csv_processor.deanonymize(df, sheet_entities)
                    
                    original_sheets[sheet_name] = sheet_result.original_data
                    all_errors.extend([
                        f"{sheet_name}: {error}" for error in sheet_result.errors
                    ])
                else:
                    original_sheets[sheet_name] = df
            
            return DeanonymizationResult(
                original_data=original_sheets,
                success=len(all_errors) == 0,
                errors=all_errors
            )
            
        except Exception as e:
            return DeanonymizationResult(
                original_data=anonymized_data,
                success=False,
                errors=[str(e)]
            )
    
    def get_supported_data_type(self) -> DataType:
        """Return supported data type"""
        return DataType.EXCEL
    
    def _group_entities_by_sheet(
        self, 
        entities_map: Dict[str, AnonymizedEntity]
    ) -> Dict[str, Dict[str, AnonymizedEntity]]:
        """Group entities by sheet name"""
        entities_by_sheet = {}
        
        for entity_id, entity in entities_map.items():
            if entity.metadata and "sheet" in entity.metadata:
                sheet_name = entity.metadata["sheet"]
                
                if sheet_name not in entities_by_sheet:
                    entities_by_sheet[sheet_name] = {}
                
                # Remove sheet prefix from entity_id for processing
                clean_entity_id = entity_id
                if entity_id.startswith(f"{sheet_name}_"):
                    clean_entity_id = entity_id[len(f"{sheet_name}_"):]
                
                entities_by_sheet[sheet_name][clean_entity_id] = entity
        
        return entities_by_sheet
