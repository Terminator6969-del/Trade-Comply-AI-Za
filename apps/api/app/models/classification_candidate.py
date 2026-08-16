"""
Classification candidate model for HS code suggestions.
Stores AI-generated classification results with confidence scores.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON

from app.core.database import Base


class ClassificationCandidate(Base):
    """
    Classification candidate model for HS code suggestions.
    
    Attributes:
        id: Unique candidate ID
        line_item_id: FK to line_items.id
        hs_code: Suggested HS code
        sa_tariff_code: Suggested SA tariff code
        confidence: Confidence score (0.0 - 1.0)
        reasoning: AI explanation for the suggestion
        permit_flags: List of permit requirements (JSON)
        duty_rate: Duty rate for this HS code
        vat_rate: VAT rate for this HS code
        created_at: Timestamp
    """

    __tablename__ = "classification_candidates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    line_item_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("line_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    hs_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    sa_tariff_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    permit_flags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    duty_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    vat_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ClassificationCandidate(line_item_id={self.line_item_id}, hs_code={self.hs_code}, conf={self.confidence})>"
