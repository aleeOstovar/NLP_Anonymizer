# =============================================================================
# recognizers/factory.py - Recognizer factory
# =============================================================================

from typing import Dict, List
from core.types import Language
from core.base import BaseRecognizer
from core.exceptions import UnsupportedLanguageError
from .german_recognizers import GermanRecognizers
from .english_recognizers import EnglishRecognizers


class RecognizerFactory:
    """Factory for creating language-specific recognizers"""
    
    _recognizers = {
        Language.GERMAN: GermanRecognizers,
        Language.ENGLISH: EnglishRecognizers
    }
    
    @classmethod
    def create_recognizers(cls, language: Language) -> BaseRecognizer:
        """Create recognizers for specified language"""
        if language not in cls._recognizers:
            raise UnsupportedLanguageError(f"Language {language.value} not supported")
        
        recognizer_class = cls._recognizers[language]
        return recognizer_class()
    
    @classmethod
    def get_base_entities(cls) -> List[str]:
        """Get base entities supported by Presidio"""
        return [
            "CREDIT_CARD", "DATE_TIME", "EMAIL_ADDRESS", "IBAN_CODE",
            "IP_ADDRESS", "LOCATION", "PERSON", "PHONE_NUMBER", "URL"
        ]
    
    @classmethod
    def get_all_supported_entities(cls, language: Language) -> List[str]:
        """Get all supported entities for a language"""
        base_entities = cls.get_base_entities()
        recognizer = cls.create_recognizers(language)
        custom_entities = recognizer.get_supported_entities()
        
        return base_entities + custom_entities
    
    @classmethod
    def get_supported_languages(cls) -> List[Language]:
        """Get all supported languages"""
        return list(cls._recognizers.keys())