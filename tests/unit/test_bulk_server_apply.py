"""Tests ordinaires du module Bulk APPLY corrigé, sans base réelle."""

from __future__ import annotations

import asyncio
import hashlib
import json
import pathlib
import subprocess
import sys
import threading
import unittest
from datetime import datetime, timedelta, timezone
from dataclasses import FrozenInstanceError, replace
from unittest import mock

import pixs.backend.bulk_server_apply as apply
import pixs.backend.bulk_streaming_import as flux
from pixs.backend.bulk_object_staging import _capture_metadata_snapshot
from pixs.backend.bulk_streaming_import import _CsvImportUnit, _NdjsonImportUnit
from pixs.backend.bulk_trusted_ports import compose_bulk_trusted_ports
from pixs.kernel.diagnostics import VALIDATE
from unit.test_bulk_execution_values import _valid_policy
from unit.test_bulk_runtime_contracts import _CODES, _FIELDS, _Hostile, _mapping
from unit.test_bulk_trusted_ports import (
    _Authority,
    _GovernanceResolve3,
    _Resolver,
    _resolved_response,
)

_CODES_ETENDUS = tuple(sorted(set(_CODES) | set(flux._CONTENT_CODES)))
_CHAMPS = tuple(sorted(_FIELDS))
_PUR = (
    "import sys; "
    "import pixs.backend.bulk_server_apply as module; "
    "assert 'django' not in sys.modules, 'orm importé'; "
    "assert callable(module.declare_server_apply_participation); "
    "assert callable(module.prepare_import_apply_readiness); "
    "assert callable(module.apply_import_chunks_atomic_per_chunk); "
    "print('PUR')"
)


class _CommandeServeur:
    """Propriétaire réel, méthodes liées au même adaptateur."""

    async def validate(self, contexte, entree, references):
        """Validation coopérative sans effet."""
        return {"accepted": True, "diagnostics": ()}

    def execute(self, contexte, entree, references):
        """Exécution synchrone sans effet."""
        return {"outcome": "APPLIED", "result_reference": None,
                "diagnostics": (), "event_references": ()}

    def canonical_bytes(self, valeurs):
        """Sérialisation déterministe."""
        return json.dumps(valeurs, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _mapping_100():
    """Mapping déclaré exact en version complète."""
    base = _mapping()
    return {**base, "mapping_reference": "mapping-test", "mapping_version": "1.0.0",
            "owner_reference": "owner-test", "variant": "IMPORT", "format": "CSV"}


def _composer_reel_applique(commande=None, obligations=()):
    """Compose les vrais ports avec propriétaire serveur réel."""
    commande = _CommandeServeur() if commande is None else commande
    mapping = _mapping_100()
    declaration = ("owner-test", "1.0.0", _CODES_ETENDUS, _CHAMPS)
    gov = _GovernanceResolve3(response=_resolved_response(obligations=obligations))
    bundle = compose_bulk_trusted_ports(
        authority_adapter=_Authority(),
        mapping_resolver=_Resolver(),
        mapping_descriptors=(mapping,),
        owner_declarations=(declaration,),
        governance_adapter=gov,
        owner_command_adapter=commande,
        owner_projection_adapter=None,
        audit_adapter=None,
    )
    return bundle, commande, mapping, gov


def _args_declare(bundle, commande, **surcharge):
    """Arguments exacts de la déclaration propriétaire."""
    args = {"trusted_ports": bundle, "owner_command_adapter": commande,
            "owner_reference": "owner-test", "mapping_reference": "mapping-test",
            "mapping_version": "1.0.0", "contract_version": "1.0.0",
            "command_type": "commande-test", "serializer_version": "1.0.0",
            "order_scope_reference": "scope-test", "outbox_failure_catalogue": (),
            "policy_reference": "policy-test", "policy_version": "1.0.0",
            "runtime_alias": "default"}
    args.update(surcharge)
    return args


def _metadonnees():
    """Onze clés exactes valides et privées."""
    donnees = b"lignes de test bulk apply"
    debut = datetime.now(timezone.utc)
    return {"object_reference": "object-test", "version_reference": "version-test",
            "tenant_reference": "tenant-test", "scope_reference": None,
            "classification_reference": "classification-test", "size_bytes": len(donnees),
            "sha256": hashlib.sha256(donnees).hexdigest(), "media_type": "text/csv",
            "is_private": True, "expires_at": debut + timedelta(hours=1),
            "retention_policy_reference": "retention-test"}


def _certificat_interne(participation):
    metadata = _metadonnees()
    snapshot, refus = _capture_metadata_snapshot(metadata)
    assert refus == []
    politique = _valid_policy()
    return apply._issue_qualified_input(
        participation_identity=participation, metadata_snapshot=snapshot,
        operation_id="operation-test", sha256=metadata["sha256"], units=(),
        parser_summary=flux._ImportSummary(True, None, ("name",), 0, 0, 0, 0, ()),
        mapping_version="1.0.0", input_reference="object-test", chunk_rows=500,
        idempotency_key_base="base-test", policy_frozen=tuple((k,tuple(v) if type(v)is list else v) for k,v in politique.items()),
        source_version="version-test", owner_reference="owner-test", mapping_reference="mapping-test",
        contract_version="1.0.0", policy_reference="policy-test", policy_version="1.0.0")


class _Bail(Exception):
    """Bail synthétique pour garde mappée."""


class _Cas(Exception):
    """Conflit synthétique."""


class _Contrainte(Exception):
    """Contrainte synthétique."""


class _Transition(Exception):
    """Transition synthétique."""


class _Magasin(Exception):
    """Persistance synthétique."""


class _Conflit(Exception):
    """Conflit idempotence synthétique."""


class _Obsolet(Exception):
    """État obsolète synthétique."""


class _Refuse(Exception):
    """Refus synthétique."""


def _gardes_synthetiques():
    """Gardes sans Django ni ORM."""
    return apply._GuardedTypes(lease=_Bail, cas=_Cas, constraint=_Contrainte,
                               transition=_Transition, store=_Magasin, conflict=_Conflit,
                               stale=_Obsolet, refused=_Refuse, invalid=(ValueError,),
                               integrity=OSError)


class ImportPurIsoleTests(unittest.TestCase):
    """Pureté d'import prouvée en sous-processus isolé."""

    def test_import_pur_sans_django(self):
        """Seul le sous-processus est inspecté, jamais la suite."""
        racine = pathlib.Path(__file__).resolve().parents[2]
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
               "PYTHONDONTWRITEBYTECODE": "1",
               "PYTHONPATH": ":".join((str(racine / "src"), str(racine / "tests")))}
        termine = subprocess.run([sys.executable, "-c", _PUR], cwd=str(racine),
                                 env=env, capture_output=True, text=True, timeout=120)
        self.assertEqual(termine.returncode, 0, msg=termine.stderr[-2000:])
        self.assertIn("PUR", termine.stdout)


class ParticipationReelleTests(unittest.TestCase):
    """Déclaration positive et négative sur ports composés réels."""

    def test_positive_declare_et_controle(self):
        """Déclaration valide acceptée puis contrôlée."""
        bundle, commande, mapping, _ = _composer_reel_applique()
        participation = apply.declare_server_apply_participation(
            **_args_declare(bundle, commande))
        self.assertIs(participation.owner_adapter, commande)
        self.assertIs(participation.trusted_ports, bundle)
        self.assertEqual(participation.mapping_reference, "mapping-test")
        self.assertEqual(participation.mapping_version, "1.0.0")
        self.assertIs(apply._check_participation(participation), participation)

    def test_negatifs_references_versions_adapter(self):
        """Références, versions et adaptateur distinct refusés."""
        bundle, commande, _, _ = _composer_reel_applique()
        base = _args_declare(bundle, commande)
        with self.assertRaises(ValueError):
            apply.declare_server_apply_participation(
                **dict(base, owner_command_adapter=_CommandeServeur()))
        for champ, valeur in (("owner_reference", ""), ("mapping_reference", _Hostile()),
                              ("mapping_version", "pas-semver"), ("contract_version", "1.0"),
                              ("policy_version", _Hostile())):
            with self.subTest(champ=champ):
                with self.assertRaises(ValueError):
                    apply.declare_server_apply_participation(**dict(base, **{champ: valeur}))
        with self.assertRaises(ValueError):
            apply.declare_server_apply_participation(
                **dict(base, outbox_failure_catalogue=["pas-tuple"]))
        with self.assertRaises(ValueError):
            apply.declare_server_apply_participation(**dict(base, trusted_ports=None))

    def test_controle_rejette_sceau_et_methodes(self):
        """Sceau et méthodes non liées refusés en refus serveur."""
        bundle, commande, _, _ = _composer_reel_applique()
        participation = apply.declare_server_apply_participation(
            **_args_declare(bundle, commande))
        with self.assertRaises(apply._ApplyRefused):
            apply._check_participation(object())
        with mock.patch.object(apply, "_load_repository_classes",
                               side_effect=AssertionError("SQL interdit")):
            with self.assertRaises(apply._ApplyRefused):
                apply._check_participation("participation-test")


class GardesPubliquesTests(unittest.IsolatedAsyncioTestCase):
    """Gardes primitives des deux fonctions publiques avant chargeur."""

    def _base_prepare(self, participation, **surcharge):
        debut = datetime.now(timezone.utc)
        args = {"participation": participation, "runtime_repository": object(),
                "report_repository": object(), "server_context": object(),
                "operation_id": "operation-test", "validate_job_id": "job-test",
                "lease_owner": "worker-test", "expected_metadata": _metadonnees(),
                "storage_resolver": object(), "deadline": debut + timedelta(seconds=60),
                "now": debut, "cancel_event": asyncio.Event(),
                "expected_schedule_revision": 1}
        args.update(surcharge)
        return args

    def _base_apply(self, participation, **surcharge):
        debut = datetime.now(timezone.utc)
        args = {"participation": participation, "runtime_repository": object(),
                "idempotency_repository": object(), "envelope_repository": object(),
                "outbox_repository": object(), "server_context": object(),
                "operation_id": "operation-test", "apply_job_id": "job-test",
                "lease_owner": "worker-test", "qualified_input": None,
                "expected_metadata": _metadonnees(), "storage_resolver": object(),
                "deadline": debut + timedelta(seconds=60), "cancel_event": asyncio.Event(),
                "expected_schedule_revision": 1}
        args.update(surcharge)
        return args

    async def _refus_avant_chargeur(self, fonction, args, element):
        with mock.patch.object(apply, "_load_repository_classes") as chargeur:
            resultat, diagnostics = await fonction(**args)
        self.assertIsNone(resultat)
        self.assertTrue(diagnostics)
        for item in diagnostics:
            self.assertEqual(item.step, VALIDATE)
            self.assertNotIn("LEAK-MARKER", str(item))
        self.assertIn(element, [item.element for item in diagnostics])
        chargeur.assert_not_called()

    async def test_prepare_gardes_froides(self):
        """Métadonnées, resolver et primitives refusés avant dépôts."""
        bundle, commande, _, _ = _composer_reel_applique()
        participation = apply.declare_server_apply_participation(
            **_args_declare(bundle, commande))
        naive = datetime.now(timezone.utc).replace(tzinfo=None)
        cas = [({"expected_metadata": {"inconnu": True}}, "bulk_object_metadata."),
               ({"storage_resolver": None}, "bulk_server_apply.storage_resolver"),
               ({"operation_id": ""}, "bulk_server_apply.references"),
               ({"cancel_event": True}, "bulk_server_apply.cancel_event"),
               ({"deadline": naive}, "bulk_server_apply.deadline"),
               ({"expected_schedule_revision": False}, "bulk_server_apply.expected_schedule_revision")]
        for index, (surcharge, _attendu) in enumerate(cas):
            with self.subTest(cas=index):
                args = self._base_prepare(participation, **surcharge)
                with mock.patch.object(apply, "_load_repository_classes") as chargeur:
                    resultat, diagnostics = await apply.prepare_import_apply_readiness(**args)
                self.assertIsNone(resultat)
                self.assertTrue(diagnostics)
                chargeur.assert_not_called()

    async def test_prepare_cache_valide_atteint_chargeur(self):
        """Cache valide avec resolver atteint le chargeur sentinelle."""
        bundle, commande, _, _ = _composer_reel_applique()
        participation = apply.declare_server_apply_participation(
            **_args_declare(bundle, commande))
        args = self._base_prepare(participation)
        with mock.patch.object(apply, "_load_repository_classes",
                               side_effect=RuntimeError("chargeur atteint")):
            with self.assertRaises(RuntimeError):
                await apply.prepare_import_apply_readiness(**args)

    async def test_apply_gardes_froides(self):
        """Seconde fonction publique gardée avant dépôts."""
        bundle, commande, _, _ = _composer_reel_applique()
        participation = apply.declare_server_apply_participation(
            **_args_declare(bundle, commande))
        naive = datetime.now(timezone.utc).replace(tzinfo=None)
        for index, surcharge in enumerate(({"operation_id": _Hostile()},
                                           {"cancel_event": object()},
                                           {"deadline": naive},
                                           {"expected_schedule_revision": 0},
                                           {"expected_metadata": {"inconnu": True}},
                                           {"storage_resolver": None})):
            with self.subTest(cas=index):
                args = self._base_apply(participation, **surcharge)
                with mock.patch.object(apply, "_load_repository_classes") as chargeur:
                    resultat, diagnostics = await apply.apply_import_chunks_atomic_per_chunk(**args)
                self.assertIsNone(resultat)
                self.assertTrue(diagnostics)
                chargeur.assert_not_called()

    async def test_apply_cache_valide_atteint_chargeur(self):
        """Cache correct avec resolver atteint le chargeur."""
        bundle, commande, _, _ = _composer_reel_applique()
        participation = apply.declare_server_apply_participation(
            **_args_declare(bundle, commande))
        args = self._base_apply(participation)
        with mock.patch.object(apply, "_load_repository_classes",
                               side_effect=RuntimeError("chargeur atteint")):
            with self.assertRaises(RuntimeError):
                await apply.apply_import_chunks_atomic_per_chunk(**args)


    async def test_cache_sans_resolver_et_certificat_etranger_avant_sql(self):
        bundle, commande, _, _ = _composer_reel_applique()
        participation = apply.declare_server_apply_participation(**_args_declare(bundle, commande))
        certificat = _certificat_interne(participation)
        args = self._base_apply(participation, qualified_input=certificat,
                                expected_metadata=None, storage_resolver=None)
        with mock.patch.object(apply, "_load_repository_classes", side_effect=RuntimeError("chargeur atteint")) as chargeur:
            with self.assertRaisesRegex(RuntimeError, "chargeur atteint"):
                await apply.apply_import_chunks_atomic_per_chunk(**args)
            chargeur.assert_called_once()
        for intrus in (_Hostile(), replace(certificat, _seal=object()),
                       replace(certificat, participation_identity=object()),
                       replace(certificat, mapping_version="9.0.0")):
            with mock.patch.object(apply, "_load_repository_classes") as chargeur:
                resultat, diagnostics = await apply.apply_import_chunks_atomic_per_chunk(**dict(args, qualified_input=intrus))
                self.assertIsNone(resultat)
                self.assertTrue(diagnostics)
                chargeur.assert_not_called()


class CacheNdjsonReelTests(unittest.TestCase):
    """Gel réel NDJSON profondément immuable."""

    def test_gel_ndjson_conserve_et_isole(self):
        """Le gel conserve l'ordre et isole le cache original."""
        valeurs = {"name": "valeur", "compte": 3, "imbrique": {"liste": [1, 2]}}
        unite = _NdjsonImportUnit(4, tuple(valeurs.items()))
        gelees = apply._freeze_qualified_units((unite,))
        self.assertEqual(len(gelees), 1)
        gelee = gelees[0]
        self.assertIs(type(gelee), apply._OwnedApplyUnit)
        self.assertEqual(gelee.line_index, 4)
        self.assertEqual(list(gelee.as_values().keys()), list(valeurs.keys()))
        valeurs["imbrique"]["liste"].append(99)
        self.assertEqual(gelee.as_values()["imbrique"]["liste"], [1, 2])
        premiere = gelee.as_values()
        premiere["imbrique"]["liste"].append(100)
        self.assertEqual(gelee.as_values()["imbrique"]["liste"], [1, 2])
        with self.assertRaises(FrozenInstanceError):
            gelee.line_index = 9

    def test_zero_unite_et_hostile(self):
        """Zéro unité vide, intrus refusé."""
        self.assertEqual(apply._freeze_qualified_units(()), ())
        with self.assertRaises(apply._ApplyRefused):
            apply._freeze_qualified_units((_Hostile(),))


class ClesRetentionTests(unittest.TestCase):
    """Clés dérivées et rétention UTC exactes."""

    def test_cle_deterministe(self):
        """Même entrée donne même clé de 64 hex."""
        args = {"tenant_id": "tenant-test", "subject_id": "sujet-test",
                "command_type": "commande-test", "base_key": "base-test", "ordinal": 1}
        self.assertEqual(apply._derive_command_key(**args),
                         apply._derive_command_key(**args))
        self.assertNotEqual(apply._derive_command_key(**args),
                            apply._derive_command_key(**dict(args, ordinal=2)))
        with self.assertRaises(apply._ApplyRefused):
            apply._derive_command_key(**dict(args, ordinal=0))

    def test_retention_bornee(self):
        """Rétention UTC bornée avec refus de débordement."""
        depart = datetime.now(timezone.utc)
        fin = apply._idempotence_expiry(expires_op=depart, retention_seconds=60)
        self.assertGreater(fin, depart)
        self.assertIs(fin.tzinfo, timezone.utc)
        with self.assertRaises(apply._ApplyRefused):
            apply._idempotence_expiry(expires_op=depart, retention_seconds=2 ** 63)


class ValidationReelleTests(unittest.IsolatedAsyncioTestCase):
    """Appels réels au validateur et au constructeur de rapport existant."""

    async def test_dedup_et_borne_reelles(self):
        from pixs.backend.bulk_import_validate import _build_report_values, _OrchestrationRefused
        appels = []
        class CommandeDiagnostics(_CommandeServeur):
            async def validate(self, contexte, entree, references):
                appels.append(entree["line_index"])
                diagnostic = {"code": "REJECTED", "field_reference": "name", "line_index": entree["line_index"]}
                return {"accepted": False, "diagnostics": (dict(diagnostic), dict(diagnostic))}
        bundle, commande, _, _ = _composer_reel_applique(CommandeDiagnostics())
        participation = apply.declare_server_apply_participation(**_args_declare(bundle, commande))
        politique = _valid_policy()
        args = dict(participation=participation, trusted_ports=bundle, server_context=object(),
                    references=("operation-test", "owner-test", "mapping-test", "1.0.0"),
                    policy_owned=politique, owner_codes=frozenset(_CODES_ETENDUS),
                    owner_fields=frozenset(_CHAMPS), max_diagnostics=1,
                    effective=datetime.now(timezone.utc)+timedelta(seconds=60),
                    cancel_event=asyncio.Event(), input_reference="object-test")
        unite = _CsvImportUnit(1, (("name", "première"),))
        valides, invalides, diagnostics = await apply._validate_all_units_bounded(units=(unite,), **args)
        self.assertEqual((valides, invalides), (1, 1))
        self.assertEqual(appels, [1])
        self.assertEqual(len(diagnostics), 1)
        rapport = _build_report_values(operation_id="operation-test", mapping_version="1.0.0",
                    source_version="version-test", total_rows=1, validated_rows=1, invalid_rows=1,
                    complete=True, parser_warnings=diagnostics, owner_diagnostics=diagnostics,
                    max_diagnostics=1)
        self.assertEqual(len(rapport["diagnostics"]), 1)
        with self.assertRaises(apply._ApplyRefused):
            await apply._validate_all_units_bounded(
                units=(unite, _CsvImportUnit(2, (("name", "deuxième"),))), **args)
        self.assertEqual(appels, [1, 1, 2])
        with self.assertRaises(_OrchestrationRefused):
            _build_report_values(operation_id="operation-test", mapping_version="1.0.0",
                    source_version="version-test", total_rows=2, validated_rows=2, invalid_rows=2,
                    complete=True, parser_warnings=[], owner_diagnostics=[diagnostics[0],dict(diagnostics[0],line_index=2)],
                    max_diagnostics=1)


class PontsTests(unittest.IsolatedAsyncioTestCase):
    """Ponts sync réels, annulation synchronisée sans délais flous."""

    async def test_lecture_sync_resultat_et_refus(self):
        """Résultat préservé, inattendu propagé, bail mappé."""
        gardes = _gardes_synthetiques()

        attendu = {"revision": 3}
        def _lire(**kwargs):
            return attendu

        def _panne(**kwargs):
            raise RuntimeError("panne inattendue")

        def _bail(**kwargs):
            raise _Bail("bail simule")

        self.assertIs(await apply._bridge_read(_lire, "execution", gardes), attendu)
        with self.assertRaises(RuntimeError):
            await apply._bridge_read(_panne, "execution", gardes)
        with self.assertRaises(apply._ApplyRefused):
            await apply._bridge_read(_bail, "lease", gardes)

    async def test_annulation_repetee_draine_thread(self):
        """Entrée et sortie thread synchronisées, CancelledError après drain."""
        gardes = _gardes_synthetiques()
        entre, liberer, sorti = threading.Event(), threading.Event(), threading.Event()
        marqueur = {}

        def _lent(*args, **kwargs):
            entre.set()
            marqueur["engage"] = True
            liberer.wait(timeout=10)
            sorti.set()
            return "tardif"

        evenement = asyncio.Event()
        tache = asyncio.create_task(
            apply._bridge_mutation(_lent, "chunk", gardes, cancel_event=evenement))
        try:
            self.assertTrue(await asyncio.to_thread(entre.wait, timeout=5))
            tache.cancel()
            await asyncio.sleep(0)
            tache.cancel()
            liberer.set()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(tache, timeout=5)
        finally:
            liberer.set()
        self.assertTrue(sorti.is_set())
        self.assertTrue(evenement.is_set())
        self.assertTrue(marqueur["engage"])

    async def test_mutation_engagee_preservee_sans_pg(self):
        """Marqueur placé avant attente conservé après annulation tardive."""
        gardes = _gardes_synthetiques()
        marqueur = {}

        def _rapide(**kwargs):
            marqueur["engage"] = True
            return "valide"

        evenement = asyncio.Event()
        resultat = await apply._bridge_mutation(_rapide, "chunk", gardes, cancel_event=evenement)
        self.assertEqual(resultat, "valide")
        self.assertTrue(marqueur["engage"])


if __name__ == "__main__":
    unittest.main()
