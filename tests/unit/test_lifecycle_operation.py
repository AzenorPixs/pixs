"""Contrat canonique des opérations de cycle de vie."""

import unittest
from enum import Enum

from pixs.kernel.lifecycle import operation as vocabulary
from pixs.kernel.lifecycle.state import LIFECYCLE_OPERATIONS, OUT_OF_SCOPE_OPERATIONS

# DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend.


class TestLifecycleOperation(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (
            ("DISCOVER", "discover"),
            ("VALIDATE", "validate"),
            ("INSTALL", "install"),
            ("ENABLE", "enable"),
            ("CONFIGURE", "configure"),
            ("START", "start"),
            ("DISABLE", "disable"),
            ("MIGRATE", "migrate"),
            ("UPGRADE", "upgrade"),
            ("UNINSTALL", "uninstall"),
            ("PURGE", "purge"),
        )
        operation_type = vocabulary.LifecycleOperation
        self.assertEqual(
            tuple((name, member.value) for name, member in operation_type.__members__.items()),
            expected,
        )
        self.assertEqual(len(operation_type), 11)
        self.assertEqual(len(operation_type.__members__), 11)
        self.assertTrue(issubclass(operation_type, Enum))
        self.assertFalse(issubclass(operation_type, str))
        self.assertEqual(vocabulary.__all__, ["LifecycleOperation"])
        self.assertIs(operation_type("discover"), operation_type.DISCOVER)
        self.assertIs(operation_type("purge"), operation_type.PURGE)
        self.assertEqual(operation_type.DISABLE.value, "disable")
        for name, member in operation_type.__members__.items():
            with self.subTest(name=name):
                self.assertEqual(member.value, member.value.lower())
                self.assertEqual(name, member.value.upper())
                self.assertIs(type(member.value), str)
                self.assertIsNot(type(member), str)

    def test_no_alias_and_lowercase_values(self):
        operation_type = vocabulary.LifecycleOperation
        values = [member.value for member in operation_type]
        self.assertEqual(len(set(values)), 11)
        self.assertEqual(tuple(values), LIFECYCLE_OPERATIONS)

    def test_coherence_with_lifecycle_operations_and_p0_preserved(self):
        self.assertEqual(
            LIFECYCLE_OPERATIONS,
            (
                "discover",
                "validate",
                "install",
                "enable",
                "configure",
                "start",
                "disable",
                "migrate",
                "upgrade",
                "uninstall",
                "purge",
            ),
        )
        self.assertEqual(len(LIFECYCLE_OPERATIONS), 11)
        self.assertTrue(OUT_OF_SCOPE_OPERATIONS.issubset(set(LIFECYCLE_OPERATIONS)))
        self.assertEqual(
            OUT_OF_SCOPE_OPERATIONS, frozenset({"migrate", "upgrade", "uninstall", "purge"})
        )
        self.assertEqual(
            tuple(member.value for member in vocabulary.LifecycleOperation),
            LIFECYCLE_OPERATIONS,
        )

    def test_undeclared_values_are_rejected_without_normalization(self):
        for value in (
            "Discover",
            "DISCOVER",
            "discover ",
            " discover",
            "DISABLED",
            "installed",
            "",
            None,
            "STAGE",
            0,
        ):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.LifecycleOperation(value)


if __name__ == "__main__":
    unittest.main()
