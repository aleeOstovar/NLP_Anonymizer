import io
import pandas as pd
from main import PIIAnonymizer
from core.types import Language


def example_german_text():
    """Example: German text anonymization"""
    print("=== GERMAN TEXT ANONYMIZATION ===")
    
    anonymizer = PIIAnonymizer()
    
    german_text = """
    Mein Name ist Claudia Schneider und mein Geburtsdatum ist 15.07.1985.
Meine Kundennummer bei der Krankenkasse lautet AOK-55678234.
Meine Handynummer ist +49 171 98765432 und meine E-Mail-Adresse lautet claudia.schneider@web.de.
Meine Kreditkartennummer ist 4111 1111 1111 1111 mit Ablaufdatum 08/27.
Ich wohne in der Musterstraße 45, 50667 Köln.
    """
    
    # Anonymize
    result = anonymizer.anonymize_text(german_text, Language.GERMAN)
    print("Original:", german_text.strip())
    print("Anonymized:", result.anonymized_data)
    print("Entities found:", result.metadata['entities_found'])
    print("Entity types:", result.metadata['entities_types'])
    
    # Deanonymize
    deanon_result = anonymizer.deanonymize_text(
        result.anonymized_data,
        result.get_entities_dict()
    )
    print("Deanonymized:", deanon_result.original_data)
    print("Success:", deanon_result.success)
    print()


def example_english_text():
    """Example: English text with crypto and medical licenses"""
    print("=== ENGLISH TEXT ANONYMIZATION ===")
    
    anonymizer = PIIAnonymizer()
    
    english_text = """
    Dr. John Smith (MD123456789) can be reached at john.smith@hospital.com.
    His Bitcoin address is 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa and phone +1-555-123-4567.
    Patient's nationality is American, religion Catholic.
    Credit card: 4532-1234-5678-9012
    """
    
    result = anonymizer.anonymize_text(english_text, Language.ENGLISH)
    print("Original:", english_text.strip())
    print("Anonymized:", result.anonymized_data)
    print("Entities found:", result.metadata)
    print()


def example_csv_anonymization():
    """Example: CSV anonymization"""
    print("=== CSV ANONYMIZATION ===")
    
    anonymizer = PIIAnonymizer()
    
    sample_csv_data = """Name,Email,Phone,Tax_ID,Comments
Hans Mueller,hans@email.com,+49 30 1234567,12 345 678 901,Patient with German nationality
John Smith,john@email.com,+1-555-123-4567,123-45-6789,American citizen
Maria Garcia,maria@email.com,+34 91 123 4567,Y1234567L,Spanish resident
"""
    
    # Show original
    original_df = pd.read_csv(io.StringIO(sample_csv_data))
    print("Original CSV:")
    print(original_df)
    
    # Anonymize
    result = anonymizer.anonymize_csv(sample_csv_data, Language.GERMAN)
    print("\nAnonymized CSV:")
    print(result.anonymized_data)
    print("Metadata:", result.metadata)
    
    # Deanonymize
    deanon_result = anonymizer.deanonymize_csv(
        result.anonymized_data,
        result.get_entities_dict()
    )
    print("\nDeanonymized CSV:")
    print(deanon_result.original_data)
    print()


def example_analysis_only():
    """Example: Analysis without anonymization"""
    print("=== ANALYSIS ONLY ===")
    
    anonymizer = PIIAnonymizer()
    
    text = "Hans Müller, Steuer-ID: 12 345 678 901, Email: hans@test.de"
    
    # Analyze without anonymizing
    entities = anonymizer.analyze_only(text, Language.GERMAN)
    
    print("Text:", text)
    print("Detected entities:")
    for entity in entities:
        print(f"  {entity['entity_type']}: '{entity['text']}' "
              f"(confidence: {entity['confidence']:.2f})")
    print()


def example_supported_features():
    """Example: Show supported features"""
    print("=== SUPPORTED FEATURES ===")
    
    anonymizer = PIIAnonymizer()
    
    print("Supported languages:", anonymizer.get_supported_languages())
    print("Supported data types:", anonymizer.get_supported_data_types())
    print("German entities:", anonymizer.get_supported_entities(Language.GERMAN)[:10], "...")
    print("English entities:", anonymizer.get_supported_entities(Language.ENGLISH)[:10], "...")
    print()


def example_custom_fake_generators():
    """Example: Using custom fake value generators"""
    print("=== CUSTOM FAKE GENERATORS ===")
    
    anonymizer = PIIAnonymizer()
    
    # Custom generators
    custom_generators = {
        "PERSON": lambda original: f"[REDACTED_PERSON_{len(original)}]",
        "EMAIL_ADDRESS": lambda original: "[REDACTED_EMAIL]",
        "PHONE_NUMBER": lambda original: "[REDACTED_PHONE]"
    }
    
    text = "Contact John Doe at john@example.com or +1-555-123-4567"
    
    result = anonymizer.anonymize_text(
        text,
        Language.ENGLISH,
        custom_fake_generators=custom_generators
    )
    
    print("Original:", text)
    print("Anonymized:", result.anonymized_data)
    print()


if __name__ == "__main__":
    """Run all examples"""
    try:
        example_german_text()
        # example_english_text()
        # example_csv_anonymization()
        # example_analysis_only()
        # example_supported_features()
        # example_custom_fake_generators()
        
        # print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        raise