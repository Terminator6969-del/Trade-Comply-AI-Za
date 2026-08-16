"""
Documents API routes for upload, retrieval, and management.
All endpoints are scoped to the authenticated organization.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    upload_document,
    get_document,
    list_documents,
    update_extraction_status,
    delete_document,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_new_document(
    shipment_id: str = Form(..., description="Shipment ID"),
    document_type: str = Form(default="other", description="Document type"),
    file: UploadFile = File(..., description="File to upload"),
    claims: Annotated[dict, Depends(get_current_user)] = None,
    session: Annotated[AsyncSession, Depends(get_async_session)] = None,
) -> DocumentResponse:
    """
    Upload a document for a shipment.
    
    Args:
        shipment_id: Shipment ID
        document_type: Document type (invoice, packing_list, etc.)
        file: File to upload (PDF, image, etc.)
        claims: Current user claims
        session: Database session
        
    Returns:
        Created document
        
    Raises:
        HTTPException: 400 if file validation fails, 404 if shipment not found
    """
    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    try:
        document = await upload_document(
            session=session,
            org_id=claims["org_id"],
            shipment_id=shipment_id,
            file_data=file_content,
            file_name=file.filename,
            content_type=file.content_type or "application/octet-stream",
            file_size=file_size,
            document_type=document_type,
            user_id=claims["user_id"],
        )
        return DocumentResponse.model_validate(document)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}",
        )


@router.get("/shipment/{shipment_id}", response_model=list[DocumentResponse])
async def list_shipment_documents(
    shipment_id: str,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[DocumentResponse]:
    """
    List documents for a shipment.
    
    Args:
        shipment_id: Shipment ID
        claims: Current user claims
        session: Database session
        
    Returns:
        List of documents
    """
    documents = await list_documents(session, claims["org_id"], shipment_id)
    return [DocumentResponse.model_validate(d) for d in documents]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_single_document(
    document_id: str,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> DocumentResponse:
    """
    Get a document by ID.
    
    Args:
        document_id: Document ID
        claims: Current user claims
        session: Database session
        
    Returns:
        Document details
        
    Raises:
        HTTPException: 404 if document not found
    """
    document = await get_document(session, claims["org_id"], document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return DocumentResponse.model_validate(document)


@router.patch("/{document_id}/status", response_model=DocumentResponse)
async def update_document_status(
    document_id: str,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    status: str = Form(..., description="New extraction status"),
) -> DocumentResponse:
    """
    Update document extraction status.
    
    Args:
        document_id: Document ID
        status: New status (pending, processing, completed, failed)
        claims: Current user claims
        session: Database session
        
    Returns:
        Updated document
        
    Raises:
        HTTPException: 404 if document not found
    """
    document = await update_extraction_status(session, claims["org_id"], document_id, status)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return DocumentResponse.model_validate(document)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_document(
    document_id: str,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    """
    Delete a document and its file.
    
    Args:
        document_id: Document ID
        claims: Current user claims
        session: Database session
        
    Raises:
        HTTPException: 404 if document not found
    """
    deleted = await delete_document(
        session, claims["org_id"], document_id, claims["user_id"]
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
