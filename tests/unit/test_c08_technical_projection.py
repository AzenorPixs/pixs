"""Scénarios du contrat C08 projection 1.0.0 ; sources de tests, sans qualification."""
from __future__ import annotations

import hashlib
import json
import unittest
from dataclasses import replace

from pixs.backend.installation.technical_projection import (
    TechnicalProjectionError, ProjectionLimits, parse_projection_bytes,
    dump_projection_canonical, projection_sha256, validate_effects_for_actions)


def _document():
    # Données synthétiques ; aucun profil réel ni secret de production.
    return {
        "schema_version": "1.0.0", "projection_ref": "projection",
        "catalog_operation": "prepare_postgresql", "catalog_version": "1.0.0",
        "operation_id": "preparation", "installation_ref": "installation",
        "target_ref": "target", "runtime_profile_ref": "runtime",
        "runtime_profile_version": "1.0.0",
        "service": {"ref": "service", "action": "REUSE_RUNNING",
                    "profile_ref": "service-profile", "profile_version": "1.0.0"},
        "role": {"ref": "role", "action": "REUSE", "profile_ref": "role-profile",
                 "profile_version": "1.0.0", "credential_binding_ref": "binding",
                 "credential_binding_version": "1.0.0"},
        "database": {"ref": "database", "action": "REUSE",
                     "profile_ref": "database-profile", "profile_version": "1.0.0"},
        "observation": {"ref": "observation", "version": "1.0.0", "sha256": "a" * 64},
        "allowed_effects": [], "correlation_id": "correlation",
        "idempotency_key": "key", "causation_id": None,
        "correlation_ids": ["c2", "c1", "c2"], "causation_ids": ["a1", "a1"],
    }


def _wire(document):
    return json.dumps(document, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


class TechnicalProjectionTests(unittest.TestCase):
    def setUp(self):
        self.limits = ProjectionLimits(8192, 128, 8, 8)

    def assertRefused(self, document):
        with self.assertRaises(TechnicalProjectionError):
            parse_projection_bytes(_wire(document), self.limits)

    def test_reuse_wire_and_digest_match_the_confirmed_document(self):
        raw = _wire(_document())
        result = parse_projection_bytes(raw, self.limits)
        self.assertEqual(dump_projection_canonical(result, self.limits), raw)
        self.assertEqual(projection_sha256(result, self.limits), hashlib.sha256(raw).hexdigest())
        self.assertIsNone(result.causation_id)
        self.assertEqual(result.allowed_effects, ())

    def test_a07_order_and_duplicates_survive(self):
        result = parse_projection_bytes(_wire(_document()), self.limits)
        self.assertEqual(result.correlation_ids, ("c2", "c1", "c2"))
        self.assertEqual(result.causation_ids, ("a1", "a1"))

    def test_install_create_has_only_the_explicit_effects(self):
        document = _document()
        document["service"]["action"] = "INSTALL_CONFIGURE_START"
        document["role"]["action"] = "CREATE"
        document["database"]["action"] = "CREATE"
        effects = ["SERVICE_INSTALL", "SERVICE_CONFIGURE", "SERVICE_START",
                   "ROLE_CREATE", "DATABASE_CREATE"]
        for initialize in (False, True):
            with self.subTest(initialize=initialize):
                document["allowed_effects"] = list(effects)
                if initialize:
                    document["allowed_effects"].insert(2, "CLUSTER_INITIALIZE")
                result = parse_projection_bytes(_wire(document), self.limits)
                self.assertEqual(result.allowed_effects, tuple(document["allowed_effects"]))

    def test_effect_order_duplicates_extras_and_missing_effects_are_refused(self):
        invalid = [("ROLE_CREATE",), ("SERVICE_START",), ("CLUSTER_INITIALIZE",),
                   ("DATABASE_DROP",), ("UNKNOWN",), ("ROLE_CREATE", "ROLE_CREATE")]
        for effects in invalid:
            with self.subTest(effects=effects):
                with self.assertRaises(TechnicalProjectionError):
                    validate_effects_for_actions("REUSE_RUNNING", "REUSE", "REUSE", effects)
        for effects in ((), ("ROLE_CREATE", "SERVICE_START"),
                        ("SERVICE_START", "ROLE_CREATE", "DATABASE_CREATE")):
            with self.subTest(effects=effects):
                with self.assertRaises(TechnicalProjectionError):
                    validate_effects_for_actions("START_EXISTING", "CREATE", "REUSE", effects)

    def test_unhashable_actions_and_non_tuple_effects_have_a_domain_refusal(self):
        for action, effects in (([], ()), ("REUSE_RUNNING", []),
                                ("REUSE_RUNNING", ([],))):
            with self.subTest(action=action, effects=effects):
                with self.assertRaises(TechnicalProjectionError):
                    validate_effects_for_actions(action, "REUSE", "REUSE", effects)

    def test_current_profile_does_not_silently_enable_docker_or_recreate(self):
        for location, action in (("service", "INITIALIZE_START"), ("database", "RECREATE")):
            document = _document()
            document[location]["action"] = action
            self.assertRefused(document)

    def test_unknown_fields_and_missing_fields_are_refused(self):
        for location in (None, "service", "role", "database", "observation"):
            with self.subTest(location=location):
                document = _document()
                target = document if location is None else document[location]
                target["sql"] = "SYNTHETIC_FORBIDDEN_FIELD"
                self.assertRefused(document)
                target.pop("sql")
                target.pop(next(iter(target)))
                self.assertRefused(document)

    def test_duplicate_root_and_nested_keys_are_refused(self):
        raw = _wire(_document())
        for original, duplicate in (
                (b'"projection_ref":"projection"',
                 b'"projection_ref":"projection","projection_ref":"other"'),
                (b'"credential_binding_ref":"binding"',
                 b'"credential_binding_ref":"binding","credential_binding_ref":"other"')):
            self.assertIn(original, raw)
            with self.assertRaises(TechnicalProjectionError):
                parse_projection_bytes(raw.replace(original, duplicate, 1), self.limits)

    def test_numbers_booleans_null_and_non_finite_values_are_not_references(self):
        for value in (0, 1.5, True, False, None, float("nan"), float("inf"), [], {}):
            document = _document()
            document["projection_ref"] = value
            with self.subTest(value=value):
                self.assertRefused(document)
        document = _document()
        document["causation_id"] = False
        self.assertRefused(document)

    def test_utf8_canonicality_and_digest_shape_are_enforced(self):
        raw = _wire(_document())
        for changed in (raw + b"\n", b"\xef\xbb\xbf" + raw, b"\xff", b"[" * 1600 + b"]" * 1600):
            with self.subTest(size=len(changed)):
                with self.assertRaises(TechnicalProjectionError):
                    parse_projection_bytes(changed, self.limits)
        for digest in ("A" * 64, "a" * 63, "g" * 64, None):
            document = _document()
            document["observation"]["sha256"] = digest
            self.assertRefused(document)

    def test_byte_and_array_limits_include_the_boundary(self):
        raw = _wire(_document())
        exact = replace(self.limits, max_bytes=len(raw), max_correlation_refs=3,
                        max_causation_refs=2)
        parse_projection_bytes(raw, exact)
        for bad in (replace(exact, max_bytes=len(raw) - 1),
                    replace(exact, max_correlation_refs=2),
                    replace(exact, max_causation_refs=1)):
            with self.subTest(limits=bad):
                with self.assertRaises(TechnicalProjectionError):
                    parse_projection_bytes(raw, bad)
        for field in ("max_bytes", "max_ref_bytes", "max_correlation_refs", "max_causation_refs"):
            with self.subTest(field=field):
                with self.assertRaises(TechnicalProjectionError):
                    parse_projection_bytes(raw, replace(self.limits, **{field: True}))

    def test_reference_limit_is_measured_in_utf8_bytes(self):
        document = _document()
        document["target_ref"] = "é" * 64
        parse_projection_bytes(_wire(document), self.limits)
        document["target_ref"] += "é"
        self.assertRefused(document)

    def test_dump_and_hash_revalidate_instead_of_coercing_invalid_dtos(self):
        value = parse_projection_bytes(_wire(_document()), self.limits)
        for bad in (replace(value, allowed_effects=[]),
                    replace(value, correlation_ids="c1"),
                    replace(value, service=object()), b"{}"):
            with self.subTest(kind=type(bad).__name__):
                with self.assertRaises(TechnicalProjectionError):
                    dump_projection_canonical(bad, self.limits)
                with self.assertRaises(TechnicalProjectionError):
                    projection_sha256(bad, self.limits)
