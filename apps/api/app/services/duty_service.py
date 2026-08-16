"""
South African Customs Duty and Import VAT Calculation Service.
Implements the SARS statutory Added Tax Value (ATV) formula under the VAT Act and Customs & Excise Schedule 1.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Shipment, LineItem, TariffRecord
from app.schemas.duty import DutyEstimateResponse, LineItemDutyBreakdown

DEFAULT_INDICATIVE_RATES = {
    "USD": 18.50,
    "EUR": 20.20,
    "GBP": 23.50,
    "CNY": 2.55,
    "JPY": 0.12,
    "AUD": 12.10,
    "INR": 0.22,
    "ZAR": 1.00,
}


async def calculate_shipment_duties(
    session: AsyncSession,
    org_id: str,
    shipment_id: str,
    exchange_rate: float | None = None,
    customs_markup_percent: float = 10.0,
) -> DutyEstimateResponse:
    """
    Calculate itemised and total South African customs duty & import VAT.
    """
    # 1. Fetch shipment (tenant isolated)
    result = await session.execute(
        select(Shipment).where(
            Shipment.id == shipment_id,
            Shipment.organization_id == org_id,
        )
    )
    shipment = result.scalar_one_or_none()
    if not shipment:
        raise ValueError(f"Shipment {shipment_id} not found in organization")

    # 2. Fetch line items
    result = await session.execute(
        select(LineItem).where(LineItem.shipment_id == shipment_id)
    )
    line_items = list(result.scalars().all())

    # 3. Determine exchange rate
    currency = (shipment.currency or "USD").upper()
    if exchange_rate is not None and exchange_rate > 0:
        rate = float(exchange_rate)
    else:
        rate = DEFAULT_INDICATIVE_RATES.get(currency, 18.50)

    # 4. Fetch tariff records for all line items
    hs_codes = set()
    for item in line_items:
        if item.hs_code_suggested:
            hs_codes.add(item.hs_code_suggested)

    tariff_map: dict[str, TariffRecord] = {}
    if hs_codes:
        result = await session.execute(
            select(TariffRecord).where(TariffRecord.hs_code.in_(list(hs_codes)))
        )
        for t in result.scalars().all():
            tariff_map[t.hs_code] = t

    # 5. Calculate per line item
    breakdowns: list[LineItemDutyBreakdown] = []
    total_customs_value_foreign = 0.0
    total_customs_value_zar = 0.0
    total_customs_duty_zar = 0.0
    total_atv_zar = 0.0
    total_import_vat_zar = 0.0

    for item in line_items:
        hs_code = item.hs_code_suggested
        tariff = tariff_map.get(hs_code) if hs_code else None

        duty_rate = getattr(tariff, "duty_rate", 0.0) if tariff else 0.0
        vat_rate = getattr(tariff, "vat_rate", 15.0) if tariff else 15.0

        foreign_val = float(item.total_value or (item.quantity * item.unit_price) or 0.0)
        customs_val_zar = round(foreign_val * rate, 2)
        duty_amt_zar = round(customs_val_zar * (duty_rate / 100.0), 2)

        # SARS ATV Formula: (Customs Value * 1.10) + Customs Duty
        markup_factor = 1.0 + (customs_markup_percent / 100.0)
        atv_zar = round((customs_val_zar * markup_factor) + duty_amt_zar, 2)
        vat_amt_zar = round(atv_zar * (vat_rate / 100.0), 2)
        total_tax_item = round(duty_amt_zar + vat_amt_zar, 2)

        total_customs_value_foreign += foreign_val
        total_customs_value_zar += customs_val_zar
        total_customs_duty_zar += duty_amt_zar
        total_atv_zar += atv_zar
        total_import_vat_zar += vat_amt_zar

        breakdowns.append(
            LineItemDutyBreakdown(
                line_item_id=str(item.id),
                description=item.description,
                hs_code=hs_code,
                quantity=float(item.quantity),
                currency=currency,
                foreign_total_value=foreign_val,
                customs_value_zar=customs_val_zar,
                duty_rate_percent=duty_rate,
                duty_amount_zar=duty_amt_zar,
                atv_zar=atv_zar,
                vat_rate_percent=vat_rate,
                vat_amount_zar=vat_amt_zar,
                total_tax_zar=total_tax_item,
            )
        )

    total_payable = round(total_customs_duty_zar + total_import_vat_zar, 2)

    return DutyEstimateResponse(
        shipment_id=str(shipment.id),
        currency=currency,
        exchange_rate_to_zar=rate,
        total_customs_value_foreign=round(total_customs_value_foreign, 2),
        total_customs_value_zar=round(total_customs_value_zar, 2),
        total_customs_duty_zar=round(total_customs_duty_zar, 2),
        total_atv_zar=round(total_atv_zar, 2),
        total_import_vat_zar=round(total_import_vat_zar, 2),
        total_payable_to_sars_zar=total_payable,
        line_items=breakdowns,
    )
