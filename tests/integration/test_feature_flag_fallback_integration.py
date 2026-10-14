"""Tests d'intégration de l'application déclarative du repli R3 (tâche 3.2).

Le scénario s'exécute dans un sous-processus frais (``sys.executable -B``,
environnement minimal explicite, ``PYTHONPATH`` vers ``src``) dont le finder
bloquant Django/SQLite/psycopg/requests/urllib3 et les douze gardes d'E/S
causales sont activés et réellement sondés AVANT l'import de
``pixs.kernel.feature_flags``. Les compteurs sont prouvés à 1 puis
réinitialisés ; après usage réel de la primitive, gardes et finder sont prouvés
à zéro invocation. La machinerie d'import conserve la lecture normale des
sources via ``io`` : le test ne revendique aucune absence de lecture physique.
La stdlib est préchargée avant les gardes ; aucun ``datetime`` ni builtin
immuable n'est patché ; la matrice unitaire complète n'est pas rejouée, seuls
quelques cas dynamiques et la preuve d'absence d'E/S sont vérifiés. Aucune
horloge, PostgreSQL, réseau, environnement métier ou secret n'est utilisé.
"""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_FALLBACK_INTEGRATION_OK"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}

_CHILD = textwrap.dedent(r'''
    import builtins
    import dataclasses
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

        def __bool__(self):
            object.__getattribute__(self, 'calls').append('bool')
            return True

    class AttributeTrap:
        def __init__(self):
            object.__setattr__(self, 'reads', [])

        def __getattribute__(self, name):
            if name != 'reads':
                object.__getattribute__(self, 'reads').append(name)
            return object.__getattribute__(self, name)

    import pixs.kernel.feature_flags as flags

    def definition(**overrides):
        fields = {
            'flag_id': 'web.dark_mode',
            'flag_version': '2026.10-r1',
            'owner_component': 'web-main',
            'purpose': "Déclarer l'option sombre du thème web.",
            'value_schema': 'BOOLEAN',
            'default_value': True,
            'targeting_dimensions': ('INSTALLATION',),
            'cohort_key': None,
            'prerequisites': ('web-main',),
            'fallback_policy': 'fail_closed',
            'expires_at': '2028-01-01T00:00:00Z',
            'audit_policy': 'standard_audit',
        }
        fields.update(overrides)
        return flags.FeatureFlagDefinition(**fields)

    fields = tuple(
        field.name for field in dataclasses.fields(flags.FeatureFlagFallback)
    )
    assert fields == ('status', 'value', 'diagnostics'), fields

    denied = flags.resolve_feature_flag_fallback(
        definition(fallback_policy='DENY'), 'NON_SENSITIVE', 'ABSENT'
    )
    assert denied.status == 'REFUSED', denied.status
    assert denied.value is None
    assert denied.diagnostics == ()

    applied = flags.resolve_feature_flag_fallback(
        definition(fallback_policy='DEFAULT', default_value=False),
        'NON_SENSITIVE',
        'INVALID',
    )
    assert applied.status == 'DEFAULT', applied.status
    assert applied.value is False
    assert applied.diagnostics == ()

    token = flags.resolve_feature_flag_fallback(
        definition(
            value_schema='VARIANT',
            default_value='sombre',
            fallback_policy='DEFAULT',
        ),
        'NON_SENSITIVE',
        'STALE',
    )
    assert token.status == 'DEFAULT'
    assert token.value == 'sombre', token.value

    for sensitive in ('PERMISSION', 'MUTATION', 'PROTECTED_DATA', 'CONTRACT'):
        refused = flags.resolve_feature_flag_fallback(
            definition(fallback_policy='DEFAULT', default_value=True),
            sensitive,
            'ABSENT',
        )
        assert refused.status == 'REFUSED', sensitive
        assert refused.value is None
        assert any(
            diagnostic.element == 'feature_flags.fallback.sensible'
            for diagnostic in refused.diagnostics
        ), refused.diagnostics

    legacy = flags.resolve_feature_flag_fallback(
        definition(fallback_policy='fail_closed'), 'NON_SENSITIVE', 'ABSENT'
    )
    assert legacy.status == 'REFUSED', legacy.status
    assert legacy.value is None
    assert any(
        diagnostic.element == 'feature_flags.fallback.policy'
        for diagnostic in legacy.diagnostics
    ), legacy.diagnostics

    lower = flags.resolve_feature_flag_fallback(
        definition(fallback_policy='deny'), 'NON_SENSITIVE', 'ABSENT'
    )
    assert lower.status == 'REFUSED'
    assert any(
        diagnostic.element == 'feature_flags.fallback.policy'
        for diagnostic in lower.diagnostics
    ), lower.diagnostics

    unknown_use = flags.resolve_feature_flag_fallback(definition(), 'non_sensitive', 'ABSENT')
    assert unknown_use.status == 'REFUSED'
    assert any(
        diagnostic.element == 'feature_flags.fallback.use_kind'
        for diagnostic in unknown_use.diagnostics
    ), unknown_use.diagnostics

    trap = CallableTrap()
    hostile_value = flags.resolve_feature_flag_fallback(
        replace(definition(fallback_policy='DEFAULT'), default_value=trap),
        'NON_SENSITIVE',
        'ABSENT',
    )
    assert hostile_value.status == 'REFUSED', hostile_value.status
    assert hostile_value.value is None
    assert trap.calls == [], trap.calls

    attribute_trap = AttributeTrap()
    hostile_definition = flags.resolve_feature_flag_fallback(
        attribute_trap, 'NON_SENSITIVE', 'ABSENT'
    )
    assert hostile_definition.status == 'REFUSED'
    assert hostile_definition.value is None
    assert any(
        diagnostic.element == 'feature_flags.fallback.definition'
        for diagnostic in hostile_definition.diagnostics
    ), hostile_definition.diagnostics
    assert attribute_trap.reads == [], attribute_trap.reads

    sentinel = 'SENTINELLE-repli'
    echoed = flags.resolve_feature_flag_fallback(
        definition(flag_id='bad space ' + sentinel, fallback_policy='DEFAULT'),
        'NON_SENSITIVE',
        'ABSENT',
    )
    assert echoed.status == 'REFUSED'
    for diagnostic in echoed.diagnostics:
        assert sentinel not in str(diagnostic), str(diagnostic)

    assert blocked == [], blocked
    counts = [guard.call_count for guard in guards]
    assert all(count == 0 for count in counts), counts
    print('FEATURE_FLAG_FALLBACK_INTEGRATION_OK')
''')


class TestFeatureFlagFallbackIntegration(unittest.TestCase):
    def test_fallback_scenarios_under_guards(self) -> None:
        child = subprocess.run(
            [sys.executable, "-B", "-c", _CHILD, _SRC],
            capture_output=True,
            text=True,
            env=_ENV,
            cwd=str(_ROOT),
            timeout=120,
            check=False,
        )
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(child.stdout, _MARKER + "\n", child.stdout)


if __name__ == "__main__":
    unittest.main()
