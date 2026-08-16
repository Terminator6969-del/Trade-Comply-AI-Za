"""
Unit and integration tests for SAD500 Customs Packet Generation.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, User, Membership, Party, Shipment, LineItem, Document, TariffRecord
from app.services.packet_service import generate_customs_packet


@pytest.mark.asyncio
async def test_generate_sad500_packet(async_session: AsyncSession):
    org = Organization(name="Packet Org", slug="packet-org", plan="pro")
    async_session.add(org)
    await async_session.flush()

    user = User(email="packuser@test.com", password_hash="hash", full_name="Packet User")
    async_session.add(user)
    await async_session.flush()

    mem = Membership(organization_id=org.id, user_id=user.id, role="owner")
    async_session.add(mem)

    importer = Party(
        organization_id=org.id,
        party_type="importer",
        name="RSA Green Logistics",
        customs_code="CCN88899",
        vat_number="4110022334",
    )
    async_session.add(importer)
    await async_session.flush()

    solar_tariff = TariffRecord(
        hs_code="8541.40",
        sa_tariff_code="8541.40.10",
        description="Solar PV Panels",
        duty_rate=0.0,
        vat_rate=15.0,
    )
    async_session.add(solar_tariff)
    await async_session.flush()

    shipment = Shipment(
        organization_id=org.id,
        reference="SAD500-2026-TEST",
        shipment_type="import",
        port_of_discharge="Durban",
        incoterms="CIF",
        currency="USD",
        importer_id=importer.id,
    )
    async_session.add(shipment)
    await async_session.flush()

    doc = Document(
        shipment_id=shipment.id,
        document_type="commercial_invoice",
        file_name="inv.pdf",
        file_key="inv-key-pack-001",
    )
    item = LineItem(
        shipment_id=shipment.id,
        description="400W Solar PV Module",
        quantity=50,
        unit_price=100.0,
        total_value=5000.0,
        hs_code_suggested="8541.40",
    )
    async_session.add_all([doc, item])
    await async_session.commit()

    # Generate CSV packet
    csv_packet = await generate_customs_packet(
        session=async_session,
        org_id=org.id,
        shipment_id=shipment.id,
        output_format="csv",
        user_id=user.id,
    )

    assert csv_packet.shipment_id == str(shipment.id)
    assert csv_packet.reference == "SAD500-2026-TEST"
    assert "ItemNo,Description,HSCode" in csv_packet.raw_content
    assert "400W Solar PV Module" in csv_packet.raw_content
    assert csv_packet.sad500_header.importer_customs_code == "CCN88899"
    assert csv_packet.duty_estimate.total_payable_to_sars_zar > 0

    # Generate Summary packet
    summary_packet = await generate_customs_packet(
        session=async_session,
        org_id=org.id,
        shipment_id=shipment.id,
        output_format="summary",
        user_id=user.id,
    )
    assert "=== SARS SAD500 CUSTOMS DECLARATION PACKET ===" in summary_packet.raw_content
    assert "RSA Green Logistics" in summary_packet.raw_content
