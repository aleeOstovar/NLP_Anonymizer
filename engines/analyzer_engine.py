from typing import Dict, List, Optional
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider

from core.types import Language, EntityMatch, ProcessingConfig
from core.base import BaseAnonymizerEngine
from core.exceptions import RecognizerInitializationError
from recognizers.factory import RecognizerFactory


class PIIAnalyzerEngine(BaseAnonymizerEngine):
    """Manages Presidio analyzer engines for different languages"""
    
    def __init__(self):
        self.analyzer_engines = self._setup_analyzer_engines()
    
    def analyze(
        self, 
        text: str, 
        language: Language, 
        entities: List[str]
    ) -> List[EntityMatch]:
        """Analyze text for PII entities"""
        analyzer = self.analyzer_engines[language.value]
        
        results = analyzer.analyze(
            text=text,
            entities=entities,
            language=language.value
        )
        
        return [
            EntityMatch(
                entity_type=result.entity_type,
                start=result.start,
                end=result.end,
                text=text[result.start:result.end],
                confidence=result.score
            )
            for result in results
        ]
    
    def anonymize_entities(
        self, 
        text: str, 
        entities: List[EntityMatch]
    ) -> 'AnonymizationResult':  # String annotation indicates import issue
        """This method is implemented in the main anonymizer engine"""
        raise NotImplementedError("Use PIIAnonymizer.anonymize_entities instead")
    
    def get_supported_entities(self, language: Language) -> List[str]:
        """Get all supported entities for a language"""
        return RecognizerFactory.get_all_supported_entities(language)
    
    def _setup_analyzer_engines(self) -> Dict[str, AnalyzerEngine]:
        """Setup analyzer engines for different languages"""
        engines = {}
        
        try:
            # English analyzer
            engines["en"] = self._create_english_analyzer()
            
            # German analyzer  
            engines["de"] = self._create_german_analyzer()
            
        except Exception as e:
            raise RecognizerInitializationError(f"Failed to initialize analyzers: {str(e)}")
        
        return engines
    
    def _create_english_analyzer(self) -> AnalyzerEngine:
        """Create English analyzer with custom recognizers"""
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers(languages=["en"])
        
        # Add custom English recognizers
        english_recognizers = RecognizerFactory.create_recognizers(Language.ENGLISH)
        for recognizer in english_recognizers.get_recognizers():
            registry.add_recognizer(recognizer)
        
        # Setup NLP engine with enhanced spaCy model
        nlp_config = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}],
        }
        provider = NlpEngineProvider(nlp_configuration=nlp_config)
        nlp_engine = provider.create_engine()
        
        return AnalyzerEngine(registry=registry, nlp_engine=nlp_engine)
    
    def _create_german_analyzer(self) -> AnalyzerEngine:
        """Create German analyzer with custom recognizers"""
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers(languages=["de"])
        
        # Add custom German recognizers
        german_recognizers = RecognizerFactory.create_recognizers(Language.GERMAN)
        for recognizer in german_recognizers.get_recognizers():
            registry.add_recognizer(recognizer)
        
        # Add English recognizers that work for German too
        english_recognizers = RecognizerFactory.create_recognizers(Language.ENGLISH)
        for recognizer in english_recognizers.get_recognizers():
            if recognizer.supported_entities[0] in ["CRYPTO_WALLET", "MEDICAL_LICENSE"]:
                registry.add_recognizer(recognizer)
        
        # Setup NLP engine with enhanced spaCy model
        nlp_config = {
            "nlp_engine_name": "spacy", 
            "models": [{"lang_code": "de", "model_name": "de_core_news_lg"}],
        }
        provider = NlpEngineProvider(nlp_configuration=nlp_config)
        nlp_engine = provider.create_engine()
        
        # Configure analyzer with balanced threshold
        return AnalyzerEngine(
            registry=registry, 
            nlp_engine=nlp_engine,
            default_score_threshold=0.65  # Higher threshold to reduce false positives
        )