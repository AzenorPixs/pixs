"""Tests d'intégration de la porte de disponibilité des capacités.

Chaque scénario s'exécute dans un sous-processus frais (``sys.executable``)
dont les gardes d'E/S et le finder d'import bloquant Django/SQL/clients
réseau sont activés causalement AVANT l'import du noyau : le finder est
réellement sondé avant l'import, chaque garde est prouvée active par une
sonde, les compteurs sont prouvés à 1 puis réinitialisés, et les imports
composition/availability/parser/semver ont lieu sous gardes. ``_PREFIX``
se termine À L'INTÉRIEUR du bloc ``with`` : les scénarios futurs
(``_SCENARIOS``) seront concaténés via ``textwrap.indent(..., "    ")``
pour rester sous gardes pendant toutes les preuves, avant le contrôle
final des compteurs résiduels. Les gardes interdisent les E/S
fonctionnelles et mutations testées ; la machinerie Python conserve la
lecture normale des sources pendant les imports. Aucun Django, PostgreSQL,
réseau ou état runtime réel : manifests ``t.*`` synthétiques de confiance.
"""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}


def _run(code: str):
    return subprocess.run(
        [sys.executable, "-B", "-c", code, _SRC],
        timeout=30,
        capture_output=True,
        text=True,
        env=_ENV,
        cwd=str(_ROOT),
    )


_PREFIX = textwrap.dedent(r'''
    import builtins
    import importlib.abc
    import os
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
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

    forbidden_modules = ('django', 'sqlite3', 'psycopg', 'psycopg2', 'requests', 'urllib3')
    for module_name in forbidden_modules:
        try:
            importlib.import_module(module_name)
        except ImportError as exc:
            assert str(exc) == 'blocked', exc
        else:
            raise AssertionError('import guard not active')
    assert blocked == list(forbidden_modules), blocked
    blocked.clear()

    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in range(12)]
    names = [
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
    ]

    with ExitStack() as stack:
        for pair, guard in zip(names, guards):
            stack.enter_context(mock.patch.object(pair[0], pair[1], guard))

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

        assert blocked == [], blocked
        for guard in guards:
            assert guard.call_count == 1, guard.call_count
        for guard in guards:
            guard.reset_mock()
        blocked.clear()

        import pixs.kernel.composition as composition
        import pixs.kernel.lifecycle.availability as availability
        import pixs.kernel.manifest.parser as parser
        import pixs.kernel.manifest.semver as semver
''')

_SCENARIOS_START = textwrap.dedent(r'''
    def _manifest_provide(provider_id, version):
        return "\n".join([
            'schema_version = "1"',
            f'id = "{provider_id}"',
            'type = "PROVIDER"',
            f'version = "{version}"',
            "",
            "[provides]",
            "[[provides.capabilities]]",
            'id = "cap.main"',
            f'version = "{version}"',
            "contracts = []",
            'criticality = "REQUIRED"',
            'fallback = "none"',
        ])

    def _manifest_consume(
        consumer_id, constraint, other_provider, other_version
    ):
        return "\n".join([
            'schema_version = "1"',
            f'id = "{consumer_id}"',
            'type = "MODULE"',
            'version = "1.0.0"',
            "",
            "[dependencies]",
            f'capabilities = ["cap.main {constraint}"]',
            f'components = ["{other_provider} =={other_version}"]',
        ])

    def _attestation(component_id, component_version, scope,
                     target_id, target_version):
        return composition.ConformityAttestation(
            component_id=component_id,
            component_version=component_version,
            scope=scope,
            target_id=target_id,
            target_version=target_version,
            suite_id='suite.test.integration', suite_version='1.0.0',
            verdict='PASS', proof_ref='synthetic:test-only',
        )

    def _observation(version, provider_id, operable=True):
        return availability.CapabilityObservation(
            capability_id='cap.main', capability_version=version,
            provider_id=provider_id, operable=operable,
        )

    def _hooks(counter, component_ids):
        hooks = {}
        for component_id in component_ids:
            hooks[component_id] = {'enable': lambda: counter.append(1)}
        return hooks

    def _activated_fixture():
        texts = (
            _manifest_provide('t.prov1', '1.0.0'),
            _manifest_provide('t.prov2', '2.0.0'),
            _manifest_consume('t.cons1', '==1.0.0', 't.prov2', '2.0.0'),
            _manifest_consume('t.cons2', '==2.0.0', 't.prov1', '1.0.0'),
        )
        manifests = tuple(parser.parse_manifest_text(text) for text in texts)
        attestations = (
            _attestation('t.prov1', '1.0.0', 'COMPONENT', 't.prov1', '1.0.0'),
            _attestation('t.prov2', '2.0.0', 'COMPONENT', 't.prov2', '2.0.0'),
            _attestation('t.cons1', '1.0.0', 'COMPONENT', 't.cons1', '1.0.0'),
            _attestation('t.cons2', '1.0.0', 'COMPONENT', 't.cons2', '1.0.0'),
            _attestation('t.prov1', '1.0.0', 'CAPABILITY', 'cap.main', '1.0.0'),
            _attestation('t.prov2', '2.0.0', 'CAPABILITY', 'cap.main', '2.0.0'),
        )
        result = composition.compose(texts, attestations=attestations)
        assert result.stage == 'activated' and result.activated, result.stage
        assert result.diagnostics == (), result.diagnostics
        assert len(result.edges) == 4, result.edges
        assert set(result.edges) == {
            ('t.cons1', 't.prov1'), ('t.cons1', 't.prov2'),
            ('t.cons2', 't.prov2'), ('t.cons2', 't.prov1')}, result.edges
        assert tuple((d.capability_id, d.capability_version, d.provider_ref)
                     for d in result.capability_descriptors) == (
            ('cap.main', '1.0.0', 't.prov1'),
            ('cap.main', '2.0.0', 't.prov2')), result.capability_descriptors
        return result, manifests

    def _scenario_success(result, manifests):
        counter = []
        gated = availability.run_gated_hooks(
            result, manifests,
            hooks=_hooks(counter, ('t.cons1', 't.cons2')),
            observations=(_observation('1.0.0', 't.prov1'),
                          _observation('2.0.0', 't.prov2')),
        )
        assert gated.diagnostics == (), gated.diagnostics
        assert gated.warnings == (), gated.warnings
        assert len(gated.capability_states) == 2, gated.capability_states
        assert all(state.state == 'AVAILABLE'
                   for state in gated.capability_states), gated.capability_states
        assert len(gated.consumed_states) == 2, gated.consumed_states
        assert all(state.state == 'AVAILABLE'
                   for state in gated.consumed_states), gated.consumed_states
        assert len(gated.calls) == 2 and counter == [1, 1], (gated.calls, counter)

    def _scenario_wrong_provider(result, manifests):
        counter = []
        gated = availability.run_gated_hooks(
            result, manifests,
            hooks=_hooks(counter, ('t.cons1', 't.cons2')),
            observations=(_observation('2.0.0', 't.prov2'),),
        )
        assert {state.capability_version: state.state
                for state in gated.capability_states} == {
            '1.0.0': 'RESOLVED', '2.0.0': 'AVAILABLE'}, gated.capability_states
        consumed = gated.consumed_states
        assert len(consumed) == 2, consumed
        blocked = [s for s in consumed if s.state == 'BLOCKED']
        assert len(blocked) == 1 and blocked[0].consumer_id == 't.cons1', blocked
        available = [s for s in consumed if s.state == 'AVAILABLE']
        assert len(available) == 1, available
        assert available[0].consumer_id == 't.cons2', available
        assert gated.diagnostics, gated.diagnostics
        assert gated.calls == () and counter == [], (gated.calls, counter)

    def _scenario_required_refusals(result, manifests):
        cases = (
            ('missing', (), (), 'RESOLVED'),
            ('false', (_observation('1.0.0', 't.prov1', False),
                       _observation('2.0.0', 't.prov2', False)), (), 'BLOCKED'),
            ('disabled', (_observation('1.0.0', 't.prov1', True),
                          _observation('2.0.0', 't.prov2', True)),
             ('cap.main',), 'DISABLED'),
        )
        for name, observations, disabled, expected in cases:
            counter = []
            gated = availability.run_gated_hooks(
                result, manifests,
                hooks=_hooks(counter, ('t.cons1', 't.cons2')),
                observations=observations,
                disabled_capabilities=disabled)
            assert gated.diagnostics, (name, gated.diagnostics)
            assert tuple(
                state.state for state in gated.capability_states
            ) == (expected, expected), gated.capability_states
            assert all(state.state == 'BLOCKED'
                       for state in gated.consumed_states), gated.consumed_states
            assert gated.calls == () and counter == [], (name, gated.calls)
''')

_SCENARIOS_END = textwrap.dedent(r'''
    def _manifest_provide_optional(provider_id, version, fallback):
        return "\n".join([
            'schema_version = "1"', f'id = "{provider_id}"',
            'type = "PROVIDER"', f'version = "{version}"', "",
            "[provides]", "[[provides.capabilities]]",
            'id = "cap.opt"', f'version = "{version}"', "contracts = []",
            'criticality = "OPTIONAL"', f'fallback = "{fallback}"',
        ])

    def _manifest_consume_optional(
        consumer_id, optional_constraint, provider_id, provider_version
    ):
        return "\n".join([
            'schema_version = "1"', f'id = "{consumer_id}"',
            'type = "MODULE"', 'version = "1.0.0"', "",
            "[dependencies]",
            f'components = ["{provider_id} =={provider_version}"]',
            "[optional_dependencies]",
            f'capabilities = ["cap.opt {optional_constraint}"]',
        ])

    def _optional_fixture(fallback, constraint="==1.0.0", has_offer=True):
        if has_offer:
            provider_text = _manifest_provide_optional(
                't.prov3', '1.0.0', fallback)
        else:
            provider_text = "\n".join([
                'schema_version = "1"', 'id = "t.prov3"',
                'type = "PROVIDER"', 'version = "1.0.0"',
            ])
        texts = (
            provider_text,
            _manifest_consume_optional(
                't.opt1', constraint, 't.prov3', '1.0.0'),
        )
        manifests = tuple(parser.parse_manifest_text(text) for text in texts)
        attestations = [
            _attestation('t.prov3', '1.0.0', 'COMPONENT', 't.prov3', '1.0.0'),
            _attestation('t.opt1', '1.0.0', 'COMPONENT', 't.opt1', '1.0.0'),
        ]
        if has_offer and semver.matches('1.0.0', 'cap.opt ' + constraint):
            attestations.append(_attestation(
                't.prov3', '1.0.0', 'CAPABILITY', 'cap.opt', '1.0.0'))
        result = composition.compose(texts, attestations=attestations)
        assert result.stage == 'activated' and result.activated, result.stage
        assert result.diagnostics == (), result.diagnostics
        if not has_offer:
            assert result.capability_descriptors == (), result.capability_descriptors
        else:
            compatible = semver.matches('1.0.0', 'cap.opt ' + constraint)
            descriptor = result.capability_descriptors[0]
            assert (descriptor.capability_id, descriptor.capability_version,
                    descriptor.provider_ref) == (
                'cap.opt', '1.0.0',
                't.prov3' if compatible else None), descriptor
        return result, manifests

    HOST_TEST_FALLBACK = 'host.test.fallback'

    def _scenario_optional_fallback():
        cases = (
            ('absence', False, '==1.0.0', ()),
            ('incompat', True, '>=2.0.0', ('DECLARED',)),
            ('unobserved', True, '==1.0.0', ('RESOLVED',)),
        )
        for name, has_offer, constraint, expected in cases:
            result, manifests = _optional_fixture(
                't.repli.local', constraint=constraint, has_offer=has_offer)
            counter = []
            gated = availability.run_gated_hooks(
                result, manifests,
                hooks=_hooks(counter, ('t.opt1',)),
                observations=(),
                optional_fallbacks=(availability.CapabilityFallback(
                    'cap.opt', HOST_TEST_FALLBACK),),
            )
            assert gated.diagnostics == (), (name, gated.diagnostics)
            capstates = tuple(
                state.state for state in gated.capability_states)
            assert capstates == expected, (name, gated.capability_states)
            consumed = gated.consumed_states
            assert len(consumed) == 1, (name, consumed)
            assert consumed[0].state == 'DEGRADED', (name, consumed)
            assert consumed[0].fallback == HOST_TEST_FALLBACK, (name, consumed)
            assert len(gated.warnings) == 1, (name, gated.warnings)
            assert len(gated.calls) == 1, (name, gated.calls)
            assert counter == [1], (name, counter)

    def _scenario_optional_no_fallback():
        result, manifests = _optional_fixture('t.repli.local')
        counter = []
        gated = availability.run_gated_hooks(
            result, manifests,
            hooks=_hooks(counter, ('t.opt1',)),
            observations=(),
        )
        assert gated.diagnostics, gated.diagnostics
        consumed = gated.consumed_states
        assert len(consumed) == 1 and consumed[0].state == 'BLOCKED', consumed
        assert gated.calls == () and counter == [], (gated.calls, counter)

    def _scenario_optional_available():
        result, manifests = _optional_fixture('t.repli.local')
        counter = []
        observation = availability.CapabilityObservation(
            capability_id='cap.opt', capability_version='1.0.0',
            provider_id='t.prov3', operable=True)
        gated = availability.run_gated_hooks(
            result, manifests,
            hooks=_hooks(counter, ('t.opt1',)),
            observations=(observation,),
        )
        assert gated.diagnostics == () and gated.warnings == (), (
            gated.diagnostics, gated.warnings)
        consumed = gated.consumed_states
        assert len(consumed) == 1 and consumed[0].state == 'AVAILABLE', consumed
        assert len(gated.calls) == 1 and counter == [1], (gated.calls, counter)

    def _mixed_fixture():
        texts = (
            _manifest_provide('t.prov1', '1.0.0'),
            _manifest_provide_optional('t.prov3', '1.0.0', 't.repli.local'),
            _manifest_consume('t.cons1', '==1.0.0', 't.prov3', '1.0.0'),
            _manifest_consume_optional(
                't.opt1', '==1.0.0', 't.prov3', '1.0.0'),
        )
        manifests = tuple(parser.parse_manifest_text(text) for text in texts)
        attestations = (
            _attestation('t.prov1', '1.0.0', 'COMPONENT', 't.prov1', '1.0.0'),
            _attestation('t.prov3', '1.0.0', 'COMPONENT', 't.prov3', '1.0.0'),
            _attestation('t.cons1', '1.0.0', 'COMPONENT', 't.cons1', '1.0.0'),
            _attestation('t.opt1', '1.0.0', 'COMPONENT', 't.opt1', '1.0.0'),
            _attestation('t.prov1', '1.0.0', 'CAPABILITY', 'cap.main', '1.0.0'),
            _attestation('t.prov3', '1.0.0', 'CAPABILITY', 'cap.opt', '1.0.0'),
        )
        result = composition.compose(texts, attestations=attestations)
        assert result.stage == 'activated' and result.activated, result.stage
        assert result.diagnostics == (), result.diagnostics
        assert tuple((d.capability_id, d.capability_version, d.provider_ref)
                     for d in result.capability_descriptors) == (
            ('cap.main', '1.0.0', 't.prov1'),
            ('cap.opt', '1.0.0', 't.prov3')), result.capability_descriptors
        return result, manifests

    def _scenario_mixed_refusal():
        result, manifests = _mixed_fixture()
        counter = []
        gated = availability.run_gated_hooks(
            result, manifests,
            hooks=_hooks(counter, ('t.cons1', 't.opt1')),
            observations=(),
            optional_fallbacks=(availability.CapabilityFallback(
                'cap.opt', HOST_TEST_FALLBACK),),
        )
        assert gated.diagnostics, gated.diagnostics
        consumed = gated.consumed_states
        assert len(consumed) == 2, consumed
        by_consumer = {state.consumer_id: state for state in consumed}
        assert by_consumer['t.cons1'].state == 'BLOCKED', by_consumer
        assert by_consumer['t.opt1'].state == 'DEGRADED', by_consumer
        assert by_consumer['t.opt1'].fallback == HOST_TEST_FALLBACK, (
            by_consumer)
        assert len(gated.warnings) == 1, gated.warnings
        assert gated.calls == () and counter == [], (gated.calls, counter)
''')

_SCENARIOS_FINAL = textwrap.dedent(r'''
    from dataclasses import replace

    def _scenario_permutations():
        result, manifests = _activated_fixture()
        observations = (
            _observation('1.0.0', 't.prov1'),
            _observation('2.0.0', 't.prov2'),
        )
        fallbacks = (availability.CapabilityFallback('cap.other', 'host.other'),
                     availability.CapabilityFallback('cap.zed', 'host.zed'))
        disabled = ('cap.other', 'cap.zed')
        reference = availability.compute_capability_availability(
            result, manifests, observations,
            optional_fallbacks=fallbacks, disabled_capabilities=disabled)
        reversed_result = replace(
            result,
            edges=tuple(reversed(result.edges)),
            capability_descriptors=tuple(
                reversed(result.capability_descriptors)))
        variant = availability.compute_capability_availability(
            reversed_result, tuple(reversed(manifests)),
            tuple(reversed(observations)),
            optional_fallbacks=tuple(reversed(fallbacks)),
            disabled_capabilities=tuple(reversed(disabled)))
        assert variant == reference, (variant, reference)
        reference_counter = []
        reference_gated = availability.run_gated_hooks(
            result, manifests,
            hooks=_hooks(reference_counter, ('t.cons1', 't.cons2')),
            observations=observations,
            optional_fallbacks=fallbacks, disabled_capabilities=disabled)
        variant_counter = []
        variant_gated = availability.run_gated_hooks(
            reversed_result, tuple(reversed(manifests)),
            hooks=_hooks(variant_counter, ('t.cons1', 't.cons2')),
            observations=tuple(reversed(observations)),
            optional_fallbacks=tuple(reversed(fallbacks)),
            disabled_capabilities=tuple(reversed(disabled)))
        assert (variant_gated.capability_states,
                variant_gated.consumed_states,
                variant_gated.diagnostics,
                variant_gated.warnings) == (
            reference_gated.capability_states,
            reference_gated.consumed_states,
            reference_gated.diagnostics,
            reference_gated.warnings), (
            variant_gated, reference_gated)
        assert reference_counter == [1, 1], reference_counter
        assert variant_counter == [1, 1], variant_counter
        reference_calls = tuple(
            (call.component_id, call.hook)
            for call in reference_gated.calls)
        variant_calls = tuple(
            (call.component_id, call.hook)
            for call in variant_gated.calls)
        assert reference_calls == variant_calls, (
            reference_calls, variant_calls)

    def _scenario_exception():
        result, manifests = _activated_fixture()
        observations = (
            _observation('1.0.0', 't.prov1'),
            _observation('2.0.0', 't.prov2'),
        )
        effects = []

        def first_callback():
            effects.append('first')

        def failing_callback():
            effects.append('second')
            raise RuntimeError('callback failure')

        hooks = {
            't.cons1': {'enable': first_callback},
            't.cons2': {'enable': failing_callback},
        }
        try:
            availability.run_gated_hooks(
                result, manifests, hooks=hooks,
                observations=observations)
        except RuntimeError as exc:
            assert str(exc) == 'callback failure', exc
        else:
            raise AssertionError('exception not propagated')
        assert effects == ['first', 'second'], effects

    def _scenario_optional_operability():
        result, manifests = _optional_fixture('t.repli.local')
        for operable, disabled, expected in (
            (False, (), 'BLOCKED'),
            (True, ('cap.opt',), 'DISABLED'),
        ):
            effects = []
            observation = availability.CapabilityObservation(
                'cap.opt', '1.0.0', 't.prov3', operable)
            gated = availability.run_gated_hooks(
                result, manifests, hooks=_hooks(effects, ('t.opt1',)),
                observations=(observation,), disabled_capabilities=disabled,
                optional_fallbacks=(availability.CapabilityFallback(
                    'cap.opt', HOST_TEST_FALLBACK),))
            assert gated.diagnostics == (), gated.diagnostics
            assert len(gated.capability_states) == 1
            assert gated.capability_states[0].state == expected
            assert gated.consumed_states[0].state == 'DEGRADED'
            assert len(gated.warnings) == 1 and effects == [1]
            assert len(gated.calls) == 1

    result, manifests = _activated_fixture()
    _scenario_success(result, manifests)
    _scenario_wrong_provider(result, manifests)
    _scenario_required_refusals(result, manifests)
    _scenario_optional_fallback()
    _scenario_optional_no_fallback()
    _scenario_optional_available()
    _scenario_optional_operability()
    _scenario_mixed_refusal()
    _scenario_permutations()
    _scenario_exception()

    assert blocked == [], blocked
    counts = [guard.call_count for guard in guards]
    assert all(count == 0 for count in counts), counts
    print('AVAILABILITY_GATE_INTEGRATION_OK')
''')


class TestCapabilityAvailabilityGateIntegration(unittest.TestCase):
    def test_availability_gate_scenarios_under_guards(self):
        child = _PREFIX + textwrap.indent(
            _SCENARIOS_START + _SCENARIOS_END + _SCENARIOS_FINAL, "    ")
        proc = _run(child)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "AVAILABILITY_GATE_INTEGRATION_OK\n",
                         proc.stdout)


if __name__ == "__main__":
    unittest.main()
