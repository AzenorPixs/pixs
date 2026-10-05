"""Contrat de source en enfant frais sous les douze mocks causaux éprouvés.

Finder bloquant avant import ; chaque mock refuse sa sonde sans effet réel,
compteur 1 remis à zéro, puis import et usages à zéro. Les imports conservent
leur lecture normale via io ; aucune absence de lecture physique n'est
revendiquée. Aucune horloge, base, réseau, secret ou administration n'est utilisé.
"""

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_SOURCE_CONTRACT_INTEGRATION_OK\n"

_CHILD = r'''
import builtins
import dataclasses
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


import pixs.kernel.feature_flags as flags
import pixs.kernel.feature_flag_sources as source
from pixs.kernel.feature_flag_cohorts import FeatureFlagCohortRule


class AttributeTrap:
    def __init__(self):
        object.__setattr__(self, "touched", [])

    def __getattribute__(self, name):
        if name != "touched":
            object.__getattribute__(self, "touched").append(name)
        return object.__getattribute__(self, name)


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


real_composition = source.evaluate_feature_flag_assignments_with_cohort
composition_calls = []


def spy(*args):
    composition_calls.append(args)
    return real_composition(*args)


source.evaluate_feature_flag_assignments_with_cohort = spy

try:
    # 1. Snapshot source valide : membre sélectionne réellement False.
    def_member = defn()
    assn_member = asgn(value=False)
    coh_member = rl(threshold_basis_points=4600)
    snap_member = snap(definitions=(def_member,), assignments=(assn_member,), cohort_rules=(coh_member,))
    ctx_member = ctx()
    before_state = (
        dataclasses.astuple(snap_member),
        dataclasses.astuple(def_member),
        dataclasses.astuple(assn_member),
        dataclasses.astuple(coh_member),
    )
    assert source.validate_feature_flag_source_snapshot(snap_member) == ()
    result_member = source.evaluate_feature_flag_source_snapshot(
        snap_member, CFG, "web.dark_mode", ctx_member, USE_KIND
    )
    assert result_member.status == "SELECTED", result_member
    assert result_member.value is False, result_member
    assert len(composition_calls) == 1, composition_calls
    args_member = composition_calls[-1]
    assert args_member[0] is def_member
    assert args_member[1] == (assn_member,)
    assert args_member[2] is ctx_member
    assert args_member[3] == USE_KIND
    assert args_member[4] is coh_member
    assert args_member[5] == CFG

    # 2. Lot invalide et version attendue divergente : refus fermé sans composition.
    calls_after_member = len(composition_calls)
    invalid_snapshot = snap(assignments=(asgn(flag_id="web.unknown"),))
    bad_lot = source.evaluate_feature_flag_source_snapshot(
        invalid_snapshot, CFG, "web.dark_mode", ctx(), USE_KIND
    )
    assert bad_lot.status == "REFUSED", bad_lot
    assert bad_lot.value is None
    assert len(composition_calls) == calls_after_member, composition_calls

    wrong_version = source.evaluate_feature_flag_source_snapshot(
        snap_member, "cfg-2", "web.dark_mode", ctx(), USE_KIND
    )
    assert wrong_version.status == "REFUSED", wrong_version
    assert wrong_version.value is None
    assert len(composition_calls) == calls_after_member, composition_calls

    hostile_context = AttributeTrap()
    hostile_use = AttributeTrap()
    hostile_result = source.evaluate_feature_flag_source_snapshot(
        snap_member, CFG, "web.dark_mode", hostile_context, hostile_use
    )
    assert hostile_result.status == "REFUSED", hostile_result
    assert hostile_context.touched == []
    assert hostile_use.touched == []
    assert len(composition_calls) == calls_after_member, composition_calls

    # 3. Définition sans cohorte standard : délègue réellement sans règle.
    def_none = defn(cohort_key=None)
    assn_none = asgn(value=False)
    snap_none = snap(definitions=(def_none,), assignments=(assn_none,), cohort_rules=())
    ctx_none = ctx()
    assert source.validate_feature_flag_source_snapshot(snap_none) == ()
    baseline_none = flags.evaluate_feature_flag_assignments_bounded(
        def_none, (assn_none,), ctx_none, USE_KIND
    )
    result_none = source.evaluate_feature_flag_source_snapshot(
        snap_none, CFG, "web.dark_mode", ctx_none, USE_KIND
    )
    assert result_none.status == baseline_none.status, result_none
    assert result_none.value == baseline_none.value, result_none
    assert result_none.diagnostics == baseline_none.diagnostics, result_none
    assert len(composition_calls) == calls_after_member + 1, composition_calls
    args_none = composition_calls[-1]
    assert args_none[0] is def_none
    assert args_none[1] == (assn_none,)
    assert args_none[2] is ctx_none
    assert args_none[4] is None
    assert args_none[5] == CFG

    after_state = (
        dataclasses.astuple(snap_member),
        dataclasses.astuple(def_member),
        dataclasses.astuple(assn_member),
        dataclasses.astuple(coh_member),
    )
    assert after_state == before_state
finally:
    source.evaluate_feature_flag_assignments_with_cohort = real_composition

assert blocked == [], blocked
assert [guard.call_count for guard in guards] == [0] * 12

print("FEATURE_FLAG_SOURCE_CONTRACT_INTEGRATION_OK")
'''


class FeatureFlagSourceContractIntegrationTests(unittest.TestCase):
    def test_source_contract_fresh_guarded(self):
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
