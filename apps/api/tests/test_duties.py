"""
Unit and integration tests for South African Customs Duty & Import VAT Calculation.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, User, Membership, Shipment, LineItem, TariffRecord
from app.services.duty_service import calculate_shipment_duties


@pytest.mark.asyncio
async def test_south_african_duty_and_vat_calculation(async_session: AsyncSession):
    # Setup org & user
    org = Organization(name="Duty Org", slug="duty-org", plan="pro")
    async_session.add(org)
    await async_session.flush()

    user = User(email="dutyuser@test.com", password_hash="hash", full_name="Duty User")
    async_session.add(user)
    await async_session.flush()

    mem = Membership(organization_id=org.id, user_id=user.id, role="owner")
    async_session.add(mem)

    # Tariff with 45% Duty and 15% VAT (e.g. Cotton T-shirts)
    apparel_tariff = TariffRecord(
        hs_code="6109.10",
        sa_tariff_code="6109.10.10",
        description="Cotton T-shirts",
        duty_rate=45.0,
        vat_rate=15.0,
    )
    async_session.add(apparel_tariff)
    await async_session.flush()

    # Shipment with 1000 USD of t-shirts
    shipment = Shipment(
        organization_id=org.id,
        reference="DUTY-TEST-001",
        shipment_type="import",
        currency="USD",
    )
    async_session.add(shipment)
    await async_session.flush()

    item = LineItem(
        shipment_id=shipment.id,
        description="Cotton T-shirts",
        quantity=100,
        unit_price=10.0,
        total_value=1000.0,
        hs_code_suggested="6109.10",
    )
    async_session.add(item)
    await async_session.commit()

    # Calculate with fixed exchange rate USD/ZAR = 18.00
    res = await calculate_shipment_duties(
        session=async_session,
        org_id=org.id,
        shipment_id=shipment.id,
        exchange_rate=18.00,
        customs_markup_percent=10.0,
    )

    # Verification:
    # 1. Customs Value ZAR = 1,000 USD * 18.00 = 18,000.00 ZAR
    assert res.total_customs_value_zar == 18000.00

    # 2. Customs Duty (45%) = 18,000 * 0.45 = 8,100.00 ZAR
    assert res.total_customs_duty_zar == 8100.00

    # 3. SARS Added Tax Value (ATV) = (Customs Value * 1.10) + Customs Duty
    #    ATV = (18,000 * 1.10) + 8,100 = 19,800 + 8,100 = 27,900.00 ZAR
    assert res.total_atv_zar == 27900.00

    # 4. Import VAT (15%) = 27,900 * 0.15 = 4,185.00 ZAR
    assert res.total_import_vat_zar == 4185.00

    # 5. Total Payable to SARS = Customs Duty + Import VAT = 8,100 + 4,185 = 12,285.00 ZAR
    assert res.total_payable_to_sars_zar == 12285.00
