"""
Party model for trade parties (importers, exporters, suppliers, consignees, clearing agents).
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Party(Base):
    """
    Trade party model for all entities involved in shipments.
    
    Party types:
        - importer: South African company importing goods
        - exporter: Foreign company exporting to South Africa
        - supplier: Company supplying goods (may differ from exporter)
        - consignee: Party receiving goods in South Africa
        - clearing_agent: Customs broker handling clearance
        - transporter: Trucking/shipping company
        - notify_party: Party to notify on arrival
    """

    __tablename__ = "parties"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    party_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # importer, exporter, supplier, consignee, clearing_agent, transporter, notify_party
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    vat_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    customs_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address_line1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    country: Mapped[str | None] = mapped_column(String(2), nullable=True)  # ISO 3166-1 alpha-2
    contact_person: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Party(id={self.id}, name={self.name}, type={self.party_type})>"
