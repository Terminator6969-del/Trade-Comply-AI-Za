"""
Pydantic schemas for document management.
"""

from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    """Base document schema."""

    document_type: str = Field(
        default="other",
        description="Document type",
        pattern="^(invoice|packing_list|bill_of_lading|airway_bill|commercial_invoice|certificate_of_origin|other)$",
    )
    file_name: str = Field(..., min_length=1, max_length=255, description="Original filename")


class DocumentCreate(DocumentBase):
    """Document creation request."""

    file_key: str = Field(..., description="MinIO object key")
    file_size: int = Field(..., ge=0, description="File size in bytes")
    mime_type: str = Field(..., description="MIME type")


class DocumentResponse(DocumentBase):
    """Document response model."""

    id: str = Field(..., description="Document ID")
    shipment_id: str = Field(..., description="Shipment ID")
    file_key: str = Field(..., description="MinIO object key")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type")
    extraction_status: str = Field(..., description="Extraction status")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic config."""

        from_attributes = True


class DocumentUploadRequest(BaseModel):
    """Document upload request (multipart form)."""

    document_type: str = Field(
        default="other",
        pattern="^(invoice|packing_list|bill_of_lading|airway_bill|commercial_invoice|certificate_of_origin|other)$",
    )
    file_name: str = Field(..., min_length=1, max_length=255)
    file_size: int = Field(..., ge=0)
    mime_type: str = Field(..., min_length=1, max_length=100)


class ExtractedFieldResponse(BaseModel):
    """Extracted field response model."""

    id: str = Field(..., description="Field ID")
    document_id: str = Field(..., description="Document ID")
    field_name: str = Field(..., description="Field name")
    field_value: str | None = Field(None, description="Field value")
    confidence: float = Field(..., description="Confidence score")
    source: str | None = Field(None, description="Extraction source")

    class Config:
        from_attributes = True

