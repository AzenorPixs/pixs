"""Contrats de pagination Core : compatibilité et refus de valeurs étrangères, sans DB."""
from __future__ import annotations

import datetime
import unittest
from dataclasses import FrozenInstanceError

from pixs.core.authz.filter_plan import PROFILE_VERSION
from pixs.core.dto import CoreInputInvalid, CorePage, CorePageItem, CoreQueryInput
from pixs.core.scope.context import ScopeContext, ScopeType


_CONTEXT = ScopeContext(ScopeType.PLATFORM)
_NOW = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
_LATER = _NOW + datetime.timedelta(seconds=60)
_ONE = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f01"
_TWO = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f02"


def item(uid):
    return CorePageItem("USER", "pixs.core.user:" + uid, _CONTEXT, 1,
                        "ACTIVE", "RETAINED", None, None, None, (("user_id", uid),))


def page(items, next_after=None):
    return CorePage(items, PROFILE_VERSION, ("epoch", ()), _NOW, _LATER, "corr", next_after)


class CorePaginationDtoTest(unittest.TestCase):
    def test_legacy_constructors_preserve_defaults(self):
        query = CoreQueryInput(_CONTEXT, "corr", (), None)
        original = CorePage((item(_ONE),), PROFILE_VERSION, ("epoch", ()), _NOW, _LATER, "corr")
        self.assertIsNone(query.after)
        self.assertIsNone(query.page_limit)
        self.assertIsNone(original.next_after)
        self.assertEqual(original.items[0].ref, "pixs.core.user:" + _ONE)

    def test_query_after_requires_page_and_strict_positive_integer(self):
        with self.assertRaises(CoreInputInvalid):
            CoreQueryInput(_CONTEXT, "corr", (), None, after="ref")
        for value in (True, False, 0, -1, 2.0, "2"):
            with self.subTest(limit=value), self.assertRaises(CoreInputInvalid):
                CoreQueryInput(_CONTEXT, "corr", (), None, page_limit=value)
        query = CoreQueryInput(_CONTEXT, "corr", (), None, after="ref", page_limit=2)
        self.assertEqual((query.after, query.page_limit), ("ref", 2))

    def test_unknown_types_rejected_before_foreign_methods(self):
        calls = []
        class Foreign:
            def __eq__(self, other):
                calls.append("eq")
                raise AssertionError("METHODE_ETRANGERE")
            def __lt__(self, other):
                calls.append("lt")
                raise AssertionError("METHODE_ETRANGERE")
        foreign = Foreign()
        for kwargs in ({"after": foreign, "page_limit": 2}, {"page_limit": foreign}):
            with self.assertRaises(CoreInputInvalid):
                CoreQueryInput(_CONTEXT, "corr", (), None, **kwargs)
        with self.assertRaises(CoreInputInvalid):
            page((item(_ONE),), foreign)
        self.assertEqual(calls, [])

    def test_next_after_matches_only_last_visible_item(self):
        first, last = item(_ONE), item(_TWO)
        actual = page((first, last), last.ref)
        self.assertEqual(actual.next_after, actual.items[-1].ref)
        with self.assertRaises(CoreInputInvalid):
            page((first, last), first.ref)
        with self.assertRaises(CoreInputInvalid):
            page((first, last), "")

    def test_empty_page_cannot_publish_a_next_boundary(self):
        self.assertEqual(page(()).items, ())
        with self.assertRaises(CoreInputInvalid):
            page((), "pixs.core.user:" + _ONE)

    def test_pagination_fields_remain_frozen(self):
        query = CoreQueryInput(_CONTEXT, "corr", (), None, page_limit=2)
        actual = page((item(_ONE),), item(_ONE).ref)
        with self.assertRaises(FrozenInstanceError):
            query.after = "other"
        with self.assertRaises(FrozenInstanceError):
            actual.next_after = "other"



class CoreCursorCodecTest(unittest.TestCase):
    def setUp(self):
        from pixs.backend.api_core_pagination import CoreCursorBinding, CoreCursorCodec, CoreCursorConfig, CoreCursorError
        class Clock:
            value = _NOW
            def now(self):
                return self.value
        self.clock = Clock()
        self.Error, self.Binding, self.Config, self.Codec = CoreCursorError, CoreCursorBinding, CoreCursorConfig, CoreCursorCodec
        self.config = CoreCursorConfig(60, 8192, 512, 10, 10)
        # Vecteur public synthétique, jamais une clé de déploiement.
        self.key = b"public-test-cursor-signing-vector-0001"
        self.codec = CoreCursorCodec(config=self.config, key=self.key, clock=self.clock)
        self.binding = CoreCursorBinding("subject-a", _CONTEXT, "USER", (), 2)
        self.snapshot = ("epoch-a", (("policy-a", "1.0.0"),))
        self.after = "pixs.core.user:" + _ONE

    def token(self, binding=None, expires=None):
        return self.codec.encode(
            binding=self.binding if binding is None else binding, after=self.after,
            snapshot_version=self.snapshot,
            decision_expires_at=_NOW + datetime.timedelta(seconds=300) if expires is None else expires)

    def test_roundtrip_and_immutable_state(self):
        state = self.codec.decode(self.token(), binding=self.binding)
        self.assertEqual(state.after, self.after)
        self.assertIsNone(self.codec.verify_snapshot(state, snapshot_version=self.snapshot))
        with self.assertRaises(FrozenInstanceError):
            state.after = "other"

    def test_decision_expiration_caps_cursor_lifetime(self):
        deadline = _NOW + datetime.timedelta(seconds=7)
        token = self.token(expires=deadline)
        state = self.codec.decode(token, binding=self.binding)
        self.assertEqual(state.expires_at, deadline)
        self.clock.value = deadline
        with self.assertRaises(self.Error):
            self.codec.decode(token, binding=self.binding)
        with self.assertRaises(self.Error):
            self.codec.verify_snapshot(state, snapshot_version=self.snapshot)

    def test_ttl_and_clock_rollback_refuse(self):
        token = self.token()
        self.assertEqual(self.codec.decode(token, binding=self.binding).expires_at,
                         _NOW + datetime.timedelta(seconds=60))
        for when in (_NOW - datetime.timedelta(microseconds=1),
                     _NOW + datetime.timedelta(seconds=60)):
            self.clock.value = when
            with self.assertRaises(self.Error):
                self.codec.decode(token, binding=self.binding)

    def test_each_binding_dimension_is_checked(self):
        from dataclasses import replace
        changed = (
            replace(self.binding, subject_id="subject-b"),
            replace(self.binding, context=ScopeContext(ScopeType.TENANT, "tenant-b", None)),
            replace(self.binding, kind="GROUP"),
            replace(self.binding, resource_refs=(self.after,)),
            replace(self.binding, page_size=3),
        )
        token = self.token()
        for value in changed:
            with self.subTest(binding=value), self.assertRaises(self.Error):
                self.codec.decode(token, binding=value)

    def test_filter_order_is_normalized_and_duplicates_refused(self):
        first = self.Binding("subject-a", _CONTEXT, "USER", ("ref-b", "ref-a"), 2)
        second = self.Binding("subject-a", _CONTEXT, "USER", ("ref-a", "ref-b"), 2)
        self.assertEqual(self.codec.decode(self.token(first), binding=second).after, self.after)
        with self.assertRaises(self.Error):
            self.Binding("subject-a", _CONTEXT, "USER", ("ref-a", "ref-a"), 2)

    def test_snapshot_change_is_refused_before_exposure(self):
        state = self.codec.decode(self.token(), binding=self.binding)
        for version in (("epoch-b", self.snapshot[1]), ("epoch-a", (("policy-a", "2.0.0"),))):
            with self.subTest(snapshot=version), self.assertRaises(self.Error):
                self.codec.verify_snapshot(state, snapshot_version=version)

    def test_signature_tampering_and_other_key_refused(self):
        token = self.token()
        altered = token[:-1] + ("A" if token[-1] != "A" else "B")
        with self.assertRaises(self.Error):
            self.codec.decode(altered, binding=self.binding)
        other = self.Codec(config=self.config, key=b"public-test-cursor-signing-vector-0002", clock=self.clock)
        with self.assertRaises(self.Error):
            other.decode(token, binding=self.binding)

    def test_signed_payload_still_requires_closed_types_and_schema(self):
        source = self.codec._signer.unsign_object(self.token())
        changes = (
            {"extra": True}, {"version": "2.0.0"}, {"binding": False},
            {"snapshot": "A" * 64}, {"page_size": True}, {"after": chr(0)},
            {"issued_at": True}, {"expires_at": 1.5}, {"order": "other"},
            {"expires_at": source["issued_at"] + 61000000},
        )
        for change in changes:
            payload = dict(source, **change)
            token = self.codec._signer.sign_object(payload)
            with self.subTest(fields=tuple(change)), self.assertRaises(self.Error):
                self.codec.decode(token, binding=self.binding)
        missing = dict(source)
        del missing["after"]
        with self.assertRaises(self.Error):
            self.codec.decode(self.codec._signer.sign_object(missing), binding=self.binding)

    def test_bounds_unissued_formats_and_configuration(self):
        from dataclasses import replace
        small = self.Codec(config=replace(self.config, max_cursor_chars=10), key=self.key, clock=self.clock)
        with self.assertRaises(self.Error):
            small.encode(binding=self.binding, after=self.after,
                         snapshot_version=self.snapshot, decision_expires_at=_LATER)
        for value in ("." + self.token(), self.token() + ":extra", self.token() + chr(10)):
            with self.assertRaises(self.Error):
                self.codec.decode(value, binding=self.binding)
        with self.assertRaises(self.Error):
            self.Codec(config=self.config, key=b"short", clock=self.clock)
        with self.assertRaises(self.Error):
            self.Config(True, 8192, 512, 10, 10)
        with self.assertRaises(self.Error):
            self.codec.encode(binding=replace(self.binding, page_size=11), after=self.after,
                              snapshot_version=self.snapshot, decision_expires_at=_LATER)

    def test_non_utc_and_foreign_values_closed(self):
        self.clock.value = _NOW.astimezone(datetime.timezone(datetime.timedelta(hours=1)))
        with self.assertRaises(self.Error):
            self.token()
        calls = []
        class Foreign:
            def __str__(self):
                calls.append("str")
                raise AssertionError("METHODE_ETRANGERE")
            def __eq__(self, other):
                calls.append("eq")
                raise AssertionError("METHODE_ETRANGERE")
        with self.assertRaises(self.Error):
            self.Binding(Foreign(), _CONTEXT, "USER", (), 2)
        with self.assertRaises(self.Error):
            self.codec.decode(Foreign(), binding=self.binding)
        self.assertEqual(calls, [])

    def test_explicit_signer_does_not_configure_django(self):
        import subprocess
        import sys
        script = """
import datetime
from django.conf import settings
from pixs.backend.api_core_pagination import CoreCursorBinding, CoreCursorCodec, CoreCursorConfig
from pixs.core.scope.context import ScopeContext, ScopeType
assert not settings.configured
now = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
class Clock:
    def now(self):
        return now
codec = CoreCursorCodec(config=CoreCursorConfig(60, 8192, 512, 10, 10),
                        key=b'public-test-cursor-signing-vector-0001', clock=Clock())
binding = CoreCursorBinding('subject-a', ScopeContext(ScopeType.PLATFORM), 'USER', (), 2)
token = codec.encode(binding=binding, after='ref', snapshot_version=('epoch', ()),
                     decision_expires_at=now+datetime.timedelta(seconds=60))
assert codec.decode(token, binding=binding).after == 'ref'
assert not settings.configured
print('CURSOR_WITHOUT_SETTINGS_OK')
"""
        result = subprocess.run([sys.executable, "-B", "-c", script], capture_output=True,
                                text=True, env={"PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"}, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "CURSOR_WITHOUT_SETTINGS_OK")

if __name__ == "__main__":
    unittest.main()
