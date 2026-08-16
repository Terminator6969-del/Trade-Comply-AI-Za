"""
Mock OCR provider for development and testing.
Returns realistic South African trade document text.
"""

from app.ai.providers import OCRProvider


class MockOCRProvider(OCRProvider):
    """
    Mock OCR provider that returns realistic South African trade document text.
    Used for development and testing without external API calls.
    """

    # Mock document templates for different document types
    MOCK_TEMPLATES: dict[str, str] = {
        "invoice": """
INVOICE

Seller: Global Electronics Ltd.
Address: 123 Industrial Road, Shanghai, China
VAT Number: CN1234567890

Buyer: Tech Solutions SA
Address: 456 Main Street, Sandton, Johannesburg, South Africa
VAT Number: 4123456789

Invoice Number: INV-2026-001
Date: 2026-08-10
Due Date: 2026-09-10

Item Details:
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

Subtotal: $3,250.00
Shipping: $200.00
Total Amount: $3,450.00

Terms: FOB Shanghai
Currency: USD
""",
        "packing_list": """
PACKING LIST

Shipper: Global Electronics Ltd.
Shipper Address: 123 Industrial Road, Shanghai, China

Consignee: Tech Solutions SA
Consignee Address: 456 Main Street, Sandton, Johannesburg, South Africa

Packing List Number: PL-2026-001
Date: 2026-08-10

Package Details:
- Package 1: Solar Panels
  Quantity: 10 panels
  Weight: 25.0 kg
  Dimensions: 1750 x 1000 x 35 mm
  Description: 500W Monocrystalline Solar Panels

- Package 2: Battery Banks
  Quantity: 5 units
  Weight: 50.0 kg
  Dimensions: 500 x 250 x 300 mm
  Description: 12V 200Ah Deep Cycle Battery Banks

Total Packages: 2
Total Weight: 75.0 kg
Total Volume: 2.5 CBM

Remarks: Fragile - Handle with care
""",
        "bill_of_lading": """
BILL OF LADING

Carrier: Maersk Line
Voyage Number: MAERSK 123E
Vessel Name: MV Maersk Enterprise
Port of Loading: Shanghai, China
Port of Discharge: Durban, South Africa
Final Destination: Johannesburg, South Africa

Shipper: Global Electronics Ltd.
Shipper Address: 123 Industrial Road, Shanghai, China

Consignee: Tech Solutions SA
Consignee Address: 456 Main Street, Sandton, Johannesburg, South Africa

Notify Party: Tech Solutions SA
Notify Address: 456 Main Street, Sandton, Johannesburg, South Africa

B/L Number: BL-2026-001
Date: 2026-08-10
Place of Receipt: Shanghai
Place of Delivery: Johannesburg

Container Number: MSCU1234567
Seal Number: 123456
Container Size: 20ft
Container Type: Dry

Gross Weight: 1500 kg
Volume: 15.0 CBM
""",
        "commercial_invoice": """
COMMERCIAL INVOICE

Exporter: Global Electronics Ltd.
Exporter Address: 123 Industrial Road, Shanghai, China
Exporter VAT: CN1234567890

Importer: Tech Solutions SA
Importer Address: 456 Main Street, Sandton, Johannesburg, South Africa
Importer VAT: 4123456789

Invoice Number: CI-2026-001
Date: 2026-08-10
Reference: PO-2026-001

Product Details:
1. Solar Panels (500W Monocrystalline)
   HS Code: 8541.40
   Quantity: 10
   Unit Price: $250.00
   Total: $2,500.00

2. Battery Banks (12V 200Ah)
   HS Code: 8507.60
   Quantity: 5
   Unit Price: $150.00
   Total: $750.00

Subtotal: $3,250.00
Freight: $200.00
Insurance: $50.00
Total: $3,500.00

Terms: FOB Shanghai
Currency: USD
Country of Origin: China
""",
        "certificate_of_origin": """
CERTIFICATE OF ORIGIN

Country of Origin: China
Exporter: Global Electronics Ltd.
Exporter Address: 123 Industrial Road, Shanghai, China

Producer: Global Electronics Manufacturing Co. Ltd.
Producer Address: 789 Factory Road, Shanghai, China

Product: Solar Panels (500W Monocrystalline)
HS Code: 8541.40
Quantity: 10
Value: $2,500.00

Certificate Number: CO-2026-001
Date of Issue: 2026-08-10
Expiry Date: 2027-08-10

Issuing Authority: Shanghai Chamber of Commerce
Certificate of Origin Code: CN-SH-2026-001

This certifies that the goods described herein are wholly obtained or produced in China.
""",
        "other": """
DOCUMENT

This is a general document for reference purposes.
Please review the contents carefully.

Document ID: DOC-2026-001
Date: 2026-08-10
""",
    }

    async def extract_text(self, file_key: str, document_type: str) -> str:
        """
        Extract text from a document using mock OCR.
        
        Args:
            file_key: MinIO object key (ignored in mock)
            document_type: Type of document
            
        Returns:
            Mock extracted text
        """
        # Return mock text based on document type
        return self.MOCK_TEMPLATES.get(document_type, self.MOCK_TEMPLATES["other"])
