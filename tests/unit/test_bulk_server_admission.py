"""Tests unitaires inertes du service B01, sans persistance ni ORM.

Ce fichier ne réalise aucune admission réussie persistante : la preuve
positive de rejeu et de persistance appartient au test PG dédié.
"""

import builtins
import copy
import os
import pathlib
import socket
import subprocess
import sys
import unittest
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
from unittest import mock

import pixs.backend.bulk_server_admission as admission
from pixs.backend.bulk_server_admission import (
    BulkAdmissionRefused,
    _check_new_path_initial,
    _check_new_path_temporal,
)
import pixs.backend.bulk_trusted_ports as ports
from unit.test_bulk_execution_values import (
    _ForeignDict,
    _ForeignList,
    _valid_execution_import,
    _valid_policy,
)
from unit.test_bulk_runtime_contracts import (
    _CODES,
    _FIELDS,
    _ForeignStr,
    _ForeignTuple,
    _Hostile,
    _authority,
    _context,
    _mapping,
)
from unit.test_bulk_trusted_ports import (
    _Authority,
    _GovernanceResolve3,
    _Resolver,
    _compose_gov,
    _resolved_response,
    _valid_profile,
)

FIXED_MESSAGE = "admission bulk refusée"
FIXED_NOW = datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc)


class _TracedForeignStr(_ForeignStr):
    """Chaîne étrangère à hash natif avec compteur sans formatage."""

    encode_calls = 0

    def encode(self, *args, **kwargs):
        type(self).encode_calls += 1
        raise AssertionError("encodage étranger refusé")


class _TracedHostile(_Hostile):
    """Valeur hostile avec compteurs sans formatage."""

    hash_calls = 0
    eq_calls = 0
    str_calls = 0

    def __hash__(self):
        type(self).hash_calls += 1
        raise AssertionError("hash étranger refusé")

    def __eq__(self, other):
        type(self).eq_calls += 1
        raise AssertionError("égalité étrangère refusée")

    def __str__(self):
        type(self).str_calls += 1
        raise AssertionError("texte étranger refusé")


class _InertGuards:
    """Gardes refusant ORM, réseau, processus et lectures sensibles."""

    def __init__(self, orm_marker=None):
        self.orm_marker = orm_marker or "blocage ORM du test inerte"
        self.orm_attempts = 0
        self.network_attempts = 0
        self.process_attempts = 0
        self.file_attempts = 0
        self.env_attempts = 0
        self._origin_import = builtins.__import__
        self._origin_open = builtins.open
        self._origin_path_open = pathlib.Path.open
        self._origin_read_text = pathlib.Path.read_text
        self._origin_read_bytes = pathlib.Path.read_bytes
        self._origin_getenv = os.getenv
        self._origin_socket = socket.socket
        self._origin_popen = subprocess.Popen
        self._origin_run = subprocess.run
        self._stack = ExitStack()

    def _guarded_import(self, name, *args, **kwargs):
        base = name.split(".")[0]
        if base in ("django", "psycopg"):
            self.orm_attempts += 1
            raise ImportError(self.orm_marker)
        return self._origin_import(name, *args, **kwargs)

    def _guarded_open(self, *args, **kwargs):
        self.file_attempts += 1
        raise OSError("lecture de données refusée par le test inerte")

    def _guarded_path_open(self, *args, **kwargs):
        self.file_attempts += 1
        raise OSError("lecture de données refusée par le test inerte")

    def _guarded_read_text(self, *args, **kwargs):
        self.file_attempts += 1
        raise OSError("lecture de données refusée par le test inerte")

    def _guarded_read_bytes(self, *args, **kwargs):
        self.file_attempts += 1
        raise OSError("lecture de données refusée par le test inerte")

    def _guarded_getenv(self, *args, **kwargs):
        self.env_attempts += 1
        raise AssertionError("accès environnement refusé par le test inerte")

    def _guarded_environ_get(self, *args, **kwargs):
        self.env_attempts += 1
        raise AssertionError("accès environnement refusé par le test inerte")

    def _guarded_socket(self, *args, **kwargs):
        self.network_attempts += 1
        raise OSError("réseau refusé par le test inerte")

    def _guarded_popen(self, *args, **kwargs):
        self.process_attempts += 1
        raise OSError("processus refusé par le test inerte")

    def _guarded_run(self, *args, **kwargs):
        self.process_attempts += 1
        raise OSError("processus refusé par le test inerte")

    def __enter__(self):
        stack = self._stack
        stack.enter_context(mock.patch.object(builtins, "__import__", side_effect=self._guarded_import))
        stack.enter_context(mock.patch.object(builtins, "open", side_effect=self._guarded_open))
        stack.enter_context(mock.patch.object(pathlib.Path, "open", self._guarded_path_open))
        stack.enter_context(mock.patch.object(pathlib.Path, "read_text", self._guarded_read_text))
        stack.enter_context(mock.patch.object(pathlib.Path, "read_bytes", self._guarded_read_bytes))
        stack.enter_context(mock.patch.object(os, "getenv", side_effect=self._guarded_getenv))
        stack.enter_context(mock.patch.object(os.environ, "get", self._guarded_environ_get))
        stack.enter_context(mock.patch.object(socket, "socket", side_effect=self._guarded_socket))
        stack.enter_context(mock.patch.object(subprocess, "Popen", side_effect=self._guarded_popen))
        stack.enter_context(mock.patch.object(subprocess, "run", side_effect=self._guarded_run))
        return self

    def __exit__(self, *args):
        self._stack.close()
        return False


def _assert_closed_refusal(case, error):
    """Vérifie le refus statique sans cause brute."""
    case.assertIs(type(error), BulkAdmissionRefused)
    case.assertEqual(str(error), FIXED_MESSAGE)
    case.assertIsNone(error.__context__)
    case.assertIsNone(error.__cause__)


def _base_time(policy):
    """Fournit des instants cohérents avec la politique fournie."""
    start = FIXED_NOW
    operation_expiry = start + timedelta(seconds=policy["max_runtime_seconds"] - 60)
    identity_expiry = operation_expiry + timedelta(seconds=policy["replay_window_seconds"] + 60)
    return start, operation_expiry, identity_expiry


def _new_execution(policy, operation_expiry):
    """Construit une exécution initiale neuve et cohérente."""
    candidate = _valid_execution_import()
    mapping = _mapping()
    context = _context()
    progress = {
        "total_rows": 0,
        "validated_rows": 0,
        "invalid_rows": 0,
        "applied_rows": 0,
        "execution_rejected_rows": 0,
        "exported_rows": 0,
    }
    candidate.update(
        {
            "status": "REQUESTED",
            "revision": 1,
            "cancellation_requested": False,
            "checkpoint_reference": None,
            "result_reference": None,
            "output_reference": None,
            "output_version": None,
            "output_sha256": None,
            "output_size_bytes": None,
            "progress": progress,
            "mapping_reference": mapping["mapping_reference"],
            "mapping_version": mapping["mapping_version"],
            "resolved_context_reference": context["context_reference"],
            "policy_reference": "policy-test",
            "policy_version": "1.0.0",
            "expires_at": operation_expiry,
        }
    )
    return candidate


def _new_schedule(job_id="job-0001"):
    """Construit un horaire synthétique à sept clés exactes."""
    return {
        "job_id": job_id,
        "policy_reference": "policy-test",
        "policy_version": "1.0.0",
        "next_run_at": None,
        "attempt_deadline": None,
        "failure_code": None,
        "revision": 1,
    }


def _valid_composition():
    """Compose réellement des ports synthétiques déclarés."""
    authority = _Authority(response=_authority())
    resolver = _Resolver()
    governance = _GovernanceResolve3(
        response=_resolved_response(policy_ref="policy-test", policy_ver="1.0.0")
    )
    bundle = ports.compose_bulk_trusted_ports(
        authority_adapter=authority,
        mapping_resolver=resolver,
        mapping_descriptors=(_mapping(),),
        owner_declarations=(("owner-test", "1.0.0", _CODES, _FIELDS),),
        governance_adapter=governance,
        owner_command_adapter=None,
        owner_projection_adapter=None,
        audit_adapter=None,
    )
    return bundle, authority, resolver, governance


def _valid_arguments():
    """Assemble des arguments valides jusqu à la frontière ORM."""
    policy = _valid_policy()
    start, operation_expiry, identity_expiry = _base_time(policy)
    bundle, authority, resolver, governance = _valid_composition()
    arguments = {
        "trusted_ports": bundle,
        "server_context": object(),
        "using": "base-test",
        "execution_values": _new_execution(policy, operation_expiry),
        "policy": policy,
        "owner_reference": "owner-test",
        "job_id": "job-0001",
        "job_causation_id": "cause-0001",
        "schedule_values": _new_schedule(),
        "identity_expires_at": identity_expiry,
        "failure_codes": frozenset({"ECHEC_TEST"}),
        "now_utc": start,
    }
    return arguments, authority, resolver, governance


def _arguments_with_governance(response=None, failed=False):
    """Recompose avec les vrais objets autorité et résolveur."""
    authority = _Authority(response=_authority())
    resolver = _Resolver()
    governance = _GovernanceResolve3(response=response, fail=failed)
    bundle = ports.compose_bulk_trusted_ports(
        authority_adapter=authority,
        mapping_resolver=resolver,
        mapping_descriptors=(_mapping(),),
        owner_declarations=(("owner-test", "1.0.0", _CODES, _FIELDS),),
        governance_adapter=governance,
        owner_command_adapter=None,
        owner_projection_adapter=None,
        audit_adapter=None,
    )
    arguments, _, _, _ = _valid_arguments()
    arguments["trusted_ports"] = bundle
    return arguments, authority, resolver, governance


class _OrderAuthority:
    """Autorité traçante sans preuve de production."""

    def __init__(self, trace):
        self.trace = trace
        self.calls = []

    def check(self, context, action, operation, resource):
        self.trace.append("authority")
        self.calls.append((context, action, operation, resource))
        return _authority()


class _OrderResolver:
    """Résolveur traçant sans preuve de production."""

    def __init__(self, trace):
        self.trace = trace
        self.calls = []

    def resolve(self, reference, version, owner):
        self.trace.append("mapping")
        self.calls.append((reference, version, owner))
        value = _mapping()
        value.update(mapping_reference=reference, mapping_version=version, owner_reference=owner)
        return value


class _OrderGovernance:
    """Gouvernance traçante sans preuve de production."""

    def __init__(self, trace):
        self.trace = trace
        self.calls = []

    def resolve(self, context, contract, references):
        self.trace.append("governance")
        self.calls.append((context, contract, references))
        return _resolved_response(policy_ref="policy-test", policy_ver="1.0.0")


class FreshImportTests(unittest.TestCase):
    """Import frais du service sous gardes strictes."""

    def test_fresh_subprocess_import_without_orm_or_data(self):
        """L import frais sous gardes refuse ORM et lectures sensibles."""
        lines = [
            "import sys",
            "import builtins",
            "import os",
            "import pathlib",
            "import socket",
            "import subprocess",
            "",
            "",
            "def guarded_import(name, *args, **kwargs):",
            "    base = name.split('.')[0]",
            "    if base in ('django', 'psycopg'):",
            "        raise ImportError('blocage ORM du frais')",
            "    return origin_import(name, *args, **kwargs)",
            "",
            "",
            "def guarded_open(*args, **kwargs):",
            "    raise OSError('lecture refusée par le frais')",
            "",
            "",
            "def guarded_getenv(*args, **kwargs):",
            "    raise AssertionError('environnement refusé par le frais')",
            "",
            "",
            "target = 'pixs.backend.bulk_server_admission'",
            "assert target not in sys.modules, 'module déjà chargé'",
            "origin_import = builtins.__import__",
            "origin_open = builtins.open",
            "origin_getenv = os.getenv",
            "origin_socket = socket.socket",
            "origin_popen = subprocess.Popen",
            "origin_run = subprocess.run",
            "builtins.__import__ = guarded_import",
            "builtins.open = guarded_open",
            "pathlib.Path.open = lambda *a, **k: (_ for _ in ()).throw(OSError('lecture refusée'))",
            "os.getenv = guarded_getenv",
            "socket.socket = lambda *a, **k: (_ for _ in ()).throw(OSError('réseau refusé'))",
            "subprocess.Popen = lambda *a, **k: (_ for _ in ()).throw(OSError('processus refusé'))",
            "try:",
            "    import pixs.backend.bulk_server_admission as service",
            "    import pixs.backend.bulk_trusted_ports",
            "    import pixs.backend.bulk_execution_values",
            "    assert hasattr(service, 'admit_bulk_operation')",
            "    print('frais-valide')",
            "finally:",
            "    builtins.__import__ = origin_import",
            "    builtins.open = origin_open",
            "    os.getenv = origin_getenv",
            "    socket.socket = origin_socket",
            "    subprocess.Popen = origin_popen",
            "    subprocess.run = origin_run",
        ]
        script = "\n".join(lines)
        completed = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("frais-valide", completed.stdout)


class FakePortsTests(unittest.TestCase):
    """Ports fictifs refusés sans exécution de hook."""

    def test_dynamic_ports_refused_without_hook(self):
        """Un port fictif dynamique est refusé avant tout hook."""
        calls = []

        class FakePorts:
            def __getattr__(self, name):
                calls.append("getattr")
                raise AssertionError("accès dynamique exécuté")

            def __getattribute__(self, name):
                if name in ("resolve_mapping", "check_authority", "resolve_governance"):
                    calls.append(name)
                    raise AssertionError("attribut dynamique exécuté")
                return object.__getattribute__(self, name)

        arguments, _, _, _ = _valid_arguments()
        arguments["trusted_ports"] = FakePorts()
        with _InertGuards():
            with self.assertRaises(BulkAdmissionRefused) as captured:
                admission.admit_bulk_operation(**arguments)
        _assert_closed_refusal(self, captured.exception)
        self.assertEqual(calls, [])


class ExactTypesTests(unittest.TestCase):
    """Types exacts validés avant parse, sémantique, ports et ORM."""

    def _refused_before_late(self, mutation):
        arguments, authority, resolver, governance = _valid_arguments()
        mutation(arguments)
        with mock.patch.object(
            admission, "validate_bulk_execution_values", wraps=admission.validate_bulk_execution_values
        ) as spy_execution, mock.patch.object(
            admission, "validate_bulk_policy_values", wraps=admission.validate_bulk_policy_values
        ) as spy_policy, mock.patch.object(
            admission, "parse_version", wraps=admission.parse_version
        ) as spy_parse, mock.patch.object(
            admission, "_is_opaque_text", wraps=admission._is_opaque_text
        ) as spy_opaque:
            with _InertGuards() as guards:
                with self.assertRaises(BulkAdmissionRefused) as captured:
                    admission.admit_bulk_operation(**arguments)
        _assert_closed_refusal(self, captured.exception)
        spy_execution.assert_not_called()
        spy_policy.assert_not_called()
        spy_parse.assert_not_called()
        spy_opaque.assert_not_called()
        self.assertEqual(authority.calls, [])
        self.assertEqual(resolver.calls, [])
        self.assertEqual(governance.calls, [])
        self.assertEqual(guards.orm_attempts, 0)
        self.assertEqual(guards.network_attempts, 0)
        self.assertEqual(guards.process_attempts, 0)
        self.assertEqual(guards.file_attempts, 0)
        self.assertEqual(guards.env_attempts, 0)

    def test_foreign_channel_refused_before_late(self):
        """Un canal étranger est refusé avant tout contrôle tardif."""
        for value in (None, 42, [], {}, _TracedHostile(), _ForeignStr("base-test")):
            with self.subTest(kind=type(value).__name__):
                _TracedHostile.hash_calls = 0
                _TracedHostile.eq_calls = 0
                _TracedHostile.str_calls = 0
                self._refused_before_late(lambda args, item=value: args.update({"using": item}))
                self.assertEqual(_TracedHostile.hash_calls, 0)
                self.assertEqual(_TracedHostile.eq_calls, 0)
                self.assertEqual(_TracedHostile.str_calls, 0)

    def test_foreign_execution_refused_before_late(self):
        """Une exécution étrangère est refusée avant tout contrôle tardif."""
        for value in (None, [], "chaîne", 42, _ForeignDict({"a": "b"})):
            with self.subTest(kind=type(value).__name__):
                self._refused_before_late(lambda args, item=value: args.update({"execution_values": item}))

    def test_missing_unknown_foreign_keys_refused(self):
        """Clés manquantes, inconnues ou étrangères refusées avant tardif."""
        base = _valid_arguments()[0]["execution_values"]

        def without_key(args):
            candidate = dict(base)
            candidate.pop("operation_id")
            args["execution_values"] = candidate

        def unknown_key(args):
            candidate = dict(base)
            candidate["CLE_INCONNUE"] = 1
            args["execution_values"] = candidate

        def foreign_key(args):
            _TracedForeignStr.encode_calls = 0
            candidate = dict(base)
            candidate[_TracedForeignStr("cle-etrangere")] = 1
            args["execution_values"] = candidate

        for mutation in (without_key, unknown_key, foreign_key):
            self._refused_before_late(mutation)
        self.assertEqual(_TracedForeignStr.encode_calls, 0)

    def test_bool_on_int_refused_before_late(self):
        """Un booléen sur un entier exact est refusé avant tout tardif."""

        def execution_bool(args):
            candidate = dict(args["execution_values"])
            candidate["revision"] = True
            args["execution_values"] = candidate

        def schedule_bool(args):
            schedule = dict(args["schedule_values"])
            schedule["revision"] = True
            args["schedule_values"] = schedule

        def policy_bool(args):
            policy = dict(args["policy"])
            policy["max_rows"] = True
            args["policy"] = policy

        for mutation in (execution_bool, schedule_bool, policy_bool):
            self._refused_before_late(mutation)

    def test_policy_lists_refused_before_late(self):
        """Listes de politique étrangères ou tuples refusées avant tardif."""

        def foreign_list(args):
            policy = dict(args["policy"])
            policy["retry_delays_seconds"] = _ForeignList([1])
            args["policy"] = policy

        def tuple_for_list(args):
            policy = dict(args["policy"])
            policy["retry_delays_seconds"] = (1, 2)
            args["policy"] = policy

        for mutation in (foreign_list, tuple_for_list):
            self._refused_before_late(mutation)

    def test_bad_progress_refused_before_late(self):
        """Un progress mal typé est refusé avant tout contrôle tardif."""

        def progress_list(args):
            candidate = dict(args["execution_values"])
            candidate["progress"] = []
            args["execution_values"] = candidate

        def progress_field(args):
            candidate = dict(args["execution_values"])
            progress = dict(candidate["progress"])
            progress["validated_rows"] = "huit"
            candidate["progress"] = progress
            args["execution_values"] = candidate

        for mutation in (progress_list, progress_field):
            self._refused_before_late(mutation)

    def test_bad_schedule_refused_before_late(self):
        """Un horaire mal typé est refusé avant tout contrôle tardif."""

        def without_job(args):
            schedule = dict(args["schedule_values"])
            schedule.pop("job_id")
            args["schedule_values"] = schedule

        def unknown_key(args):
            schedule = dict(args["schedule_values"])
            schedule["CLE_INCONNUE"] = 1
            args["schedule_values"] = schedule

        def bad_deadline(args):
            schedule = dict(args["schedule_values"])
            schedule["next_run_at"] = "demain"
            args["schedule_values"] = schedule

        for mutation in (without_job, unknown_key, bad_deadline):
            self._refused_before_late(mutation)

    def test_foreign_failure_catalog_refused(self):
        """Un catalogue de codes étranger est refusé avant tout tardif."""
        for value in (["ECHEC_TEST"], ("ECHEC_TEST",), "ECHEC_TEST", _ForeignTuple(("ECHEC_TEST",))):
            with self.subTest(kind=type(value).__name__):
                self._refused_before_late(lambda args, item=value: args.update({"failure_codes": item}))

    def test_bad_instants_refused_before_late(self):
        """Des instants mal typés sont refusés avant tout contrôle tardif."""

        def bad_now(args):
            args["now_utc"] = "2026-06-01"

        def naive_expiry(args):
            args["identity_expires_at"] = datetime(2027, 1, 1)

        for mutation in (bad_now, naive_expiry):
            self._refused_before_late(mutation)


class StaticRefusalTests(unittest.TestCase):
    """Refus d autorité et de gouvernance sans import ORM."""

    def test_denied_authority_without_orm(self):
        """Une autorité refusée ne touche jamais l ORM."""
        for decision in ("DENY", "UNAVAILABLE"):
            with self.subTest(decision=decision):
                authority = _Authority({"decision": decision, "resolved_context": None})
                resolver = _Resolver()
                bundle = ports.compose_bulk_trusted_ports(
                    authority_adapter=authority,
                    mapping_resolver=resolver,
                    mapping_descriptors=(_mapping(),),
                    owner_declarations=(("owner-test", "1.0.0", _CODES, _FIELDS),),
                    governance_adapter=_GovernanceResolve3(response=_resolved_response()),
                    owner_command_adapter=None,
                    owner_projection_adapter=None,
                    audit_adapter=None,
                )
                arguments, _, _, _ = _valid_arguments()
                arguments["trusted_ports"] = bundle
                with _InertGuards() as guards:
                    with self.assertRaises(BulkAdmissionRefused) as captured:
                        admission.admit_bulk_operation(**arguments)
                _assert_closed_refusal(self, captured.exception)
                self.assertEqual(guards.orm_attempts, 0)
                self.assertTrue(resolver.calls)
                self.assertTrue(authority.calls)

    def test_missing_governance_without_orm(self):
        """Une gouvernance absente est refusée sans import ORM."""
        bundle = ports.compose_bulk_trusted_ports(
            authority_adapter=_Authority(response=_authority()),
            mapping_resolver=_Resolver(),
            mapping_descriptors=(_mapping(),),
            owner_declarations=(("owner-test", "1.0.0", _CODES, _FIELDS),),
            governance_adapter=None,
            owner_command_adapter=None,
            owner_projection_adapter=None,
            audit_adapter=None,
        )
        arguments, _, _, _ = _valid_arguments()
        arguments["trusted_ports"] = bundle
        with _InertGuards() as guards:
            with self.assertRaises(BulkAdmissionRefused) as captured:
                admission.admit_bulk_operation(**arguments)
        _assert_closed_refusal(self, captured.exception)
        self.assertEqual(guards.orm_attempts, 0)

    def test_denied_or_failed_governance_without_orm(self):
        """DENY, UNAVAILABLE ou exception de gouvernance refusés sans ORM."""
        for decision in ("DENY", "UNAVAILABLE"):
            with self.subTest(decision=decision):
                response = {
                    "resolution_version": "1.0.0",
                    "decision": decision,
                    "resolved_context": None,
                    "policy": None,
                    "profile": None,
                    "obligations": None,
                }
                arguments, _, _, governance = _arguments_with_governance(response=response)
                with _InertGuards() as guards:
                    with self.assertRaises(BulkAdmissionRefused) as captured:
                        admission.admit_bulk_operation(**arguments)
                _assert_closed_refusal(self, captured.exception)
                self.assertEqual(guards.orm_attempts, 0)
                self.assertTrue(governance.calls)
        arguments, _, _, _ = _arguments_with_governance(failed=True)
        with _InertGuards() as guards:
            with self.assertRaises(BulkAdmissionRefused) as captured:
                admission.admit_bulk_operation(**arguments)
        _assert_closed_refusal(self, captured.exception)
        self.assertEqual(guards.orm_attempts, 0)

    def test_divergent_context_without_orm(self):
        """Un contexte divergent est refusé sans import ORM."""
        response = _resolved_response()
        divergent = dict(response["resolved_context"])
        divergent["subject_id"] = "autre-sujet"
        response["resolved_context"] = divergent
        arguments, _, _, governance = _arguments_with_governance(response=response)
        with _InertGuards() as guards:
            with self.assertRaises(BulkAdmissionRefused) as captured:
                admission.admit_bulk_operation(**arguments)
        _assert_closed_refusal(self, captured.exception)
        self.assertEqual(guards.orm_attempts, 0)
        self.assertTrue(governance.calls)

    def test_divergent_policy_without_orm(self):
        """Une politique explicite différente de la résolution est refusée."""
        arguments, _, _, _ = _valid_arguments()
        policy = dict(arguments["policy"])
        policy["max_rows"] = policy["max_rows"] + 1
        arguments["policy"] = policy
        with _InertGuards() as guards:
            with self.assertRaises(BulkAdmissionRefused) as captured:
                admission.admit_bulk_operation(**arguments)
        _assert_closed_refusal(self, captured.exception)
        self.assertEqual(guards.orm_attempts, 0)


class OrmBoundaryTests(unittest.TestCase):
    """Frontière ORM atteinte une fois dans l ordre attendu."""

    def test_orm_reached_once_in_order_without_marker(self):
        """La frontière ORM est atteinte après mapping, autorité et gouvernance."""
        trace = []
        authority = _OrderAuthority(trace)
        resolver = _OrderResolver(trace)
        governance = _OrderGovernance(trace)
        bundle = ports.compose_bulk_trusted_ports(
            authority_adapter=authority,
            mapping_resolver=resolver,
            mapping_descriptors=(_mapping(),),
            owner_declarations=(("owner-test", "1.0.0", _CODES, _FIELDS),),
            governance_adapter=governance,
            owner_command_adapter=None,
            owner_projection_adapter=None,
            audit_adapter=None,
        )
        arguments, _, _, _ = _valid_arguments()
        arguments["trusted_ports"] = bundle
        marker = "MARQUEUR_FUITE_ORM_B01"
        with _InertGuards(orm_marker=marker) as guards:
            with self.assertRaises(BulkAdmissionRefused) as captured:
                admission.admit_bulk_operation(**arguments)
        _assert_closed_refusal(self, captured.exception)
        self.assertNotIn(marker, str(captured.exception))
        self.assertEqual(trace, ["mapping", "authority", "governance"])
        self.assertEqual(len(resolver.calls), 1)
        self.assertEqual(len(authority.calls), 1)
        self.assertEqual(len(governance.calls), 1)
        self.assertTrue(guards.orm_attempts >= 1)


class NoMutationTests(unittest.TestCase):
    """Aucune mutation des structures du caller sur refus."""

    def test_caller_structures_unchanged_on_refusal(self):
        """Les dicts et listes du caller restent intacts après refus."""
        arguments, _, _, _ = _valid_arguments()
        before_execution = copy.deepcopy(arguments["execution_values"])
        before_policy = copy.deepcopy(arguments["policy"])
        before_schedule = copy.deepcopy(arguments["schedule_values"])
        arguments["job_id"] = arguments["execution_values"]["operation_id"]
        with _InertGuards():
            with self.assertRaises(BulkAdmissionRefused):
                admission.admit_bulk_operation(**arguments)
        self.assertEqual(arguments["execution_values"], before_execution)
        self.assertEqual(arguments["policy"], before_policy)
        self.assertEqual(arguments["schedule_values"], before_schedule)


class PureTemporalTests(unittest.TestCase):
    """Contrôles temporels purs sans base."""

    def test_initial_bounds_without_database(self):
        """Les bornes exactes du chemin neuf sont vérifiées sans base."""
        policy = _valid_policy()
        _, operation_expiry, _ = _base_time(policy)
        execution = _new_execution(policy, operation_expiry)
        schedule = _new_schedule()
        _check_new_path_initial(execution=execution, schedule_owned=dict(schedule))
        bad_execution = dict(execution)
        bad_execution["status"] = "STAGED"
        with self.assertRaises(Exception):
            _check_new_path_initial(execution=bad_execution, schedule_owned=dict(schedule))

    def test_temporal_bounds_and_overflow_without_database(self):
        """Les bornes temporelles exactes et l overflow sont refusés proprement."""
        policy = _valid_policy()
        start, operation_expiry, identity_expiry = _base_time(policy)
        execution = _new_execution(policy, operation_expiry)
        schedule = _new_schedule()
        _check_new_path_temporal(
            execution=execution,
            policy_owned=dict(policy),
            schedule_owned=dict(schedule),
            identity_expires_at=identity_expiry,
            now_utc=start,
        )
        with self.assertRaises(Exception):
            _check_new_path_temporal(
                execution=dict(execution, expires_at=start),
                policy_owned=dict(policy),
                schedule_owned=dict(schedule),
                identity_expires_at=identity_expiry,
                now_utc=start,
            )
        huge = dict(policy)
        huge["max_runtime_seconds"] = 10**18
        huge["replay_window_seconds"] = 10**18
        with self.assertRaises(Exception):
            _check_new_path_temporal(
                execution=dict(execution),
                policy_owned=huge,
                schedule_owned=dict(schedule),
                identity_expires_at=identity_expiry,
                now_utc=start,
            )


class InvalidResolvedProfileTests(unittest.TestCase):
    """Profils résolus invalides refusés sans ORM."""

    def _profile_with_field(self, field, value):
        template = _valid_profile()
        options = {
            "profile_version": template.profile_version,
            "data_asset_id": template.data_asset_id,
            "owner_component": template.owner_component,
            "source_of_truth": template.source_of_truth,
            "data_classes": template.data_classes,
            "confidentiality": template.confidentiality,
            "personal_data": template.personal_data,
            "purpose_refs": template.purpose_refs,
            "retention_policy": template.retention_policy,
            "deletion_policy": template.deletion_policy,
            "residency_constraints": template.residency_constraints,
            "authorized_consumers": template.authorized_consumers,
            "processor_refs": template.processor_refs,
            "export_policy": template.export_policy,
            "lineage": template.lineage,
        }
        options[field] = value
        candidate = ports.DataGovernanceProfile(**options)
        return template, candidate

    def _public_refusal_without_orm(self, profile):
        response = _resolved_response()
        response["profile"] = profile
        governance = _GovernanceResolve3(response=response)
        bundle = ports.compose_bulk_trusted_ports(
            authority_adapter=_Authority(response=_authority()),
            mapping_resolver=_Resolver(),
            mapping_descriptors=(_mapping(),),
            owner_declarations=(("owner-test", "1.0.0", _CODES, _FIELDS),),
            governance_adapter=governance,
            owner_command_adapter=None,
            owner_projection_adapter=None,
            audit_adapter=None,
        )
        arguments, _, _, _ = _valid_arguments()
        arguments["trusted_ports"] = bundle
        with _InertGuards() as guards:
            with self.assertRaises(BulkAdmissionRefused) as captured:
                admission.admit_bulk_operation(**arguments)
        _assert_closed_refusal(self, captured.exception)
        self.assertEqual(guards.orm_attempts, 0)
        self.assertTrue(governance.calls)

    def test_nul_simple_and_collection_refused(self):
        """Une référence simple ou une collection avec NUL est refusée."""
        _, nul_simple = self._profile_with_field("data_asset_id", "actif\x00test")
        self._public_refusal_without_orm(nul_simple)
        template = _valid_profile()
        nul_collection = ports.DataGovernanceProfile(
            profile_version=template.profile_version,
            data_asset_id=template.data_asset_id,
            owner_component=template.owner_component,
            source_of_truth=template.source_of_truth,
            data_classes=frozenset({"classe\x00test"}),
            confidentiality=template.confidentiality,
            personal_data=template.personal_data,
            purpose_refs=template.purpose_refs,
            retention_policy=template.retention_policy,
            deletion_policy=template.deletion_policy,
            residency_constraints=template.residency_constraints,
            authorized_consumers=template.authorized_consumers,
            processor_refs=template.processor_refs,
            export_policy=template.export_policy,
            lineage=template.lineage,
        )
        self._public_refusal_without_orm(nul_collection)
        self.assertEqual(template.data_classes, frozenset({"classe-test"}))

    def test_invalid_surrogate_simple_and_collection_refused(self):
        """Un substitut invalide est refusé en simple et en collection."""
        high = chr(0xD800)
        low = chr(0xDFFF)
        _, surrogate_simple = self._profile_with_field("data_asset_id", "actif" + high + "test")
        self._public_refusal_without_orm(surrogate_simple)
        template = _valid_profile()
        surrogate_collection = ports.DataGovernanceProfile(
            profile_version=template.profile_version,
            data_asset_id=template.data_asset_id,
            owner_component=template.owner_component,
            source_of_truth=template.source_of_truth,
            data_classes=frozenset({"classe" + low + "test"}),
            confidentiality=template.confidentiality,
            personal_data=template.personal_data,
            purpose_refs=template.purpose_refs,
            retention_policy=template.retention_policy,
            deletion_policy=template.deletion_policy,
            residency_constraints=template.residency_constraints,
            authorized_consumers=template.authorized_consumers,
            processor_refs=template.processor_refs,
            export_policy=template.export_policy,
            lineage=template.lineage,
        )
        self._public_refusal_without_orm(surrogate_collection)

    def test_valid_replacement_character_accepted_by_opaque_check(self):
        """Le caractère de remplacement valide n est pas rejeté comme substitut."""
        _, replacement = self._profile_with_field("data_asset_id", "actif�test")
        response = _resolved_response()
        response["profile"] = replacement
        bundle, _ = _compose_gov(_GovernanceResolve3(response=response))
        from pixs.backend.bulk_runtime_contracts import _build_authority_assessment_snapshot

        snapshot = _build_authority_assessment_snapshot(_authority())
        with _InertGuards() as guards:
            result, diagnostics = bundle.resolve_governance(
                server_context=object(),
                authority_snapshot=snapshot,
                governance_contract=_mapping(),
                governance_references=("policy-test", "1.0.0"),
            )
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(result)
        self.assertEqual(guards.orm_attempts, 0)


if __name__ == "__main__":
    unittest.main()
