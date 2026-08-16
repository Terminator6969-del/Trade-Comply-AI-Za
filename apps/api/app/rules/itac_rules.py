"""
ITAC (International Trade Administration Commission of South Africa) rules.
Checks for import permits on controlled items (steel, second-hand goods, textiles with anti-dumping duties).
"""

from typing import Any
from app.rules.base import ComplianceSeverity, RulePack, RuleResult


class ITACSteelImportPermitRule:
    """Flag steel and iron imports under Chapters 72 and 73 that require an ITAC import permit."""
    rule_code = "ITAC-STL-001"
    rule_pack = RulePack.ITAC_PERMITS
    title = "ITAC Steel & Iron Import Permit Check"

    STEEL_PREFIXES = ("7213", "7208", "7209", "7210", "7214", "7304", "7306")

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        steel_items = []
        for item in line_items:
            hs = getattr(item, "hs_code_suggested", None) or getattr(item, "hs_code_declared", None) or ""
            normalized_hs = hs.replace(".", "").strip()
            desc = (getattr(item, "description", None) or "").lower()

            if any(normalized_hs.startswith(p.replace(".", "")) for p in self.STEEL_PREFIXES) or "rebar" in desc or "steel plate" in desc:
                steel_items.append(getattr(item, "id", None) or getattr(item, "description", "Unknown item"))

        if steel_items:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.CRITICAL,
                message=f"Shipment contains {len(steel_items)} steel/iron line item(s) subject to ITAC Import Control Regulations.",
                recommended_action="Obtain and attach a valid ITAC Import Permit before cargo arrival to prevent SARS border detention.",
                affected_line_items=[str(x) for x in steel_items],
                metadata={"regulated_category": "Steel & Base Metals"},
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message="No controlled steel or iron line items detected.",
        )


class ITACTextilesHighTariffRule:
    """Warns about high customs duty rates (40%-45%) on imported clothing and apparel (Chapters 61 & 62)."""
    rule_code = "ITAC-TXT-002"
    rule_pack = RulePack.ITAC_PERMITS
    title = "High Tariff Textiles & Apparel Warning"

    TEXTILE_CHAPTERS = ("61", "62", "63", "64")

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        apparel_items = []
        for item in line_items:
            hs = getattr(item, "hs_code_suggested", None) or getattr(item, "hs_code_declared", None) or ""
            clean_hs = hs.replace(".", "").strip()

            if any(clean_hs.startswith(ch) for ch in self.TEXTILE_CHAPTERS):
                tariff = tariff_map.get(hs)
                duty_rate = getattr(tariff, "duty_rate", 45.0) if tariff else 45.0
                apparel_items.append({
                    "id": str(getattr(item, "id", "")),
                    "description": getattr(item, "description", ""),
                    "hs_code": hs,
                    "duty_rate": duty_rate,
                })

        if apparel_items:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.WARNING,
                message=f"Detected {len(apparel_items)} clothing/textile item(s) subject to high SARS ad valorem duty rates (up to 45%).",
                recommended_action="Verify if the importer qualifies for ITAC Rebate Item 470.03 or SADC preferential certificates of origin to reduce duties.",
                affected_line_items=[item["id"] for item in apparel_items],
                metadata={"items": apparel_items},
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message="No high-tariff clothing or footwear line items detected.",
        )


class ITACSecondHandGoodsRule:
    """Checks for used / refurbished goods which strictly require an ITAC used goods permit."""
    rule_code = "ITAC-USD-003"
    rule_pack = RulePack.ITAC_PERMITS
    title = "Second-Hand / Refurbished Goods Permit Check"

    KEYWORDS = ["used", "refurbished", "second-hand", "2nd hand", "pre-owned", "reconditioned"]

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        flagged = []
        for item in line_items:
            desc = (getattr(item, "description", None) or "").lower()
            if any(kw in desc for kw in self.KEYWORDS):
                flagged.append(str(getattr(item, "id", None) or getattr(item, "description", "")))

        if flagged:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.CRITICAL,
                message=f"Found {len(flagged)} line item(s) described as used/refurbished. All second-hand goods require a specific ITAC Import Permit.",
                recommended_action="Provide an official ITAC Used Goods Import Permit. SARS will seize undeclared used capital or consumer goods.",
                affected_line_items=flagged,
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message="All goods declared appear to be brand new.",
        )
