"""Enveloppe EventEnvelopeV1 : frontières exactes, hostiles, UTC strict, délégation bornée."""

import unittest
from datetime import datetime, timezone, timedelta, tzinfo
from unittest import mock

import pixs.backend.bulk_event_envelope_values as envelope
import pixs.backend.bulk_runtime_contracts as contracts
from pixs.kernel.diagnostics import Diagnostic, VALIDATE


class _HostileMeta(type):
    def __eq__(self, other):
        raise AssertionError("foreign type comparison")

    def __hash__(self):
        raise AssertionError("foreign type hash")


class _Hostile(metaclass=_HostileMeta):
    def __bool__(self):
        raise AssertionError("foreign bool")

    def __eq__(self, other):
        raise AssertionError("foreign equality")

    def __hash__(self):
        raise AssertionError("foreign hash")

    def __str__(self):
        raise AssertionError("foreign str")

    def __repr__(self):
        raise AssertionError("foreign repr")

    def __iter__(self):
        raise AssertionError("foreign iteration")


class _ForeignDict(dict, metaclass=_HostileMeta):
    def items(self):
        raise AssertionError("foreign items")

    def keys(self):
        raise AssertionError("foreign keys")


class _ForeignList(list, metaclass=_HostileMeta):
    def __iter__(self):
        raise AssertionError("foreign iteration")


class _ForeignTuple(tuple, metaclass=_HostileMeta):
    def __iter__(self):
        raise AssertionError("foreign iteration")


class _ForeignStr(str, metaclass=_HostileMeta):
    def encode(self, *args, **kwargs):
        raise AssertionError("foreign encode")


class _ForeignInt(int, metaclass=_HostileMeta):
    pass


class _ForeignDatetime(datetime, metaclass=_HostileMeta):
    pass


class _HashOnce:
    def __init__(self):
        self.calls = 0

    def __hash__(self):
        self.calls += 1
        if self.calls > 1:
            raise AssertionError("foreign key rehashed")
        return 17

    def __eq__(self, other):
        raise AssertionError("foreign key compared")


def _valid_envelope(*, kind="DOMAIN"):
    return {
        "event_id": "event-test",
        "kind": kind,
        "event_type": "type-test",
        "event_version": "1.2.3",
        "producer_reference": "producer-test",
        "schema_reference": "schema-test",
        "order_scope_reference": "scope-test",
        "occurred_at": datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
        "subject_reference": "subject-test",
        "tenant_context_reference": "tenant-test",
        "correlation_id": "correlation-test",
        "causation_id": None,
        "payload": {"name": "value"},
    }


def _validate(values, **kwargs):
    # Bornes synthétiques de test, aucun défaut de production.
    params = {"max_depth": 8, "max_members": 10, "non_tenant_authorized": False}
    params.update(kwargs)
    return envelope.validate_bulk_event_envelope_values(values, **params)


class BulkEventEnvelopeValuesTests(unittest.TestCase):
    def assert_valid(self, value, **kwargs):
        before = dict(value)
        result = _validate(value, **kwargs)
        self.assertIs(type(result), list)
        self.assertEqual(result, [])
        self.assertIsNot(result, _validate(dict(value), **kwargs))
        self.assertEqual(value, before)

    def assert_refused(self, value, **kwargs):
        result = _validate(value, **kwargs)
        self.assertIs(type(result), list)
        self.assertTrue(result)
        for diagnostic in result:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertNotIn("LEAK-MARKER", str(diagnostic))
        keys = [(d.element, d.constraint, d.message) for d in result]
        self.assertEqual(keys, sorted(set(keys)))

    def test_exports_exact(self):
        self.assertEqual(envelope.__all__, ["validate_bulk_event_envelope_values"])

    def test_domain_and_integration_positive(self):
        for kind in ("DOMAIN", "INTEGRATION"):
            self.assert_valid(_valid_envelope(kind=kind))

    def test_missing_and_unknown_keys_refused_without_echo(self):
        for key in _valid_envelope():
            value = _valid_envelope()
            del value[key]
            self.assert_refused(value)
        value = _valid_envelope()
        value["LEAK-MARKER"] = _Hostile()
        self.assert_refused(value)

    def test_foreign_roots_keys_and_subclasses_without_hooks(self):
        self.assert_refused(_Hostile())
        self.assert_refused(_ForeignDict(_valid_envelope()))
        key = _HashOnce()
        value = _valid_envelope()
        value[key] = _Hostile()
        self.assert_refused(value)
        self.assertEqual(key.calls, 1)
        for field in (
            "event_id", "kind", "event_type", "event_version",
            "producer_reference", "schema_reference", "order_scope_reference",
            "subject_reference", "correlation_id",
        ):
            for bad in (_Hostile(), _ForeignStr("x"), True, 1):
                self.assert_refused({**_valid_envelope(), field: bad})
        self.assert_refused({**_valid_envelope(), "occurred_at": _ForeignDatetime(
            2026, 1, 2, tzinfo=timezone.utc)})
        self.assert_refused({**_valid_envelope(), "occurred_at": "2026-01-02T03:04:05+00:00"})

    def test_occurred_utc_exact_before_callbacks(self):
        for bad in (
            datetime(2026, 1, 2, 3, 4, 5),
            datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=1))),
            _Hostile(),
        ):
            value = {**_valid_envelope(), "occurred_at": bad}
            with mock.patch.object(
                envelope, "_is_complete_semver",
                side_effect=AssertionError("semver before utc guard")):
                with mock.patch.object(
                    envelope, "validate_json_value",
                    side_effect=AssertionError("helper before utc guard")):
                    self.assert_refused(value)

    def test_params_required_before_hostile_payload(self):
        hostile = {**_valid_envelope(), "payload": _Hostile()}
        for kwargs in (
            {}, {"max_depth": 0}, {"max_depth": True}, {"max_depth": _Hostile()},
            {"max_members": 0}, {"max_members": False}, {"max_members": _Hostile()},
            {"non_tenant_authorized": 1}, {"non_tenant_authorized": None},
            {"non_tenant_authorized": _Hostile()},
        ):
            base = {"max_depth": 8, "max_members": 10, "non_tenant_authorized": False}
            base.update(kwargs)
            if "max_depth" not in kwargs and "max_members" not in kwargs \
                    and "non_tenant_authorized" not in kwargs:
                continue
            with mock.patch.object(
                envelope, "validate_json_value",
                side_effect=AssertionError("helper before param guard")) as helper:
                result = envelope.validate_bulk_event_envelope_values(hostile, **base)
                self.assertTrue(result)
                helper.assert_not_called()

    def test_tenant_none_guard_and_causation_nullable(self):
        value = {**_valid_envelope(), "tenant_context_reference": None}
        self.assert_refused(value, non_tenant_authorized=False)
        self.assert_valid(value, non_tenant_authorized=True)
        self.assert_valid(_valid_envelope(), non_tenant_authorized=True)
        self.assert_valid(_valid_envelope(), non_tenant_authorized=False)
        self.assert_valid(
            {**_valid_envelope(), "causation_id": "cause-test"})
        self.assert_valid(
            {**_valid_envelope(), "tenant_context_reference": "t",
             "causation_id": "c"},
            non_tenant_authorized=True)

    def test_opaques_refused(self):
        for field in (
            "event_id", "event_type", "producer_reference", "schema_reference",
            "order_scope_reference", "subject_reference", "correlation_id",
            "tenant_context_reference", "causation_id",
        ):
            for bad in ("", "LEAK-MARKER\x00", "\ud800", _ForeignStr("x")):
                base = _valid_envelope()
                base[field] = bad
                if field == "causation_id":
                    self.assert_refused(base)
                else:
                    self.assert_refused(base)
        self.assert_refused({**_valid_envelope(), "kind": "UNKNOWN"})
        self.assert_refused({**_valid_envelope(), "kind": "domain"})
        for bad in ("not-semver", "", "1.2", "LEAK-MARKER\x00"):
            self.assert_refused({**_valid_envelope(), "event_version": bad})

    def test_payload_json_types_delegated(self):
        for payload in (
            None, False, True, 0, -1, 2**100, 0.0, 1.25, "", "\x00", "é😀",
            [], [None, True, 2, ""], {}, {"a": [1, {"b": None}]},
        ):
            self.assert_valid({**_valid_envelope(), "payload": payload})
        for payload in (
            float("nan"), float("inf"), float("-inf"), "\ud800", {"\ud800": 1},
            _Hostile(), _ForeignDict({"a": 1}), _ForeignList([1]),
            _ForeignStr("t"), _ForeignInt(1), (), b"bytes",
            datetime(2026, 1, 1, tzinfo=timezone.utc),
            {"a": _Hostile()}, [_Hostile()],
        ):
            self.assert_refused({**_valid_envelope(), "payload": payload})
        direct = []
        direct.append(direct)
        self.assert_refused({**_valid_envelope(), "payload": direct})
        self.assert_refused(
            {**_valid_envelope(), "payload": {"a": 1, "b": 2}},
            max_members=1)
        deep = 1
        for _ in range(60):
            deep = [deep]
        self.assert_refused(
            {**_valid_envelope(), "payload": deep},
            max_depth=8, max_members=100)

    def test_helper_called_once_only_when_metadata_valid(self):
        with mock.patch.object(
            envelope, "validate_json_value",
            wraps=contracts.validate_json_value) as helper:
            self.assertEqual(_validate(_valid_envelope()), [])
            helper.assert_called_once()
            _, kwargs = helper.call_args
            self.assertEqual(kwargs, {"max_depth": 8, "max_members": 10})
        with mock.patch.object(
            envelope, "validate_json_value",
            side_effect=AssertionError("helper must not run")) as helper:
            self.assert_refused({**_valid_envelope(), "kind": "UNKNOWN"})
            helper.assert_not_called()

    def test_diagnostics_fresh_dedup_without_echo_nor_capture(self):
        first = _validate({**_valid_envelope(), "kind": "UNKNOWN"})
        second = _validate({**_valid_envelope(), "kind": "UNKNOWN"})
        self.assertIsNot(first, second)
        self.assertEqual(first, second)
        value = _valid_envelope()
        snapshot = __import__("copy").deepcopy(value)
        _validate(value)
        self.assertEqual(value, snapshot)


class AdditionalEnvelopeBoundaryTests(unittest.TestCase):
    assert_valid = BulkEventEnvelopeValuesTests.assert_valid
    assert_refused = BulkEventEnvelopeValuesTests.assert_refused
    def test_required_parameters_no_defaults(self):
        all_params = {"max_depth": 8, "max_members": 10, "non_tenant_authorized": False}
        for missing in all_params:
            params = dict(all_params)
            del params[missing]
            with self.assertRaises(TypeError):
                envelope.validate_bulk_event_envelope_values(_valid_envelope(), **params)

    def test_foreign_tz_before_all_helpers(self):
        class BadZone(tzinfo):
            def utcoffset(self, value):
                raise AssertionError("foreign utcoffset")
        value = {**_valid_envelope(), "occurred_at": datetime(2026, 1, 1, tzinfo=BadZone())}
        with mock.patch.object(envelope, "_is_complete_semver", side_effect=AssertionError("semver too early")):
            with mock.patch.object(envelope, "validate_json_value", side_effect=AssertionError("JSON too early")):
                self.assert_refused(value)

    def test_json_limits_exact_edges(self):
        self.assert_valid({**_valid_envelope(), "payload": [[]]}, max_depth=2, max_members=1)
        self.assert_refused({**_valid_envelope(), "payload": [[]]}, max_depth=1, max_members=1)
        self.assert_valid({**_valid_envelope(), "payload": {"a": 1, "b": 2}}, max_members=2)
        self.assert_refused({**_valid_envelope(), "payload": {"a": 1, "b": 2}}, max_members=1)

    def test_json_foreign_key_before_hash(self):
        key = _HashOnce()
        payload = {key: 1}
        self.assert_refused({**_valid_envelope(), "payload": payload})
        self.assertEqual(key.calls, 1)

    def test_explicit_bounds_subclasses(self):
        for param in ("max_depth", "max_members"):
            for bad in (_ForeignInt(2), True, 1.0, None):
                self.assert_refused({**_valid_envelope(), "payload": _Hostile()}, **{param: bad})


if __name__ == "__main__":
    unittest.main()
