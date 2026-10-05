"""Tests d'intégration de la résolution déclarative de candidats (tâche 3.2, C2).

Le scénario s'exécute dans un sous-processus frais (``sys.executable -B``,
environnement minimal explicite, ``PYTHONPATH`` vers ``src``) dont le finder
bloquant Django/SQLite/psycopg/requests/urllib3 et les douze gardes d'E/S
causales sont activés et réellement sondés AVANT l'import de
``pixs.kernel.feature_flags``. Les compteurs sont prouvés à 1 puis
réinitialisés ; après usage réel du module, gardes et finder sont prouvés à
zéro invocation. La machinerie d'import conserve la lecture normale des sources
via ``io`` : le test ne revendique aucune absence de lecture physique. La
stdlib est préchargée avant les gardes ; aucun ``datetime`` ni builtin immuable
n'est patché ; aucune horloge, PostgreSQL, réseau, environnement métier ou
secret n'est utilisé.
"""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_EVALUATION_INTEGRATION_OK"
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
    import itertools
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

    definition = flags.FeatureFlagDefinition(
        flag_id='web.dark_mode',
        flag_version='2026.10-r1',
        owner_component='web-main',
        purpose="Déclarer l'option sombre du thème web.",
        value_schema='BOOLEAN',
        default_value=False,
        targeting_dimensions=('INSTALLATION', 'TENANT', 'SCOPE'),
        cohort_key=None,
        prerequisites=('web-main',),
        fallback_policy='fail_closed',
        expires_at='2028-01-01T00:00:00Z',
        audit_policy='standard_audit',
    )
    context = flags.FeatureFlagEvaluationContext(
        installation='installation-principale',
        environment=None,
        tenant=None,
        scope=None,
        as_of='2026-06-01T00:00:00Z',
    )

    def assignment(**overrides):
        fields = {
            'flag_id': 'web.dark_mode',
            'selector': 'INSTALLATION',
            'selector_value': 'installation-principale',
            'value': False,
            'valid_from': '2026-01-01T00:00:00Z',
            'valid_until': '2027-01-01T00:00:00Z',
            'configuration_version': 'cfg-1',
            'updated_by': 'administrateur.1',
        }
        fields.update(overrides)
        return flags.FeatureFlagAssignment(**fields)

    general = assignment()
    selected = flags.resolve_feature_flag_assignment(definition, [general], context)
    assert selected.status == 'SELECTED', selected.status
    assert selected.assignment is general
    assert selected.assignment.value is False
    assert selected.diagnostics == ()

    again = flags.resolve_feature_flag_assignment(definition, [general], context)
    assert again == selected, again.status

    empty = flags.resolve_feature_flag_assignment(definition, [], context)
    assert empty.status == 'NO_MATCH', empty.status
    assert empty.assignment is None and empty.diagnostics == ()

    hidden = assignment(selector='ENVIRONMENT', selector_value='prod')
    ignored = flags.resolve_feature_flag_assignment(
        definition,
        [hidden],
        replace(context, environment='prod'),
    )
    assert ignored.status == 'NO_MATCH', ignored.status

    other = assignment(selector_value='installation-secondaire')
    assert flags.resolve_feature_flag_assignment(
        definition, [other], context
    ).status == 'NO_MATCH'

    until_edge = assignment(valid_until='2026-06-01T00:00:00Z')
    assert flags.resolve_feature_flag_assignment(
        definition, [until_edge], context
    ).status == 'NO_MATCH'
    from_edge = assignment(valid_from='2026-06-01T00:00:00Z')
    assert flags.resolve_feature_flag_assignment(
        definition, [from_edge], context
    ).status == 'SELECTED'

    tenant = assignment(selector='TENANT', selector_value='tenant-a',
                        configuration_version='cfg-2')
    scope = assignment(selector='SCOPE', selector_value='scope-a',
                       configuration_version='cfg-3')
    deep = replace(context, tenant='tenant-a', scope='scope-a')
    ordered = flags.resolve_feature_flag_assignment(
        definition, [general, tenant, scope], deep
    )
    assert ordered.status == 'SELECTED'
    assert ordered.assignment.configuration_version == 'cfg-3'
    for permutation in itertools.permutations((general, tenant, scope)):
        assert flags.resolve_feature_flag_assignment(
            definition, list(permutation), deep
        ) == ordered
    tenant_only = flags.resolve_feature_flag_assignment(
        definition, [general, tenant], replace(context, tenant='tenant-a')
    )
    assert tenant_only.assignment is tenant

    twin = assignment(configuration_version='cfg-twin')
    ambiguous = flags.resolve_feature_flag_assignment(
        definition, [general, twin], context
    )
    assert ambiguous.status == 'REFUSED', ambiguous.status
    assert ambiguous.assignment is None
    assert any(
        diagnostic.element == 'feature_flags.evaluation.candidats'
        for diagnostic in ambiguous.diagnostics
    ), ambiguous.diagnostics
    for permutation in itertools.permutations((general, twin)):
        assert flags.resolve_feature_flag_assignment(
            definition, list(permutation), context
        ).status == 'REFUSED'

    bad_shape = flags.resolve_feature_flag_assignment(
        definition, [general], replace(context, scope='scope-a')
    )
    assert bad_shape.status == 'REFUSED'
    assert any(
        diagnostic.element == 'feature_flags.evaluation.scope'
        for diagnostic in bad_shape.diagnostics
    ), bad_shape.diagnostics

    trap = CallableTrap()
    hostile = flags.resolve_feature_flag_assignment(
        definition, [replace(general, value=trap)], context
    )
    assert hostile.status == 'REFUSED', hostile.status
    assert trap.calls == [], trap.calls

    naive = flags.resolve_feature_flag_assignment(
        definition, [replace(general, valid_from='2026-01-01T00:00:00')], context
    )
    assert naive.status == 'REFUSED'
    assert any(
        diagnostic.element == 'assignments.valid_from'
        or diagnostic.element == 'feature_flags.assignments.valid_from'
        for diagnostic in naive.diagnostics
    ), [str(diagnostic) for diagnostic in naive.diagnostics]

    variant = replace(definition, value_schema='VARIANT', default_value='sombre')
    variant_token = flags.resolve_feature_flag_assignment(
        variant, [assignment(value='sombre')], context
    )
    assert variant_token.status == 'SELECTED'
    assert variant_token.assignment.value == 'sombre'
    variant_bool = flags.resolve_feature_flag_assignment(
        variant, [assignment(value=False)], context
    )
    assert variant_bool.status == 'REFUSED'
    assert any(
        diagnostic.element == 'feature_flags.evaluation.value'
        for diagnostic in variant_bool.diagnostics
    ), variant_bool.diagnostics
    boolean_bool = flags.resolve_feature_flag_assignment(
        definition, [assignment(value='clair')], context
    )
    assert boolean_bool.status == 'REFUSED'

    sentinel = 'SENTINELLE-valeur'
    echoed = flags.resolve_feature_flag_assignment(
        definition, [assignment(selector_value=sentinel)], context
    )
    assert echoed.status == 'NO_MATCH', echoed.status
    assert echoed.diagnostics == ()

    dataclass_fields = tuple(
        field.name for field in dataclasses.fields(flags.FeatureFlagResolution)
    )
    assert dataclass_fields == ('status', 'assignment', 'diagnostics')

    assert blocked == [], blocked
    counts = [guard.call_count for guard in guards]
    assert all(count == 0 for count in counts), counts
    print('FEATURE_FLAG_EVALUATION_INTEGRATION_OK')
''')


class TestFeatureFlagEvaluationIntegration(unittest.TestCase):
    def test_resolution_scenarios_under_guards(self) -> None:
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
