"""
Pydantic schemas for Tariff lookup and search.
"""

from pydantic import BaseModel, ConfigDict


class TariffRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    hs_code: str
    sa_tariff_code: str
    description: str
    duty_rate: float
    vat_rate: float
    unit_of_measure: str | None = None
    chapter: str | None = None
    section: str | None = None
