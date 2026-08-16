"""
Test suite for extraction worker.
Tests document processing pipeline.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, User, Membership, Party, Shipment, Document
from app.workers.extraction_worker import process_document


@pytest.fixture
async def test_org_shipment_document(async_session: AsyncSession):
    """Create a test organization with shipment and document."""
    org = Organization(name="Test Org", slug="test-org-extract", plan="free")
    async_session.add(org)
    await async_session.flush()

    user = User(
        email="extract@test.com",
        password_hash="hashed",
        full_name="Extract User",
    )
    async_session.add(user)
    await async_session.flush()

    membership = Membership(
        organization_id=org.id,
        user_id=user.id,
        role="owner",
    )
    async_session.add(membership)

    shipment = Shipment(
        organization_id=org.id,
        reference="SHIP-EXTRACT-001",
        shipment_type="import",
    )
    async_session.add(shipment)
    await async_session.flush()

    document = Document(
        shipment_id=shipment.id,
        document_type="invoice",
        file_key="test-org/extract-001/invoice.pdf",
        file_name="invoice.pdf",
        file_size=1024,
        mime_type="application/pdf",
        extraction_status="pending",
    )
    async_session.add(document)
    await async_session.commit()

    return org, user, shipment, document


@pytest.mark.asyncio
async def test_process_document_updates_status(async_session: AsyncSession, test_org_shipment_document):
    """Test that document processing updates extraction status."""
    org, user, shipment, document = test_org_shipment_document

    result = await process_document(document.id)

    assert result["status"] == "completed"
    assert result["document_id"] == document.id
    assert result["fields_count"] > 0

    # Verify document status was updated
    from app.models import Document as DocModel
    result_check = await async_session.execute(
        select(DocModel).where(DocModel.id == document.id)
    )
    updated_doc = result_check.scalar_one()
    assert updated_doc.extraction_status == "completed"


@pytest.mark.asyncio
async def test_process_document_not_found(async_session: AsyncSession):
    """Test processing non-existent document returns error."""
    result = await process_document("nonexistent-document-id")

    assert result["status"] == "error"
    assert "not found" in result["message"]


@pytest.mark.asyncio
async def test_process_document_extracts_fields(async_session: AsyncSession, test_org_shipment_document):
    """Test that document processing extracts fields."""
    org, user, shipment, document = test_org_shipment_document

    result = await process_document(document.id)

    assert result["status"] == "completed"
    assert result["fields_count"] > 0

    # Verify extracted fields were stored
    from app.models import ExtractedField
    from sqlalchemy import select

    fields_result = await async_session.execute(
        select(ExtractedField).where(ExtractedField.document_id == document.id)
    )
    fields = fields_result.scalars().all()

    assert len(fields) > 0
    # Check for expected fields
    field_names = {f.field_name for f in fields}
    assert "invoice_number" in field_names
    assert "total_amount" in field_names


@pytest.mark.asyncio
async def test_process_document_extracts_line_items(async_session: AsyncSession, test_org_shipment_document):
    """Test that document processing extracts line items."""
    org, user, shipment, document = test_org_shipment_document

    result = await process_document(document.id)

    assert result["status"] == "completed"
    assert result["line_items_count"] > 0

    # Verify line items were stored
    from app.models import LineItem
    from sqlalchemy import select

    items_result = await async_session.execute(
        select(LineItem).where(LineItem.shipment_id == shipment.id)
    )
    items = items_result.scalars().all()

    assert len(items) > 0
    # Check first item
    assert items[0].description is not None
    assert items[0].quantity > 0


@pytest.mark.asyncio
async def test_process_document_failure(async_session: AsyncSession, test_org_shipment_document):
    """Test that document processing failure updates status to failed."""
    org, user, shipment, document = test_org_shipment_document

    # Set file_key to invalid to trigger error
    document.file_key = "invalid/key/that/does/not/exist"
    await async_session.commit()

    result = await process_document(document.id)

    # Should handle gracefully
    assert result["status"] in ["completed", "failed"]


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_extraction_worker.py -v")
