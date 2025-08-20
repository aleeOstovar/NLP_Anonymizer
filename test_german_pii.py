from engines.analyzer_engine import PIIAnalyzerEngine
from engines.anonymizer_engine import PIIAnonymizerEngine
from core.types import Language

def test_german_pii():
    # Initialize the analyzer and anonymizer
    analyzer = PIIAnalyzerEngine()
    anonymizer = PIIAnonymizerEngine()
    
    # German text with PII
    german_text = """
    Mein Name ist Hans Müller und meine Steuer-ID ist 12 345 678 901.
    Meine Telefonnummer ist +49 30 12345678 und E-Mail hans.mueller@example.com.
    Meine IBAN ist DE89 3704 0044 0532 0130 00.
    Ich wohne in der Friedrichstraße 123, Berlin.
    """
    
    # Analyze the text
    analysis_results = analyzer.analyze(text=german_text, language=Language.GERMAN)
    
    # Print analysis results
    print("Entities found:", len(analysis_results))
    print("Entity types:", [result.entity_type for result in analysis_results])
    
    # Anonymize the text
    anonymized_result = anonymizer.anonymize(
        text=german_text,
        analyzer_results=analysis_results,
        language=Language.GERMAN
    )
    
    # Print original and anonymized text
    print("\nOriginal:")
    print(german_text)
    print("\nAnonymized:")
    print(anonymized_result.text)
    
    # Check if phone number was detected
    phone_detected = any(result.entity_type == "DE_PHONE_NUMBER" for result in analysis_results)
    print("\nPhone number detected:", phone_detected)
    
    # Check if address was detected
    address_detected = any(result.entity_type == "DE_STREET_ADDRESS" for result in analysis_results)
    print("Address detected:", address_detected)

if __name__ == "__main__":
    test_german_pii()