"""
Unit and integration tests for TradeComply South African Compliance Rule Engine.
"""

import pytest
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, User, Membership, Party, Shipment, LineItem, Document, TariffRecord
from app.services.compliance_service import evaluate_shipment_compliance
from app.rules.base import ComplianceSeverity
from app.rules.engine import compliance_engine


@pytest.fixture
async def compliance_test_data(async_session: AsyncSession):
    org = Organization(name="Compliance Test Org", slug="comp-test-org", plan="pro")
    async_session.add(org)
    await async_session.flush()

    user = User(email="compuser@test.com", password_hash="hash", full_name="Comp User")
    async_session.add(user)
    await async_session.flush()

    mem = Membership(organization_id=org.id, user_id=user.id, role="owner")
    async_session.add(mem)

    importer = Party(
        organization_id=org.id,
        party_type="importer",
        name="SA Clean Solar Ltd",
        customs_code="CCN12345",
        vat_number="4990123456",
        country="ZA",
    )
    supplier = Party(
        organization_id=org.id,
        party_type="supplier",
        name="Guangdong Solar Factory",
        country="CN",
    )
    async_session.add_all([importer, supplier])
    await async_session.flush()

    # Add Solar tariff & Battery tariff
    solar_tariff = TariffRecord(
        hs_code="8541.40",
        sa_tariff_code="8541.40.10",
        description="Solar PV Panels",
        duty_rate=0.0,
        vat_rate=15.0,
    )
    battery_tariff = TariffRecord(
        hs_code="8507.60",
        sa_tariff_code="8507.60.10",
        description="Lithium-ion Batteries",
        duty_rate=5.0,
        vat_rate=15.0,
    )
    async_session.add_all([solar_tariff, battery_tariff])
    await async_session.commit()

    return org, user, importer, supplier


@pytest.mark.asyncio
async def test_missing_invoice_detected(async_session: AsyncSession, compliance_test_data):
    org, user, importer, supplier = compliance_test_data

    # Create shipment with no documents
    shipment = Shipment(
        organization_id=org.id,
        reference="TC-COMP-001",
        shipment_type="import",
        incoterms="CIF",
        currency="USD",
        importer_id=importer.id,
        supplier_id=supplier.id,
    )
    async_session.add(shipment)
    await async_session.commit()

    report = await evaluate_shipment_compliance(async_session, org.id, shipment.id)

    # Missing invoice rule must fail with critical severity
    inv_check = next(c for c in report.checks if c.rule_code == "SARS-DOC-001")
    assert inv_check.passed is False
    assert report.is_compliant is False
    assert report.risk_level == "critical"


@pytest.mark.asyncio
async def test_dangerous_goods_lithium_battery_flagged(async_session: AsyncSession, compliance_test_data):
    org, user, importer, supplier = compliance_test_data

    shipment = Shipment(
        organization_id=org.id,
        reference="TC-COMP-002",
        shipment_type="import",
        incoterms="CIF",
        currency="USD",
        importer_id=importer.id,
        supplier_id=supplier.id,
    )
    async_session.add(shipment)
    await async_session.flush()

    # Add invoice doc
    doc = Document(
        shipment_id=shipment.id,
        document_type="commercial_invoice",
        file_name="invoice.pdf",
        file_key="inv-key-002",
    )
    # Add lithium battery line item
    item = LineItem(
        shipment_id=shipment.id,
        description="Lithium-ion 48V energy storage batteries",
        quantity=10,
        unit_price=500.0,
        total_value=5000.0,
        hs_code_suggested="8507.60",
    )
    async_session.add_all([doc, item])
    await async_session.commit()

    report = await evaluate_shipment_compliance(async_session, org.id, shipment.id)

    # DG rule should trigger
    dg_check = next(c for c in report.checks if c.rule_code == "DG-LITH-001")
    assert dg_check.passed is False
    assert dg_check.severity == ComplianceSeverity.CRITICAL or dg_check.severity.value == "critical"
    assert "UN 3480" in dg_check.message


@pytest.mark.asyncio
async def test_itac_steel_permit_flagged(async_session: AsyncSession, compliance_test_data):
    org, user, importer, supplier = compliance_test_data

    shipment = Shipment(
        organization_id=org.id,
        reference="TC-COMP-003",
        shipment_type="import",
        incoterms="FOB",
        currency="USD",
        importer_id=importer.id,
        supplier_id=supplier.id,
    )
    async_session.add(shipment)
    await async_session.flush()

    doc = Document(
        shipment_id=shipment.id,
        document_type="invoice",
        file_name="steel_invoice.pdf",
        file_key="steel-inv-003",
    )
    item = LineItem(
        shipment_id=shipment.id,
        description="Deformed steel rebar 12mm",
        quantity=100,
        unit_price=20.0,
        total_value=2000.0,
        hs_code_suggested="7213.10",
    )
    async_session.add_all([doc, item])
    await async_session.commit()

    report = await evaluate_shipment_compliance(async_session, org.id, shipment.id)

    steel_check = next(c for c in report.checks if c.rule_code == "ITAC-STL-001")
    assert steel_check.passed is False
    assert "ITAC Import Permit" in steel_check.recommended_action
