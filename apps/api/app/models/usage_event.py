"""
Usage event model for tracking API usage and analytics.
Used for monitoring, billing, and feature adoption.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UsageEvent(Base):
    """
    API usage tracking for monitoring and analytics.
    
    Attributes:
        id: Unique event ID
        organization_id: FK to organizations.id
        event_type: Type of event (document_uploaded, classification_run, etc.)
        shipment_id: FK to shipments.id (optional)
        metadata: Additional event data (JSON)
        created_at: When event occurred
    """

    __tablename__ = "usage_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    shipment_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    event_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<UsageEvent(org_id={self.organization_id}, event_type={self.event_type}, "
            f"shipment_id={self.shipment_id})>"
        )
