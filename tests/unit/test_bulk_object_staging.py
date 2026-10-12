"""B04 : métadonnées et intégrité synthétiques, aucune autorisation déduite."""

import hashlib
import unittest
from datetime import datetime, timedelta, timezone, tzinfo
from dataclasses import FrozenInstanceError

import pixs.backend.bulk_object_staging as runtime
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from unit.test_bulk_runtime_contracts import (
    _Hostile, _ForeignDict, _ForeignStr, _ForeignInt, _HashOnce,
)
from unit.test_bulk_execution_values import _valid_policy


_DATA = b"synthetic private input\n"
_NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _metadata():
    return {
        "object_reference": "object-test", "version_reference": "version-test",
        "tenant_reference": "tenant-test", "scope_reference": None,
        "classification_reference": "classification-test", "size_bytes": len(_DATA),
        "sha256": hashlib.sha256(_DATA).hexdigest(), "media_type": "text/csv",
        "is_private": True, "expires_at": _NOW + timedelta(hours=1),
        "retention_policy_reference": "retention-test",
    }


def _new(**updates):
    kwargs = {
        "metadata": _metadata(), "expected_metadata": _metadata(),
        "policy": _valid_policy(), "deadline": _NOW + timedelta(seconds=60),
        "now": _NOW, "cancelled": False,
    }
    kwargs.update(updates)
    verifier, refusals = runtime.new_object_integrity_verifier(**kwargs)
    return verifier, refusals


def _good(**updates):
    verifier, refusals = _new(**updates)
    if verifier is None or refusals:
        raise AssertionError("valid synthetic object declarations refused")
    return verifier


def _finish(verifier, **updates):
    kwargs = {"observed_metadata": _metadata(), "now": _NOW, "cancelled": False}
    kwargs.update(updates)
    return verifier.finish(**kwargs)


class _ForeignTimezone(tzinfo):
    def utcoffset(self, value):
        raise AssertionError("foreign tz callback")

    def dst(self, value):
        raise AssertionError("foreign tz callback")

    def tzname(self, value):
        raise AssertionError("foreign tz callback")


class _ForeignDatetime(datetime):
    @property
    def tzinfo(self):
        raise AssertionError("foreign datetime attribute")


class _ForeignBytes(bytes):
    def __len__(self):
        raise AssertionError("foreign length")

    def __bool__(self):
        raise AssertionError("foreign bool")


class _Storage:
    """Provider purement synthétique, structure seule sans garantie de production."""

    def stat_private(self, *args, **kwargs):
        raise AssertionError("no storage invocation")

    def iter_bytes(self, *args, **kwargs):
        raise AssertionError("no storage invocation")

    def begin_private_write(self, *args, **kwargs):
        raise AssertionError("no storage invocation")

    def finalize_private_write(self, *args, **kwargs):
        raise AssertionError("no storage invocation")

    def revoke(self, *args, **kwargs):
        raise AssertionError("no storage invocation")

    def purge_authorized(self, *args, **kwargs):
        raise AssertionError("no storage invocation")


class BulkObjectStagingTests(unittest.TestCase):
    def assert_refusals(self, result):
        self.assertIs(type(result), list)
        self.assertTrue(result)
        for diagnostic in result:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertNotIn("LEAK-MARKER", str(diagnostic))
        keys = [(d.element, d.constraint, d.message) for d in result]
        self.assertEqual(keys, sorted(set(keys)))

    def test_exports_exact(self):
        self.assertEqual(runtime.__all__, [
            "validate_object_metadata_values", "new_object_integrity_verifier",
            "validate_object_storage_contract",
        ])

    def test_valid_metadata_and_explicit_nullable_scope(self):
        self.assertEqual(runtime.validate_object_metadata_values(_metadata()), [])
        self.assertEqual(runtime.validate_object_metadata_values({
            **_metadata(), "scope_reference": "scope-test",
        }), [])

    def test_each_key_missing_and_unknown_refused(self):
        for key in _metadata():
            value = _metadata()
            del value[key]
            self.assert_refusals(runtime.validate_object_metadata_values(value))
        self.assert_refusals(runtime.validate_object_metadata_values({
            **_metadata(), "LEAK-MARKER": _Hostile(),
        }))

    def test_foreign_roots_and_every_slot_refused_before_hooks(self):
        for value in (_Hostile(), _ForeignDict(_metadata()), None):
            self.assert_refusals(runtime.validate_object_metadata_values(value))
        for key in _metadata():
            value = _metadata()
            value[key] = _Hostile()
            self.assert_refusals(runtime.validate_object_metadata_values(value))

    def test_foreign_key_never_rehashed(self):
        key = _HashOnce()
        value = _metadata()
        value[key] = _Hostile()
        self.assert_refusals(runtime.validate_object_metadata_values(value))
        self.assertEqual(key.calls, 1)

    def test_opaque_references_exact_without_normalization(self):
        fields = (
            "object_reference", "version_reference", "tenant_reference",
            "scope_reference", "classification_reference", "retention_policy_reference",
        )
        for field in fields:
            for bad in ("", "LEAK-MARKER\x00", "\ud800", _ForeignStr("ref")):
                self.assert_refusals(runtime.validate_object_metadata_values({
                    **_metadata(), field: bad,
                }))
        value = {**_metadata(), "tenant_reference": " tenant-test "}
        self.assertEqual(runtime.validate_object_metadata_values(value), [])
        self.assertEqual(value["tenant_reference"], " tenant-test ")

    def test_size_integer_domain_and_private_boolean(self):
        for bad in (True, -1, _ForeignInt(1), 1.0):
            self.assert_refusals(runtime.validate_object_metadata_values({
                **_metadata(), "size_bytes": bad,
            }))
        for bad in (False, 1, "True", None):
            self.assert_refusals(runtime.validate_object_metadata_values({
                **_metadata(), "is_private": bad,
            }))

    def test_sha_lowercase_hex64_and_media_exact(self):
        for bad in ("a"*63, "a"*65, "A"*64, "g"*64, _ForeignStr("a"*64)):
            self.assert_refusals(runtime.validate_object_metadata_values({
                **_metadata(), "sha256": bad,
            }))
        for bad in ("TEXT/CSV", "text/plain", "", _ForeignStr("text/csv")):
            self.assert_refusals(runtime.validate_object_metadata_values({
                **_metadata(), "media_type": bad,
            }))
        self.assertEqual(runtime.validate_object_metadata_values({
            **_metadata(), "media_type": "application/x-ndjson",
        }), [])

    def test_datetime_exact_utc_without_foreign_tz_callbacks(self):
        for bad in (
            datetime(2026,1,1),
            datetime(2026,1,1,tzinfo=timezone(timedelta(hours=2))),
            datetime(2026,1,1,tzinfo=_ForeignTimezone()),
            _ForeignDatetime(2026,1,1,tzinfo=timezone.utc),
        ):
            self.assert_refusals(runtime.validate_object_metadata_values({
                **_metadata(), "expires_at": bad,
            }))

    def test_factory_each_foreign_argument_is_refused(self):
        for key in ("metadata", "expected_metadata", "policy", "deadline", "now", "cancelled"):
            verifier, refusals = _new(**{key: _Hostile()})
            self.assertIsNone(verifier)
            self.assert_refusals(refusals)

    def test_factory_context_divergence_all_fields_refused(self):
        values = {
            "object_reference":"other-object", "version_reference":"other-version",
            "tenant_reference":"other-tenant", "scope_reference":"scope-test",
            "classification_reference":"other-class", "size_bytes":len(_DATA)+1,
            "sha256":"a"*64, "media_type":"application/x-ndjson",
            "expires_at":_NOW+timedelta(hours=2), "retention_policy_reference":"other-retention",
        }
        for key, value in values.items():
            verifier, refusals = _new(metadata={**_metadata(),key:value})
            self.assertIsNone(verifier)
            self.assert_refusals(refusals)

    def test_factory_expired_deadline_metadata_or_cancelled_refused(self):
        for kwargs in (
            {"deadline":_NOW}, {"now":_NOW+timedelta(seconds=60)},
            {"metadata":{**_metadata(),"expires_at":_NOW}, "expected_metadata":{**_metadata(),"expires_at":_NOW}},
            {"cancelled":True},
        ):
            verifier, refusals = _new(**kwargs)
            self.assertIsNone(verifier)
            self.assert_refusals(refusals)

    def test_factory_budget_and_invalid_boolean_clock_refused(self):
        policy = _valid_policy()
        policy["max_input_bytes"] = len(_DATA)-1
        for kwargs in (
            {"policy":policy}, {"cancelled":1},
            {"deadline":datetime(2026,1,1,tzinfo=_ForeignTimezone())},
            {"now":_ForeignDatetime(2026,1,1,tzinfo=timezone.utc)},
        ):
            verifier, refusals = _new(**kwargs)
            self.assertIsNone(verifier)
            self.assert_refusals(refusals)

    def test_integrity_complete_sha_and_size_really_checked(self):
        verifier = _good()
        self.assertEqual(verifier.feed(_DATA,now=_NOW,cancelled=False), [])
        result = _finish(verifier)
        self.assertTrue(result.complete)
        self.assertEqual(result.as_values()["complete"], True)
        self.assertEqual(result.diagnostics, ())

    def test_integrity_all_byte_boundaries(self):
        for split in range(len(_DATA)+1):
            verifier = _good()
            self.assertEqual(verifier.feed(_DATA[:split],now=_NOW,cancelled=False), [])
            self.assertEqual(verifier.feed(_DATA[split:],now=_NOW,cancelled=False), [])
            self.assertTrue(_finish(verifier).complete)

    def test_same_size_wrong_hash_and_truncation_refused(self):
        for data in (b"x"*len(_DATA), _DATA[:-1], b""):
            verifier = _good()
            verifier.feed(data,now=_NOW,cancelled=False)
            result = _finish(verifier)
            self.assertFalse(result.complete)
            self.assertTrue(result.diagnostics)

    def test_announced_hash_wrong_even_when_metadata_equal(self):
        metadata = {**_metadata(),"sha256":"a"*64}
        verifier = _good(metadata=metadata,expected_metadata=metadata)
        verifier.feed(_DATA,now=_NOW,cancelled=False)
        result = _finish(verifier,observed_metadata=metadata)
        self.assertFalse(result.complete)

    def test_oversized_chunk_and_total_never_complete(self):
        policy = _valid_policy()
        policy["read_chunk_bytes"]=4
        verifier = _good(policy=policy)
        self.assert_refusals(verifier.feed(_DATA,now=_NOW,cancelled=False))
        self.assertFalse(_finish(verifier).complete)
        verifier = _good()
        self.assert_refusals(verifier.feed(_DATA+b"x",now=_NOW,cancelled=False))
        self.assertFalse(_finish(verifier).complete)

    def test_foreign_chunk_and_dynamic_clock_before_behavior(self):
        for chunk, now, cancelled in (
            (_Hostile(),_NOW,False), (_ForeignBytes(b"x"),_NOW,False),
            ("bytes",_NOW,False), (_DATA,_Hostile(),False),
            (_DATA,datetime(2026,1,1,tzinfo=_ForeignTimezone()),False),
            (_DATA,_NOW,_Hostile()),
        ):
            verifier = _good()
            self.assert_refusals(verifier.feed(chunk,now=now,cancelled=cancelled))
            self.assertFalse(_finish(verifier).complete)

    def test_expiry_or_cancel_during_feed_refused(self):
        for now, cancelled in ((_NOW+timedelta(seconds=60),False),(_NOW,True)):
            verifier = _good()
            self.assert_refusals(verifier.feed(_DATA,now=now,cancelled=cancelled))
            self.assertFalse(_finish(verifier).complete)

    def test_expiry_or_cancel_fresh_at_eof_refused(self):
        for now, cancelled in ((_NOW+timedelta(seconds=60),False),(_NOW,True)):
            verifier = _good()
            verifier.feed(_DATA,now=_NOW,cancelled=False)
            result = _finish(verifier,now=now,cancelled=cancelled)
            self.assertFalse(result.complete)
            self.assertTrue(result.diagnostics)
            self.assertIs(type(result.diagnostics), tuple)

    def test_observed_version_drift_at_eof_refused(self):
        verifier = _good()
        verifier.feed(_DATA,now=_NOW,cancelled=False)
        self.assertFalse(_finish(verifier,observed_metadata={
            **_metadata(),"version_reference":"version-other",
        }).complete)

    def test_every_observed_context_drift_at_eof_refused(self):
        for updates in (
            {"tenant_reference":"other"}, {"scope_reference":"scope-other"},
            {"classification_reference":"class-other"},
            {"media_type":"application/x-ndjson"},
            {"sha256":"a"*64}, {"size_bytes":len(_DATA)+1},
            {"object_reference":"object-other"}, {"retention_policy_reference":"ret-other"},
        ):
            verifier = _good()
            verifier.feed(_DATA,now=_NOW,cancelled=False)
            self.assertFalse(_finish(verifier,observed_metadata={**_metadata(),**updates}).complete)

    def test_foreign_observed_metadata_at_eof_refused(self):
        verifier = _good()
        verifier.feed(_DATA,now=_NOW,cancelled=False)
        result = _finish(verifier,observed_metadata=_ForeignDict(_metadata()))
        self.assertFalse(result.complete)

    def test_terminal_result_immutable_idempotent_and_no_double_count(self):
        verifier = _good()
        verifier.feed(_DATA,now=_NOW,cancelled=False)
        result = _finish(verifier)
        before = result.as_values()
        self.assertIs(_finish(verifier), result)
        with self.assertRaises(ValueError):
            verifier.feed(b"x",now=_NOW,cancelled=False)
        self.assertEqual(result.as_values(),before)
        with self.assertRaises((FrozenInstanceError,AttributeError)):
            result.complete=False

    def test_close_incomplete_and_foreign_reason(self):
        verifier = _good()
        with self.assertRaises(ValueError):
            verifier.close(_Hostile())
        verifier.feed(_DATA[:3],now=_NOW,cancelled=False)
        verifier.close("CANCELLED")
        self.assertFalse(_finish(verifier).complete)

    def test_inputs_owned_after_factory_and_result_dict_is_fresh(self):
        metadata, expected, policy = _metadata(),_metadata(),_valid_policy()
        verifier = _good(metadata=metadata,expected_metadata=expected,policy=policy)
        metadata["sha256"]="a"*64
        expected["version_reference"]="mutated"
        policy["read_chunk_bytes"]=1
        verifier.feed(_DATA,now=_NOW,cancelled=False)
        result = _finish(verifier)
        self.assertTrue(result.complete)
        rendered=result.as_values()
        rendered["complete"]=False
        self.assertTrue(result.as_values()["complete"])

    def test_storage_structure_checks_no_methods_called(self):
        self.assertEqual(runtime.validate_object_storage_contract(_Storage()), [])
        self.assert_refusals(runtime.validate_object_storage_contract(None))
        self.assert_refusals(runtime.validate_object_storage_contract(object()))

    def test_storage_structure_does_not_run_properties_or_getattr(self):
        calls=[]
        class PropertyStorage:
            @property
            def stat_private(self):
                calls.append("property")
                raise AssertionError("property executed")
        class DynamicStorage:
            def __getattr__(self,name):
                calls.append("getattr")
                raise AssertionError("getattr executed")
        self.assert_refusals(runtime.validate_object_storage_contract(PropertyStorage()))
        self.assert_refusals(runtime.validate_object_storage_contract(DynamicStorage()))
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
