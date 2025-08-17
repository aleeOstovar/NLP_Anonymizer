# PII Anonymizer

A comprehensive system for detecting and anonymizing Personally Identifiable Information (PII) in text, images (OCR), CSV, and Excel files. Supports English and German languages with extensive pattern recognition for country-specific identification numbers and formats.

## Features

### 🌍 Multi-language Support
- **English**: Standard PII types plus crypto wallets, medical licenses, professional licenses
- **German**: Comprehensive German PII including Steuer-ID, RVNR, health insurance, VAT-ID, IBAN, and more

### 📊 Multiple Data Formats
- **Text**: Plain text anonymization with customizable entity detection
- **Images**: OCR text extraction and anonymization
- **CSV**: Column-wise processing with metadata tracking
- **Excel**: Multi-sheet support with selective processing

### 🔒 Advanced Anonymization
- **Deterministic**: Same input always produces same anonymized output
- **Reversible**: Full deanonymization support with entity mapping
- **Customizable**: Custom fake value generators and confidence thresholds
- **Format-preserving**: Maintains data structure and relationships

### 🎯 German PII Detection
- Tax ID (Steuer-ID)
- Pension Insurance Number (RVNR) 
- Health Insurance Numbers
- VAT ID (Umsatzsteuer-ID)
- German IBAN and BIC/SWIFT codes
- Commercial Register Numbers
- ID Cards, Passports, Driving Licenses
- German phone numbers and addresses

## Installation

```bash
pip install pii-anonymizer

# Install spaCy language models
python -m spacy download en_core_web_lg
python -m spacy download de_core_news_lg

# For OCR support (optional)
# Install Tesseract: https://github.com/tesseract-ocr/tesseract
```

## Quick Start

```python
from pii_anonymizer import PIIAnonymizer, Language

# Initialize anonymizer
anonymizer = PIIAnonymizer()

# German text example
german_text = '''
Mein Name ist Hans Müller und meine Steuer-ID ist 12 345 678 901.
E-Mail: hans.mueller@example.com, Telefon: +49 30 12345678
IBAN: DE89 3704 0044 0532 0130 00
'''

# Anonymize
result = anonymizer.anonymize_text(german_text, Language.GERMAN)
print("Anonymized:", result.anonymized_data)

# Deanonymize
original = anonymizer.deanonymize_text(
    result.anonymized_data, 
    result.get_entities_dict()
)
print("Original:", original.original_data)
```

## Usage Examples

### Text Anonymization

```python
# English text with various PII types
text = "Dr. John Smith (MD123456) at john@hospital.com, Bitcoin: 1A1zP1eP..."
result = anonymizer.anonymize_text(text, Language.ENGLISH)
```

### CSV Processing

```python
import pandas as pd

# CSV with PII data
csv_data = '''Name,Email,Phone,Tax_ID
Hans Mueller,hans@email.com,+49 30 1234567,12 345 678 901'''

result = anonymizer.anonymize_csv(csv_data, Language.GERMAN)
print(result.anonymized_data)  # Returns anonymized DataFrame
```

### Image OCR

```python
from PIL import Image

# Process image with OCR
image = Image.open("document.jpg")
result = anonymizer.anonymize_image_ocr(image, Language.GERMAN)

print("Original text:", result.anonymized_data["original_text"])
print("Anonymized:", result.anonymized_data["anonymized_text"])
```

### Excel Processing

```python
# Multi-sheet Excel processing
result = anonymizer.anonymize_excel(
    "data.xlsx", 
    Language.GERMAN,
    sheets_to_process=["Sheet1", "Customers"],
    text_columns={"Sheet1": ["Name", "Email"], "Customers": ["Contact"]}
)
```

### Analysis Only (No Anonymization)

```python
# Just detect PII without anonymizing
entities = anonymizer.analyze_only("Hans Müller, Tel: +49 30 123456", Language.GERMAN)

for entity in entities:
    print(f"{entity['entity_type']}: {entity['text']} (confidence: {entity['confidence']:.2f})")
```

### Custom Fake Value Generators

```python
# Custom anonymization logic
custom_generators = {
    "PERSON": lambda original: f"[PERSON-{len(original)}]",
    "EMAIL_ADDRESS": lambda original: "[REDACTED-EMAIL]"
}

result = anonymizer.anonymize_text(
    "Contact John at john@example.com",
    Language.ENGLISH,
    custom_fake_generators=custom_generators
)
```

## Architecture

The system is built with a modular architecture:

```
pii_anonymizer/
├── core/                    # Core types and base classes
├── recognizers/             # Language-specific PII recognizers  
├── processors/              # Data format processors
├── engines/                 # Anonymization engines
├── utils/                   # Utilities and helpers
└── examples/                # Usage examples
```

### Key Components

- **PIIAnonymizer**: Main API interface
- **RecognizerFactory**: Creates language-specific recognizers
- **ProcessorFactory**: Creates data-type-specific processors  
- **PIIAnalyzerEngine**: Coordinates PII detection
- **FakeDataGenerator**: Generates replacement values

## Supported Entity Types

### Universal
- PERSON, EMAIL_ADDRESS, PHONE_NUMBER, CREDIT_CARD
- IP_ADDRESS, URL, LOCATION, DATE_TIME, IBAN_CODE

### English-Specific  
- CRYPTO_WALLET, MEDICAL_LICENSE, PROFESSIONAL_LICENSE
- NRP (Nationality, Religion, Politics)

### German-Specific
- DE_TAX_ID, DE_PENSION_INSURANCE, DE_HEALTH_INSURANCE
- DE_VAT_ID, DE_COMMERCIAL_REGISTER, DE_IBAN
- BIC_SWIFT, DE_PHONE_NUMBER, DE_STREET_ADDRESS  
- DE_ID_CARD, DE_PASSPORT, DE_DRIVING_LICENSE
- DE_RESIDENCE_PERMIT

## Configuration Options

```python
from pii_anonymizer.core.types import ProcessingConfig

config = ProcessingConfig(
    language=Language.GERMAN,
    entities_to_process=["PERSON", "EMAIL_ADDRESS"],  # Specific entities only
    confidence_threshold=0.8,                         # Higher confidence required
    preserve_format=True,                            # Maintain original formatting
    custom_fake_generators={                         # Custom replacements
        "PERSON": lambda x: "[REDACTED]"
    }
)

result = anonymizer.anonymize_text(text, config)
```

## Entity Mapping and Deanonymization

The system maintains detailed mapping between original and anonymized values:

```python
result = anonymizer.anonymize_text(text, Language.GERMAN)

# Access entity mapping
entities_map = result.get_entities_dict()
for entity_id, entity_data in entities_map.items():
    print(f"{entity_id}: {entity_data['original_value']} -> {entity_data['fake_value']}")

# Save mapping for later use
anonymizer.save_entities_map(result.entities_map, "mapping.json")

# Load and deanonymize later
loaded_mapping = anonymizer.load_entities_map("mapping.json")
original = anonymizer.deanonymize_text(anonymized_text, loaded_mapping)
```

## Error Handling

The system provides comprehensive error handling:

```python
from pii_anonymizer.core.exceptions import ProcessingError, UnsupportedLanguageError

try:
    result = anonymizer.anonymize_text(text, Language.GERMAN)
except UnsupportedLanguageError as e:
    print(f"Language not supported: {e}")
except ProcessingError as e:
    print(f"Processing failed: {e}")
```

## Performance Considerations

- **Caching**: Processors and generators are cached for reuse
- **Batch Processing**: Process multiple texts in batches for better performance
- **Memory Usage**: Large Excel files are processed sheet by sheet
- **Confidence Thresholds**: Higher thresholds improve speed but may miss entities

## Dependencies

- **presidio-analyzer/anonymizer**: Core PII detection engine
- **spaCy**: NLP processing (en_core_web_lg, de_core_news_lg models required)
- **pandas**: Data processing for CSV/Excel
- **Pillow + pytesseract**: Image OCR capabilities
- **openpyxl**: Excel file processing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- GitHub Issues: [Create an issue](https://github.com/your-org/pii-anonymizer/issues)
- Email: info@pii-anonymizer.com
- Documentation: [Read the docs](https://pii-anonymizer.readthedocs.io)