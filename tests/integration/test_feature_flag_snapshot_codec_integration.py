"""Codec en enfant frais : douze gardes d’effets et quatre gardes d’horloge.

Chaque garde est éprouvée puis remise à zéro avant import et usages.
Les lectures normales d’import via io restent permises ; aucune absence totale
de lecture physique n’est revendiquée. Pas de base, réseau ou secret réel.
"""

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_SNAPSHOT_CODEC_INTEGRATION_OK\n"

_CHILD = r'''
import builtins
import json
import datetime as clock_datetime
import time as clock_time
import importlib
import importlib.abc
import os
import socket
import subprocess
import sys
from pathlib import Path
from unittest import mock

src = sys.argv[1]
sys.path.insert(0, src)

blocked = []


class BlockSQLAndDjango(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path, target=None):
        base = name.split(".")[0]
        if base in (
            "django",
            "sqlite3",
            "psycopg",
            "psycopg2",
            "requests",
            "urllib3",
        ):
            blocked.append(name)
            raise ImportError("blocked")
        return None


sys.meta_path.insert(0, BlockSQLAndDjango())

forbidden_modules = (
    "django",
    "sqlite3",
    "psycopg",
    "psycopg2",
    "requests",
    "urllib3",
)
for module_name in forbidden_modules:
    try:
        importlib.import_module(module_name)
    except ImportError as exc:
        assert str(exc) == "blocked", exc
    else:
        raise AssertionError("import guard not active")
assert blocked == list(forbidden_modules), blocked
blocked.clear()

guards = [mock.Mock(side_effect=AssertionError("forbidden")) for _ in range(12)]
targets = (
    (builtins, "open"),
    (Path, "open"),
    (os, "remove"),
    (os, "rename"),
    (os, "mkdir"),
    (os, "putenv"),
    (type(os.environ), "__setitem__"),
    (subprocess, "Popen"),
    (subprocess, "run"),
    (os, "system"),
    (socket.socket, "connect"),
    (socket, "create_connection"),
)
for (owner, member), guard in zip(targets, guards):
    mock.patch.object(owner, member, guard).start()

probes = (
    lambda: builtins.open("dummy-path"),
    lambda: Path("dummy-path").open(),
    lambda: os.remove("dummy-path"),
    lambda: os.rename("dummy-path", "dummy-other"),
    lambda: os.mkdir("dummy-path"),
    lambda: os.putenv("DUMMY_KEY", "dummy-value"),
    lambda: os.environ.__setitem__("DUMMY_KEY", "dummy-value"),
    lambda: subprocess.Popen(["true"]),
    lambda: subprocess.run(["true"]),
    lambda: os.system("true"),
    lambda: socket.socket.connect(object(), ("127.0.0.1", 0)),
    lambda: socket.create_connection(("127.0.0.1", 0)),
)
for probe in probes:
    try:
        probe()
    except AssertionError as exc:
        assert str(exc) == "forbidden"
    else:
        raise AssertionError("guard not active")
for guard in guards:
    assert guard.call_count == 1, guard.call_count
    guard.reset_mock()
assert blocked == [], blocked
assert [guard.call_count for guard in guards] == [0] * 12


clock_guards = [mock.Mock(side_effect=AssertionError("clock forbidden")) for _ in range(4)]
mock.patch.object(clock_time, "time", clock_guards[0]).start()
mock.patch.object(clock_time, "monotonic", clock_guards[1]).start()
real_datetime = clock_datetime.datetime

class GuardedDateTime(real_datetime):
    @classmethod
    def now(cls, *args, **kwargs):
        return clock_guards[2](*args, **kwargs)

    @classmethod
    def utcnow(cls, *args, **kwargs):
        return clock_guards[3](*args, **kwargs)

clock_datetime.datetime = GuardedDateTime
for probe in (clock_time.time, clock_time.monotonic, GuardedDateTime.now, GuardedDateTime.utcnow):
    try:
        probe()
    except AssertionError as exc:
        assert str(exc) == "clock forbidden"
    else:
        raise AssertionError("clock guard not active")
for guard in clock_guards:
    assert guard.call_count == 1
    guard.reset_mock()

import pixs.kernel.feature_flags as flags
import pixs.kernel.feature_flag_sources as source
from pixs.kernel.feature_flag_cohorts import FeatureFlagCohortRule
import pixs.backend.feature_flag_snapshot_codec as codec

CFG = "cfg-1"
VALID_USE_KINDS = tuple(sorted(flags._FALLBACK_USE_KINDS))
USE_KIND = VALID_USE_KINDS[0]


def defn(**overrides):
    values = dict(
        flag_id="web.dark_mode",
        flag_version="v1",
        owner_component="web-main",
        purpose="Source",
        value_schema="BOOLEAN",
        default_value=False,
        targeting_dimensions=("TENANT", "SCOPE"),
        cohort_key="beta",
        prerequisites=(),
        fallback_policy="DENY",
        expires_at="2099-01-01T00:00:00Z",
        audit_policy="standard_audit",
    )
    values.update(overrides)
    return flags.FeatureFlagDefinition(**values)


def ctx(**overrides):
    values = dict(
        installation=None,
        environment=None,
        tenant="tenant-a",
        scope=None,
        as_of="2026-01-01T00:00:00Z",
    )
    values.update(overrides)
    return flags.FeatureFlagEvaluationContext(
        values["installation"],
        values["environment"],
        values["tenant"],
        values["scope"],
        values["as_of"],
    )


def asgn(**overrides):
    values = dict(
        flag_id="web.dark_mode",
        selector="TENANT",
        selector_value="tenant-a",
        value=True,
        valid_from="2025-01-01T00:00:00Z",
        valid_until="2099-01-01T00:00:00Z",
        configuration_version=CFG,
        updated_by="administrator.1",
    )
    values.update(overrides)
    return flags.FeatureFlagAssignment(**values)


def rl(**overrides):
    values = dict(
        cohort_key="beta",
        subject_dimension="TENANT",
        threshold_basis_points=4600,
        configuration_version=CFG,
    )
    values.update(overrides)
    return FeatureFlagCohortRule(**values)


def snap(definitions=None, assignments=None, cohort_rules=None, version=CFG):
    if definitions is None:
        definitions = (defn(),)
    if assignments is None:
        assignments = (asgn(value=False),)
    if cohort_rules is None:
        cohort_rules = (rl(),)
    return source.FeatureFlagSourceSnapshot(version, definitions, assignments, cohort_rules)


original = snap()
real_validator = codec.validate_feature_flag_source_snapshot
real_composition = source.evaluate_feature_flag_assignments_with_cohort
with mock.patch.object(codec, "validate_feature_flag_source_snapshot", wraps=real_validator) as validator, mock.patch.object(source, "evaluate_feature_flag_assignments_with_cohort", wraps=real_composition) as composition:
    document = codec.encode_feature_flag_source_snapshot(original)
    before_document = json.loads(json.dumps(document))
    decoded = codec.decode_feature_flag_source_snapshot(json.loads(json.dumps(document)))
    assert decoded == original
    assert document == before_document
    assert validator.call_count == 2
    member = source.evaluate_feature_flag_source_snapshot(decoded, CFG, "web.dark_mode", ctx(), "PERMISSION")
    assert (member.status, member.value) == ("SELECTED", False)
    assert not hasattr(member, "permission")
    assert composition.call_count == 1
    assert composition.call_args.args[0] is decoded.definitions[0]
    assert composition.call_args.args[1] == decoded.assignments
    assert composition.call_args.args[4] is decoded.cohort_rules[0]

    cases = (
        snap(definitions=(defn(fallback_policy="DEFAULT"),), assignments=(asgn(value="synthetic-invalid-boolean"),)),
        snap(definitions=(defn(fallback_policy="DEFAULT"),), cohort_rules=(rl(threshold_basis_points=0),)),
        snap(definitions=(defn(fallback_policy="DEFAULT", expires_at="2025-01-01T00:00:00Z"),), cohort_rules=(rl(threshold_basis_points=10000),)),
    )
    for snapshot in cases:
        restored = codec.decode_feature_flag_source_snapshot(json.loads(json.dumps(codec.encode_feature_flag_source_snapshot(snapshot))))
        assert restored == snapshot
        for use_kind in ("NON_SENSITIVE", "PERMISSION", "MUTATION", "PROTECTED_DATA", "CONTRACT"):
            result = source.evaluate_feature_flag_source_snapshot(restored, CFG, "web.dark_mode", ctx(), use_kind)
            expected = ("DEFAULT", False) if use_kind == "NON_SENSITIVE" else ("REFUSED", None)
            assert (result.status, result.value) == expected
            assert not hasattr(result, "permission")
    assert composition.call_count == 16

    invalid_document = json.loads(json.dumps(document))
    invalid_document["assignments"][0]["configuration_version"] = "other"
    for operation, value in (
        (codec.decode_feature_flag_source_snapshot, invalid_document),
        (codec.encode_feature_flag_source_snapshot, snap(version="other")),
    ):
        try:
            operation(value)
        except codec.FeatureFlagSnapshotCodecError as exc:
            assert str(exc) == "Snapshot source de fanions invalide"
        else:
            raise AssertionError("incoherent lot accepted")
    assert validator.call_count == 10
    wrong_version = source.evaluate_feature_flag_source_snapshot(decoded, "other", "web.dark_mode", ctx(), "PERMISSION")
    assert (wrong_version.status, wrong_version.value) == ("REFUSED", None)
    assert composition.call_count == 16
    document["definitions"][0]["targeting_dimensions"].append("INSTALLATION")
    assert decoded == original

assert blocked == [], blocked
assert [guard.call_count for guard in guards] == [0] * 12
assert [guard.call_count for guard in clock_guards] == [0] * 4
print("FEATURE_FLAG_SNAPSHOT_CODEC_INTEGRATION_OK")
'''


class FeatureFlagSnapshotCodecIntegrationTests(unittest.TestCase):
    def test_snapshot_codec_fresh_guarded(self):
        env = {
            "PATH": "/usr/bin:/bin",
            "LANG": "C.UTF-8",
            "PYTHONPATH": _SRC,
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        result = subprocess.run(
            [sys.executable, "-B", "-c", _CHILD, _SRC],
            cwd=str(_ROOT),
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)


if __name__ == "__main__":
    unittest.main()
