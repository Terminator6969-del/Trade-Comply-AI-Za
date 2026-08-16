"""
User model for authentication and authorization.
Users belong to organizations via Membership.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """
    User account model.
    
    Attributes:
        id: Unique user ID (UUID)
        email: Email address (unique)
        password_hash: Argon2 hashed password (never plain text)
        full_name: User's full name
        is_active: Whether user account is active
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name})>"
