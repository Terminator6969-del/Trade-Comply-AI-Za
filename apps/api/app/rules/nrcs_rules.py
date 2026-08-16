"""
NRCS (National Regulator for Compulsory Specifications) rules.
Checks for mandatory Letters of Authority (LOA) for regulated electrical, electronics, appliances, and automotive goods.
"""

from typing import Any
from app.rules.base import ComplianceSeverity, RulePack, RuleResult


class NRCSLetterOfAuthorityRule:
    """Checks for electrical/electronic commodities requiring a valid NRCS Letter of Authority (LOA)."""
    rule_code = "NRCS-LOA-001"
    rule_pack = RulePack.NRCS_LOA
    title = "NRCS Letter of Authority (LOA) Requirement"

    LOA_HS_PREFIXES = {
        "8539.50": "LED Lamps and light bulbs (VC 8032)",
        "8504.40": "Inverters, UPS and power converters (VC 8055)",
        "8544.42": "Electrical cables and flexible cords (VC 8006)",
        "8471.30": "Laptops and IT equipment (VC 8055)",
        "8528.72": "Television sets and display monitors (VC 8055)",
        "8516.40": "Electric smoothing irons and small domestic appliances (VC 8055)",
        "8509.40": "Food grinders and electric blenders (VC 8055)",
    }

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        nrcs_items = []
        for item in line_items:
            hs = getattr(item, "hs_code_suggested", None) or getattr(item, "hs_code_declared", None) or ""
            normalized_hs = hs.strip()

            for prefix, compulsory_spec in self.LOA_HS_PREFIXES.items():
                if normalized_hs.startswith(prefix) or prefix.startswith(normalized_hs):
                    nrcs_items.append({
                        "id": str(getattr(item, "id", "")),
                        "description": getattr(item, "description", ""),
                        "hs_code": hs,
                        "regulation": compulsory_spec,
                    })
                    break

        if nrcs_items:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.ERROR,
                message=f"Found {len(nrcs_items)} electrical/electronic product(s) subject to NRCS Compulsory Specifications.",
                recommended_action="Ensure a valid NRCS Letter of Authority (LOA) certificate is issued and registered on the SARS Customs system.",
                affected_line_items=[i["id"] for i in nrcs_items],
                metadata={"regulated_items": nrcs_items},
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message="No NRCS LOA-regulated electrical items identified.",
        )


class NRCSAutomotiveSafetyRule:
    """Checks motor vehicles and safety-critical automotive replacement parts for NRCS Homologation."""
    rule_code = "NRCS-AUT-002"
    rule_pack = RulePack.NRCS_LOA
    title = "Automotive Homologation & Safety Compliance"

    AUTO_PREFIXES = ("8703", "8704", "8708")

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
            hs = (getattr(item, "hs_code_suggested", None) or getattr(item, "hs_code_declared", None) or "").replace(".", "")
            if any(hs.startswith(p) for p in self.AUTO_PREFIXES):
                flagged.append(str(getattr(item, "id", None) or getattr(item, "description", "")))

        if flagged:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.WARNING,
                message=f"Detected {len(flagged)} automotive vehicle or replacement part item(s) subject to NRCS Homologation standards (VC 8016 / VC 8021).",
                recommended_action="Verify NRCS Homologation Approval certificate and E-mark / SANS standard markings.",
                affected_line_items=flagged,
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message="No automotive homologation items detected.",
        )
