"""
Shipment model for tracking import/export/transit shipments.
Shipments are organization-scoped and linked to parties.
"""

from datetime import datetime, date
from uuid import uuid4

from sqlalchemy import DateTime, String, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Shipment(Base):
    """
    Shipment model representing a trade shipment.
    
    Attributes:
        id: Unique shipment ID (UUID)
        organization_id: FK to organizations.id (multi-tenant isolation)
        reference: Human-readable reference number
        shipment_type: import, export, or transit
        transport_mode: sea, air, road, rail
        status: draft, documents_received, extracting, needs_review, compliance_ready, approved, packet_generated, completed, rejected, archived
        risk_level: low, medium, high, critical
        origin_country: ISO 3166-1 alpha-2 country code
        destination_country: ISO 3166-1 alpha-2 country code
        port_of_loading: Port where goods loaded
        port_of_discharge: Port where goods discharged
        border_post: Border post for road/rail shipments
        incoterms: International commercial terms (FOB, CIF, EXW, etc.)
        currency: ISO 4217 currency code
        invoice_date: Commercial invoice date
        estimated_arrival_date: Expected arrival date
        importer_id: FK to parties.id (importer)
        exporter_id: FK to parties.id (exporter)
        supplier_id: FK to parties.id (supplier)
        consignee_id: FK to parties.id (consignee)
        notify_party_id: FK to parties.id (notify party)
        clearing_agent_id: FK to parties.id (clearing agent)
        created_by: FK to users.id (creator)
        created_at: Timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "shipments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reference: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    shipment_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="import",
    )
    transport_mode: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="draft",
    )
    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="low",
    )
    origin_country: Mapped[str | None] = mapped_column(String(2), nullable=True)
    destination_country: Mapped[str | None] = mapped_column(String(2), nullable=True)
    port_of_loading: Mapped[str | None] = mapped_column(String(100), nullable=True)
    port_of_discharge: Mapped[str | None] = mapped_column(String(100), nullable=True)
    border_post: Mapped[str | None] = mapped_column(String(100), nullable=True)
    incoterms: Mapped[str | None] = mapped_column(String(10), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    invoice_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    estimated_arrival_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    importer_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("parties.id", ondelete="SET NULL"), nullable=True
    )
    exporter_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("parties.id", ondelete="SET NULL"), nullable=True
    )
    supplier_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("parties.id", ondelete="SET NULL"), nullable=True
    )
    consignee_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("parties.id", ondelete="SET NULL"), nullable=True
    )
    notify_party_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("parties.id", ondelete="SET NULL"), nullable=True
    )
    clearing_agent_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("parties.id", ondelete="SET NULL"), nullable=True
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Shipment(id={self.id}, ref={self.reference}, type={self.shipment_type}, status={self.status})>"
