from typing import Dict, List, Optional, Any,Union
from core.types import (
    AnonymizationResult, AnonymizedEntity, EntityMatch, 
    ProcessingConfig, Language, DeanonymizationResult
)
from core.exceptions import ProcessingError
from utils.fake_data import FakeDataGenerator
from utils.helpers import TextProcessingHelper, ValidationHelper
from .analyzer_engine import PIIAnalyzerEngine


class PIIAnonymizerEngine:
    """Main anonymization engine that coordinates analysis and anonymization"""
    
    def __init__(self):
        self.analyzer = PIIAnalyzerEngine()
        self.fake_generators = {}  # Cache generators by language
    
    def anonymize_text(
        self,
        text: str,
        config: ProcessingConfig
    ) -> AnonymizationResult:
        """Anonymize text content with given configuration"""
        try:
            # Validate inputs
            ValidationHelper.validate_language(config.language)
            ValidationHelper.validate_confidence_threshold(config.confidence_threshold)
            ValidationHelper.validate_entities_list(config.entities_to_process)
            
            # Get entities to process
            entities_to_analyze = self._get_entities_to_analyze(config)
            
            # Analyze text for PII
            detected_entities = self.analyzer.analyze(
                text=text,
                language=config.language,
                entities=entities_to_analyze
            )
            
            # Filter by confidence threshold
            filtered_entities = TextProcessingHelper.filter_entities_by_confidence(
                detected_entities, config.confidence_threshold
            )
            
            # Merge overlapping entities
            merged_entities = TextProcessingHelper.merge_overlapping_entities(
                filtered_entities
            )
            
            # Anonymize entities
            return self._anonymize_detected_entities(text, merged_entities, config)
            
        except Exception as e:
            raise ProcessingError(f"Text anonymization failed: {str(e)}")
    
    def deanonymize_text(
        self,
        anonymized_text: str,
        entities_map: Dict[str, Union[AnonymizedEntity, Dict[str, Any]]]
    ) -> DeanonymizationResult:
        try:
            original_text = anonymized_text
            
            # Process entities - handle both AnonymizedEntity objects and dictionaries
            sorted_entities = []
            for entity_id, entity in entities_map.items():
                # If entity is a dictionary, extract the values we need
                if isinstance(entity, dict):
                    if "fake_value" in entity and "original_value" in entity:
                        sorted_entities.append({
                            "fake_value": entity["fake_value"],
                            "original_value": entity["original_value"]
                        })
                else:  # It's an AnonymizedEntity object
                    sorted_entities.append(entity)
            
            # Sort by fake value length (longest first) to avoid partial replacements
            sorted_entities = sorted(
                sorted_entities,
                key=lambda x: len(x.fake_value if hasattr(x, "fake_value") else x["fake_value"]),
                reverse=True
            )
            
            for entity in sorted_entities:
                fake_val = entity.fake_value if hasattr(entity, "fake_value") else entity["fake_value"]
                orig_val = entity.original_value if hasattr(entity, "original_value") else entity["original_value"]
                
                if fake_val in original_text:
                    original_text = original_text.replace(fake_val, orig_val)
            
            # Return a DeanonymizationResult object
            return DeanonymizationResult(
                original_data=original_text,
                success=True,
                errors=[]
            )
            
        except Exception as e:
            result = DeanonymizationResult(
                original_data=anonymized_text,
                success=False,
                errors=[f"Text deanonymization failed: {str(e)}"] 
            )
            return result
    
    def analyze_only(
        self,
        text: str,
        config: ProcessingConfig
    ) -> List[EntityMatch]:
        """Analyze text and return found entities without anonymization"""
        try:
            entities_to_analyze = self._get_entities_to_analyze(config)
            
            detected_entities = self.analyzer.analyze(
                text=text,
                language=config.language,
                entities=entities_to_analyze
            )
            
            return TextProcessingHelper.filter_entities_by_confidence(
                detected_entities, config.confidence_threshold
            )
            
        except Exception as e:
            raise ProcessingError(f"Text analysis failed: {str(e)}")
    
    def _get_entities_to_analyze(self, config: ProcessingConfig) -> List[str]:
        """Get list of entities to analyze based on configuration"""
        if config.entities_to_process:
            return config.entities_to_process
        else:
            return self.analyzer.get_supported_entities(config.language)
    
    def _get_fake_generator(self, language: Language) -> FakeDataGenerator:
        """Get or create fake data generator for language"""
        if language not in self.fake_generators:
            self.fake_generators[language] = FakeDataGenerator(language)
        return self.fake_generators[language]
    
    def _anonymize_detected_entities(
        self,
        text: str,
        entities: List[EntityMatch],
        config: ProcessingConfig
    ) -> AnonymizationResult:  # This is referenced but might cause issues
        """Anonymize detected entities in text"""
        fake_generator = self._get_fake_generator(config.language)
        entities_map = {}
        anonymized_text = text
        
        # Sort entities for safe replacement (reverse order by start position)
        sorted_entities = TextProcessingHelper.sort_entities_for_replacement(entities)
        
        for entity in sorted_entities:
            # Generate entity ID and fake value
            entity_id = fake_generator.generate_entity_id(
                entity.entity_type, 
                entity.text
            )
            
            # Use custom generator if provided
            custom_generator = None
            if (config.custom_fake_generators and 
                entity.entity_type in config.custom_fake_generators):
                custom_generator = config.custom_fake_generators[entity.entity_type]
            
            fake_value = fake_generator.generate_fake_value(
                entity.entity_type,
                entity.text,
                custom_generator
            )
            
            # Create anonymized entity
            anonymized_entity = AnonymizedEntity(
                entity_id=entity_id,
                original_value=entity.text,
                entity_type=entity.entity_type,
                fake_value=fake_value,
                confidence=entity.confidence
            )
            
            # Store in mapping
            entities_map[entity_id] = anonymized_entity
            
            # Replace in text
            anonymized_text = (
                anonymized_text[:entity.start] +
                fake_value +
                anonymized_text[entity.end:]
            )
        
        # Create metadata
        metadata = {
            "language": config.language.value,
            "entities_found": len(entities),
            "entities_types": list(set([e.entity_type for e in entities])),
            "confidence_threshold": config.confidence_threshold,
            "preserve_format": config.preserve_format
        }
        
        return AnonymizationResult(
            anonymized_data=anonymized_text,
            entities_map=entities_map,
            metadata=metadata
        )