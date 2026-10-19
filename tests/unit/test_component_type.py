"""Contrat canonique du vocabulaire ComponentType."""

import unittest
from enum import Enum

from pixs.kernel import component_type as vocabulary
from pixs.kernel.manifest.models import (
    COMPONENT_TYPES,
    ManifestValidationError,
    parse_manifest,
)

# DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend.


class TestComponentType(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (
            ("KERNEL", "KERNEL"),
            ("MODULE", "MODULE"),
            ("SUBMODULE", "SUBMODULE"),
            ("PROVIDER", "PROVIDER"),
            ("EXTENSION", "EXTENSION"),
            ("THEME", "THEME"),
        )
        kind = vocabulary.ComponentType
        self.assertEqual(
            tuple((name, member.value) for name, member in kind.__members__.items()),
            expected,
        )
        self.assertEqual(len(kind), 6)
        self.assertTrue(issubclass(kind, Enum))
        self.assertFalse(issubclass(kind, str))
        self.assertEqual(vocabulary.__all__, ["ComponentType"])
        self.assertIs(kind("KERNEL"), kind.KERNEL)
        self.assertEqual(kind.THEME.value, "THEME")

    def test_undeclared_values_are_rejected_without_normalization(self):
        for value in (
            "kernel",
            "Kernel",
            "KERNEL ",
            " KERNEL",
            "module",
            "PLUGIN",
            "APPLICATION",
            "",
            None,
            "pixs.kernel",
        ):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.ComponentType(value)

    def test_coherence_with_existing_component_types_without_enum_acceptance(self):
        self.assertEqual(
            set(COMPONENT_TYPES),
            {"KERNEL", "MODULE", "SUBMODULE", "PROVIDER", "EXTENSION", "THEME"},
        )
        self.assertEqual(
            {member.value for member in vocabulary.ComponentType},
            set(COMPONENT_TYPES),
        )
        self.assertEqual(
            set(vocabulary.ComponentType.__members__),
            set(COMPONENT_TYPES),
        )
        base = {
            "schema_version": "1",
            "id": "acme.example",
            "type": "MODULE",
            "version": "0.1.0",
        }
        manifest = parse_manifest(dict(base))
        self.assertEqual(manifest.type, "MODULE")
        rejected = dict(base)
        rejected["type"] = vocabulary.ComponentType.MODULE
        with self.assertRaises(ManifestValidationError) as ctx:
            parse_manifest(rejected)
        self.assertTrue(any(d.startswith("type") for d in ctx.exception.diagnostics))


if __name__ == "__main__":
    unittest.main()
