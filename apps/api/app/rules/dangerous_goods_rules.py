"""
Dangerous Goods & Hazardous Cargo compliance rules.
Flags UN numbers, Lithium Batteries (UN3480/3481), corrosive chemicals, and toxic substances.
"""

from typing import Any
from app.rules.base import ComplianceSeverity, RulePack, RuleResult


class LithiumBatteryDGRule:
    """Checks for Lithium-Ion and Lithium-Metal batteries requiring IMDG/IATA Dangerous Goods Declaration."""
    rule_code = "DG-LITH-001"
    rule_pack = RulePack.DANGEROUS_GOODS
    title = "Lithium Battery Hazardous Cargo (UN3480 / UN3481)"

    LITHIUM_HS_CODES = {"8507.60", "8507.80", "8507.50"}

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        dg_battery_items = []
        for item in line_items:
            hs = getattr(item, "hs_code_suggested", None) or getattr(item, "hs_code_declared", None) or ""
            desc = (getattr(item, "description", None) or "").lower()

            if hs in self.LITHIUM_HS_CODES or "lithium" in desc or "lfp" in desc or "battery pack" in desc:
                dg_battery_items.append(str(getattr(item, "id", None) or getattr(item, "description", "")))

        if dg_battery_items:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.CRITICAL,
                message=f"Shipment contains {len(dg_battery_items)} Lithium Battery item(s) classified under IMDG Class 9 (UN 3480 / UN 3481).",
                recommended_action="Ensure UN 38.3 Test Summary Report, MSDS / SDS, and signed Dangerous Goods Declaration (DGD) are attached.",
                affected_line_items=dg_battery_items,
                metadata={"un_number": "UN3480 / UN3481", "hazard_class": "Class 9 Miscellaneous"},
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message="No dangerous goods lithium batteries detected.",
        )


class HazardousChemicalsDGRule:
    """Checks for chemical commodities with dangerous goods UN numbers (Class 3, 6, 8)."""
    rule_code = "DG-CHEM-002"
    rule_pack = RulePack.DANGEROUS_GOODS
    title = "Hazardous Chemicals & Dangerous Goods (IMDG / ADR)"

    HAZARD_KEYWORDS = ["un2789", "dangerous goods", "flammable", "corrosive", "acid", "toxic", "poison", "imdg"]

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        hazardous_items = []
        for item in line_items:
            hs = getattr(item, "hs_code_suggested", None) or getattr(item, "hs_code_declared", None) or ""
            desc = (getattr(item, "description", None) or "").lower()

            if hs.startswith("2915.21") or hs.startswith("2710") or any(kw in desc for kw in self.HAZARD_KEYWORDS):
                hazardous_items.append(str(getattr(item, "id", None) or getattr(item, "description", "")))

        if hazardous_items:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.CRITICAL,
                message=f"Detected {len(hazardous_items)} hazardous chemical line item(s).",
                recommended_action="Attach Material Safety Data Sheet (MSDS), Road Transport Tremcard, and IMDG Multimodal Dangerous Goods Form.",
                affected_line_items=hazardous_items,
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message="No dangerous chemical cargo detected.",
        )
