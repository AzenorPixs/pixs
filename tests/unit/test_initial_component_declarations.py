"""Tests ciblés des déclarations initiales via seules API publiques du noyau."""

import unittest
from pathlib import Path

from pixs.backend.composition_initial import (
    COMPOSITION_VERSION,
    MANIFEST_PATHS,
    OFFICIAL_IDS,
    REQUIRED_IDS,
)
from pixs.kernel.composition import compose, discover, resolve, validate


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _texts() -> tuple[str, ...]:
    root = _root()
    return tuple((root / rel).read_text(encoding="utf-8") for rel in MANIFEST_PATHS)


class TestConstants(unittest.TestCase):
    def test_donnees_exactes(self) -> None:
        self.assertEqual(COMPOSITION_VERSION, "0.1.0")
        self.assertEqual(
            MANIFEST_PATHS,
            (
                "src/pixs/kernel/component.toml",
                "src/pixs/core/component.toml",
                "src/pixs/example/component.toml",
            ),
        )
        self.assertEqual(OFFICIAL_IDS, ("pixs.kernel", "pixs.core"))
        self.assertEqual(REQUIRED_IDS, ("pixs.kernel", "pixs.core", "example.hello"))


class TestManifests(unittest.TestCase):
    def test_schema_types_versions(self) -> None:
        manifests, diagnostics = validate(
            _texts(), official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS
        )
        self.assertEqual(diagnostics, ())
        self.assertEqual(len(manifests), 3)
        by_id = {m.id: m for m in manifests}
        kernel = by_id["pixs.kernel"]
        core = by_id["pixs.core"]
        example = by_id["example.hello"]
        self.assertEqual((kernel.schema_version, kernel.type, kernel.version), ("1", "KERNEL", "0.1.0"))
        self.assertEqual((core.schema_version, core.type, core.version), ("1", "MODULE", "0.1.0"))
        self.assertEqual((example.schema_version, example.type, example.version), ("1", "MODULE", "1.0.0"))
        self.assertEqual(kernel.provided_capabilities, ())
        self.assertEqual(kernel.implemented_contracts, ())
        self.assertEqual(core.provided_capabilities, ())
        self.assertEqual(core.implemented_contracts, ())
        self.assertEqual(core.dependency_components, ("pixs.kernel ==0.1.0",))


class TestValidateDiscover(unittest.TestCase):
    def test_discover_validate_sans_diagnostic(self) -> None:
        texts = _texts()
        self.assertEqual(discover(texts), tuple(texts))
        _, diagnostics = validate(texts, official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS)
        self.assertEqual(diagnostics, ())


class TestResolve(unittest.TestCase):
    def test_graphe_precedence_et_determinisme(self) -> None:
        manifests, diagnostics = validate(
            _texts(), official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS
        )
        self.assertEqual(diagnostics, ())
        edges, order, diag = resolve(manifests)
        self.assertEqual(diag, ())
        self.assertIn(("pixs.core", "pixs.kernel"), tuple(edges))
        self.assertEqual(len(order), 3)
        self.assertEqual(set(order), set(REQUIRED_IDS))
        self.assertLess(order.index("pixs.kernel"), order.index("pixs.core"))
        edges2, order2, diag2 = resolve(manifests)
        self.assertEqual(tuple(order), tuple(order2))
        self.assertEqual(tuple(edges), tuple(edges2))
        self.assertEqual(diag2, ())


class TestComposeRefus(unittest.TestCase):
    def test_sans_attestations_refuse_resolve(self) -> None:
        texts = _texts()
        first = compose(texts, official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS)
        second = compose(texts, official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS)
        self.assertEqual(first, second)
        for result in (first, second):
            self.assertEqual(result.stage, "resolve")
            self.assertIs(result.activated, False)
            self.assertIs(result.globally_compatible, False)
            self.assertEqual(
                result.evaluation_scope,
                ("components", "capabilities", "contracts", "conformity"),
            )
            self.assertEqual(
                result.unevaluated_dimensions,
                ("schemas", "migrations", "events", "providers", "clients"),
            )
            self.assertEqual(tuple(result.order), ())
            self.assertEqual(tuple(result.edges), ())
            self.assertTrue(result.diagnostics)

    def test_omission_chacun_refuse_validate(self) -> None:
        texts = _texts()
        for index in range(3):
            rest = tuple(t for i, t in enumerate(texts) if i != index)
            result = compose(rest, official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS)
            self.assertEqual(result.stage, "validate")
            self.assertIs(result.activated, False)

    def test_sans_official_ids_namespace_refuse(self) -> None:
        result = compose(_texts(), required_ids=REQUIRED_IDS)
        self.assertEqual(result.stage, "validate")
        self.assertIs(result.activated, False)
        self.assertTrue(result.diagnostics)

    def test_version_kernel_incompatible(self) -> None:
        texts = list(_texts())
        texts[0] = texts[0].replace('version = "0.1.0"', 'version = "0.2.0"', 1)
        manifests, diagnostics = validate(
            tuple(texts), official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS
        )
        self.assertEqual(diagnostics, ())
        _, _, resolve_diag = resolve(manifests)
        self.assertTrue(resolve_diag)
        result = compose(tuple(texts), official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS)
        self.assertEqual(result.stage, "resolve")
        self.assertIs(result.activated, False)


if __name__ == "__main__":
    unittest.main()
