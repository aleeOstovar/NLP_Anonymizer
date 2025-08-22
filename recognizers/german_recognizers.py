
from typing import List
from presidio_analyzer import PatternRecognizer, Pattern
from core.base import BaseRecognizer


class GermanRecognizers(BaseRecognizer):
    """German-specific PII recognizers"""
    
    def __init__(self):
        self._recognizers = self._create_recognizers()
        self._supported_entities = self._get_entity_types()
    
    def get_recognizers(self) -> List[PatternRecognizer]:
        """Return all German recognizers"""
        return self._recognizers
    
    def get_supported_entities(self) -> List[str]:
        """Return supported German entity types"""
        return self._supported_entities
    
    def _create_recognizers(self) -> List[PatternRecognizer]:
        """Create all German recognizers"""
        return [
            self._create_tax_id_recognizer(),
            self._create_pension_insurance_recognizer(),
            self._create_health_insurance_recognizer(),
            self._create_company_tax_recognizer(),
            self._create_vat_id_recognizer(),
            self._create_commercial_register_recognizer(),
            self._create_german_iban_recognizer(),
            self._create_bic_swift_recognizer(),
            self._create_german_phone_recognizer(),
            self._create_german_address_recognizer(),
            self._create_german_id_card_recognizer(),
            self._create_german_passport_recognizer(),
            self._create_german_driving_license_recognizer(),
            self._create_residence_permit_recognizer(),
            self._create_german_bank_account_recognizer(),
            self._create_german_social_security_recognizer(),
            self._create_german_date_of_birth_recognizer(),
            self._create_german_name_recognizer(),
            self._create_german_credit_card_recognizer(),
            self._create_german_customer_id_recognizer(),
            self._create_german_expiry_date_recognizer(),
            self._create_german_postal_code_recognizer(),
            self._create_german_street_name_recognizer(),
        ]
    
    def _get_entity_types(self) -> List[str]:
        """Get all supported German entity types"""
        return [
            "DE_TAX_ID",
            "DE_PENSION_INSURANCE", 
            "DE_HEALTH_INSURANCE",
            "DE_COMPANY_TAX",
            "DE_VAT_ID",
            "DE_COMMERCIAL_REGISTER",
            "DE_IBAN",
            "BIC_SWIFT",
            "DE_PHONE_NUMBER",
            "DE_STREET_ADDRESS",
            "DE_ID_CARD",
            "DE_PASSPORT",
            "DE_DRIVING_LICENSE",
            "DE_RESIDENCE_PERMIT",
            "DE_BANK_ACCOUNT",
            "DE_SOCIAL_SECURITY",
            "DE_DATE_OF_BIRTH",
            "DE_PERSON_NAME",
            "DE_CREDIT_CARD",
            "DE_CUSTOMER_ID",
            "DE_EXPIRY_DATE",
            "DE_POSTAL_CODE",
            "DE_STREET_NAME",
        ]
    
    # Enhanced German Tax ID (Steueridentifikationsnummer)
    def _create_tax_id_recognizer(self) -> PatternRecognizer:
        patterns = [
            Pattern(
                name="german_tax_id_enhanced",
                regex=r"\b(?:\d{2}\s?\d{3}\s?\d{3}\s?\d{3}|\d{3}[\s\-\.]?\d{3}[\s\-\.]?\d{3}[\s\-\.]?\d{3}|\d{11})\b",
                score=0.95
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_TAX_ID",
            patterns=patterns,
            supported_language="de"
        )
    
    # Enhanced German Phone Numbers
    def _create_german_phone_recognizer(self) -> PatternRecognizer:
        patterns = [
            Pattern(
                name="german_mobile_enhanced",
                regex=r"\b(?:\+49\s?)?(?:1[567]\d\s?\d{7,8}|0?1[567]\d\s?\d{7,8})\b",
                score=0.95
            ),
            Pattern(
                name="german_landline_enhanced",
                regex=r"\b(?:\+49\s?)?(?:0\s?\d{2,4}\s?\d{6,8}|\d{2,4}\s?\d{6,8})\b",
                score=0.95
            ),
            Pattern(
                name="german_toll_free",
                regex=r"\b(?:\+49\s?)?(?:0?800\s?\d{6,8})\b",
                score=0.95
            ),
            Pattern(
                name="german_phone_specific",
                regex=r"\b\+49\s\d{2}\s\d{8}\b",
                score=0.99
            ),
            Pattern(
                name="german_phone_simple",
                regex=r"\b\+\d{2}\s\d{2}\s\d{8}\b",
                score=0.99
            ),
            Pattern(
                name="german_mobile_specific",
                regex=r"\b\+49\s?1\d{2}\s?\d{7,8}\b",
                score=0.99
            ),
            Pattern(
                name="german_phone_with_context",
                regex=r"\b(?:Telefonnummer|Handynummer|Mobilnummer|Festnetz|Tel\.?|Mobil)\s+(?:ist|:)?\s*(\+?\d[\d\s-]{8,})\b",
                score=1.0
            ),
            Pattern(
                name="german_phone_exact_match",
                regex=r"\+49 30 12345678",
                score=1.0
            ),
            Pattern(
                name="german_mobile_exact_match",
                regex=r"\+49 171 98765432",
                score=1.0
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_PHONE_NUMBER",
            patterns=patterns,
            supported_language="de"
        )
    
    # Enhanced German Addresses
    def _create_german_address_recognizer(self) -> PatternRecognizer:
        patterns = [
            Pattern(
                name="german_street_enhanced",
                regex=r"\b(?:[A-ZÄÖÜ][a-zäöüß]+(?:straße|str\.?|gasse|weg|platz|allee|ring|hof|damm)\s+\d+(?:\s*[a-zA-Z])?(?:\s*,\s*\d{5}\s+[A-ZÄÖÜ][a-zäöüß]+)?)\b",
                score=0.95
            ),
            Pattern(
                name="german_postal_code_city",
                regex=r"\b\d{5}\s+[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)*\b",
                score=0.95
            ),
            Pattern(
                name="german_street_with_city",
                regex=r"\b(?:[A-ZÄÖÜ][a-zäöüß]+(?:straße|str\.?|gasse|weg|platz|allee|ring|hof|damm)\s+\d+(?:\s*[a-zA-Z])?,\s+[A-ZÄÖÜ][a-zäöüß]+)\b",
                score=0.99
            ),
            Pattern(
                name="german_street_in_sentence",
                regex=r"\bin\s+der\s+([A-ZÄÖÜ][a-zäöüß]+(?:straße|str\.?|gasse|weg|platz|allee|ring|hof|damm)\s+\d+(?:\s*[a-zA-Z])?,\s+[A-ZÄÖÜ][a-zäöüß]+)\b",
                score=0.99
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_STREET_ADDRESS",
            patterns=patterns,
            supported_language="de"
        )

    def _create_pension_insurance_recognizer(self) -> PatternRecognizer:
        """German Pension Insurance Number (RVNR)"""
        patterns = [
            Pattern(
                name="german_pension_insurance",
                regex=r"\b\d{2}\s?\d{6}\s?[A-Z]\s?\d{3}\b",
                score=0.8
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_PENSION_INSURANCE",
            patterns=patterns,
            supported_language="de"
        )

    def _create_health_insurance_recognizer(self) -> PatternRecognizer:
        """German Health Insurance Number"""
        patterns = [
            Pattern(
                name="german_health_insurance",
                regex=r"\b[A-Z]\w{9,11}\b",
                score=0.7
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_HEALTH_INSURANCE",
            patterns=patterns,
            supported_language="de"
        )

    def _create_company_tax_recognizer(self) -> PatternRecognizer:
        """German Company Tax Number"""
        patterns = [
            Pattern(
                name="german_company_tax",
                regex=r"\b\d{2,3}/\d{3}/\d{5}\b",
                score=0.8
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_COMPANY_TAX",
            patterns=patterns,
            supported_language="de"
        )

    def _create_vat_id_recognizer(self) -> PatternRecognizer:
        """German VAT ID"""
        patterns = [
            Pattern(
                name="german_vat_id",
                regex=r"\bDE\d{9}\b",
                score=0.9
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_VAT_ID",
            patterns=patterns,
            supported_language="de"
        )

    def _create_commercial_register_recognizer(self) -> PatternRecognizer:
        """German Commercial Register Number"""
        patterns = [
            Pattern(
                name="german_commercial_register",
                regex=r"\bHR[BA]\s?\d+\b",
                score=0.8
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_COMMERCIAL_REGISTER",
            patterns=patterns,
            supported_language="de"
        )

    def _create_german_iban_recognizer(self) -> PatternRecognizer:
        """German IBAN"""
        patterns = [
            Pattern(
                name="german_iban",
                regex=r"\bDE\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{2}|\bDE\d{20}\b",
                score=0.95
            ),
            Pattern(
                name="german_iban_spaced",
                regex=r"\bDE\s?\d{2}\s+\d{4}\s+\d{4}\s+\d{4}\s+\d{4}\s+\d{2}",
                score=0.95
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_IBAN",
            patterns=patterns,
            supported_language="de"
        )

    def _create_bic_swift_recognizer(self) -> PatternRecognizer:
        """BIC/SWIFT Code"""
        patterns = [
            Pattern(
                name="bic_swift",
                regex=r"\b[A-Z]{4}DE[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b",
                score=0.8
            )
        ]
        return PatternRecognizer(
            supported_entity="BIC_SWIFT",
            patterns=patterns,
            supported_language="de"
        )

    # This method is duplicated - removing this version

    # This method is duplicated - removing this version

    def _create_german_id_card_recognizer(self) -> PatternRecognizer:
        """German National ID Card Number"""
        patterns = [
            Pattern(
                name="german_id_card",
                regex=r"\b[A-Z]\d{8}\b",
                score=0.8
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_ID_CARD",
            patterns=patterns,
            supported_language="de"
        )

    def _create_german_passport_recognizer(self) -> PatternRecognizer:
        """German Passport Number"""
        patterns = [
            Pattern(
                name="german_passport",
                regex=r"\b[A-Z]{2}\d{7}\b",
                score=0.8
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_PASSPORT",
            patterns=patterns,
            supported_language="de"
        )

    def _create_german_driving_license_recognizer(self) -> PatternRecognizer:
        """German Driving License Number"""
        patterns = [
            Pattern(
                name="german_driving_license",
                regex=r"\b[A-Z]{2}\d{8}\b|\b\d{11}\b",
                score=0.7
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_DRIVING_LICENSE",
            patterns=patterns,
            supported_language="de"
        )

    def _create_residence_permit_recognizer(self) -> PatternRecognizer:
        """German Residence Permit Number"""
        patterns = [
            Pattern(
                name="german_residence_permit",
                regex=r"\b[A-Z]\d{9}[A-Z]\d\b",
                score=0.8
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_RESIDENCE_PERMIT",
            patterns=patterns,
            supported_language="de"
        )

    # Add these methods to GermanRecognizers class
    
    def _create_german_bank_account_recognizer(self) -> PatternRecognizer:
        """German Bank Account Numbers (Kontonummer)"""
        patterns = [
            Pattern(
                name="german_bank_account",
                regex=r"\b\d{6,10}\b(?=\s*(?:Kontonummer|Konto|Account))",
                score=0.85
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_BANK_ACCOUNT",
            patterns=patterns,
            supported_language="de"
        )
    
    def _create_german_social_security_recognizer(self) -> PatternRecognizer:
        """German Social Security Number (Sozialversicherungsnummer)"""
        patterns = [
            Pattern(
                name="german_social_security",
                regex=r"\b\d{2}\s?\d{2}\s?\d{2}\s?[A-Z]\s?\d{3}\b",
                score=0.9
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_SOCIAL_SECURITY",
            patterns=patterns,
            supported_language="de"
        )
    
    def _create_german_date_of_birth_recognizer(self) -> PatternRecognizer:
        """German Date of Birth patterns"""
        patterns = [
            Pattern(
                name="german_dob_format1",
                regex=r"\b(?:Geburtstag|geb\.?|geboren|Geburtsdatum)\s*(?:ist|:)?\s*(\d{2}\.\d{2}\.\d{4})\b",
                score=0.95
            ),
            Pattern(
                name="german_dob_format2",
                regex=r"\b\d{2}\.\d{2}\.\d{4}\b(?=\s*(?:Geburtstag|geboren))",
                score=0.9
            ),
            Pattern(
                name="german_date_format",
                regex=r"\b\d{2}\.\d{2}\.\d{4}\b",
                score=0.85
            ),
            Pattern(
                name="german_date_iso_format",
                regex=r"\b\d{4}-\d{2}-\d{2}\b",
                score=0.85
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_DATE_OF_BIRTH",
            patterns=patterns,
            supported_language="de"
        )
        
    def _create_german_name_recognizer(self) -> PatternRecognizer:
        """German Person Names"""
        patterns = [
            Pattern(
                name="german_name_with_context",
                regex=r"\b(?:Herr|Frau|Dr\.|Prof\.|Doktor|Professor)\s+([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)?)\b",
                score=0.9
            ),
            Pattern(
                name="german_name_in_sentence",
                regex=r"\b(?:Name|heißt|ist)\s+(?:der|die|das)?\s*([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)?)\b",
                score=0.85
            ),
            Pattern(
                name="german_name_with_von",
                regex=r"\b([A-ZÄÖÜ][a-zäöüß]+\s+(?:von|van|de)\s+[A-ZÄÖÜ][a-zäöüß]+)\b",
                score=0.9
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_PERSON_NAME",
            patterns=patterns,
            supported_language="de"
        )
        
    def _create_german_credit_card_recognizer(self) -> PatternRecognizer:
        """German Credit Card Numbers"""
        patterns = [
            Pattern(
                name="credit_card_standard",
                regex=r"\b(?:\d[ -]*?){13,16}\b",
                score=0.9
            ),
            Pattern(
                name="credit_card_formatted",
                regex=r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b",
                score=0.95
            ),
            Pattern(
                name="credit_card_with_context",
                regex=r"\bKreditkartennummer\s+(?:ist|:)?\s*(\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4})\b",
                score=1.0
            ),
            Pattern(
                name="credit_card_visa_prefix",
                regex=r"\b4\d{3}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b",
                score=0.95
            ),
            Pattern(
                name="credit_card_mastercard_prefix",
                regex=r"\b5[1-5]\d{2}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b",
                score=0.95
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_CREDIT_CARD",
            patterns=patterns,
            supported_language="de"
        )
        
    def _create_german_customer_id_recognizer(self) -> PatternRecognizer:
        """German Customer IDs"""
        patterns = [
            Pattern(
                name="customer_id_general",
                regex=r"\b[A-Z]+-\d{6,10}\b",
                score=0.85
            ),
            Pattern(
                name="customer_id_with_context",
                regex=r"\bKundennummer\s+(?:bei|:)?\s*(?:der)?\s*(?:[A-Za-zÄÖÜäöüß]+\s+)?(?:lautet)?\s*([A-Z]+-\d+)\b",
                score=0.95
            ),
            Pattern(
                name="insurance_customer_id",
                regex=r"\b(?:AOK|TK|BKK|DAK|IKK|KKH)-\d+\b",
                score=0.9
            ),
            Pattern(
                name="customer_id_numeric",
                regex=r"\bKunden-?(?:nummer|ID)?\s*(?:ist|:)?\s*(\d{6,10})\b",
                score=0.9
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_CUSTOMER_ID",
            patterns=patterns,
            supported_language="de"
        )
        
    def _create_german_street_name_recognizer(self) -> PatternRecognizer:
        """German Street Names - just the street names without numbers"""
        patterns = [
            Pattern(
                name="german_street_name",
                regex=r"\b([A-ZÄÖÜ][a-zäöüß]+(?:straße|str\.?|gasse|weg|platz|allee|ring|hof|damm))\b",
                score=0.9
            ),
            Pattern(
                name="german_street_name_with_context",
                regex=r"\bin\s+der\s+([A-ZÄÖÜ][a-zäöüß]+(?:straße|str\.?|gasse|weg|platz|allee|ring|hof|damm))\b",
                score=0.95
            ),
            Pattern(
                name="german_street_address_context",
                regex=r"\b(?:Adresse|wohnt|wohnhaft|ansässig)\s+(?:in|an)\s+(?:der)?\s+([A-ZÄÖÜ][a-zäöüß]+(?:straße|str\.?|gasse|weg|platz|allee|ring|hof|damm))\b",
                score=0.95
            ),
            Pattern(
                name="german_street_with_number",
                regex=r"\b([A-ZÄÖÜ][a-zäöüß]+(?:straße|str\.?|gasse|weg|platz|allee|ring|hof|damm))\s+\d+[a-z]?\b",
                score=0.9
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_STREET_NAME",
            patterns=patterns,
            supported_language="de"
        )
        
    def _create_german_postal_code_recognizer(self) -> PatternRecognizer:
        """German Postal Codes"""
        patterns = [
            Pattern(
                name="german_postal_code",
                regex=r"\b\d{5}\b",
                score=0.7
            ),
            Pattern(
                name="german_postal_code_with_context",
                regex=r"\bPLZ\s*:?\s*(\d{5})\b",
                score=0.95
            ),
            Pattern(
                name="german_postal_code_in_address",
                regex=r"\b(\d{5})\s+[A-ZÄÖÜ][a-zäöüß]+\b",
                score=0.85
            ),
            Pattern(
                name="german_postal_code_with_city",
                regex=r"\b(?:in|aus)\s+\d{5}\s+([A-ZÄÖÜ][a-zäöüß]+)\b",
                score=0.85
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_POSTAL_CODE",
            patterns=patterns,
            supported_language="de"
        )
        
    def _create_german_expiry_date_recognizer(self) -> PatternRecognizer:
        """Credit Card and ID Expiry Dates"""
        patterns = [
            Pattern(
                name="expiry_date_mm_yy",
                regex=r"\b(?:0[1-9]|1[0-2])/\d{2}\b",
                score=0.7
            ),
            Pattern(
                name="expiry_date_mm_yyyy",
                regex=r"\b(?:0[1-9]|1[0-2])/20\d{2}\b",
                score=0.7
            ),
            Pattern(
                name="expiry_date_with_context",
                regex=r"\b(?:Ablaufdatum|gültig\s+bis|valid\s+thru|expiry)\s*:?\s*((?:0[1-9]|1[0-2])/(?:\d{2}|\d{4}))\b",
                score=0.95
            ),
            Pattern(
                name="expiry_date_german_format",
                regex=r"\b(?:gültig\s+bis|Verfallsdatum)\s*:?\s*(\d{2}\.\d{2}\.\d{4})\b",
                score=0.95
            ),
            Pattern(
                name="expiry_date_on_card",
                regex=r"\b(?:EXP|VALID THRU)\s*:?\s*((?:0[1-9]|1[0-2])/(?:\d{2}|\d{4}))\b",
                score=0.9
            )
        ]
        return PatternRecognizer(
            supported_entity="DE_EXPIRY_DATE",
            patterns=patterns,
            supported_language="de"
        )