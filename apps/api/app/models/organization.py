"""
Organization model for multi-tenant support.
Each organization is a separate SaaS customer.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Organization(Base):
    """
    Organization (SaaS tenant) model.
    
    Attributes:
        id: Unique organization ID (UUID)
        name: Human-readable organization name
        slug: URL-friendly slug (unique)
        plan: Subscription plan (free, pro, enterprise)
        created_at: Timestamp when created
        updated_at: Last update timestamp
    """

    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    plan: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="free",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, name={self.name}, plan={self.plan})>"
