"""
Extracted field model for storing LLM-extracted data.
Each field has a confidence score and verification status.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON

from app.core.database import Base


class ExtractedField(Base):
    """
    Extracted field model for storing AI-extracted data from documents.
    
    Attributes:
        id: Unique field ID
        document_id: FK to documents.id
        field_name: Name of extracted field (e.g., "invoice_number")
        field_value: Extracted value (JSON for complex types)
        confidence: Confidence score (0.0 - 1.0)
        verified: Whether a human has verified this field
        created_at: Timestamp
    """

    __tablename__ = "extracted_fields"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    document_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    field_value: Mapped[Any] = mapped_column(JSON, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ExtractedField(doc_id={self.document_id}, field={self.field_name}, conf={self.confidence})>"
