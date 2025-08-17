class PIIAnonymizerError(Exception):
    """Base exception for PII anonymizer"""
    pass


class UnsupportedLanguageError(PIIAnonymizerError):
    """Raised when unsupported language is used"""
    pass


class UnsupportedDataTypeError(PIIAnonymizerError):
    """Raised when unsupported data type is processed"""
    pass


class RecognizerInitializationError(PIIAnonymizerError):
    """Raised when recognizer fails to initialize"""
    pass


class ProcessingError(PIIAnonymizerError):
    """Raised when processing fails"""
    pass


class DeanonymizationError(PIIAnonymizerError):
    """Raised when deanonymization fails"""
    pass
