"""
Document model for tracking uploaded files and extraction status.
Documents are linked to shipments and stored in MinIO.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Document(Base):
    """
    Document model representing uploaded trade documents.
    
    Attributes:
        id: Unique document ID (UUID)
        shipment_id: FK to shipments.id
        document_type: invoice, packing_list, bill_of_lading, etc.
        file_key: MinIO object key for file storage
        file_name: Original filename
        file_size: File size in bytes
        mime_type: MIME type of file
        extraction_status: pending, processing, completed, failed
        created_at: Timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    shipment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="other",
    )
    file_key: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False, default=0)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False, default="application/octet-stream")
    extraction_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, type={self.document_type}, status={self.extraction_status})>"
