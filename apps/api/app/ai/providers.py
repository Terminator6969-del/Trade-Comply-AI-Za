"""
AI provider abstractions for OCR and LLM services.
Provides factory functions to get provider implementations.
"""

from abc import ABC, abstractmethod
from typing import Any

from app.core.config import settings


class OCRProvider(ABC):
    """
    Abstract base class for OCR providers.
    Extracts text from uploaded documents (PDFs, images).
    """

    @abstractmethod
    async def extract_text(
        self,
        file_key: str,
        document_type: str,
    ) -> str:
        """
        Extract text from a document.
        
        Args:
            file_key: MinIO object key for the document
            document_type: Type of document (invoice, packing_list, etc.)
            
        Returns:
            Extracted text content
        """
        pass


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    Extracts structured fields from text content.
    """

    @abstractmethod
    async def extract_fields(
        self,
        text: str,
        document_type: str,
    ) -> dict[str, Any]:
        """
        Extract structured fields from text.
        
        Args:
            text: Extracted text content
            document_type: Type of document
            
        Returns:
            Dictionary of extracted fields with confidence scores
        """
        pass

    @abstractmethod
    async def classify_hs_code(
        self,
        description: str,
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Classify a product description to HS codes.
        
        Args:
            description: Product description
            context: Additional context (country, value, etc.)
            
        Returns:
            List of HS code candidates with confidence scores
        """
        pass


def get_ocr_provider(provider_name: str | None = None) -> OCRProvider:
    """
    Factory function to get OCR provider.
    
    Args:
        provider_name: Provider name (mock, azure, aws, gcp)
        
    Returns:
        OCRProvider instance
    """
    name = provider_name or settings.OCR_PROVIDER

    if name == "mock":
        from app.ai.mock_ocr import MockOCRProvider
        return MockOCRProvider()
    elif name == "azure":
        from app.ai.azure_ocr import AzureOCRProvider
        return AzureOCRProvider()
    elif name == "aws":
        from app.ai.aws_ocr import AWSOCRProvider
        return AWSOCRProvider()
    elif name == "gcp":
        from app.ai.gcp_ocr import GCPOCRProvider
        return GCPOCRProvider()
    else:
        raise ValueError(f"Unknown OCR provider: {name}")


def get_llm_provider(provider_name: str | None = None) -> LLMProvider:
    """
    Factory function to get LLM provider.
    
    Args:
        provider_name: Provider name (mock, azure, aws, gcp, openai)
        
    Returns:
        LLMProvider instance
    """
    name = provider_name or settings.LLM_PROVIDER

    if name == "mock":
        from app.ai.mock_llm import MockLLMProvider
        return MockLLMProvider()
    elif name == "azure":
        from app.ai.azure_llm import AzureLLMProvider
        return AzureLLMProvider()
    elif name == "aws":
        from app.ai.aws_llm import AWSLLMProvider
        return AWSLLMProvider()
    elif name == "gcp":
        from app.ai.gcp_llm import GCPLLMProvider
        return GCPLLMProvider()
    elif name == "openai":
        from app.ai.openai_llm import OpenAILLMProvider
        return OpenAILLMProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {name}")
