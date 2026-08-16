"""
Membership model for multi-tenancy and RBAC.
Links users to organizations with role-based permissions.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Membership(Base):
    """
    Membership model linking Users to Organizations with roles.
    
    Attributes:
        id: Unique membership ID
        organization_id: FK to organizations.id
        user_id: FK to users.id
        role: Permission level (owner, admin, compliance_manager, clerk, viewer, api_service)
        created_at: When membership was created
    
    Roles:
        - owner: Full control, can delete org, manage users
        - admin: Can manage users, view all data
        - compliance_manager: Can review/approve shipments
        - clerk: Can create/edit shipments
        - viewer: Read-only access
        - api_service: Service account for API integration
    """

    __tablename__ = "memberships"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="viewer",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Membership(org_id={self.organization_id}, user_id={self.user_id}, role={self.role})>"
