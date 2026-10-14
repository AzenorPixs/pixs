"""Tests d'intégration de l'évaluation bornée des affectations (tâche 3.2).

Le scénario s'exécute dans un sous-processus frais (``sys.executable -B``,
environnement minimal explicite, ``PYTHONPATH`` vers ``src``) dont le finder
bloquant Django/SQLite/psycopg/requests/urllib3 et les douze gardes d'E/S
causales sont activés et réellement sondés AVANT l'import de
``pixs.kernel.feature_flags``. Les compteurs sont prouvés à 1 puis
réinitialisés ; après usage réel de la composition, gardes et finder sont
prouvés à zéro invocation. La machinerie d'import conserve la lecture normale
des sources via ``io`` : le test ne revendique aucune absence de lecture
physique. La stdlib est préchargée avant les gardes ; aucun ``datetime`` ni
builtin immuable n'est patché ; la matrice unitaire complète n'est pas rejouée.
Aucune horloge, PostgreSQL, réseau, environnement métier ou secret n'est utilisé.
"""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_EVALUATION_BOUNDED_INTEGRATION_OK"
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

    def definition(**overrides):
        fields = {
            'flag_id': 'web.dark_mode',
            'flag_version': '2026.10-r1',
            'owner_component': 'web-main',
            'purpose': "Déclarer l'option sombre du thème web.",
            'value_schema': 'BOOLEAN',
            'default_value': True,
            'targeting_dimensions': ('INSTALLATION', 'TENANT'),
            'cohort_key': None,
            'prerequisites': (),
            'fallback_policy': 'DENY',
            'expires_at': '2028-01-01T00:00:00Z',
            'audit_policy': 'standard_audit',
        }
        fields.update(overrides)
        return flags.FeatureFlagDefinition(**fields)

    def assignment(**overrides):
        fields = {
            'flag_id': 'web.dark_mode',
            'selector': 'INSTALLATION',
            'selector_value': 'installation-principale',
            'value': True,
            'valid_from': '2026-01-01T00:00:00Z',
            'valid_until': '2027-01-01T00:00:00Z',
            'configuration_version': 'cfg-1',
            'updated_by': 'administrateur.1',
        }
        fields.update(overrides)
        return flags.FeatureFlagAssignment(**fields)

    context = flags.FeatureFlagEvaluationContext(
        installation='installation-principale',
        environment=None,
        tenant=None,
        scope=None,
        as_of='2026-06-01T00:00:00Z',
    )

    sensitive_selected = flags.evaluate_feature_flag_assignments_bounded(
        definition(), [assignment()], context, 'PERMISSION'
    )
    assert sensitive_selected.status == 'SELECTED', sensitive_selected.status
    assert sensitive_selected.value is True
    assert sensitive_selected.diagnostics == ()

    default_false = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', default_value=False),
        [],
        context,
        'NON_SENSITIVE',
    )
    assert default_false.status == 'DEFAULT', default_false.status
    assert default_false.value is False

    stale = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', default_value=False),
        [assignment(valid_until='2026-06-01T00:00:00Z')],
        context,
        'NON_SENSITIVE',
    )
    assert stale.status == 'DEFAULT'
    assert stale.value is False

    future = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', default_value=False),
        [assignment(valid_from='2026-09-01T00:00:00Z')],
        context,
        'MUTATION',
    )
    assert future.status == 'REFUSED', future.status
    assert future.value is None
    assert any(
        diagnostic.element == 'feature_flags.fallback.sensible'
        for diagnostic in future.diagnostics
    ), future.diagnostics

    ambiguous = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', default_value=True),
        [assignment(), assignment(configuration_version='cfg-2')],
        context,
        'NON_SENSITIVE',
    )
    assert ambiguous.status == 'REFUSED', ambiguous.status
    assert ambiguous.value is None
    assert any(
        diagnostic.element == 'feature_flags.evaluation.candidats'
        for diagnostic in ambiguous.diagnostics
    ), ambiguous.diagnostics

    unknown_policy = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='fail_closed'),
        [assignment()],
        context,
        'NON_SENSITIVE',
    )
    assert unknown_policy.status == 'REFUSED', unknown_policy.status
    assert unknown_policy.value is None
    assert any(
        diagnostic.element == 'feature_flags.evaluation_bounded.policy'
        for diagnostic in unknown_policy.diagnostics
    ), unknown_policy.diagnostics

    unsupported = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', cohort_key='beta.cohorte-x'),
        [assignment()],
        context,
        'NON_SENSITIVE',
    )
    assert unsupported.status == 'REFUSED'
    assert unsupported.value is None
    assert any(
        diagnostic.element == 'feature_flags.evaluation_bounded.configuration'
        for diagnostic in unsupported.diagnostics
    ), unsupported.diagnostics

    trap = AttributeTrap()
    hostile = flags.evaluate_feature_flag_assignments_bounded(
        trap, [assignment()], context, 'NON_SENSITIVE'
    )
    assert hostile.status == 'REFUSED'
    assert hostile.value is None
    assert trap.reads == [], trap.reads

    sentinel = 'SENTINELLE-bornee'
    echoed = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', flag_id='bad space ' + sentinel),
        [assignment()],
        context,
        'NON_SENSITIVE',
    )
    assert echoed.status == 'REFUSED'
    for diagnostic in echoed.diagnostics:
        assert sentinel not in str(diagnostic), str(diagnostic)

    assert flags.validate_feature_flag_assignment_expiry(
        definition(), context
    ) == ()
    assert [
        diagnostic.element
        for diagnostic in flags.validate_feature_flag_assignment_expiry(
            definition(expires_at='2026-06-01T00:00:00Z'), context
        )
    ] == ['feature_flags.expiry.expires_at']

    before_expiry = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', expires_at='2028-01-01T00:00:00Z'),
        [assignment()],
        context,
        'CONTRACT',
    )
    assert before_expiry.status == 'SELECTED', before_expiry.status
    assert before_expiry.value is True
    assert before_expiry.diagnostics == ()

    expired_default = flags.evaluate_feature_flag_assignments_bounded(
        definition(
            fallback_policy='DEFAULT',
            default_value=False,
            expires_at='2026-06-01T00:00:00+00:00',
        ),
        [assignment(value=True)],
        context,
        'NON_SENSITIVE',
    )
    assert expired_default.status == 'DEFAULT', expired_default.status
    assert expired_default.value is False
    assert [
        diagnostic.element for diagnostic in expired_default.diagnostics
    ] == ['feature_flags.expiry.expires_at']

    expired_denied = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DENY', expires_at='2026-06-01T00:00:00Z'),
        [assignment(value=True)],
        context,
        'MUTATION',
    )
    assert expired_denied.status == 'REFUSED', expired_denied.status
    assert expired_denied.value is None
    assert [
        diagnostic.element for diagnostic in expired_denied.diagnostics
    ] == ['feature_flags.expiry.expires_at']

    expired_sensitive_default = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', default_value=False,
                   expires_at='2026-06-01T00:00:00Z'),
        [assignment(value=True)], context, 'PROTECTED_DATA',
    )
    assert expired_sensitive_default.status == 'REFUSED'
    assert expired_sensitive_default.value is None
    assert {d.element for d in expired_sensitive_default.diagnostics} == {
        'feature_flags.expiry.expires_at', 'feature_flags.fallback.sensible',
    }

    expired_ambiguous = flags.evaluate_feature_flag_assignments_bounded(
        definition(fallback_policy='DEFAULT', expires_at='2026-06-01T00:00:00Z'),
        [assignment(), assignment(configuration_version='cfg-2')],
        context,
        'NON_SENSITIVE',
    )
    assert expired_ambiguous.status == 'REFUSED', expired_ambiguous.status
    assert expired_ambiguous.value is None
    assert [
        diagnostic.element for diagnostic in expired_ambiguous.diagnostics
    ] == ['feature_flags.evaluation.candidats']

    assert datetime.fromisoformat(context.as_of).year == 2026
    assert blocked == [], blocked
    counts = [guard.call_count for guard in guards]
    assert all(count == 0 for count in counts), counts
    print('FEATURE_FLAG_EVALUATION_BOUNDED_INTEGRATION_OK')
''')


class TestFeatureFlagEvaluationBoundedIntegration(unittest.TestCase):

    def test_evaluation_scenarios_under_guards(self) -> None:
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
