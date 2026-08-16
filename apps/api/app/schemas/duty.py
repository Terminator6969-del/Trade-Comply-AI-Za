"""
Pydantic schemas for South African Customs Duty & VAT calculations.
"""

from pydantic import BaseModel, Field, ConfigDict


class LineItemDutyBreakdown(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    line_item_id: str
    description: str
    hs_code: str | None
    quantity: float
    currency: str
    foreign_total_value: float
    customs_value_zar: float
    duty_rate_percent: float
    duty_amount_zar: float
    atv_zar: float
    vat_rate_percent: float
    vat_amount_zar: float
    total_tax_zar: float


class DutyEstimateRequest(BaseModel):
    exchange_rate: float | None = Field(
        default=None,
        description="Exchange rate to ZAR (e.g. USD/ZAR 18.50). If omitted, standard indicative rates are used.",
    )
    customs_markup_percent: float = Field(
        default=10.0,
        description="South African SARS statutory Added Tax Value (ATV) markup percentage on non-BLNS imports (standard 10%).",
    )


class DutyEstimateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    shipment_id: str
    currency: str
    exchange_rate_to_zar: float
    total_customs_value_foreign: float
    total_customs_value_zar: float
    total_customs_duty_zar: float
    total_atv_zar: float
    total_import_vat_zar: float
    total_payable_to_sars_zar: float
    line_items: list[LineItemDutyBreakdown]
    disclaimer: str = (
        "Estimates only based on South African Customs & Excise Act Schedule 1 and VAT Act Section 13. "
        "Official liability is determined upon SARS SAD500 clearance submission."
    )
