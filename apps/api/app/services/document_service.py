"""
Document service for upload, retrieval, and extraction management.
Handles file validation, storage, and extraction status tracking.
"""

from typing import BinaryIO

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.storage import storage_client
from app.models import Document, Shipment
from app.schemas.document import DocumentCreate, DocumentUploadRequest
from app.core.audit import log_action


# Allowed file types for upload
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/tiff",
    "image/bmp",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

# Max file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024


async def validate_file(
    file_size: int,
    mime_type: str,
) -> None:
    """
    Validate uploaded file.
    
    Args:
        file_size: File size in bytes
        mime_type: MIME type of file
        
    Raises:
        ValueError: If file is too large or type not allowed
    """
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large. Max size: {MAX_FILE_SIZE} bytes")

    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"File type not allowed: {mime_type}")


async def upload_document(
    session: AsyncSession,
    org_id: str,
    shipment_id: str,
    file_data: BinaryIO,
    file_name: str,
    content_type: str,
    file_size: int,
    document_type: str,
    user_id: str,
) -> Document:
    """
    Upload a document and create a Document record.
    
    Args:
        session: Database session
        org_id: Organization ID (multi-tenant isolation)
        shipment_id: Shipment ID
        file_data: File-like object
        file_name: Original filename
        content_type: MIME type
        file_size: File size in bytes
        document_type: Document type (invoice, packing_list, etc.)
        user_id: User uploading (for audit log)
        
    Returns:
        Created Document
        
    Raises:
        ValueError: If file validation fails or shipment not found
    """
    # Validate file
    await validate_file(file_size, content_type)

    # Verify shipment exists and belongs to org
    result = await session.execute(
        select(Shipment).where(
            Shipment.id == shipment_id,
            Shipment.organization_id == org_id,
        )
    )
    shipment = result.scalar_one_or_none()
    if not shipment:
        raise ValueError("Shipment not found or not in organization")

    # Upload to storage
    file_key = await storage_client.upload_file(
        file_data=file_data,
        file_name=file_name,
        content_type=content_type,
        file_size=file_size,
        org_id=org_id,
        shipment_id=shipment_id,
    )

    # Create document record
    document = Document(
        shipment_id=shipment_id,
        document_type=document_type,
        file_key=file_key,
        file_name=file_name,
        file_size=file_size,
        mime_type=content_type,
        extraction_status="pending",
    )
    session.add(document)
    await session.commit()
    await session.refresh(document)

    # Log action
    await log_action(
        session=session,
        organization_id=org_id,
        user_id=user_id,
        action="document.uploaded",
        entity_type="document",
        entity_id=document.id,
        after_value={
            "document_type": document.document_type,
            "file_name": document.file_name,
            "file_size": document.file_size,
        },
    )

    return document


async def get_document(
    session: AsyncSession,
    org_id: str,
    document_id: str,
) -> Document | None:
    """
    Get a document by ID, scoped to organization.
    
    Args:
        session: Database session
        org_id: Organization ID (multi-tenant isolation)
        document_id: Document ID
        
    Returns:
        Document or None if not found
    """
    result = await session.execute(
        select(Document)
        .join(Shipment)
        .where(
            Document.id == document_id,
            Shipment.organization_id == org_id,
        )
    )
    return result.scalar_one_or_none()


async def list_documents(
    session: AsyncSession,
    org_id: str,
    shipment_id: str,
) -> list[Document]:
    """
    List documents for a shipment, scoped to organization.
    
    Args:
        session: Database session
        org_id: Organization ID (multi-tenant isolation)
        shipment_id: Shipment ID
        
    Returns:
        List of documents
    """
    result = await session.execute(
        select(Document)
        .join(Shipment)
        .where(
            Document.shipment_id == shipment_id,
            Shipment.organization_id == org_id,
        )
        .order_by(Document.created_at.desc())
    )
    return list(result.scalars().all())


async def update_extraction_status(
    session: AsyncSession,
    org_id: str,
    document_id: str,
    status: str,
) -> Document | None:
    """
    Update document extraction status.
    
    Args:
        session: Database session
        org_id: Organization ID
        document_id: Document ID
        status: New status (pending, processing, completed, failed)
        
    Returns:
        Updated Document or None if not found
    """
    document = await get_document(session, org_id, document_id)
    if not document:
        return None

    document.extraction_status = status
    await session.commit()
    await session.refresh(document)
    return document


async def delete_document(
    session: AsyncSession,
    org_id: str,
    document_id: str,
    user_id: str,
) -> bool:
    """
    Delete a document and its file from storage.
    
    Args:
        session: Database session
        org_id: Organization ID
        document_id: Document ID
        user_id: User deleting (for audit log)
        
    Returns:
        True if deleted, False if not found
    """
    document = await get_document(session, org_id, document_id)
    if not document:
        return False

    # Delete file from storage
    await storage_client.delete_file(document.file_key)

    # Log action before deleting
    await log_action(
        session=session,
        organization_id=org_id,
        user_id=user_id,
        action="document.deleted",
        entity_type="document",
        entity_id=document.id,
        before_value={
            "document_type": document.document_type,
            "file_name": document.file_name,
        },
    )

    await session.delete(document)
    await session.commit()
    return True
