"""Manifest facultatif du fournisseur d evaluation bornee, sans activation P0."""

from __future__ import annotations

from pixs.kernel.manifest.models import ComponentManifest


BUSINESS_RULES_MANIFEST_TEXT = """schema_version = "1"
id = "pixs.business-rules"
name = "Évaluation bornée des règles métier"
type = "PROVIDER"
version = "1.0.0"

[dependencies]
components = ["pixs.kernel ==0.1.0", "pixs.core ==0.1.0"]

[[provides.capabilities]]
id = "business-rules.evaluate"
version = "1.0.0"
contracts = ["business-rules.evaluation"]
criticality = "OPTIONAL"
fallback = "none"

[[implements.contracts]]
id = "business-rules.evaluation"
version = "1.0.0"
"""


def parse_business_rules_manifest() -> ComponentManifest:
    """Parse pur du manifest facultatif via le parser Kernel partage."""
    from pixs.kernel.manifest.parser import parse_manifest_text

    return parse_manifest_text(BUSINESS_RULES_MANIFEST_TEXT)
