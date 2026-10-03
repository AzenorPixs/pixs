"""Tests d'intégration des définitions déclaratives de fanions (tâche 2.3).

Le scénario s'exécute dans un sous-processus frais (``sys.executable -B``,
environnement minimal explicite) dont le finder bloquant
Django/SQLite/psycopg/requests/urllib3 et les douze gardes d'E/S sont activés
et réellement sondés AVANT l'import de ``pixs.kernel.feature_flags``, sur le
principe causal éprouvé par la gate de disponibilité (aucun manifeste, aucune
composition ici). Les compteurs sont prouvés à 1 puis réinitialisés ; après
usage réel du module, gardes et finder sont prouvés à zéro invocation. La
machinerie d'import conserve la lecture normale des sources via ``io`` : le
test ne revendique aucune absence de lecture physique. Aucun datetime ni
builtin immuable n'est patché ; aucune horloge, PostgreSQL, réseau ou effet
métier n'est utilisé.
"""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_DEFINITIONS_INTEGRATION_OK"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}

_CHILD = textwrap.dedent(r'''
    import builtins
    import importlib
    import importlib.abc
    import os
    import socket
    import subprocess
    import sys
    from dataclasses import replace
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

    class CallableTrap:
        def __init__(self):
            object.__setattr__(self, 'calls', [])

        def __call__(self, *args, **kwargs):
            object.__getattribute__(self, 'calls').append('call')

    import pixs.kernel.feature_flags as flags

    witness = flags.FeatureFlagDefinition(
        flag_id='web.dark_mode',
        flag_version='2026.10-r1',
        owner_component='web-main',
        purpose="Déclarer l'option sombre du thème web.",
        value_schema='BOOLEAN',
        default_value=False,
        targeting_dimensions=('INSTALLATION',),
        cohort_key=None,
        prerequisites=('web-main',),
        fallback_policy='fail_closed',
        expires_at='2027-01-01T00:00:00Z',
        audit_policy='standard_audit',
    )
    assert flags.validate_feature_flag_definitions([witness]) == ()

    full = {name: getattr(witness, name)
            for name in witness.__dataclass_fields__}
    for unknown in ('expression', 'code', 'rule', 'callback'):
        try:
            flags.FeatureFlagDefinition(**{**full, unknown: lambda: None})
        except TypeError:
            pass
        else:
            raise AssertionError('unknown field accepted')

    trap = CallableTrap()
    elements = set()
    for overrides in (
        {'default_value': trap},
        {'value_schema': 'VARIANT', 'default_value': trap},
        {'value_schema': 'VARIANT',
         'default_value': "remote.get('dark_mode')"},
    ):
        diagnostics = flags.validate_feature_flag_definitions(
            [replace(witness, **overrides)]
        )
        assert diagnostics, overrides
        elements.update(diagnostic.element for diagnostic in diagnostics)
    assert 'feature_flags.default_value' in elements, elements
    assert trap.calls == [], trap.calls

    prose = flags.validate_feature_flag_definitions(
        [replace(witness, purpose="Si activé : run('reboot') — finalité prose.")]
    )
    assert prose == (), prose

    expired = flags.validate_feature_flag_definitions(
        [replace(witness, expires_at='2025-02-29T00:00:00Z')]
    )
    assert any(
        diagnostic.element == 'feature_flags.expires_at'
        for diagnostic in expired
    ), expired

    assert blocked == [], blocked
    counts = [guard.call_count for guard in guards]
    assert all(count == 0 for count in counts), counts
    print('FEATURE_FLAG_DEFINITIONS_INTEGRATION_OK')
''')


class TestFeatureFlagDefinitionsIntegration(unittest.TestCase):
    def test_definitions_scenarios_under_guards(self) -> None:
        child = subprocess.run(
            [sys.executable, "-B", "-c", _CHILD, _SRC],
            timeout=30,
            capture_output=True,
            text=True,
            env=_ENV,
            cwd=str(_ROOT),
        )
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(child.stdout, _MARKER + "\n", child.stdout)


if __name__ == "__main__":
    unittest.main()
