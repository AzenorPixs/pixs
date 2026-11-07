"""TEST C08 confirmation PostgreSQL 1.0 : forme et octets seulement."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import unittest

from pixs.backend.installation.postgresql_confirmation import (
    Confirmation,
    ConfirmationError,
    ConfirmationLimits,
    confirmation_binding,
    confirmation_sha256,
    dump_confirmation,
    match_confirmation_bundle,
    parse_confirmation,
)
from pixs.backend.installation.planning_bundle import (
    PlanningBundleError,
    dump_planning_bundle,
)
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError,
)
from c08_e5_fixtures import (
    TEST_CONFIRMED_AT,
    make_deferred_graph,
    make_limits,
    make_reuse_graph,
)


CONF_SCHEMA = "pixs.c08.postgresql-confirmation.v1"
CONF_VERSION = "1.0.0"
CONF_FIELDS = (
    "schema",
    "schema_version",
    "confirmation_ref",
    "installation_ref",
    "target_ref",
    "operation_id",
    "operator_ref",
    "projection_binding",
    "observation_binding",
    "plan_binding",
    "preconditions_binding",
    "effects_binding",
    "policy_ref",
    "policy_version",
    "confirmed_at",
    "correlation_id",
)
OTHER_AT = "2027-05-06T07:08:09.123456Z"
OLD_AT = "2000-01-01T00:00:00.000000Z"


def _raw_doc(value, limits):
    return json.loads(dump_confirmation(value, limits).decode("utf-8"))


def _raw_with(value, limits, **over):
    doc = _raw_doc(value, limits)
    doc.update(over)
    return json.dumps(
        doc,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _raw_with_allow_nan(value, limits, **over):
    doc = _raw_doc(value, limits)
    doc.update(over)
    return json.dumps(
        doc,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=True,
    ).encode("utf-8")


class TestC08PostgresqlConfirmation(unittest.TestCase):
    def test_schema_and_fields_exact(self):
        g = make_reuse_graph("conf-exact-a")
        self.assertEqual(g.confirmation.schema, CONF_SCHEMA)
        self.assertEqual(g.confirmation.schema_version, CONF_VERSION)
        doc = _raw_doc(g.confirmation, g.limits.confirmation_limits)
        self.assertEqual(set(doc), set(CONF_FIELDS))
        self.assertEqual(len(doc), 16)

    def test_bindings_shape_from_dump(self):
        g = make_reuse_graph("conf-shape-a")
        doc = _raw_doc(g.confirmation, g.limits.confirmation_limits)
        for name in (
            "projection_binding",
            "observation_binding",
            "plan_binding",
            "preconditions_binding",
            "effects_binding",
        ):
            self.assertEqual(set(doc[name]), {"ref", "version", "sha256"})
            self.assertIs(type(getattr(g.confirmation, name)), ContentBinding)

    def test_four_versions_imposed(self):
        g = make_reuse_graph("conf-v4-a")
        self.assertEqual(g.confirmation.projection_binding.version, "1.0.0")
        self.assertEqual(g.confirmation.observation_binding.version, "1.0.0")
        self.assertEqual(g.confirmation.preconditions_binding.version, "1.0.0")
        self.assertEqual(g.confirmation.effects_binding.version, "1.0.0")

    def test_four_versions_refused_if_20(self):
        g = make_reuse_graph("conf-v4-b")
        lim = g.limits.confirmation_limits
        for name in (
            "projection_binding",
            "observation_binding",
            "preconditions_binding",
            "effects_binding",
        ):
            with self.subTest(name=name):
                doc = _raw_doc(g.confirmation, lim)
                doc[name] = {"ref": "r-test", "version": "2.0", "sha256": "a" * 64}
                raw = json.dumps(doc, ensure_ascii=False, sort_keys=True,
                                 separators=(",", ":"), allow_nan=False).encode("utf-8")
                with self.assertRaises(ConfirmationError):
                    parse_confirmation(raw, lim)

    def test_schema_version_roots_unknown(self):
        g = make_reuse_graph("conf-root-a")
        lim = g.limits.confirmation_limits
        with self.assertRaises(ConfirmationError):
            parse_confirmation(_raw_with(g.confirmation, lim, schema="pixs.unknown"), lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(_raw_with(g.confirmation, lim, schema_version="2.0.0"), lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(_raw_with(g.confirmation, lim, schema_version="9.9.9"), lim)

    def test_str_subclass_rejected_on_constructor(self):
        class S(str):
            pass
        g = make_reuse_graph("conf-sub-a")
        for kwargs in ({"operator_ref": S("operator-test-x")},
                       {"schema": S(CONF_SCHEMA)},
                       {"schema_version": S("1.0.0")}):
            with self.subTest(kwargs=list(kwargs)):
                with self.assertRaises(ConfirmationError):
                    dataclasses.replace(g.confirmation, **kwargs)

    def test_plan_version_opaque_valid_alone(self):
        g = make_reuse_graph("conf-opaque-a")
        lim = g.limits.confirmation_limits
        other = ContentBinding(ref=g.confirmation.plan_binding.ref,
                               version="opaque-v9-test",
                               sha256=g.confirmation.plan_binding.sha256)
        c2 = dataclasses.replace(g.confirmation, plan_binding=other)
        self.assertEqual(parse_confirmation(dump_confirmation(c2, lim), lim), c2)

    def test_plan_version_opaque_distinct_refused_match(self):
        g = make_reuse_graph("conf-opaque-b")
        lim = g.limits.confirmation_limits
        other = ContentBinding(ref=g.confirmation.plan_binding.ref,
                               version="opaque-v9-test",
                               sha256=g.confirmation.plan_binding.sha256)
        c2 = dataclasses.replace(g.confirmation, plan_binding=other)
        dump_confirmation(c2, lim)
        with self.assertRaises(ConfirmationError):
            match_confirmation_bundle(c2, lim, g.bundle, g.limits.bundle_limits)

    def test_digest_wellformed_accepted_alone_refused_match(self):
        g = make_reuse_graph("conf-digest-a")
        lim = g.limits.confirmation_limits
        other = ContentBinding(ref=g.confirmation.projection_binding.ref,
                               version="1.0.0", sha256="f" * 64)
        c2 = dataclasses.replace(g.confirmation, projection_binding=other)
        self.assertEqual(parse_confirmation(dump_confirmation(c2, lim), lim), c2)
        dump_confirmation(c2, lim)
        with self.assertRaises(ConfirmationError):
            match_confirmation_bundle(c2, lim, g.bundle, g.limits.bundle_limits)

    def test_roundtrips(self):
        for mk, suffix in ((make_reuse_graph, "conf-rt-a"), (make_deferred_graph, "conf-rt-b")):
            with self.subTest(suffix=suffix):
                g = mk(suffix)
                lim = g.limits.confirmation_limits
                self.assertEqual(parse_confirmation(dump_confirmation(g.confirmation, lim), lim), g.confirmation)

    def test_sha_and_binding_external(self):
        g = make_reuse_graph("conf-sha-a")
        lim = g.limits.confirmation_limits
        raw = dump_confirmation(g.confirmation, lim)
        self.assertEqual(confirmation_sha256(g.confirmation, lim), hashlib.sha256(raw).hexdigest())
        b = confirmation_binding(g.confirmation, lim)
        self.assertEqual(b.ref, g.confirmation.confirmation_ref)
        self.assertEqual(b.version, "1.0.0")
        self.assertEqual(b.sha256, confirmation_sha256(g.confirmation, lim))
        a = make_reuse_graph("conf-sha-b")
        c = make_deferred_graph("conf-sha-c")
        self.assertNotEqual(confirmation_sha256(a.confirmation, a.limits.confirmation_limits),
                            confirmation_sha256(c.confirmation, c.limits.confirmation_limits))

    def test_no_self_binding_signature_acte_a07(self):
        g = make_reuse_graph("conf-noself-a")
        doc = _raw_doc(g.confirmation, g.limits.confirmation_limits)
        for k in ("signature", "mandate", "mandate_ref", "act", "withdrawal",
                  "correlation_ids", "causation_ids", "plan_digest", "bundle", "future"):
            self.assertNotIn(k, doc)

    def test_confirmed_at_len27_ascii(self):
        g = make_reuse_graph("conf-utc-a")
        v = g.confirmation.confirmed_at
        self.assertEqual(len(v), 27)
        v.encode("ascii")
        self.assertEqual(v, TEST_CONFIRMED_AT)

    def test_confirmed_at_forms_invalid(self):
        g = make_reuse_graph("conf-utc-b")
        lim = g.limits.confirmation_limits
        bads = (
            "2026-01-02 00:00:00.000000Z",
            "2026/01/02T00:00:00.000000Z",
            "2026-01-02T00:00:00.000000+00:00",
            "2026-01-02t00:00:00.000000z",
            "2026-01-02T00:00:00.00000Z",
            "2026-01-02T00:00:00.0000000Z",
            "2026-13-02T00:00:00.000000Z",
            "２０２６-01-02T00:00:00.000000Z",
        )
        for v in bads:
            with self.subTest(v=v):
                with self.assertRaises(ConfirmationError):
                    parse_confirmation(_raw_with(g.confirmation, lim, confirmed_at=v), lim)

    def test_confirmed_at_impossible_cause_exact(self):
        g = make_reuse_graph("conf-utc-c")
        lim = g.limits.confirmation_limits
        with self.assertRaises(ConfirmationError) as ctx:
            parse_confirmation(_raw_with(g.confirmation, lim, confirmed_at="2026-02-30T00:00:00.000000Z"), lim)
        self.assertIs(type(ctx.exception.__cause__), ValueError)

    def test_unknown_missing_duplicate(self):
        g = make_reuse_graph("conf-doc-a")
        lim = g.limits.confirmation_limits
        with self.assertRaises(ConfirmationError):
            parse_confirmation(_raw_with(g.confirmation, lim, signature="x"), lim)
        doc = _raw_doc(g.confirmation, lim)
        del doc["policy_ref"]
        raw = json.dumps(doc, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
        with self.assertRaises(ConfirmationError):
            parse_confirmation(raw, lim)
        raw = dump_confirmation(g.confirmation, lim)
        text = raw.decode("utf-8")
        self.assertEqual(text.count('"schema":'), 1)
        dup = raw[:-1] + b',"schema":"x"}'
        self.assertEqual(dup.decode("utf-8").count('"schema":'), 2)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(dup, lim)
        proj_ref = g.confirmation.projection_binding.ref
        old = '"ref":"' + proj_ref + '"'
        self.assertEqual(text.count(old), 1)
        nested = text.replace(old, old + ',"ref":"' + proj_ref + '"', 1)
        self.assertNotEqual(nested, text)
        self.assertEqual(nested.count(old), 2)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(nested.encode("utf-8"), lim)

    def test_bool_numbers_nan_inf(self):
        g = make_reuse_graph("conf-num-a")
        lim = g.limits.confirmation_limits
        for v in (True, False, 0, 1.5):
            with self.subTest(v=v):
                doc = _raw_doc(g.confirmation, lim)
                doc["operator_ref"] = v
                raw = json.dumps(doc, ensure_ascii=False, sort_keys=True,
                                 separators=(",", ":"), allow_nan=False).encode("utf-8")
                with self.assertRaises(ConfirmationError):
                    parse_confirmation(raw, lim)
        for v in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(v=v):
                with self.assertRaises(ConfirmationError):
                    parse_confirmation(_raw_with_allow_nan(g.confirmation, lim, operator_ref=v), lim)

    def test_wire_bytes_forms(self):
        g = make_reuse_graph("conf-wire-a")
        lim = g.limits.confirmation_limits
        raw = dump_confirmation(g.confirmation, lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(raw + b"\n", lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(b"\xef\xbb\xbf" + raw, lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(raw[:20] + b"\xff" + raw[20:], lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation("x", lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(bytearray(raw), lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(None, lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(object(), lim)
        text = raw.decode("utf-8")
        old = json.dumps(g.confirmation.operator_ref)
        self.assertEqual(text.count(old), 1)
        bad = text.replace(old, '"\\ud800"', 1)
        self.assertNotEqual(bad, text)
        self.assertEqual(bad.count(old), 0)
        self.assertEqual(bad.count('"\\ud800"'), 1)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(bad.encode("utf-8"), lim)
        self.assertEqual(parse_confirmation(raw, lim), g.confirmation)

    def test_utf8_ref_exact_and_max_bytes_exact(self):
        g = make_reuse_graph("conf-bounds-a")
        lim = g.limits.confirmation_limits
        ok = dataclasses.replace(g.confirmation, operator_ref="é" * 64)
        self.assertEqual(len(ok.operator_ref.encode("utf-8")), 128)
        self.assertEqual(parse_confirmation(dump_confirmation(ok, lim), lim), ok)
        over = dataclasses.replace(g.confirmation, operator_ref="é" * 64 + "a")
        self.assertEqual(len(over.operator_ref.encode("utf-8")), 129)
        with self.assertRaises(ConfirmationError):
            dump_confirmation(over, lim)
        raw = dump_confirmation(g.confirmation, lim)
        exact = ConfirmationLimits(payload=g.limits.payload, max_confirmation_bytes=len(raw))
        self.assertEqual(parse_confirmation(raw, exact), g.confirmation)
        short = ConfirmationLimits(payload=g.limits.payload, max_confirmation_bytes=len(raw) - 1)
        with self.assertRaises(ConfirmationError):
            dump_confirmation(g.confirmation, short)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(raw, short)

    def test_wrappers_frozen_and_bad_public_types(self):
        lim0 = make_limits()
        for kwargs in ({"payload": True, "max_confirmation_bytes": 10},
                       {"payload": lim0.payload, "max_confirmation_bytes": True},
                       {"payload": lim0.payload, "max_confirmation_bytes": False},
                       {"payload": lim0.payload, "max_confirmation_bytes": 0},
                       {"payload": object(), "max_confirmation_bytes": 10}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ConfirmationError):
                    ConfirmationLimits(**kwargs)
        g = make_reuse_graph("conf-wrap-a")
        lim = g.limits.confirmation_limits
        with self.assertRaises(dataclasses.FrozenInstanceError):
            g.confirmation.operator_ref = "x"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            lim.max_confirmation_bytes = 10
        for fn in (lambda: dump_confirmation("x", lim),
                   lambda: dump_confirmation(None, lim),
                   lambda: dump_confirmation(g.confirmation, "x"),
                   lambda: dump_confirmation(g.confirmation, None),
                   lambda: confirmation_sha256(g.confirmation, "x"),
                   lambda: confirmation_sha256("x", lim),
                   lambda: confirmation_binding(g.confirmation, "x"),
                   lambda: confirmation_binding("x", lim),
                   lambda: parse_confirmation("x", lim),
                   lambda: parse_confirmation(bytearray(b"{}"), lim),
                   lambda: parse_confirmation(b"{}", "x")):
            with self.assertRaises(ConfirmationError):
                fn()

    def test_constructors_invalid_direct(self):
        g = make_reuse_graph("conf-ctor-a")
        lim = g.limits.confirmation_limits
        with self.assertRaises(ConfirmationError):
            Confirmation(schema="bad", schema_version="1.0.0", confirmation_ref="a",
                         installation_ref="b", target_ref="c", operation_id="d",
                         operator_ref="e", projection_binding=g.confirmation.projection_binding,
                         observation_binding=g.confirmation.observation_binding,
                         plan_binding=g.confirmation.plan_binding,
                         preconditions_binding=g.confirmation.preconditions_binding,
                         effects_binding=g.confirmation.effects_binding,
                         policy_ref="p", policy_version="1.0.0",
                         confirmed_at=TEST_CONFIRMED_AT, correlation_id="k")
        with self.assertRaises(ConfirmationError):
            parse_confirmation(b"{}", lim)

    def test_match_positive_and_unmutated(self):
        g = make_reuse_graph("conf-match-a")
        lim = g.limits.confirmation_limits
        before = dump_planning_bundle(g.bundle, g.limits.bundle_limits)
        self.assertIsNone(match_confirmation_bundle(g.confirmation, lim, g.bundle, g.limits.bundle_limits))
        self.assertEqual(dump_planning_bundle(g.bundle, g.limits.bundle_limits), before)

    def test_match_operator_dates_positive(self):
        g = make_reuse_graph("conf-match-b")
        lim = g.limits.confirmation_limits
        for c2 in (dataclasses.replace(g.confirmation, operator_ref="operator-other-test"),
                   dataclasses.replace(g.confirmation, confirmed_at=OTHER_AT),
                   dataclasses.replace(g.confirmation, confirmed_at=OLD_AT)):
            dump_confirmation(c2, lim)
            self.assertIsNone(match_confirmation_bundle(c2, lim, g.bundle, g.limits.bundle_limits))

    def test_match_negative_scalar_refs(self):
        for i, name in enumerate(("confirmation_ref", "installation_ref", "target_ref",
                                  "operation_id", "correlation_id", "policy_ref", "policy_version")):
            with self.subTest(name=name):
                g = make_reuse_graph(f"conf-neg{i}-a")
                lim = g.limits.confirmation_limits
                c2 = dataclasses.replace(g.confirmation, **{name: "other-" + name})
                dump_confirmation(c2, lim)
                with self.assertRaises(ConfirmationError):
                    match_confirmation_bundle(c2, lim, g.bundle, g.limits.bundle_limits)

    def test_match_negative_each_binding(self):
        base = make_reuse_graph("conf-negbind-a")
        lim = base.limits.confirmation_limits
        for name in ("projection_binding", "observation_binding",
                     "preconditions_binding", "effects_binding"):
            with self.subTest(name=name):
                old = getattr(base.confirmation, name)
                c2 = dataclasses.replace(base.confirmation, **{
                    name: ContentBinding(ref="other-" + name, version="1.0.0", sha256=old.sha256)})
                dump_confirmation(c2, lim)
                with self.assertRaises(ConfirmationError):
                    match_confirmation_bundle(c2, lim, base.bundle, base.limits.bundle_limits)
                c3 = dataclasses.replace(base.confirmation, **{
                    name: ContentBinding(ref=old.ref, version="1.0.0", sha256="e" * 64)})
                dump_confirmation(c3, lim)
                with self.assertRaises(ConfirmationError):
                    match_confirmation_bundle(c3, lim, base.bundle, base.limits.bundle_limits)
        oldp = base.confirmation.plan_binding
        for other in (ContentBinding(ref="other-plan", version=oldp.version, sha256=oldp.sha256),
                      ContentBinding(ref=oldp.ref, version=oldp.version, sha256="e" * 64),
                      ContentBinding(ref=oldp.ref, version="opaque-v9-test", sha256=oldp.sha256)):
            with self.subTest(other=other.version + other.ref[:5]):
                c4 = dataclasses.replace(base.confirmation, plan_binding=other)
                dump_confirmation(c4, lim)
                with self.assertRaises(ConfirmationError):
                    match_confirmation_bundle(c4, lim, base.bundle, base.limits.bundle_limits)

    def test_wire_binding_cause_exact(self):
        g = make_reuse_graph("conf-wire-b")
        lim = g.limits.confirmation_limits
        doc = _raw_doc(g.confirmation, lim)
        doc["projection_binding"] = {"ref": "", "version": "1.0.0", "sha256": "a" * 64}
        raw = json.dumps(doc, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
        with self.assertRaises(ConfirmationError) as ctx:
            parse_confirmation(raw, lim)
        self.assertIs(type(ctx.exception.__cause__), ContractError)

    def test_bundle_malformed_cause_exact(self):
        g = make_reuse_graph("conf-badbundle-a")
        lim = g.limits.confirmation_limits
        with self.assertRaises(ConfirmationError) as ctx:
            match_confirmation_bundle(g.confirmation, lim, None, g.limits.bundle_limits)
        self.assertIs(type(ctx.exception.__cause__), PlanningBundleError)

    def test_withdrawal_distinct(self):
        g = make_reuse_graph("conf-wd-a")
        lim = g.limits.confirmation_limits
        with self.assertRaises(ConfirmationError):
            parse_confirmation(_raw_with(g.confirmation, lim, schema="pixs.c08.postgresql-withdrawal.v1"), lim)
        with self.assertRaises(ConfirmationError):
            parse_confirmation(_raw_with(g.confirmation, lim, mandate_ref="m"), lim)


if __name__ == "__main__":
    unittest.main()
