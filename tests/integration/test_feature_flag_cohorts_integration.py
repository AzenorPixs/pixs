"""Deux processus frais : gardes causales éprouvées avant import et usage réel.

Finder Django/SQL/réseau et douze mocks sont sondés à 1 puis remis à zéro
avant import. Aucun effet réel des sondes : chaque mock refuse l'opération.
Les imports conservent leur lecture normale via io ; aucune absence de lecture
physique n'est revendiquée. Seeds d'interpréteur différents, aucun secret/env
métier et aucune horloge immuable patchée.
"""

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_COHORTS_INTEGRATION_OK:4599:922:1393\n"

_CHILD = r'''

import builtins
import importlib
import importlib.abc
import os
import socket
import subprocess
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from unittest import mock

src = sys.argv[1]
sys.path.insert(0, src)

blocked = []

class BlockSQLAndDjango(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path, target=None):
        base = name.split('.')[0]
        if base in (
            'django', 'sqlite3', 'psycopg', 'psycopg2',
            'requests', 'urllib3',
        ):
            blocked.append(name)
            raise ImportError('blocked')
        return None

sys.meta_path.insert(0, BlockSQLAndDjango())

forbidden_modules = (
    'django', 'sqlite3', 'psycopg', 'psycopg2', 'requests', 'urllib3',
)
for module_name in forbidden_modules:
    try:
        importlib.import_module(module_name)
    except ImportError as exc:
        assert str(exc) == 'blocked', exc
    else:
        raise AssertionError('import guard not active')
assert blocked == list(forbidden_modules), blocked
blocked.clear()

guards = [mock.Mock(side_effect=AssertionError('forbidden'))
          for _ in range(12)]
targets = (
    (builtins, 'open'),
    (Path, 'open'),
    (os, 'remove'),
    (os, 'rename'),
    (os, 'mkdir'),
    (os, 'putenv'),
    (type(os.environ), '__setitem__'),
    (subprocess, 'Popen'),
    (subprocess, 'run'),
    (os, 'system'),
    (socket.socket, 'connect'),
    (socket, 'create_connection'),
)
for (owner, member), guard in zip(targets, guards):
    mock.patch.object(owner, member, guard).start()

probes = (
    lambda: builtins.open('dummy-path'),
    lambda: Path('dummy-path').open(),
    lambda: os.remove('dummy-path'),
    lambda: os.rename('dummy-path', 'dummy-other'),
    lambda: os.mkdir('dummy-path'),
    lambda: os.putenv('DUMMY_KEY', 'dummy-value'),
    lambda: os.environ.__setitem__('DUMMY_KEY', 'dummy-value'),
    lambda: subprocess.Popen(['true']),
    lambda: subprocess.run(['true']),
    lambda: os.system('true'),
    lambda: socket.socket.connect(object(), ('127.0.0.1', 0)),
    lambda: socket.create_connection(('127.0.0.1', 0)),
)
for probe in probes:
    try:
        probe()
    except AssertionError as exc:
        assert str(exc) == 'forbidden'
    else:
        raise AssertionError('guard not active')
for guard in guards:
    assert guard.call_count == 1, guard.call_count
    guard.reset_mock()
assert blocked == [], blocked

class AttributeTrap:
    def __init__(self):
        object.__setattr__(self, 'reads', [])

    def __getattribute__(self, name):
        if name != 'reads':
            object.__getattribute__(self, 'reads').append(name)
        return object.__getattribute__(self, name)

import pixs.kernel.feature_flags as flags
from pixs.kernel.feature_flag_cohorts import (
    FeatureFlagCohortRule, resolve_feature_flag_cohort,
    validate_feature_flag_cohort_rule,
)

def definition(**overrides):
    values = dict(flag_id='web.dark_mode', flag_version='v1',
                  owner_component='web-main', purpose='Cohorte',
                  value_schema='BOOLEAN', default_value=False,
                  targeting_dimensions=('TENANT', 'SCOPE'), cohort_key='beta',
                  prerequisites=(), fallback_policy='DENY',
                  expires_at='2099-01-01T00:00:00Z', audit_policy='standard_audit')
    values.update(overrides)
    return flags.FeatureFlagDefinition(**values)

def context(tenant='tenant-a', scope=None):
    return flags.FeatureFlagEvaluationContext(None, None, tenant, scope,
                                              '2026-01-01T00:00:00Z')

vectors = []
for dim, ctx, expected in (
    ('TENANT', context(), 4599),
    ('TENANT', context(tenant='tenant-é'), 922),
    ('SCOPE', context(scope='scope-a'), 1393),
):
    rule = FeatureFlagCohortRule('beta', dim, 10000, 'cfg-1')
    assert validate_feature_flag_cohort_rule(rule) == ()
    result = resolve_feature_flag_cohort(definition(), rule, ctx, 'cfg-1')
    assert result.status == 'MEMBER' and result.bucket == expected
    assert result.diagnostics == ()
    vectors.append(result.bucket)
zero = FeatureFlagCohortRule('beta', 'TENANT', 0, 'cfg-1')
assert resolve_feature_flag_cohort(definition(), zero, context(), 'cfg-1').status == 'NON_MEMBER'
wrong_version = resolve_feature_flag_cohort(definition(), zero, context(), 'cfg-other')
assert wrong_version.status == 'REFUSED' and wrong_version.bucket is None
assert resolve_feature_flag_cohort(definition(), zero, context(tenant=None), 'cfg-1').status == 'REFUSED'
trap = AttributeTrap()
refused = resolve_feature_flag_cohort(trap, zero, context(), 'cfg-1')
assert refused.status == 'REFUSED' and trap.reads == []
assert blocked == [], blocked
counts = [guard.call_count for guard in guards]
assert counts == [0] * 12, counts
print('FEATURE_FLAG_COHORTS_INTEGRATION_OK:4599:922:1393')
'''

class CohortsIntegrationTests(unittest.TestCase):
    def test_fresh_guarded_processes_ignore_hash_seed(self):
        outputs = []
        for seed in ("0", "777"):
            env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
                   "PYTHONPATH": _SRC, "PYTHONDONTWRITEBYTECODE": "1",
                   "PYTHONHASHSEED": seed}
            result = subprocess.run([sys.executable, "-B", "-c", _CHILD, _SRC],
                                    cwd=str(_ROOT), env=env, capture_output=True,
                                    text=True, timeout=120, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, _MARKER)
            outputs.append(result.stdout)
        self.assertEqual(outputs, [_MARKER, _MARKER])


if __name__ == "__main__":
    unittest.main()
