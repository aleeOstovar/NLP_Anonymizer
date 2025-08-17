from typing import Dict, Type,List
from core.types import DataType
from core.base import BaseProcessor
from core.exceptions import UnsupportedDataTypeError
from .text_processor import TextProcessor
from .image_processor import ImageOCRProcessor
from .csv_processor import CSVProcessor
from .excel_processor import ExcelProcessor


class ProcessorFactory:
    """Factory for creating data type specific processors"""
    
    _processors: Dict[DataType, Type[BaseProcessor]] = {
        DataType.TEXT: TextProcessor,
        DataType.IMAGE_OCR: ImageOCRProcessor,
        DataType.CSV: CSVProcessor,
        DataType.EXCEL: ExcelProcessor
    }
    
    @classmethod
    def create_processor(cls, data_type: DataType) -> BaseProcessor:
        """Create processor for specified data type"""
        if data_type not in cls._processors:
            raise UnsupportedDataTypeError(f"Data type {data_type.value} not supported")
        
        processor_class = cls._processors[data_type]
        return processor_class()
    
    @classmethod
    def get_supported_data_types(cls) -> List[DataType]:
        """Get all supported data types"""
        return list(cls._processors.keys())
    
    @classmethod
    def register_processor(
        cls, 
        data_type: DataType, 
        processor_class: Type[BaseProcessor]
    ) -> None:
        """Register a new processor for a data type"""
        cls._processors[data_type] = processor_class