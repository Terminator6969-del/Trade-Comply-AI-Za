"""
Celery worker for document extraction.
Processes uploaded documents: OCR → LLM extraction → store results.
"""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.ai.extraction import extract_document_fields
from app.models import Document, ExtractedField, LineItem
from app.core.audit import log_action


async def process_document(document_id: str) -> dict[str, Any]:
    """
    Process a document: OCR → LLM extraction → store results.
    
    Args:
        document_id: ID of document to process
        
    Returns:
        Processing result with status and extracted fields count
    """
    async with AsyncSessionLocal() as session:
        # Get document
        result = await session.execute(select(Document).where(Document.id == document_id))
        document = result.scalar_one_or_none()

        if not document:
            return {"status": "error", "message": "Document not found"}

        # Update status to processing
        document.extraction_status = "processing"
        await session.commit()

        try:
            # Run extraction pipeline
            extracted_fields = await extract_document_fields(
                file_key=document.file_key,
                document_type=document.document_type,
            )

            # Store extracted fields
            for field_name, field_data in extracted_fields.items():
                extracted_field = ExtractedField(
                    document_id=document.id,
                    field_name=field_name,
                    field_value=field_data["value"],
                    confidence=field_data["confidence"],
                    verified=False,
                )
                session.add(extracted_field)

            # Extract line items if present
            if "line_items" in extracted_fields:
                line_items_data = extracted_fields["line_items"]["value"]
                for item_data in line_items_data:
                    line_item = LineItem(
                        shipment_id=document.shipment_id,
                        description=item_data["description"],
                        quantity=item_data["quantity"],
                        unit_price=item_data["unit_price"],
                        total_value=item_data["total_value"],
                    )
                    session.add(line_item)

            # Update document status
            document.extraction_status = "completed"
            await session.commit()

            # Log action
            await log_action(
                session=session,
                organization_id=document.shipment.organization_id if document.shipment else "unknown",
                user_id="system",
                action="document.extraction_completed",
                entity_type="document",
                entity_id=document.id,
                after_value={"fields_count": len(extracted_fields)},
            )

            return {
                "status": "completed",
                "document_id": document.id,
                "fields_count": len(extracted_fields),
                "line_items_count": len(extracted_fields.get("line_items", {}).get("value", [])),
            }

        except Exception as e:
            # Update status to failed
            document.extraction_status = "failed"
            await session.commit()

            # Log error
            await log_action(
                session=session,
                organization_id=document.shipment.organization_id if document.shipment else "unknown",
                user_id="system",
                action="document.extraction_failed",
                entity_type="document",
                entity_id=document.id,
                after_value={"error": str(e)},
            )

            return {
                "status": "failed",
                "document_id": document.id,
                "error": str(e),
            }
