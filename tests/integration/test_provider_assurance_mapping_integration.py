"""Tests d'intégration du mapping d'assurance fournisseur (tâche 2.3).

Le scénario s'exécute dans un sous-processus frais (``sys.executable -B``,
environnement minimal explicite) où les douze gardes d'E/S fonctionnelles et
le finder bloquant Django/SQLite/psycopg/requests/urllib3 sont activés et
réellement sondés AVANT l'import de ``pixs.core.authz.assurance_mapping``,
puis réinitialisés ; les compteurs sont revérifiés à zéro après usage réel. La
machinerie d'import conserve la lecture normale des sources via ``io`` : cette
suite ne revendique aucune absence de lecture physique. Aucune authentification
réelle, aucune cryptographie, aucun credential, aucune horloge système, aucun
Django/PostgreSQL/réseau ; horodatages UTC fixes.
"""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "PROVIDER_ASSURANCE_MAPPING_INTEGRATION_OK"
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
    from datetime import datetime, timezone
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

    class Trap:
        def __init__(self):
            object.__setattr__(self, 'calls', [])

        def __eq__(self, other):
            object.__getattribute__(self, 'calls').append('eq')
            return False

        def __hash__(self):
            object.__getattribute__(self, 'calls').append('hash')
            return 1

        def __str__(self):
            object.__getattribute__(self, 'calls').append('str')
            return 'trap'

        def __repr__(self):
            object.__getattribute__(self, 'calls').append('repr')
            return '<trap>'

        def __bool__(self):
            object.__getattribute__(self, 'calls').append('bool')
            return True

        def __iter__(self):
            object.__getattribute__(self, 'calls').append('iter')
            return iter(())

    from pixs.core.authz.assurance_mapping import (
        AssuranceDimension,
        AssuranceMappingError,
        AssuranceRule,
        ProofObservation,
        ProviderAssuranceMapping,
        evaluate_assurance,
    )
    from pixs.core.authz.policy import (
        AuthenticationAssurance,
        FederationTrust,
        IdentityAssurance,
    )

    utc = timezone.utc
    VALID_FROM = datetime(2026, 1, 1, tzinfo=utc)
    VALID_UNTIL = datetime(2027, 1, 1, tzinfo=utc)
    REF = datetime(2026, 6, 1, tzinfo=utc)
    ATTESTED = datetime(2026, 5, 1, tzinfo=utc)
    EXPIRES = datetime(2026, 12, 1, tzinfo=utc)

    def witness_rule(dimension, method, level):
        return AssuranceRule(dimension=dimension, method=method, level=level)

    MAPPING = ProviderAssuranceMapping(
        provider_id='t.sso',
        max_identity_assurance=IdentityAssurance.PROOFED,
        max_authentication_assurance=AuthenticationAssurance.PHISHING_RESISTANT,
        max_federation_trust=FederationTrust.STRONGLY_BOUND,
        accepted_rules=(
            witness_rule(
                AssuranceDimension.IDENTITY, 'webauthn',
                IdentityAssurance.VERIFIED,
            ),
        ),
        valid_from=VALID_FROM,
        valid_until=VALID_UNTIL,
    )

    def witness_observation(**overrides):
        fields = {
            'observation_id': 'obs-1',
            'provider_id': 't.sso',
            'method': 'webauthn',
            'status': 'VERIFIED',
            'attested_at': ATTESTED,
            'expires_at': EXPIRES,
        }
        fields.update(overrides)
        return ProofObservation(**fields)

    OBSERVATION = witness_observation()

    result = evaluate_assurance(MAPPING, (OBSERVATION,), REF)
    assert result.identity_assurance is IdentityAssurance.VERIFIED, result
    assert (
        result.authentication_assurance
        is AuthenticationAssurance.SINGLE_FACTOR
    ), result
    assert result.federation_trust is FederationTrust.UNTRUSTED, result

    repeated = evaluate_assurance(MAPPING, (OBSERVATION,), REF)
    assert repeated == result
    second = witness_observation(observation_id='obs-2')
    assert evaluate_assurance(MAPPING, (OBSERVATION, second), REF) == result
    assert evaluate_assurance(MAPPING, (second, OBSERVATION), REF) == result

    for status in ('ABSENT', 'AMBIGUOUS', 'EXPIRED', 'UNVERIFIED'):
        stalled = evaluate_assurance(
            MAPPING, (witness_observation(status=status),), REF
        )
        assert stalled.identity_assurance is IdentityAssurance.CLAIMED, status
    foreign = evaluate_assurance(
        MAPPING, (witness_observation(provider_id='autre.sso'),), REF
    )
    assert foreign.identity_assurance is IdentityAssurance.CLAIMED

    stale_mapping = replace(
        MAPPING,
        valid_from=datetime(2020, 1, 1, tzinfo=utc),
        valid_until=datetime(2021, 1, 1, tzinfo=utc),
    )
    minima = evaluate_assurance(stale_mapping, (OBSERVATION,), REF)
    assert minima.identity_assurance is IdentityAssurance.CLAIMED
    assert (
        minima.authentication_assurance
        is AuthenticationAssurance.SINGLE_FACTOR
    )
    assert minima.federation_trust is FederationTrust.UNTRUSTED
    try:
        evaluate_assurance(
            stale_mapping,
            (OBSERVATION, witness_observation(observation_id='obs-1')),
            REF,
        )
    except AssuranceMappingError:
        pass
    else:
        raise AssertionError('malformed observation hidden by stale mapping')

    over_ceiling = replace(
        MAPPING,
        max_identity_assurance=IdentityAssurance.CLAIMED,
    )
    try:
        evaluate_assurance(over_ceiling, (OBSERVATION,), REF)
    except AssuranceMappingError:
        pass
    else:
        raise AssertionError('level above ceiling accepted')
    assert evaluate_assurance(MAPPING, (OBSERVATION,), REF) == result

    expired = evaluate_assurance(
        MAPPING,
        (witness_observation(attested_at=ATTESTED, expires_at=REF),),
        REF,
    )
    assert expired.identity_assurance is IdentityAssurance.CLAIMED

    traps = {
        'provider_id': Trap(),
        'method': Trap(),
        'status': Trap(),
    }
    for field, trap in traps.items():
        try:
            evaluate_assurance(
                MAPPING, (witness_observation(**{field: trap}),), REF
            )
        except AssuranceMappingError:
            pass
        else:
            raise AssertionError('hostile field accepted')
    forged = object.__new__(IdentityAssurance)
    forged_name = Trap()
    object.__setattr__(forged, '_name_', forged_name)
    try:
        evaluate_assurance(
            replace(
                MAPPING,
                accepted_rules=(
                    witness_rule(
                        AssuranceDimension.IDENTITY, 'webauthn', forged
                    ),
                ),
            ),
            (OBSERVATION,),
            REF,
        )
    except AssuranceMappingError:
        pass
    else:
        raise AssertionError('forged enum level accepted')

    assert object.__getattribute__(traps['provider_id'], 'calls') == []
    assert object.__getattribute__(traps['method'], 'calls') == []
    assert object.__getattribute__(traps['status'], 'calls') == []
    assert object.__getattribute__(forged_name, 'calls') == []

    assert blocked == [], blocked
    counts = [guard.call_count for guard in guards]
    assert all(count == 0 for count in counts), counts
    print('PROVIDER_ASSURANCE_MAPPING_INTEGRATION_OK')
''')


class TestProviderAssuranceMappingIntegration(unittest.TestCase):
    def test_mapping_scenarios_under_guards(self) -> None:
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
