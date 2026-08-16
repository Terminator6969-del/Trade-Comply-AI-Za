"""
Audit log model for immutable action tracking.
Every mutation must be logged here for compliance and debugging.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, String, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AuditLog(Base):
    """
    Immutable audit log of all mutations in the system.
    
    Attributes:
        id: Unique log entry ID
        organization_id: FK to organizations.id
        user_id: FK to users.id
        action: Action type (created, updated, deleted, etc.)
        entity_type: Type of entity modified (shipment, document, etc.)
        entity_id: ID of the entity modified
        before_value: JSON snapshot of entity before change
        after_value: JSON snapshot of entity after change
        ip_address: IP address of user making the change
        created_at: Immutable timestamp of action
    """

    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    before_value: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    after_value: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)  # IPv4 or IPv6
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<AuditLog(org_id={self.organization_id}, action={self.action}, "
            f"entity_type={self.entity_type}, entity_id={self.entity_id})>"
        )
