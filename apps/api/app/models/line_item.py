"""
Line item model for shipment products.
Each line item represents a product in a shipment.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LineItem(Base):
    """
    Line item model representing a product in a shipment.
    
    Attributes:
        id: Unique line item ID
        shipment_id: FK to shipments.id
        description: Product description
        quantity: Quantity of items
        unit_price: Price per unit
        total_value: Total value (quantity * unit_price)
        hs_code_suggested: AI-suggested HS code
        confidence: Confidence score for HS code suggestion
        created_at: Timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "line_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    shipment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    hs_code_suggested: Mapped[str | None] = mapped_column(String(20), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<LineItem(shipment_id={self.shipment_id}, desc={self.description[:30]}..., hs={self.hs_code_suggested})>"
