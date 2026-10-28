import unittest
from pathlib import Path

from pixs.kernel.composition import compose, discover, resolve, validate


def _root():
    return Path(__file__).resolve().parents[2]


def _texts():
    root = _root()
    rels = ("src/pixs/kernel/component.toml", "src/pixs/core/component.toml", "src/pixs/pzt/component.toml", "src/pixs/dns/component.toml")
    return tuple((root / r).read_text(encoding="utf-8") for r in rels)


class TestManifests(unittest.TestCase):
    def test_validate_quatre_manifests(self):
        texts = _texts()
        manifests, diags = validate(texts, official_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"), required_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"))
        self.assertEqual(diags, ())
        self.assertEqual(len(manifests), 4)
        by_id = {m.id: m for m in manifests}
        dns = by_id["pixs.dns"]
        pzt = by_id["pixs.pzt"]
        self.assertEqual((dns.schema_version, dns.type, dns.version), ("1", "MODULE", "0.1.0"))
        self.assertEqual((pzt.schema_version, pzt.type, pzt.version), ("1", "MODULE", "0.1.0"))
        self.assertEqual(dns.provided_capabilities[0].id, "dns.management")
        self.assertEqual(dns.provided_capabilities[0].version, "1.0.0")
        self.assertEqual(tuple(sorted(c.id for c in dns.implemented_contracts)), ("pixs.dns.policy.query", "pixs.dns.records.command", "pixs.dns.views.query", "pixs.dns.zones.command"))
        self.assertEqual(pzt.provided_capabilities[0].id, "pzt.management")
        self.assertEqual(tuple(sorted(c.id for c in pzt.implemented_contracts)), ("pixs.pzt.control.command", "pixs.pzt.control.query", "pixs.pzt.state.query"))
        self.assertIn("pixs.dns ==0.1.0", pzt.dependency_components)
        self.assertIn("pixs.dns.views.query ==1.0.0", pzt.dependency_contracts)
        self.assertIn("pixs.dns.policy.query ==1.0.0", pzt.dependency_contracts)

    def test_dag_dns_avant_pzt(self):
        texts = _texts()
        manifests, diags = validate(texts, official_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"), required_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"))
        self.assertEqual(diags, ())
        edges, order, diag = resolve(manifests)
        self.assertEqual(diag, ())
        self.assertLess(order.index("pixs.dns"), order.index("pixs.pzt"))
        self.assertIn(("pixs.pzt", "pixs.dns"), tuple(edges))

    def test_dependance_manquante_refusee(self):
        texts = _texts()
        rest = (texts[0], texts[1], texts[2])
        manifests, diags = validate(rest, official_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"), required_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"))
        self.assertTrue(diags)

    def test_contrat_version_inconnue_resolve_diagnostic(self):
        texts = list(_texts())
        texts[2] = texts[2].replace("pixs.dns.views.query ==1.0.0", "pixs.dns.views.query ==9.9.9")
        manifests, diags = validate(tuple(texts), official_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"), required_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"))
        self.assertEqual(diags, ())
        edges, order, rdiag = resolve(manifests)
        self.assertTrue(rdiag)

    def test_cycle_reel_dns_pzt_resolve_diagnostic(self):
        texts = list(_texts())
        texts[3] = texts[3].replace('components = ["pixs.kernel ==0.1.0", "pixs.core ==0.1.0"]', 'components = ["pixs.kernel ==0.1.0", "pixs.core ==0.1.0", "pixs.pzt ==0.1.0"]')
        manifests, diags = validate(tuple(texts), official_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"), required_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"))
        self.assertEqual(diags, ())
        edges, order, rdiag = resolve(manifests)
        self.assertTrue(rdiag)

    def test_compose_sans_attestation_refuse_p0(self):
        texts = _texts()
        result = compose(texts, official_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"), required_ids=("pixs.kernel", "pixs.core", "pixs.pzt", "pixs.dns"))
        self.assertFalse(result.activated)
        self.assertTrue(result.diagnostics)


if __name__ == "__main__":
    unittest.main()
