import pandas as pd
from typing import Dict, Union, List, Optional, Tuple
from core.types import (
    DataType, AnonymizationResult, DeanonymizationResult,
    ProcessingConfig, AnonymizedEntity
)
from core.base import BaseProcessor
from core.exceptions import ProcessingError
from utils.file_io import FileIOHandler
from utils.helpers import DataFrameHelper, EntityMappingHelper
from engines.anonymizer_engine import PIIAnonymizerEngine


class CSVProcessor(BaseProcessor):
    """Processes CSV data"""
    
    def __init__(self):
        self.engine = PIIAnonymizerEngine()
    
    def anonymize(
        self, 
        data: Union[str, pd.DataFrame], 
        config: ProcessingConfig,
        text_columns: Optional[List[str]] = None
    ) -> AnonymizationResult:
        """Anonymize CSV data"""
        try:
            # Load CSV data
            df = FileIOHandler.load_csv_data(data)
            
            # Determine text columns to process
            if text_columns is None:
                text_columns = DataFrameHelper.identify_text_columns(df)
            
            anonymized_df = df.copy()
            combined_entities_map = {}
            
            # Process each text column
            for column in text_columns:
                if column not in df.columns:
                    continue
                
                # Get non-null cells from column
                cells_to_process = DataFrameHelper.get_non_null_cells(df, column)
                
                for idx, cell_value in cells_to_process:
                    # Anonymize cell content
                    cell_result = self.engine.anonymize_text(cell_value, config)
                    anonymized_df.loc[idx, column] = cell_result.anonymized_data
                    
                    # Store entity mappings with location metadata
                    for entity_id, entity in cell_result.entities_map.items():
                        location_entity_id = f"{entity_id}_r{idx}_c{column}"
                        enhanced_entity = EntityMappingHelper.add_location_metadata(
                            entity, row=idx, column=column
                        )
                        combined_entities_map[location_entity_id] = enhanced_entity
            
            # Create statistics
            stats = EntityMappingHelper.create_entity_statistics(combined_entities_map)
            
            return AnonymizationResult(
                anonymized_data=anonymized_df,
                entities_map=combined_entities_map,
                metadata={
                    "data_type": DataType.CSV.value,
                    "language": config.language.value,
                    "columns_processed": text_columns,
                    "total_rows": len(df),
                    **stats
                }
            )
            
        except Exception as e:
            raise ProcessingError(f"CSV processing failed: {str(e)}")
    
    def deanonymize(
        self, 
        anonymized_data: pd.DataFrame, 
        entities_map: Dict[str, AnonymizedEntity]
    ) -> DeanonymizationResult:
        """Deanonymize CSV data"""
        try:
            original_df = anonymized_data.copy()
            errors = []
            
            # Group entities by location
            location_groups = EntityMappingHelper.group_entities_by_location(entities_map)
            
            # Restore original values
            for location_key, entities_list in location_groups.items():
                parts = location_key.split('_')
                if len(parts) >= 3:
                    sheet = '_'.join(parts[:-2])  # Handle sheet names with underscores
                    row = int(parts[-2]) 
                    col = parts[-1]
                    
                    if col in original_df.columns and row in original_df.index:
                        cell_value = str(original_df.loc[row, col])
                        
                        # Replace fake values with original values
                        for entity in entities_list:
                            if entity.fake_value in cell_value:
                                cell_value = cell_value.replace(
                                    entity.fake_value, 
                                    entity.original_value
                                )
                            else:
                                errors.append(
                                    f"Fake value not found in cell [{row}, {col}]: {entity.fake_value}"
                                )
                        
                        original_df.loc[row, col] = cell_value
            
            return DeanonymizationResult(
                original_data=original_df,
                success=len(errors) == 0,
                errors=errors
            )
            
        except Exception as e:
            return DeanonymizationResult(
                original_data=anonymized_data,
                success=False,
                errors=[str(e)]
            )
    
    def get_supported_data_type(self) -> DataType:
        """Return supported data type"""
        return DataType.CSV