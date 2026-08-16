"""
Tariff record model for South African tariff codes.
Stores HS codes, SA tariff codes, duty rates, and vector embeddings.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON

from app.core.database import Base


class TariffRecord(Base):
    """
    Tariff record model for South African tariff codes.
    
    Attributes:
        id: Unique record ID
        hs_code: Harmonized System code (e.g., "8541.40")
        sa_tariff_code: South African specific tariff code
        description: Product description
        duty_rate: Customs duty rate (percentage)
        vat_rate: VAT rate (percentage, typically 15% in SA)
        unit_of_measure: Unit of measure (kg, set, etc.)
        country_of_origin: Applicable countries (JSON list)
        chapter: HS chapter number
        section: HS section number
        embedding: Vector embedding for similarity search (1536 dimensions)
        created_at: Timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "tariff_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    hs_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    sa_tariff_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    duty_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    vat_rate: Mapped[float] = mapped_column(Float, nullable=False, default=15.0)
    unit_of_measure: Mapped[str | None] = mapped_column(String(50), nullable=True)
    country_of_origin: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    chapter: Mapped[str | None] = mapped_column(String(10), nullable=True, index=True)
    section: Mapped[str | None] = mapped_column(String(10), nullable=True)
    embedding: Mapped[list[float] | None] = mapped_column(
        # VECTOR(1536) type for pgvector
        # Using JSON for compatibility, will be converted to VECTOR in migration
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<TariffRecord(hs_code={self.hs_code}, sa_code={self.sa_tariff_code})>"
