"""
Test suite for mock OCR and LLM providers.
Tests extraction pipeline with realistic South African trade documents.
"""

import pytest

from app.ai.mock_ocr import MockOCRProvider
from app.ai.mock_llm import MockLLMProvider
from app.ai.extraction import extract_document_fields, classify_line_item


@pytest.fixture
def ocr_provider():
    """Create mock OCR provider."""
    return MockOCRProvider()


@pytest.fixture
def llm_provider():
    """Create mock LLM provider."""
    return MockLLMProvider()


@pytest.mark.asyncio
async def test_mock_ocr_extracts_invoice_text(ocr_provider):
    """Test that mock OCR extracts invoice text."""
    text = await ocr_provider.extract_text("fake_key", "invoice")

    assert "INVOICE" in text
    assert "Invoice Number" in text
    assert "Global Electronics" in text
    assert "Tech Solutions SA" in text


@pytest.mark.asyncio
async def test_mock_ocr_extracts_packing_list_text(ocr_provider):
    """Test that mock OCR extracts packing list text."""
    text = await ocr_provider.extract_text("fake_key", "packing_list")

    assert "PACKING LIST" in text
    assert "Shipper" in text
    assert "Consignee" in text


@pytest.mark.asyncio
async def test_mock_ocr_extracts_bill_of_lading_text(ocr_provider):
    """Test that mock OCR extracts bill of lading text."""
    text = await ocr_provider.extract_text("fake_key", "bill_of_lading")

    assert "BILL OF LADING" in text
    assert "Maersk" in text
    assert "Container" in text


@pytest.mark.asyncio
async def test_mock_ocr_unknown_type_returns_default(ocr_provider):
    """Test that unknown document type returns default template."""
    text = await ocr_provider.extract_text("fake_key", "unknown_type")

    assert "DOCUMENT" in text


@pytest.mark.asyncio
async def test_extract_fields_returns_confidence(llm_provider):
    """Test that field extraction returns confidence scores."""
    text = """
    INVOICE
    Invoice Number: INV-2026-001
    Date: 2026-08-10
    Total Amount: $3,450.00
    Subtotal: $3,250.00
    Shipping: $200.00
    Seller: Global Electronics Ltd.
    Buyer: Tech Solutions SA
    Currency: USD
    Terms: FOB Shanghai
    Country of Origin: China
    """

    fields = await llm_provider.extract_fields(text, "invoice")

    assert "invoice_number" in fields
    assert fields["invoice_number"]["value"] == "INV-2026-001"
    assert fields["invoice_number"]["confidence"] >= 0.9

    assert "total_amount" in fields
    assert fields["total_amount"]["value"] == 3450.00
    assert fields["total_amount"]["confidence"] >= 0.8

    assert "currency" in fields
    assert fields["currency"]["value"] == "USD"


@pytest.mark.asyncio
async def test_extract_fields_line_items(llm_provider):
    """Test that line items are extracted correctly."""
    text = """
    INVOICE
    1. Solar Panels (500W Monocrystalline)
       Quantity: 10
       Unit Price: $250.00
       Total: $2,500.00
       HS Code: 8541.40

    2. Battery Banks (12V 200Ah)
       Quantity: 5
       Unit Price: $150.00
       Total: $750.00
       HS Code: 8507.60
    """

    fields = await llm_provider.extract_fields(text, "invoice")

    assert "line_items" in fields
    assert len(fields["line_items"]["value"]) == 2

    item1 = fields["line_items"]["value"][0]
    assert item1["description"] == "Solar Panels (500W Monocrystalline)"
    assert item1["quantity"] == 10
    assert item1["unit_price"] == 250.00
    assert item1["total_value"] == 2500.00

    item2 = fields["line_items"]["value"][1]
    assert item2["description"] == "Battery Banks (12V 200Ah)"
    assert item2["quantity"] == 5


@pytest.mark.asyncio
async def test_extract_fields_hs_codes(llm_provider):
    """Test that HS codes are extracted from text."""
    text = """
    INVOICE
    1. Solar Panels
       HS Code: 8541.40
    2. Battery Banks
       HS Code: 8507.60
    """

    fields = await llm_provider.extract_fields(text, "invoice")

    assert "hs_codes" in fields
    assert "8541.40" in fields["hs_codes"]["value"]
    assert "8507.60" in fields["hs_codes"]["value"]


@pytest.mark.asyncio
async def test_classify_solar_panel(llm_provider):
    """Test HS code classification for solar panels."""
    candidates = await llm_provider.classify_hs_code("500W Monocrystalline Solar Panels")

    assert len(candidates) > 0
    assert candidates[0]["hs_code"] == "8541.40"
    assert candidates[0]["confidence"] >= 0.9
    assert "solar" in candidates[0]["reasoning"].lower()


@pytest.mark.asyncio
async def test_classify_battery(llm_provider):
    """Test HS code classification for batteries."""
    candidates = await llm_provider.classify_hs_code("12V 200Ah Deep Cycle Battery")

    assert len(candidates) > 0
    assert candidates[0]["hs_code"] == "8507.60"
    assert candidates[0]["confidence"] >= 0.9


@pytest.mark.asyncio
async def test_classify_unknown_product(llm_provider):
    """Test HS code classification for unknown product returns fallback."""
    candidates = await llm_provider.classify_hs_code("Generic electronic component")

    assert len(candidates) > 0
    # Should return fallback candidates with lower confidence
    assert candidates[0]["confidence"] < 0.5


@pytest.mark.asyncio
async def test_classify_returns_sorted_by_confidence(llm_provider):
    """Test that classification results are sorted by confidence."""
    candidates = await llm_provider.classify_hs_code("Solar Panels")

    # Verify sorted descending by confidence
    for i in range(len(candidates) - 1):
        assert candidates[i]["confidence"] >= candidates[i + 1]["confidence"]


@pytest.mark.asyncio
async def test_extract_document_fields_pipeline():
    """Test the full extraction pipeline."""
    fields = await extract_document_fields("fake_key", "invoice")

    assert "invoice_number" in fields
    assert "total_amount" in fields
    assert "line_items" in fields
    assert "hs_codes" in fields

    # All fields should have confidence scores
    for field_name, field_data in fields.items():
        assert "value" in field_data
        assert "confidence" in field_data
        assert "verified" in field_data
        assert 0.0 <= field_data["confidence"] <= 1.0


@pytest.mark.asyncio
async def test_classify_line_item():
    """Test line item classification."""
    candidates = await classify_line_item("500W Monocrystalline Solar Panels")

    assert len(candidates) > 0
    assert candidates[0]["hs_code"] == "8541.40"
    assert "confidence" in candidates[0]
    assert "reasoning" in candidates[0]


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_extraction.py -v")
