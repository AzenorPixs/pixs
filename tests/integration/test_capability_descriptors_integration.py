"""Tests d'intégration des descripteurs de capacités via compose (tâche 2.4).

Chaque scénario s'exécute dans un sous-processus frais (``sys.executable``)
dont les gardes d'E/S sont activées causalement AVANT l'import du noyau :
chaque garde est prouvée active par une sonde, puis les compteurs sont
réinitialisés ; après les scénarios, aucun appel résiduel n'est toléré.
Les fixtures ``t.*`` sont des manifests synthétiques de confiance ; les
preuves ``ConformityAttestation`` sont des doubles exclusivement destinés
aux tests (suite et référence ``synthetic:``), aux neuf champs exacts et
aux versions propres exactes, couvrant chaque composant et chaque capacité
effectivement résolue. Sans preuve, ``compose`` refuse et reste inactif,
la liaison descriptrice subsistant structurellement. Aucun état de
disponibilité, aucune activation runtime, aucun Django, PostgreSQL,
réseau ni disque.
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


_GUARDED = textwrap.dedent(r'''
    import builtins
    import importlib.abc
    import os
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from dataclasses import fields
    from pathlib import Path
    from unittest import mock

    src = sys.argv[1]
    sys.path.insert(0, src)

    blocked = []

    class BlockSQLAndDjango(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            base = name.split('.')[0]
            if base in ('django', 'sqlite3', 'psycopg', 'psycopg2', 'requests', 'urllib3'):
                blocked.append(name)
                raise ImportError('blocked')
            return None

    sys.meta_path.insert(0, BlockSQLAndDjango())

    for module_name in ('django', 'psycopg'):
        try:
            importlib.import_module(module_name)
        except ImportError as exc:
            assert str(exc) == 'blocked', exc
        else:
            raise AssertionError('import guard not active')
    assert blocked == ['django', 'psycopg'], blocked
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

        def attestation(component_id, component_version, scope, target_id, target_version):
            return composition.ConformityAttestation(
                component_id=component_id,
                component_version=component_version,
                scope=scope,
                target_id=target_id,
                target_version=target_version,
                suite_id='suite.test.only',
                suite_version='1.0.0',
                verdict='PASS',
                proof_ref='synthetic:test-only',
            )

        prov_text = "\n".join(
            [
                'schema_version = "1"',
                'id = "t.prov"',
                'type = "PROVIDER"',
                'version = "1.2.0+build.7"',
                "",
                "[provides]",
                "[[provides.capabilities]]",
                'id = "cap.main"',
                'version = "2.0.0"',
                "contracts = []",
                'criticality = "REQUIRED"',
                'fallback = "none"',
            ]
        )
        cons_text = "\n".join(
            [
                'schema_version = "1"',
                'id = "t.cons"',
                'type = "MODULE"',
                'version = "0.3.0"',
                "",
                "[dependencies]",
                'capabilities = ["cap.main >=1.0.0"]',
            ]
        )
        solo_text = "\n".join(
            [
                'schema_version = "1"',
                'id = "t.solo"',
                'type = "MODULE"',
                'version = "1.1.0"',
                "",
                "[provides]",
                "[[provides.capabilities]]",
                'id = "cap.solo"',
                'version = "0.9.0"',
                "contracts = []",
                'criticality = "OPTIONAL"',
                'fallback = "t.repli.local"',
            ]
        )
        bad_text = "\n".join(
            [
                'schema_version = "1"',
                'id = "t.bad"',
                'type = "APPLICATION"',
                'version = "1.0.0"',
            ]
        )
        orphan_text = "\n".join(
            [
                'schema_version = "1"',
                'id = "t.orphan"',
                'type = "MODULE"',
                'version = "0.2.0"',
                "",
                "[dependencies]",
                'capabilities = ["cap.absente >=1.0.0"]',
            ]
        )

        attestations = (
            attestation('t.prov', '1.2.0+build.7', 'COMPONENT', 't.prov', '1.2.0+build.7'),
            attestation('t.cons', '0.3.0', 'COMPONENT', 't.cons', '0.3.0'),
            attestation('t.solo', '1.1.0', 'COMPONENT', 't.solo', '1.1.0'),
            attestation('t.prov', '1.2.0+build.7', 'CAPABILITY', 'cap.main', '2.0.0'),
        )

        success_texts = (prov_text, cons_text, solo_text)
        success = composition.compose(success_texts, attestations=attestations)
        assert success.stage == 'activated', success.stage
        assert success.activated
        assert success.diagnostics == (), success.diagnostics
        descriptors = success.capability_descriptors
        assert tuple(d.capability_id for d in descriptors) == ('cap.main', 'cap.solo'), descriptors
        main, solo = descriptors
        assert (
            main.capability_id,
            main.capability_version,
            main.owner_component,
            main.contract_refs,
            main.provider_ref,
            main.criticality,
            main.fallback,
        ) == ('cap.main', '2.0.0', 't.prov', (), 't.prov', 'REQUIRED', 'none'), main
        assert (
            solo.capability_id,
            solo.capability_version,
            solo.owner_component,
            solo.contract_refs,
            solo.provider_ref,
            solo.criticality,
            solo.fallback,
        ) == ('cap.solo', '0.9.0', 't.solo', (), None, 'OPTIONAL', 't.repli.local'), solo

        reversed_success = composition.compose(
            tuple(reversed(success_texts)),
            attestations=tuple(reversed(attestations)),
        )
        assert reversed_success == success, (reversed_success, success)

        configured = composition.compose(
            success_texts,
            configured_providers={'cap.main': 't.prov'},
            attestations=attestations,
        )
        assert configured.activated
        assert configured.capability_descriptors == success.capability_descriptors

        refused = composition.compose(success_texts, attestations=())
        assert refused.stage == 'resolve' and not refused.activated
        assert refused.diagnostics and not refused.order and not refused.edges
        assert refused.capability_descriptors == success.capability_descriptors, refused.capability_descriptors
        by_id = {d.capability_id: d.provider_ref for d in refused.capability_descriptors}
        assert by_id == {'cap.main': 't.prov', 'cap.solo': None}, by_id

        invalid = composition.compose((bad_text, prov_text), attestations=attestations)
        assert invalid.stage == 'validate' and not invalid.activated
        assert invalid.capability_descriptors == ()

        unresolved = composition.compose(
            (orphan_text, prov_text, solo_text), attestations=attestations
        )
        assert unresolved.stage == 'resolve' and not unresolved.activated
        assert unresolved.diagnostics
        assert len(unresolved.capability_descriptors) == 2, unresolved.capability_descriptors
        assert all(d.provider_ref is None for d in unresolved.capability_descriptors)

        exact_fields = (
            'capability_id',
            'capability_version',
            'owner_component',
            'contract_refs',
            'provider_ref',
            'criticality',
            'fallback',
        )
        assert tuple(f.name for f in fields(main)) == exact_fields, fields(main)
        assert not hasattr(success, 'availability')
        assert not any(
            hasattr(d, 'availability') or hasattr(d, 'status') or hasattr(d, 'activated')
            for d in descriptors
        )

    assert blocked == [], blocked
    counts = [guard.call_count for guard in guards]
    assert all(count == 0 for count in counts), counts
    print('GUARDS_OK')
''')


class TestDescripteursCapacitesSousGardes(unittest.TestCase):
    def test_import_et_compose_sous_gardes_io(self) -> None:
        proc = _run(_GUARDED)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "GUARDS_OK\n")
        self.assertEqual(proc.stderr, "", proc.stderr)


if __name__ == "__main__":
    unittest.main()
