import unittest

from pixs.kernel.manifest.models import ManifestValidationError
from pixs.kernel.manifest.parser import parse_manifest_text


FAKE_JWT = "eyJhbGciOiJub25lIn0.eyJzdWIiOiJmYWtlIn0.ZmFrZS1zaWduYXR1cmU"
INJECTED_BRACES_VALUE = "demo{{ injected }}"

VALID_TOML = """
schema_version = "1"
id = "acme.demo"
type = "MODULE"
version = "1.0.0"
name = "Demo"

[provides]
[[provides.capabilities]]
id = "demo.echo"
version = "1.0.0"
contracts = []
criticality = "REQUIRED"
fallback = "none"
"""

INJECTED_TOML = f"""
schema_version = "1"
id = "acme.demo"
type = "MODULE"
version = "1.0.0"
name = "{FAKE_JWT}"

[provides]
[[provides.capabilities]]
id = "{INJECTED_BRACES_VALUE}"
version = "1.0.0"
contracts = []
criticality = "REQUIRED"
fallback = "none"
"""


class ManifestGuardsTest(unittest.TestCase):
    def test_valid_manifest_is_accepted(self):
        parsed = parse_manifest_text(VALID_TOML)
        self.assertIsNotNone(parsed)

    def test_injected_values_are_rejected_by_path_without_value(self):
        with self.assertRaises(ManifestValidationError) as ctx:
            parse_manifest_text(INJECTED_TOML)

        diagnostics = ctx.exception.diagnostics
        self.assertTrue(any("name" in d for d in diagnostics))
        self.assertTrue(
            any("provides.capabilities[0]" in d for d in diagnostics)
        )
        for diagnostic in diagnostics:
            self.assertNotIn(FAKE_JWT, diagnostic)
            self.assertNotIn(INJECTED_BRACES_VALUE, diagnostic)


if __name__ == "__main__":
    unittest.main()
