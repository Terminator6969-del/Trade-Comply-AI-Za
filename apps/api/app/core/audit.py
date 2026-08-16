"""
Audit logging utilities for tracking all mutations.
All create/update/delete operations must be logged via log_action.
"""

import json
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

# Import models at function level to avoid circular imports


async def log_action(
    session: AsyncSession,
    organization_id: str,
    user_id: str,
    action: str,
    entity_type: str,
    entity_id: str,
    before_value: dict[str, Any] | None = None,
    after_value: dict[str, Any] | None = None,
    ip_address: str | None = None,
) -> None:
    """
    Log an action for audit trail.
    
    Args:
        session: Database session
        organization_id: Organization performing the action
        user_id: User performing the action
        action: Action type (e.g., "created", "updated", "deleted")
        entity_type: Entity being modified (e.g., "shipment", "document")
        entity_id: ID of entity being modified
        before_value: State before modification
        after_value: State after modification
        ip_address: User's IP address (optional)
    """
    # Import here to avoid circular imports
    from app.models.audit_log import AuditLog

    audit_log = AuditLog(
        organization_id=organization_id,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        before_value=before_value,
        after_value=after_value,
        ip_address=ip_address,
    )

    session.add(audit_log)
    # Don't commit - let caller decide when to commit
