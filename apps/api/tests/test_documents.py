"""
Test suite for document management.
Tests upload, retrieval, and multi-tenant isolation.
"""

import pytest
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, User, Membership, Party, Shipment, Document
from app.schemas.document import DocumentCreate
from app.services.document_service import (
    upload_document,
    get_document,
    list_documents,
    update_extraction_status,
    delete_document,
    validate_file,
    MAX_FILE_SIZE,
)


@pytest.fixture
async def test_org_shipment(async_session: AsyncSession):
    """Create a test organization with a shipment."""
    org = Organization(name="Test Org", slug="test-org-docs", plan="free")
    async_session.add(org)
    await async_session.flush()

    user = User(
        email="docowner@test.com",
        password_hash="hashed",
        full_name="Doc Owner",
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
        reference="SHIP-DOC-001",
        shipment_type="import",
    )
    async_session.add(shipment)
    await async_session.commit()

    return org, user, shipment


@pytest.mark.asyncio
async def test_validate_file_valid():
    """Test file validation with valid file."""
    await validate_file(1024, "application/pdf")
    # Should not raise


@pytest.mark.asyncio
async def test_validate_file_too_large():
    """Test file validation rejects large files."""
    with pytest.raises(ValueError, match="too large"):
        await validate_file(MAX_FILE_SIZE + 1, "application/pdf")


@pytest.mark.asyncio
async def test_validate_file_invalid_type():
    """Test file validation rejects invalid MIME types."""
    with pytest.raises(ValueError, match="not allowed"):
        await validate_file(1024, "application/x-executable")


@pytest.mark.asyncio
async def test_upload_document(async_session: AsyncSession, test_org_shipment):
    """Test uploading a document."""
    org, user, shipment = test_org_shipment

    file_content = b"%PDF-1.4 fake pdf content"
    file_data = BytesIO(file_content)

    document = await upload_document(
        session=async_session,
        org_id=org.id,
        shipment_id=shipment.id,
        file_data=file_data,
        file_name="invoice.pdf",
        content_type="application/pdf",
        file_size=len(file_content),
        document_type="invoice",
        user_id=user.id,
    )

    assert document.id is not None
    assert document.shipment_id == shipment.id
    assert document.document_type == "invoice"
    assert document.file_name == "invoice.pdf"
    assert document.file_size == len(file_content)
    assert document.mime_type == "application/pdf"
    assert document.extraction_status == "pending"
    assert document.file_key is not None


@pytest.mark.asyncio
async def test_upload_document_invalid_shipment(async_session: AsyncSession, test_org_shipment):
    """Test uploading document to non-existent shipment fails."""
    org, user, _ = test_org_shipment

    file_content = b"test content"
    file_data = BytesIO(file_content)

    with pytest.raises(ValueError, match="Shipment not found"):
        await upload_document(
            session=async_session,
            org_id=org.id,
            shipment_id="nonexistent-shipment",
            file_data=file_data,
            file_name="test.pdf",
            content_type="application/pdf",
            file_size=len(file_content),
            document_type="invoice",
            user_id=user.id,
        )


@pytest.mark.asyncio
async def test_upload_document_invalid_file_type(async_session: AsyncSession, test_org_shipment):
    """Test uploading invalid file type fails."""
    org, user, shipment = test_org_shipment

    file_content = b"test content"
    file_data = BytesIO(file_content)

    with pytest.raises(ValueError, match="not allowed"):
        await upload_document(
            session=async_session,
            org_id=org.id,
            shipment_id=shipment.id,
            file_data=file_data,
            file_name="test.exe",
            content_type="application/x-executable",
            file_size=len(file_content),
            document_type="invoice",
            user_id=user.id,
        )


@pytest.mark.asyncio
async def test_get_document(async_session: AsyncSession, test_org_shipment):
    """Test retrieving a document."""
    org, user, shipment = test_org_shipment

    file_content = b"test content"
    file_data = BytesIO(file_content)

    document = await upload_document(
        session=async_session,
        org_id=org.id,
        shipment_id=shipment.id,
        file_data=file_data,
        file_name="test.pdf",
        content_type="application/pdf",
        file_size=len(file_content),
        document_type="invoice",
        user_id=user.id,
    )

    retrieved = await get_document(async_session, org.id, document.id)
    assert retrieved is not None
    assert retrieved.file_name == "test.pdf"


@pytest.mark.asyncio
async def test_get_document_not_found(async_session: AsyncSession, test_org_shipment):
    """Test retrieving non-existent document returns None."""
    org, _, _ = test_org_shipment

    result = await get_document(async_session, org.id, "nonexistent-id")
    assert result is None


@pytest.mark.asyncio
async def test_list_documents(async_session: AsyncSession, test_org_shipment):
    """Test listing documents for a shipment."""
    org, user, shipment = test_org_shipment

    # Upload multiple documents
    for i in range(3):
        file_data = BytesIO(f"content {i}".encode())
        await upload_document(
            session=async_session,
            org_id=org.id,
            shipment_id=shipment.id,
            file_data=file_data,
            file_name=f"doc_{i}.pdf",
            content_type="application/pdf",
            file_size=100,
            document_type="invoice",
            user_id=user.id,
        )

    documents = await list_documents(async_session, org.id, shipment.id)
    assert len(documents) == 3


@pytest.mark.asyncio
async def test_update_extraction_status(async_session: AsyncSession, test_org_shipment):
    """Test updating document extraction status."""
    org, user, shipment = test_org_shipment

    file_data = BytesIO(b"test content")
    document = await upload_document(
        session=async_session,
        org_id=org.id,
        shipment_id=shipment.id,
        file_data=file_data,
        file_name="test.pdf",
        content_type="application/pdf",
        file_size=100,
        document_type="invoice",
        user_id=user.id,
    )

    updated = await update_extraction_status(async_session, org.id, document.id, "completed")
    assert updated is not None
    assert updated.extraction_status == "completed"


@pytest.mark.asyncio
async def test_document_multi_tenant_isolation(async_session: AsyncSession):
    """Test that documents are isolated between organizations."""
    # Create two orgs with shipments
    org1 = Organization(name="Org 1", slug="org-1-docs", plan="free")
    org2 = Organization(name="Org 2", slug="org-2-docs", plan="free")
    async_session.add_all([org1, org2])
    await async_session.flush()

    shipment1 = Shipment(organization_id=org1.id, reference="SHIP-1", shipment_type="import")
    shipment2 = Shipment(organization_id=org2.id, reference="SHIP-2", shipment_type="import")
    async_session.add_all([shipment1, shipment2])
    await async_session.commit()

    # Upload document to org1's shipment
    file_data = BytesIO(b"test content")
    document = await upload_document(
        session=async_session,
        org_id=org1.id,
        shipment_id=shipment1.id,
        file_data=file_data,
        file_name="test.pdf",
        content_type="application/pdf",
        file_size=100,
        document_type="invoice",
        user_id="test-user-id",
    )

    # Try to get document from org2 (should not find it)
    result = await get_document(async_session, org2.id, document.id)
    assert result is None

    # List documents for org2's shipment (should be empty)
    docs = await list_documents(async_session, org2.id, shipment2.id)
    assert len(docs) == 0


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_documents.py -v")
