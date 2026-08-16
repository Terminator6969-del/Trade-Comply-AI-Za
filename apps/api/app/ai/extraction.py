"""
Extraction pipeline for document field extraction.
Orchestrates OCR → LLM extraction → validation.
"""

from typing import Any

from app.ai.providers import get_ocr_provider, get_llm_provider
from app.core.config import settings


async def extract_document_fields(
    file_key: str,
    document_type: str,
) -> dict[str, Any]:
    """
    Extract structured fields from a document.
    
    Pipeline:
    1. OCR provider extracts text from document
    2. LLM provider extracts structured fields from text
    3. Fields are validated and returned with confidence scores
    
    Args:
        file_key: MinIO object key for the document
        document_type: Type of document (invoice, packing_list, etc.)
        
    Returns:
        Dictionary of extracted fields with confidence scores
    """
    # Get providers
    ocr_provider = get_ocr_provider(settings.OCR_PROVIDER)
    llm_provider = get_llm_provider(settings.LLM_PROVIDER)

    # Step 1: Extract text via OCR
    text = await ocr_provider.extract_text(file_key, document_type)

    # Step 2: Extract structured fields via LLM
    fields = await llm_provider.extract_fields(text, document_type)

    # Step 3: Validate and normalize
    validated_fields = _validate_fields(fields)

    return validated_fields


def _validate_fields(fields: dict[str, Any]) -> dict[str, Any]:
    """
    Validate and normalize extracted fields.
    
    Args:
        fields: Raw extracted fields from LLM
        
    Returns:
        Validated and normalized fields
    """
    validated = {}

    for field_name, field_data in fields.items():
        if isinstance(field_data, dict) and "value" in field_data and "confidence" in field_data:
            # Already in expected format
            validated[field_name] = {
                "value": field_data["value"],
                "confidence": float(field_data["confidence"]),
                "verified": False,
            }
        else:
            # Wrap raw value
            validated[field_name] = {
                "value": field_data,
                "confidence": 0.5,  # Default confidence
                "verified": False,
            }

    return validated


async def classify_line_item(
    description: str,
    context: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """
    Classify a line item to HS codes.
    
    Args:
        description: Product description
        context: Additional context (country, value, etc.)
        
    Returns:
        List of HS code candidates with confidence scores
    """
    llm_provider = get_llm_provider(settings.LLM_PROVIDER)
    candidates = await llm_provider.classify_hs_code(description, context)

    return candidates
