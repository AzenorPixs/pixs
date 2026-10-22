"""Contrat valeurs idempotence Core : cle complete, retention minimum, forges refuses."""

import dataclasses
import datetime
import unittest

from pixs.core.api_core_idempotency_values import (
    ApiCoreIdempotencyConfig,
    ApiCoreIdempotencyEntry,
    ApiCoreIdempotencyKey,
    ApiCoreIdempotencyProofInvalid,
    resolve_idempotency_key,
    validate_idempotency_entry,
)
from pixs.core.api_core_serializer_v1 import API_CORE_SERIALIZER_VERSION
from pixs.core.dto import CoreMutationResult
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.kernel.data_persistence_states import DataPersistenceState


def _cfg(**over):
    base = dict(replay_window_seconds=3600, max_tenant_chars=64, max_scope_chars=64, max_subject_chars=128, max_command_type_chars=128, max_key_chars=128)
    base.update(over)
    return ApiCoreIdempotencyConfig(**base)


def _platform():
    return ScopeContext(ScopeType.PLATFORM, None, None)


def _tenant(tid="t-test", sid=None):
    return ScopeContext(ScopeType.TENANT, tid, sid)


def _result():
    return CoreMutationResult(operation_id="op-1", result_ref="pixs.core.user:x", version=1, persistence_state=DataPersistenceState.ACTIVE, correlation_id="c-1")


def _entry(state="IN_PROGRESS", **over):
    created = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
    ctx = over.pop("context", _platform())
    if state == "IN_PROGRESS":
        data = dict(key=resolve_idempotency_key(context=ctx, subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=_cfg()), content_sha256="0" * 64, serializer_version=API_CORE_SERIALIZER_VERSION, context=ctx, state="IN_PROGRESS", result=None, created_at=created, completed_at=None, expires_at=created + datetime.timedelta(seconds=10), revision=1)
    else:
        completed = created + datetime.timedelta(seconds=5)
        data = dict(key=resolve_idempotency_key(context=ctx, subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=_cfg()), content_sha256="a" * 64, serializer_version=API_CORE_SERIALIZER_VERSION, context=ctx, state="SUCCEEDED", result=_result(), created_at=created, completed_at=completed, expires_at=completed + datetime.timedelta(seconds=3600), revision=1)
    data.update(over)
    return ApiCoreIdempotencyEntry(**data)


class IdempotencyValuesTest(unittest.TestCase):
    def test_config_frozen_and_overflow(self):
        cfg = _cfg()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            cfg.max_key_chars = 0
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            ApiCoreIdempotencyConfig(replay_window_seconds=True, max_tenant_chars=64, max_scope_chars=64, max_subject_chars=128, max_command_type_chars=128, max_key_chars=128)
        forged = _cfg()
        object.__setattr__(forged, "replay_window_seconds", 1.5)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(_entry(), config=forged)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            ApiCoreIdempotencyConfig(replay_window_seconds=10 ** 30, max_tenant_chars=64, max_scope_chars=64, max_subject_chars=128, max_command_type_chars=128, max_key_chars=128)

    def test_namespace_platform_tenant_scope_bounded(self):
        cfg = _cfg()
        k = resolve_idempotency_key(context=_platform(), subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=cfg)
        self.assertEqual(k.namespace, "PLATFORM")
        self.assertIsNone(k.tenant_id)
        k2 = resolve_idempotency_key(context=_tenant("t-a", "s-a"), subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=cfg)
        self.assertEqual((k2.namespace, k2.tenant_id), ("TENANT", "t-a"))
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            resolve_idempotency_key(context=_tenant("t-" + "x" * 100, None), subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=cfg)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            resolve_idempotency_key(context=_tenant("t-a", "s-" + "y" * 100), subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=cfg)

    def test_key_bounds_utf8_nul_types(self):
        cfg = _cfg()
        for bad in ("", "a\x00b", "x" * 129, chr(0xD800)):
            with self.assertRaises(ApiCoreIdempotencyProofInvalid):
                resolve_idempotency_key(context=_platform(), subject_id=bad, command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=cfg)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            resolve_idempotency_key(context=_platform(), subject_id=123, command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=cfg)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            resolve_idempotency_key(context=_platform(), subject_id="s-1", command_type="BAD", idempotency_key="k-1", config=cfg)
        good = resolve_idempotency_key(context=_platform(), subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=cfg)
        forged = ApiCoreIdempotencyKey(namespace="PLATFORM", tenant_id=None, subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1")
        object.__setattr__(forged, "subject_id", True)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(ApiCoreIdempotencyEntry(key=forged, content_sha256="0" * 64, serializer_version=API_CORE_SERIALIZER_VERSION, context=_platform(), state="IN_PROGRESS", result=None, created_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc), completed_at=None, expires_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(seconds=10), revision=1), config=cfg)
        self.assertEqual(good.namespace, "PLATFORM")
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            resolve_idempotency_key(
                context=_platform(), subject_id="s-1",
                command_type="pixs.core.identity.user.create:v1",
                idempotency_key="123456", config=_cfg(max_key_chars=5),
            )
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            resolve_idempotency_key(
                context=_platform(), subject_id="s-1",
                command_type="pixs.core.identity.user.create:v1",
                idempotency_key="k", config=_cfg(max_command_type_chars=8),
            )

    def test_hostile_never_called(self):
        class Hostile:
            @property
            def scope_type(self):
                raise AssertionError("propriete appelee")

            def __eq__(self, other):
                raise AssertionError("egalite appelee")

            @property
            def replay_window_seconds(self):
                raise AssertionError("configuration etrangere lue")

            @property
            def key(self):
                raise AssertionError("entree etrangere lue")

        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            resolve_idempotency_key(context=Hostile(), subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=_cfg())
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            resolve_idempotency_key(context=_platform(), subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", config=Hostile())
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(Hostile(), config=_cfg())
        entry = _entry()
        forged_key = dataclasses.replace(entry.key)
        object.__setattr__(forged_key, "namespace", Hostile())
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(dataclasses.replace(entry, key=forged_key), config=_cfg())

    def test_in_progress_non_terminal(self):
        validate_idempotency_entry(_entry("IN_PROGRESS"), config=_cfg())
        progress = _entry("IN_PROGRESS")
        for changed in (
            dataclasses.replace(progress, completed_at=progress.created_at),
            dataclasses.replace(progress, result=_result()),
        ):
            with self.assertRaises(ApiCoreIdempotencyProofInvalid):
                validate_idempotency_entry(changed, config=_cfg())
        bad = _entry("IN_PROGRESS")
        forged = ApiCoreIdempotencyEntry(key=bad.key, content_sha256=bad.content_sha256, serializer_version=bad.serializer_version, context=bad.context, state="SUCCEEDED", result=None, created_at=bad.created_at, completed_at=None, expires_at=bad.expires_at, revision=1)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(forged, config=_cfg())

    def test_succeeded_result_timestamps(self):
        validate_idempotency_entry(_entry("SUCCEEDED"), config=_cfg())
        base = _entry("SUCCEEDED")
        for timestamp in (
            datetime.datetime(2026, 1, 1),
            datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
        ):
            with self.assertRaises(ApiCoreIdempotencyProofInvalid):
                validate_idempotency_entry(dataclasses.replace(base, created_at=timestamp), config=_cfg())
        forged = ApiCoreIdempotencyEntry(key=base.key, content_sha256=base.content_sha256, serializer_version=base.serializer_version, context=base.context, state="SUCCEEDED", result=base.result, created_at="2026-01-01", completed_at=base.completed_at, expires_at=base.expires_at, revision=1)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(forged, config=_cfg())
        early = ApiCoreIdempotencyEntry(key=base.key, content_sha256=base.content_sha256, serializer_version=base.serializer_version, context=base.context, state="SUCCEEDED", result=base.result, created_at=base.created_at, completed_at=datetime.datetime(2025, 12, 31, tzinfo=datetime.timezone.utc), expires_at=base.expires_at, revision=1)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(early, config=_cfg())

    def test_retention_minimum_longer_admitted_overflow(self):
        base = _entry("SUCCEEDED")
        longer = ApiCoreIdempotencyEntry(key=base.key, content_sha256=base.content_sha256, serializer_version=base.serializer_version, context=base.context, state="SUCCEEDED", result=base.result, created_at=base.created_at, completed_at=base.completed_at, expires_at=base.completed_at + datetime.timedelta(seconds=7200), revision=1)
        validate_idempotency_entry(longer, config=_cfg())
        short = ApiCoreIdempotencyEntry(key=base.key, content_sha256=base.content_sha256, serializer_version=base.serializer_version, context=base.context, state="SUCCEEDED", result=base.result, created_at=base.created_at, completed_at=base.completed_at, expires_at=base.completed_at + datetime.timedelta(seconds=10), revision=1)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(short, config=_cfg())
        top = ApiCoreIdempotencyEntry(key=base.key, content_sha256=base.content_sha256, serializer_version=base.serializer_version, context=base.context, state="SUCCEEDED", result=base.result, created_at=base.created_at, completed_at=datetime.datetime(9999, 12, 31, 23, 0, tzinfo=datetime.timezone.utc), expires_at=datetime.datetime(9999, 12, 31, 23, 0, tzinfo=datetime.timezone.utc), revision=1)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(top, config=_cfg())

    def test_sha_version_and_incomplete(self):
        base = _entry("IN_PROGRESS")
        bad_sha = ApiCoreIdempotencyEntry(key=base.key, content_sha256="Z" * 64, serializer_version=base.serializer_version, context=base.context, state=base.state, result=None, created_at=base.created_at, completed_at=None, expires_at=base.expires_at, revision=1)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(bad_sha, config=_cfg())
        bad_ver = ApiCoreIdempotencyEntry(key=base.key, content_sha256=base.content_sha256, serializer_version="9.9.9", context=base.context, state=base.state, result=None, created_at=base.created_at, completed_at=None, expires_at=base.expires_at, revision=1)
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(bad_ver, config=_cfg())
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(object.__new__(ApiCoreIdempotencyEntry), config=_cfg())
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(base, config=object.__new__(ApiCoreIdempotencyConfig))
        with self.assertRaises(ApiCoreIdempotencyProofInvalid):
            validate_idempotency_entry(dataclasses.replace(base, key=object.__new__(ApiCoreIdempotencyKey)), config=_cfg())


if __name__ == "__main__":
    unittest.main()
