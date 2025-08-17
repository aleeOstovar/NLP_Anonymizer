import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from core.types import EntityMatch, Language, AnonymizedEntity  # Add AnonymizedEntity here


class ValidationHelper:
    """Helper functions for validation"""
    
    @staticmethod
    def validate_language(language: Language) -> None:
        """Validate language parameter"""
        if not isinstance(language, Language):
            raise ValueError(f"Language must be a Language enum, got {type(language)}")
    
    @staticmethod
    def validate_confidence_threshold(threshold: float) -> None:
        """Validate confidence threshold"""
        if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
            raise ValueError("Confidence threshold must be a number between 0 and 1")
    
    @staticmethod
    def validate_entities_list(entities: Optional[List[str]]) -> None:
        """Validate entities list"""
        if entities is not None:
            if not isinstance(entities, list):
                raise ValueError("Entities must be a list of strings")
            if not all(isinstance(entity, str) for entity in entities):
                raise ValueError("All entities must be strings")


class TextProcessingHelper:
    """Helper functions for text processing"""
    
    @staticmethod
    def filter_entities_by_confidence(
        entities: List[EntityMatch], 
        threshold: float
    ) -> List[EntityMatch]:
        """Filter entities by confidence threshold"""
        return [entity for entity in entities if entity.confidence >= threshold]
    
    @staticmethod
    def merge_overlapping_entities(entities: List[EntityMatch]) -> List[EntityMatch]:
        """Merge overlapping entities, keeping higher confidence ones"""
        if not entities:
            return []
        
        # Sort by start position, then by confidence (descending)
        sorted_entities = sorted(entities, key=lambda x: (x.start, -x.confidence))
        merged = []
        
        for entity in sorted_entities:
            # Check if this entity overlaps with any in merged list
            overlaps = False
            for merged_entity in merged:
                if (entity.start < merged_entity.end and 
                    entity.end > merged_entity.start):
                    overlaps = True
                    break
            
            if not overlaps:
                merged.append(entity)
        
        return merged
    
    @staticmethod
    def sort_entities_for_replacement(entities: List[EntityMatch]) -> List[EntityMatch]:
        """Sort entities by start position in reverse order for safe replacement"""
        return sorted(entities, key=lambda x: x.start, reverse=True)


class DataFrameHelper:
    """Helper functions for DataFrame operations"""
    
    @staticmethod
    def identify_text_columns(df: pd.DataFrame) -> List[str]:
        """Identify columns that likely contain text data"""
        return df.select_dtypes(include=['object']).columns.tolist()
    
    @staticmethod
    def get_non_null_cells(df: pd.DataFrame, column: str) -> List[Tuple[int, str]]:
        """Get non-null cells from a DataFrame column"""
        return [
            (idx, str(value)) 
            for idx, value in df[column].items() 
            if pd.notna(value) and isinstance(value, str) and value.strip()
        ]
    
    @staticmethod
    def validate_sheet_names(
        available_sheets: List[str], 
        requested_sheets: Optional[List[str]]
    ) -> List[str]:
        """Validate and return list of sheets to process"""
        if requested_sheets is None:
            return available_sheets
        
        invalid_sheets = set(requested_sheets) - set(available_sheets)
        if invalid_sheets:
            raise ValueError(f"Sheets not found: {invalid_sheets}")
        
        return requested_sheets


class EntityMappingHelper:
    """Helper functions for entity mapping operations"""
    
    @staticmethod
    def add_location_metadata(
        entity: AnonymizedEntity, 
        row: Optional[int] = None, 
        column: Optional[str] = None,
        sheet: Optional[str] = None
    ) -> AnonymizedEntity:
        """Add location metadata to an entity"""
        if entity.metadata is None:
            entity.metadata = {}
        
        if row is not None:
            entity.metadata["row"] = row
        if column is not None:
            entity.metadata["column"] = column
        if sheet is not None:
            entity.metadata["sheet"] = sheet
        
        return entity
    
    @staticmethod
    def group_entities_by_location(
        entities_map: Dict[str, AnonymizedEntity]
    ) -> Dict[str, List[AnonymizedEntity]]:
        """Group entities by their location (row, column, sheet)"""
        location_groups = {}
        
        for entity_id, entity in entities_map.items():
            if entity.metadata:
                row = entity.metadata.get("row")
                col = entity.metadata.get("column")
                sheet = entity.metadata.get("sheet", "default")
                
                key = f"{sheet}_{row}_{col}"
                if key not in location_groups:
                    location_groups[key] = []
                location_groups[key].append(entity)
        
        return location_groups
    
    @staticmethod
    def create_entity_statistics(
        entities_map: Dict[str, AnonymizedEntity]
    ) -> Dict[str, Any]:
        """Create statistics about detected entities"""
        if not entities_map:
            return {"total_entities": 0, "entity_types": {}}
        
        entity_types = {}
        for entity in entities_map.values():
            entity_type = entity.entity_type
            if entity_type not in entity_types:
                entity_types[entity_type] = {"count": 0, "avg_confidence": 0.0}
            
            entity_types[entity_type]["count"] += 1
            # Update running average
            current_avg = entity_types[entity_type]["avg_confidence"]
            count = entity_types[entity_type]["count"]
            entity_types[entity_type]["avg_confidence"] = (
                (current_avg * (count - 1) + entity.confidence) / count
            )
        
        return {
            "total_entities": len(entities_map),
            "entity_types": entity_types,
            "unique_types": len(entity_types)
        }