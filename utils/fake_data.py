import secrets
import hashlib
from typing import Dict, Callable, Optional
from core.types import Language


class FakeDataGenerator:
    """Generates fake replacement values for anonymized entities"""
    
    def __init__(self, language: Language = Language.ENGLISH):
        self.language = language
        self._generators = self._create_generators()
    
    def generate_fake_value(
        self, 
        entity_type: str, 
        original_value: str,
        custom_generator: Optional[Callable] = None
    ) -> str:
        """Generate fake value for given entity type"""
        if custom_generator:
            return custom_generator(original_value)
        
        generator = self._generators.get(entity_type)
        if generator:
            return generator()
        else:
            # Default anonymization with entity type and hash
            return self._generate_default_value(entity_type, original_value)
    
    def generate_entity_id(self, entity_type: str, original_value: str) -> str:
        """Generate a unique, deterministic ID for an entity"""
        hash_input = f"{entity_type}:{original_value}"
        entity_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
        return f"{entity_type}_{entity_hash}"
    
    def _generate_default_value(self, entity_type: str, original_value: str) -> str:
        """Generate default anonymized value"""
        return f"[{entity_type}_{secrets.token_hex(4)}]"
    
    def _create_generators(self) -> Dict[str, Callable]:
        """Create fake value generators for different entity types"""
        generators = {
            # Universal generators
            "PERSON": lambda: f"Person_{secrets.token_hex(4)}",
            "EMAIL_ADDRESS": lambda: f"user{secrets.randbelow(9999)}@example.com",
            "PHONE_NUMBER": lambda: self._generate_phone_number(),
            "CREDIT_CARD": lambda: f"****-****-****-{secrets.randbelow(9000)+1000:04d}",
            "IP_ADDRESS": lambda: f"192.168.{secrets.randbelow(255)}.{secrets.randbelow(255)}",
            "LOCATION": lambda: f"City_{secrets.token_hex(3)}",
            "URL": lambda: f"https://example-{secrets.token_hex(4)}.com",
            "DATE_TIME": lambda: "YYYY-MM-DD HH:MM:SS",
            "IBAN_CODE": lambda: self._generate_iban(),
            "CRYPTO_WALLET": lambda: f"1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa{secrets.token_hex(4)}",
            "MEDICAL_LICENSE": lambda: f"MD{secrets.randbelow(9999999):07d}",
            "NRP": lambda: f"GROUP_{secrets.token_hex(3)}",
            "PROFESSIONAL_LICENSE": lambda: f"LIC{secrets.randbelow(999999):06d}",
        }
        
        # Add language-specific generators
        if self.language == Language.GERMAN:
            generators.update(self._create_german_generators())
        
        return generators
    
    def _generate_phone_number(self) -> str:
        """Generate phone number based on language"""
        if self.language == Language.GERMAN:
            return f"+49{secrets.randbelow(9999):04d}{secrets.randbelow(99999999):08d}"
        else:
            return f"+1-555-{secrets.randbelow(900)+100:03d}-{secrets.randbelow(9000)+1000:04d}"
    
    def _generate_iban(self) -> str:
        """Generate IBAN based on language"""
        if self.language == Language.GERMAN:
            return f"DE{secrets.randbelow(90)+10:02d}{secrets.randbelow(9999999999999999):016d}"
        else:
            return f"GB{secrets.randbelow(90)+10:02d}ABCD{secrets.randbelow(999999999999):012d}"
    
    def _create_german_generators(self) -> Dict[str, Callable]:
        """Create German-specific generators"""
        return {
            "DE_TAX_ID": lambda: f"{secrets.randbelow(90000000000)+10000000000:011d}",
            "DE_PENSION_INSURANCE": lambda: f"{secrets.randbelow(90):02d}{secrets.randbelow(999999):06d}A{secrets.randbelow(999):03d}",
            "DE_HEALTH_INSURANCE": lambda: f"A{secrets.randbelow(9999999999):010d}",
            "DE_VAT_ID": lambda: f"DE{secrets.randbelow(999999999):09d}",
            "DE_IBAN": lambda: f"DE{secrets.randbelow(90)+10:02d}{secrets.randbelow(9999999999999999):016d}",
            "DE_PHONE_NUMBER": lambda: f"+49{secrets.randbelow(9999):04d}{secrets.randbelow(99999999):08d}",
            "DE_COMPANY_TAX": lambda: f"{secrets.randbelow(900)+100}/{secrets.randbelow(900)+100}/{secrets.randbelow(90000)+10000}",
            "DE_COMMERCIAL_REGISTER": lambda: f"HR{'BA'[secrets.randbelow(2)]}{secrets.randbelow(99999)+1000}",
            "BIC_SWIFT": lambda: f"DEUT{'DE'}2H{secrets.randbelow(999):03d}",
            "DE_STREET_ADDRESS": lambda: f"Musterstraße {secrets.randbelow(999)+1}",
            "DE_ID_CARD": lambda: f"{'ABCDEFGH'[secrets.randbelow(8)]}{secrets.randbelow(99999999):08d}",
            "DE_PASSPORT": lambda: f"{'ABCDEFGH'[secrets.randbelow(8)]}{'ABCDEFGH'[secrets.randbelow(8)]}{secrets.randbelow(9999999):07d}",
            "DE_DRIVING_LICENSE": lambda: f"DE{secrets.randbelow(99999999):08d}" if secrets.randbelow(2) else f"{secrets.randbelow(99999999999):011d}",
            "DE_RESIDENCE_PERMIT": lambda: f"{'ABCDEFGH'[secrets.randbelow(8)]}{secrets.randbelow(999999999):09d}{'ABCDEFGH'[secrets.randbelow(8)]}{secrets.randbelow(9)}"
        }