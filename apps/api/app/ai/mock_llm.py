"""
Mock LLM provider for development and testing.
Returns deterministic extraction and classification results.
"""

import re
from typing import Any

from app.ai.providers import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    Mock LLM provider that returns deterministic extraction and classification results.
    Used for development and testing without external API calls.
    """

    # Mock HS code database for classification
    MOCK_HS_CODES: list[dict[str, Any]] = [
        {
            "hs_code": "8541.40",
            "description": "Solar panels for electricity generation",
            "duty_rate": 0.0,
            "vat_rate": 15.0,
            "confidence": 0.95,
        },
        {
            "hs_code": "8507.60",
            "description": "Batteries for storage of electricity",
            "duty_rate": 0.0,
            "vat_rate": 15.0,
            "confidence": 0.92,
        },
        {
            "hs_code": "8504.40",
            "description": "Power supplies for automatic data processing machines",
            "duty_rate": 0.0,
            "vat_rate": 15.0,
            "confidence": 0.88,
        },
        {
            "hs_code": "8517.62",
            "description": "Lithium-ion batteries",
            "duty_rate": 0.0,
            "vat_rate": 15.0,
            "confidence": 0.85,
        },
        {
            "hs_code": "8503.00",
            "description": "Electrical transformers and converters",
            "duty_rate": 0.0,
            "vat_rate": 15.0,
            "confidence": 0.80,
        },
    ]

    async def extract_fields(self, text: str, document_type: str) -> dict[str, Any]:
        """
        Extract structured fields from text using mock LLM.
        
        Args:
            text: Extracted text content
            document_type: Type of document
            
        Returns:
            Dictionary of extracted fields with confidence scores
        """
        fields: dict[str, Any] = {}

        # Extract invoice number
        invoice_match = re.search(r"Invoice Number:\s*(\S+)", text, re.IGNORECASE)
        if invoice_match:
            fields["invoice_number"] = {
                "value": invoice_match.group(1),
                "confidence": 0.95,
            }

        # Extract invoice date
        date_match = re.search(r"Date:\s*(\d{4}-\d{2}-\d{2})", text)
        if date_match:
            fields["invoice_date"] = {
                "value": date_match.group(1),
                "confidence": 0.92,
            }

        # Extract total amount
        total_match = re.search(r"Total Amount:\s*\$?([\d,]+\.?\d*)", text)
        if total_match:
            fields["total_amount"] = {
                "value": float(total_match.group(1).replace(",", "")),
                "confidence": 0.90,
            }

        # Extract subtotal
        subtotal_match = re.search(r"Subtotal:\s*\$?([\d,]+\.?\d*)", text)
        if subtotal_match:
            fields["subtotal"] = {
                "value": float(subtotal_match.group(1).replace(",", "")),
                "confidence": 0.88,
            }

        # Extract shipping cost
        shipping_match = re.search(r"Shipping:\s*\$?([\d,]+\.?\d*)", text)
        if shipping_match:
            fields["shipping_cost"] = {
                "value": float(shipping_match.group(1).replace(",", "")),
                "confidence": 0.85,
            }

        # Extract seller info
        seller_match = re.search(r"Seller:\s*(.+)\n", text)
        if seller_match:
            fields["seller_name"] = {
                "value": seller_match.group(1).strip(),
                "confidence": 0.90,
            }

        # Extract buyer info
        buyer_match = re.search(r"Buyer:\s*(.+)\n", text)
        if buyer_match:
            fields["buyer_name"] = {
                "value": buyer_match.group(1).strip(),
                "confidence": 0.90,
            }

        # Extract VAT numbers
        vat_matches = re.findall(r"VAT Number:\s*(\S+)", text)
        if vat_matches:
            fields["vat_numbers"] = {
                "value": vat_matches,
                "confidence": 0.85,
            }

        # Extract line items
        line_items = self._extract_line_items(text)
        if line_items:
            fields["line_items"] = {
                "value": line_items,
                "confidence": 0.80,
            }

        # Extract HS codes from text
        hs_codes = re.findall(r"HS Code:\s*(\d+\.\d+)", text)
        if hs_codes:
            fields["hs_codes"] = {
                "value": hs_codes,
                "confidence": 0.95,
            }

        # Extract currency
        currency_match = re.search(r"Currency:\s*(\w+)", text)
        if currency_match:
            fields["currency"] = {
                "value": currency_match.group(1),
                "confidence": 0.95,
            }

        # Extract terms
        terms_match = re.search(r"Terms:\s*(.+)\n", text)
        if terms_match:
            fields["terms"] = {
                "value": terms_match.group(1).strip(),
                "confidence": 0.90,
            }

        # Extract country of origin
        origin_match = re.search(r"Country of Origin:\s*(\w+)", text)
        if origin_match:
            fields["country_of_origin"] = {
                "value": origin_match.group(1),
                "confidence": 0.95,
            }

        return fields

    def _extract_line_items(self, text: str) -> list[dict[str, Any]]:
        """Extract line items from invoice text."""
        items = []

        # Pattern: "1. Description\n   Quantity: X\n   Unit Price: $Y\n   Total: $Z"
        pattern = r"(\d+)\.\s*(.+)\n\s*Quantity:\s*(\d+)\n\s*Unit Price:\s*\$?([\d,]+\.?\d*)\n\s*Total:\s*\$?([\d,]+\.?\d*)"
        matches = re.findall(pattern, text)

        for match in matches:
            items.append({
                "line_number": int(match[0]),
                "description": match[1].strip(),
                "quantity": int(match[2]),
                "unit_price": float(match[3].replace(",", "")),
                "total_value": float(match[4].replace(",", "")),
            })

        return items

    async def classify_hs_code(
        self,
        description: str,
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Classify a product description to HS codes using mock LLM.
        
        Args:
            description: Product description
            context: Additional context
            
        Returns:
            List of HS code candidates with confidence scores
        """
        description_lower = description.lower()
        candidates = []

        # Match based on keywords
        if "solar" in description_lower and "panel" in description_lower:
            candidates.append({
                "hs_code": "8541.40",
                "description": "Solar panels for electricity generation",
                "confidence": 0.95,
                "reasoning": "Description contains 'solar' and 'panel' keywords matching HS code 8541.40",
            })
        elif "battery" in description_lower:
            candidates.append({
                "hs_code": "8507.60",
                "description": "Batteries for storage of electricity",
                "confidence": 0.92,
                "reasoning": "Description contains 'battery' keyword matching HS code 8507.60",
            })
        elif "power supply" in description_lower or "adapter" in description_lower:
            candidates.append({
                "hs_code": "8504.40",
                "description": "Power supplies for automatic data processing machines",
                "confidence": 0.88,
                "reasoning": "Description contains 'power supply' or 'adapter' matching HS code 8504.40",
            })
        elif "lithium" in description_lower:
            candidates.append({
                "hs_code": "8517.62",
                "description": "Lithium-ion batteries",
                "confidence": 0.85,
                "reasoning": "Description contains 'lithium' matching HS code 8517.62",
            })
        elif "transformer" in description_lower:
            candidates.append({
                "hs_code": "8503.00",
                "description": "Electrical transformers and converters",
                "confidence": 0.80,
                "reasoning": "Description contains 'transformer' matching HS code 8503.00",
            })
        else:
            # Default fallback - return top candidates with lower confidence
            for code in self.MOCK_HS_CODES[:3]:
                candidates.append({
                    "hs_code": code["hs_code"],
                    "description": code["description"],
                    "confidence": code["confidence"] * 0.5,  # Lower confidence for unmatched
                    "reasoning": f"Fallback match based on general electronics category",
                })

        # Sort by confidence
        candidates.sort(key=lambda x: x["confidence"], reverse=True)

        return candidates
