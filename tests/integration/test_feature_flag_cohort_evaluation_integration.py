"""Composition réelle en enfant frais sous les douze mocks causaux éprouvés.

Finder bloquant avant import ; chaque mock refuse sa sonde sans effet réel,
compteur 1 remis à zéro, puis import/usages à zéro. La lecture normale via io
n'est pas présentée comme absente. Aucune base, réseau, secret ou horloge.
"""

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_COHORT_EVALUATION_INTEGRATION_OK\n"

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
from pixs.kernel.feature_flag_cohorts import FeatureFlagCohortRule, evaluate_feature_flag_assignments_with_cohort

_AS_OF = '2026-01-01T00:00:00Z'
_FAR = '2099-01-01T00:00:00Z'
_VALID_USE_KINDS = ('NON_SENSITIVE', 'PERMISSION', 'MUTATION', 'PROTECTED_DATA', 'CONTRACT')


class AttributeTrap:
    def __init__(self):
        object.__setattr__(self, 'touched', [])

    def __getattribute__(self, name):
        if name != 'touched':
            object.__getattribute__(self, 'touched').append(name)
        return object.__getattribute__(self, name)


def definition(**overrides):
    values = dict(
        flag_id='web.dark_mode',
        flag_version='v1',
        owner_component='web-main',
        purpose='Cohorte',
        value_schema='BOOLEAN',
        default_value=False,
        targeting_dimensions=('TENANT', 'SCOPE'),
        cohort_key='beta',
        prerequisites=(),
        fallback_policy='DENY',
        expires_at=_FAR,
        audit_policy='standard_audit',
    )
    values.update(overrides)
    return flags.FeatureFlagDefinition(**values)


def context(**overrides):
    values = dict(installation=None, environment=None, tenant='tenant-a', scope=None, as_of=_AS_OF)
    values.update(overrides)
    return flags.FeatureFlagEvaluationContext(
        values['installation'], values['environment'], values['tenant'], values['scope'], values['as_of'],
    )


def assignment(**overrides):
    values = dict(
        flag_id='web.dark_mode',
        selector='TENANT',
        selector_value='tenant-a',
        value=True,
        valid_from='2025-01-01T00:00:00Z',
        valid_until=_FAR,
        configuration_version='assign-1',
        updated_by='administrator.1',
    )
    values.update(overrides)
    return flags.FeatureFlagAssignment(**values)


for use_kind in _VALID_USE_KINDS:
    member = evaluate_feature_flag_assignments_with_cohort(
        definition(), [assignment(value=False)], context(), use_kind,
        FeatureFlagCohortRule('beta', 'TENANT', 4600, 'cfg-1'), 'cfg-1',
    )
    assert member.status == 'SELECTED' and member.value is False, (member.status, member.value)

    nonmember = evaluate_feature_flag_assignments_with_cohort(
        definition(fallback_policy='DEFAULT'), [assignment(value=True)], context(), use_kind,
        FeatureFlagCohortRule('beta', 'TENANT', 0, 'cfg-1'), 'cfg-1',
    )
    expected = flags.resolve_feature_flag_fallback(definition(fallback_policy='DEFAULT'), use_kind, 'ABSENT')
    assert (nonmember.status, nonmember.value) == (expected.status, expected.value)

    expired = evaluate_feature_flag_assignments_with_cohort(
        definition(expires_at='2025-01-01T00:00:00Z'), [assignment(value=False)], context(), use_kind,
        FeatureFlagCohortRule('beta', 'TENANT', 4600, 'cfg-1'), 'cfg-1',
    )
    stale_expected = flags.resolve_feature_flag_fallback(definition(expires_at='2025-01-01T00:00:00Z'), use_kind, 'STALE')
    assert (expired.status, expired.value) == (stale_expected.status, stale_expected.value)
    assert any(d.element == 'feature_flags.expiry.expires_at' for d in expired.diagnostics)

rule_trap = AttributeTrap()
version_trap = AttributeTrap()
assignments_trap = AttributeTrap()
no_cohort_rule = definition(cohort_key=None)
baseline = flags.evaluate_feature_flag_assignments_bounded(no_cohort_rule, [assignment(value=False)], context(), _VALID_USE_KINDS[0])
delegated = evaluate_feature_flag_assignments_with_cohort(no_cohort_rule, [assignment(value=False)], context(), _VALID_USE_KINDS[0], rule_trap, version_trap)
assert delegated.status == baseline.status and delegated.value == baseline.value
assert rule_trap.touched == [] and version_trap.touched == []

invalid_cohort = evaluate_feature_flag_assignments_with_cohort(definition(), assignments_trap, context(), _VALID_USE_KINDS[0], FeatureFlagCohortRule('beta', 'TENANT', 4600, 'cfg-other'), 'cfg-1')
assert invalid_cohort.status == 'REFUSED' and invalid_cohort.value is None and assignments_trap.touched == []

bad_rule = AttributeTrap()
bad = evaluate_feature_flag_assignments_with_cohort(definition(), [assignment()], context(), 'NON_SENSITIVE', bad_rule, 'cfg-1')
assert bad.status == 'REFUSED' and bad.value is None and bad_rule.touched == []
for threshold in (0, 4600):
    expired = evaluate_feature_flag_assignments_with_cohort(
        definition(expires_at=_AS_OF, fallback_policy='DEFAULT'), [assignment(value=True)], context(),
        'NON_SENSITIVE', FeatureFlagCohortRule('beta', 'TENANT', threshold, 'cfg-1'), 'cfg-1')
    assert expired.status == 'DEFAULT' and expired.value is False
    assert any(d.element == 'feature_flags.expiry.expires_at' for d in expired.diagnostics)
assert blocked == [], blocked
assert [guard.call_count for guard in guards] == [0] * 12

print('FEATURE_FLAG_COHORT_EVALUATION_INTEGRATION_OK')
'''

class CohortEvaluationIntegrationTests(unittest.TestCase):
    def test_composition_fresh_guarded(self):
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONPATH": _SRC,
               "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([sys.executable, "-B", "-c", _CHILD, _SRC], cwd=str(_ROOT),
                                env=env, capture_output=True, text=True, timeout=120, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)


if __name__ == "__main__":
    unittest.main()
