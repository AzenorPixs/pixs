"""Contrat pur des commandes C08, sans autorite ni IO."""

from __future__ import annotations

import dataclasses
import hashlib
import unittest
from enum import Enum

from pixs.backend.installation.mode_commands import (
    MODE_SERIALIZER_VERSION, ModeCommandInput, check_mode_command,
    mode_action_ref, mode_command_type, mode_resource_ref,
    canonical_mode_bytes, mode_content_sha256)
from pixs.backend.installation.mode_values import ModeOperationKind

LIMIT = 64


class Explosive:
    def __repr__(self):
        raise RuntimeError("boom")

    def __str__(self):
        raise RuntimeError("boom")


class FakeKind(Enum):
    OTHER = "FINALIZE_CONFIGURATION"


def base(**over):
    fields = dict(installation_ref="installation:alpha", actor_ref="actor:alpha",
                  kind=ModeOperationKind.FINALIZE_CONFIGURATION,
                  expected_version=1, idempotency_key="idem:alpha")
    fields.update(over)
    return ModeCommandInput(**fields)


class TestCouples(unittest.TestCase):
    def test_three_distinct(self):
        self.assertEqual(mode_action_ref(ModeOperationKind.FINALIZE_CONFIGURATION),
                         "pixs.backend.modes.finalize")
        self.assertEqual(mode_command_type(ModeOperationKind.FINALIZE_CONFIGURATION),
                         "pixs.backend.modes.finalize:v1")
        self.assertEqual(mode_action_ref(ModeOperationKind.ENTER_MAINTENANCE),
                         "pixs.backend.modes.enter_maintenance")
        self.assertEqual(mode_command_type(ModeOperationKind.ENTER_MAINTENANCE),
                         "pixs.backend.modes.enter_maintenance:v1")
        self.assertEqual(mode_action_ref(ModeOperationKind.EXIT_MAINTENANCE),
                         "pixs.backend.modes.exit_maintenance")
        self.assertEqual(mode_command_type(ModeOperationKind.EXIT_MAINTENANCE),
                         "pixs.backend.modes.exit_maintenance:v1")
        kinds = [mode_action_ref(k) for k in ModeOperationKind]
        types = [mode_command_type(k) for k in ModeOperationKind]
        self.assertEqual(len(set(kinds + types)), 6)


class TestReference(unittest.TestCase):
    def test_encoding(self):
        value = base(installation_ref="a b/c:d%e\u00e9")
        self.assertEqual(mode_resource_ref(value, max_ref_len=LIMIT),
                         "pixs.backend.modes:a%20b%2Fc%3Ad%25e%C3%A9")

    def test_no_collision(self):
        left = base(installation_ref="a/b")
        right = base(installation_ref="a%2Fb")
        self.assertNotEqual(mode_resource_ref(left, max_ref_len=LIMIT),
                            mode_resource_ref(right, max_ref_len=LIMIT))


class TestCanonical(unittest.TestCase):
    def test_expected_literal(self):
        value = base()
        expected = (b'{"actor_ref":"actor:alpha","expected_version":1,'
                    b'"idempotency_key":"idem:alpha",'
                    b'"installation_ref":"installation:alpha",'
                    b'"kind":"FINALIZE_CONFIGURATION",'
                    b'"serializer_version":"1.0.0"}')
        self.assertEqual(MODE_SERIALIZER_VERSION, "1.0.0")
        self.assertEqual(canonical_mode_bytes(value, max_ref_len=LIMIT), expected)
        self.assertEqual(mode_content_sha256(value, max_ref_len=LIMIT),
                         hashlib.sha256(expected).hexdigest())

    def test_no_normalization(self):
        nfc = base(installation_ref="caf\u00e9")
        nfd = base(installation_ref="cafe\u0301")
        raw_nfc = canonical_mode_bytes(nfc, max_ref_len=LIMIT)
        raw_nfd = canonical_mode_bytes(nfd, max_ref_len=LIMIT)
        self.assertNotEqual(raw_nfc, raw_nfd)
        self.assertIn("caf\u00e9".encode("utf-8"), raw_nfc)
        spaced = base(installation_ref="a b")
        self.assertIn(b"a b", canonical_mode_bytes(spaced, max_ref_len=LIMIT))

    def test_each_field_changes_digest(self):
        first = mode_content_sha256(base(), max_ref_len=LIMIT)
        variants = [base(installation_ref="installation:beta"),
                    base(actor_ref="actor:beta"),
                    base(kind=ModeOperationKind.ENTER_MAINTENANCE),
                    base(expected_version=2),
                    base(idempotency_key="idem:beta")]
        for other in variants:
            self.assertNotEqual(mode_content_sha256(other, max_ref_len=LIMIT), first)


class TestVersion(unittest.TestCase):
    def test_refused(self):
        for bad in (True, False, "1", 1.0, None, 0, -1, 2 ** 63):
            with self.assertRaises(ValueError):
                ModeCommandInput("i", "a", ModeOperationKind.FINALIZE_CONFIGURATION,
                                 bad, "k")

    def test_bounds_admitted(self):
        for good in (1, 2 ** 63 - 1):
            value = base(expected_version=good)
            check_mode_command(value, max_ref_len=LIMIT)
            canonical_mode_bytes(value, max_ref_len=LIMIT)
            mode_content_sha256(value, max_ref_len=LIMIT)


class TestLimits(unittest.TestCase):
    def test_invalid_strings_on_each_field(self):
        helpers = (check_mode_command, mode_resource_ref,
                   canonical_mode_bytes, mode_content_sha256)
        for field in ("installation_ref", "actor_ref", "idempotency_key"):
            for bad in ("", "a\x00b", "a\x07b", "x" * (LIMIT + 1)):
                with self.subTest(field=field, invalid_length=len(bad)):
                    value = base(**{field: bad})
                    for helper in helpers:
                        with self.assertRaises(ValueError) as ctx:
                            helper(value, max_ref_len=LIMIT)
                        self.assertEqual(str(ctx.exception), "Commande C08 refusee.")
            value = base(**{field: "x" * LIMIT})
            for helper in helpers:
                helper(value, max_ref_len=LIMIT)

    def test_bad_limits(self):
        value = base()
        for limit in (True, False, None, 0, -1, "64", 64.0, Explosive()):
            with self.assertRaises(ValueError):
                check_mode_command(value, max_ref_len=limit)
            with self.assertRaises(ValueError):
                mode_resource_ref(value, max_ref_len=limit)
            with self.assertRaises(ValueError):
                canonical_mode_bytes(value, max_ref_len=limit)
            with self.assertRaises(ValueError):
                mode_content_sha256(value, max_ref_len=limit)


class TestClosed(unittest.TestCase):
    def test_foreign_and_explosive(self):
        with self.assertRaises(ValueError) as ctx:
            ModeCommandInput("i", "a", FakeKind.OTHER, 1, "k")
        self.assertEqual(str(ctx.exception), "Commande C08 refusee.")
        for bad in (Explosive(), FakeKind.OTHER):
            with self.assertRaises(ValueError) as ctx:
                ModeCommandInput(bad, "a", ModeOperationKind.FINALIZE_CONFIGURATION, 1, "k")
            self.assertNotIn("boom", str(ctx.exception))
        with self.assertRaises(ValueError):
            mode_action_ref(FakeKind.OTHER)
        with self.assertRaises(ValueError):
            mode_command_type("FINALIZE_CONFIGURATION")

    def test_frozen_slots_opaque(self):
        value = base()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.installation_ref = "x"
        self.assertIn("__slots__", dir(ModeCommandInput))
        self.assertFalse(hasattr(value, "__dict__"))
        text = repr(value)
        self.assertNotIn("installation:alpha", text)
        self.assertNotIn("actor:alpha", text)
        self.assertNotIn("idem:alpha", text)

    def test_wrong_dto_is_closed_without_formatting(self):
        for bad in (Explosive(), None, {}, FakeKind.OTHER):
            for helper in (check_mode_command, mode_resource_ref,
                           canonical_mode_bytes, mode_content_sha256):
                with self.assertRaises(ValueError) as ctx:
                    helper(bad, max_ref_len=LIMIT)
                self.assertEqual(str(ctx.exception), "Commande C08 refusee.")

    def test_setattr_frontier(self):
        for field, bad in (("kind", "BAD"), ("expected_version", True),
                           ("expected_version", 0), ("actor_ref", Explosive())):
            value = base()
            object.__setattr__(value, field, bad)
            for helper in (check_mode_command, mode_resource_ref,
                           canonical_mode_bytes, mode_content_sha256):
                with self.assertRaises(ValueError) as ctx:
                    helper(value, max_ref_len=LIMIT)
                self.assertEqual(str(ctx.exception), "Commande C08 refusee.")


if __name__ == "__main__":
    unittest.main()
