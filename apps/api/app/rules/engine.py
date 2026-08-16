"""
Deterministic Compliance Engine for TradeComply AI South Africa.
Orchestrates SARS, ITAC, NRCS, DG, and Documentation validation pipelines.
"""

from dataclasses import dataclass, field
from typing import Any

from app.rules.base import ComplianceSeverity, RuleResult
from app.rules.sars_valuation_rules import (
    MissingCommercialInvoiceRule,
    MissingVatOrCustomsCodeRule,
    IncotermsCurrencyValidationRule,
)
from app.rules.itac_rules import (
    ITACSteelImportPermitRule,
    ITACTextilesHighTariffRule,
    ITACSecondHandGoodsRule,
)
from app.rules.nrcs_rules import (
    NRCSLetterOfAuthorityRule,
    NRCSAutomotiveSafetyRule,
)
from app.rules.dangerous_goods_rules import (
    LithiumBatteryDGRule,
    HazardousChemicalsDGRule,
)


@dataclass
class ComplianceReport:
    """Consolidated compliance validation report for a shipment."""
    shipment_id: str
    is_compliant: bool
    risk_level: str  # low, medium, high, critical
    passed_count: int
    warning_count: int
    error_count: int
    critical_count: int
    checks: list[RuleResult] = field(default_factory=list)
    summary_notes: list[str] = field(default_factory=list)


class ComplianceEngine:
    """Orchestrator for all registered deterministic compliance rules."""

    def __init__(self):
        self.rules = [
            # Mandatory Documentation & SARS
            MissingCommercialInvoiceRule(),
            MissingVatOrCustomsCodeRule(),
            IncotermsCurrencyValidationRule(),
            # ITAC Import Control
            ITACSteelImportPermitRule(),
            ITACTextilesHighTariffRule(),
            ITACSecondHandGoodsRule(),
            # NRCS Standards
            NRCSLetterOfAuthorityRule(),
            NRCSAutomotiveSafetyRule(),
            # Dangerous Goods
            LithiumBatteryDGRule(),
            HazardousChemicalsDGRule(),
        ]

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> ComplianceReport:
        """Run all deterministic rules and compute risk score."""
        results: list[RuleResult] = []
        passed_count = 0
        warning_count = 0
        error_count = 0
        critical_count = 0
        summary_notes = []

        for rule in self.rules:
            res = rule.evaluate(
                shipment=shipment,
                line_items=line_items,
                parties=parties,
                documents=documents,
                tariff_map=tariff_map,
            )
            results.append(res)

            if res.passed:
                passed_count += 1
            else:
                if res.severity == ComplianceSeverity.WARNING:
                    warning_count += 1
                    summary_notes.append(f"⚠️ {res.title}: {res.message}")
                elif res.severity == ComplianceSeverity.ERROR:
                    error_count += 1
                    summary_notes.append(f"❌ {res.title}: {res.message}")
                elif res.severity == ComplianceSeverity.CRITICAL:
                    critical_count += 1
                    summary_notes.append(f"🚨 CRITICAL {res.title}: {res.message}")

        # Compute deterministic overall risk score
        if critical_count > 0:
            risk_level = "critical"
            is_compliant = False
        elif error_count > 0:
            risk_level = "high"
            is_compliant = False
        elif warning_count > 0:
            risk_level = "medium"
            is_compliant = True  # Can proceed with warnings acknowledged
        else:
            risk_level = "low"
            is_compliant = True

        return ComplianceReport(
            shipment_id=str(getattr(shipment, "id", "")),
            is_compliant=is_compliant,
            risk_level=risk_level,
            passed_count=passed_count,
            warning_count=warning_count,
            error_count=error_count,
            critical_count=critical_count,
            checks=results,
            summary_notes=summary_notes,
        )


# Global default engine instance
compliance_engine = ComplianceEngine()
