"""Tests unitaires VALIDATE IMPORT VALIDATE_ONLY, sans base réelle.

Preuves du parcours qualifié réel, des verdicts par unité réelle et des
gardes primitives, avec ports composés réels et doubles B04 réutilisés.
Aucune preuve PostgreSQL simulée : le nominal complet reste réservé au
harnais d'intégration. La pureté d'import est prouvée en sous-processus
isolé à environnement minimal, sans aucun effet global sur la suite.
Les diagnostics attendus sont statiques, sans valeur fournie.
"""

import asyncio
import hashlib
import pathlib
import subprocess
import sys
import unittest
from datetime import datetime, timedelta, timezone
from unittest import mock

from pixs.backend import bulk_import_validate as orch
from pixs.backend import bulk_streaming_import as flux
from pixs.backend.bulk_trusted_ports import (
    _OwnerDeclarationSnapshot,
    declare_bulk_mapping_descriptor,
)
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from unit.test_bulk_execution_values import _valid_policy
from unit.test_bulk_private_object_reader import (
    _Fournisseur,
    _FournisseurChangeant,
    _Resolveur,
    _compose_reel,
    _metadonnees,
)
from unit.test_bulk_runtime_contracts import (
    _CODES,
    _FIELDS,
    _Hostile,
    _mapping,
)

_CSV = b"source_name,source_count\nalice,1\nbob,2\n"
_NDJSON = b'{"source_name":"alice","source_count":1}\n{"source_name":"bob","source_count":2}\n'
_CODES_ETENDUS = tuple(sorted(set(_CODES) | set(flux._CONTENT_CODES)))
_CHAMPS = tuple(sorted(_FIELDS))
_PUR = (
    "import sys; "
    "import pixs.backend.bulk_import_validate as module; "
    "assert 'django' not in sys.modules, 'orm importé'; "
    "assert callable(module.validate_import_only); "
    "print('PUR')"
)


def _declaration():
    return _OwnerDeclarationSnapshot(
        owner_reference="owner-test",
        contract_version="1.0.0",
        declared_codes=_CODES_ETENDUS,
        declared_fields=_CHAMPS,
    )


def _mappage_ndjson():
    return dict(_mapping(), format="NDJSON")


def _fabrique_parseur(mapping=None, politique=None):
    mapping = _mapping() if mapping is None else mapping
    politique = _valid_policy() if politique is None else dict(politique)
    parseur, refus = flux.new_bulk_import_parser(
        mapping=dict(mapping),
        policy=dict(politique),
        declared_owner_fields=tuple(_CHAMPS),
        declared_codes=tuple(_CODES_ETENDUS),
    )
    assert refus == []
    assert parseur is not None
    return parseur, politique


def _composer_limites(limites):
    from unit.test_bulk_trusted_ports import _resolved_response

    reponse = _resolved_response()
    reponse["policy"]["limits"] = dict(limites)
    return _compose_reel(reponse=reponse)


def _args_prepare(metadata, politique, parseur, bundle, **surcharge):
    debut = datetime.now(timezone.utc)
    args = {
        "trusted_ports": bundle,
        "server_context": object(),
        "operation_reference": "operation-test",
        "expected_metadata": dict(metadata),
        "policy_reference": "policy-test",
        "policy_version": "1.0.0",
        "storage_resolver": None,
        "expected_policy": dict(politique),
        "parser": parseur,
        "deadline": debut + timedelta(seconds=60),
        "now": debut,
        "cancel_event": asyncio.Event(),
    }
    args.update(surcharge)
    return args


async def lecteur_prepare(**args):
    from pixs.backend.bulk_private_object_reader import _prepare_qualified_import_units

    return await _prepare_qualified_import_units(**args)


def _prepare_csv(donnees=_CSV, politique=None, metadata=None, **surcharge):
    politique = _valid_policy() if politique is None else dict(politique)
    metadata, _ = _metadonnees(donnees) if metadata is None else (metadata, None)
    fournisseur = _Fournisseur(dict(metadata), [donnees] if donnees else [])
    resolveur = _Resolveur(fournisseur)
    if politique == _valid_policy():
        bundle, _, _ = _compose_reel()
    else:
        bundle, _, _ = _composer_limites(politique)
    parseur, _ = _fabrique_parseur(politique=politique)
    args = _args_prepare(metadata, politique, parseur, bundle, storage_resolver=resolveur, **surcharge)
    return args, fournisseur, resolveur


class ParcoursQualifiePrepareTests(unittest.IsolatedAsyncioTestCase):
    def assert_refus(self, resultat):
        bilan, diagnostics = resultat
        self.assertIsNone(bilan)
        self.assertIs(type(diagnostics), list)
        self.assertTrue(diagnostics)
        for item in diagnostics:
            self.assertIs(type(item), Diagnostic)
            self.assertEqual(item.step, VALIDATE)

    async def test_succes_csv_unites_exactes_fermeture(self):
        args, fournisseur, resolveur = _prepare_csv()
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assertEqual(diagnostics, [])
        self.assertTrue(bilan.complete)
        self.assertEqual(bilan.accepted_size, len(_CSV))
        self.assertEqual(bilan.sha256, hashlib.sha256(_CSV).hexdigest())
        self.assertEqual(len(bilan.units), 2)
        for unite in bilan.units:
            self.assertIs(type(unite), flux._CsvImportUnit)
        self.assertEqual(bilan.units[0].as_values(), {"name": "alice", "count": "1"})
        self.assertEqual(bilan.units[1].as_values(), {"name": "bob", "count": "2"})
        self.assertTrue(bilan.parser_summary.complete)
        self.assertEqual(fournisseur.stat_appels, 2)
        self.assertEqual(fournisseur.iter_appels, 1)
        self.assertTrue(fournisseur.dernier_iterateur.ferme)
        self.assertEqual(len(resolveur.appels), 1)

    async def test_succes_ndjson_unites_exactes(self):
        metadata, _ = _metadonnees(_NDJSON, media_type="application/x-ndjson")
        politique = _valid_policy()
        fournisseur = _Fournisseur(dict(metadata), [_NDJSON])
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _compose_reel()
        parseur, _ = _fabrique_parseur(mapping=_mappage_ndjson())
        args = _args_prepare(metadata, politique, parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assertEqual(diagnostics, [])
        self.assertTrue(bilan.complete)
        self.assertEqual(len(bilan.units), 2)
        for unite in bilan.units:
            self.assertIs(type(unite), flux._NdjsonImportUnit)
        self.assertEqual(bilan.units[0].as_values(), {"name": "alice", "count": 1})
        self.assertEqual(bilan.units[1].as_values(), {"name": "bob", "count": 2})

    async def test_succes_ndjson_vide_zero_unite(self):
        donnees = b""
        metadata, _ = _metadonnees(donnees, media_type="application/x-ndjson")
        politique = _valid_policy()
        fournisseur = _Fournisseur(dict(metadata), [])
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _compose_reel()
        parseur, _ = _fabrique_parseur(mapping=_mappage_ndjson())
        args = _args_prepare(metadata, politique, parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assertEqual(diagnostics, [])
        self.assertTrue(bilan.complete)
        self.assertEqual(bilan.units, ())

    async def test_sha_corrompu_aucun_bilan_fermeture(self):
        metadata, _ = _metadonnees(_CSV)
        corrompu = dict(metadata, sha256="a" * 64)
        fournisseur = _Fournisseur(dict(corrompu), [_CSV])
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _compose_reel()
        parseur, _ = _fabrique_parseur()
        args = _args_prepare(corrompu, _valid_policy(), parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assert_refus((bilan, diagnostics))
        self.assertEqual(fournisseur.stat_appels, 2)
        self.assertEqual(fournisseur.iter_appels, 1)
        self.assertTrue(fournisseur.dernier_iterateur.ferme)
        self.assertTrue(any("sha256" in item.element for item in diagnostics))

    async def test_metadonnees_finales_divergentes_aucun_bilan(self):
        metadata, _ = _metadonnees(_CSV)
        fournisseur = _FournisseurChangeant(dict(metadata), [_CSV])
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _compose_reel()
        parseur, _ = _fabrique_parseur()
        args = _args_prepare(metadata, _valid_policy(), parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assert_refus((bilan, diagnostics))
        self.assertEqual(fournisseur.stat_appels, 2)
        self.assertEqual(fournisseur.iter_appels, 1)
        self.assertTrue(fournisseur.dernier_iterateur.ferme)

    async def test_fermeture_echouee_aucun_bilan(self):
        metadata, _ = _metadonnees(_CSV)
        fournisseur = _Fournisseur(dict(metadata), [_CSV], fail_close=True)
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _compose_reel()
        parseur, _ = _fabrique_parseur()
        args = _args_prepare(metadata, _valid_policy(), parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assert_refus((bilan, diagnostics))
        self.assertTrue(fournisseur.dernier_iterateur.ferme)

    async def test_parseur_imposteur_refuse_avant_fournisseur(self):
        for imposteur in (object(), None):
            metadata, _ = _metadonnees(_CSV)
            fournisseur = _Fournisseur(dict(metadata), [_CSV])
            resolveur = _Resolveur(fournisseur)
            bundle, _, _ = _compose_reel()
            args = _args_prepare(metadata, _valid_policy(), imposteur, bundle, storage_resolver=resolveur)
            bilan, diagnostics = await lecteur_prepare(**args)
            with self.subTest(imposteur=type(imposteur).__name__):
                self.assert_refus((bilan, diagnostics))
                self.assertEqual(fournisseur.stat_appels, 0)
                self.assertEqual(fournisseur.iter_appels, 0)
                self.assertEqual(resolveur.appels, [])

    async def test_format_mapping_incoherent_refuse_avant_fournisseur(self):
        metadata, _ = _metadonnees(_CSV, media_type="application/x-ndjson")
        fournisseur = _Fournisseur(dict(metadata), [_CSV])
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _compose_reel()
        parseur, _ = _fabrique_parseur()
        args = _args_prepare(metadata, _valid_policy(), parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assert_refus((bilan, diagnostics))
        self.assertEqual(fournisseur.stat_appels, 0)
        self.assertEqual(fournisseur.iter_appels, 0)

        metadata_csv, _ = _metadonnees(_CSV)
        fournisseur2 = _Fournisseur(dict(metadata_csv), [_CSV])
        parseur2, _ = _fabrique_parseur()
        parseur2._mapping = declare_bulk_mapping_descriptor(_mappage_ndjson())
        args2 = _args_prepare(
            metadata_csv, _valid_policy(), parseur2, bundle, storage_resolver=_Resolveur(fournisseur2)
        )
        bilan2, diagnostics2 = await lecteur_prepare(**args2)
        self.assert_refus((bilan2, diagnostics2))
        self.assertEqual(fournisseur2.stat_appels, 0)
        self.assertEqual(fournisseur2.iter_appels, 0)

    async def test_policy_incoherente_refusee_avant_fournisseur(self):
        metadata, _ = _metadonnees(_CSV)
        fournisseur = _Fournisseur(dict(metadata), [_CSV])
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _compose_reel()
        parseur, _ = _fabrique_parseur()
        autre = dict(_valid_policy(), max_rows=7)
        args = _args_prepare(metadata, autre, parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assert_refus((bilan, diagnostics))
        self.assertEqual(fournisseur.stat_appels, 0)
        self.assertEqual(fournisseur.iter_appels, 0)

    async def test_chunk_borne_refuse_fermeture(self):
        politique = dict(_valid_policy(), read_chunk_bytes=4)
        metadata, _ = _metadonnees(_CSV)
        fournisseur = _Fournisseur(dict(metadata), [_CSV])
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _composer_limites(politique)
        parseur, _ = _fabrique_parseur(politique=politique)
        args = _args_prepare(metadata, politique, parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assert_refus((bilan, diagnostics))
        self.assertTrue(fournisseur.dernier_iterateur.ferme)

    async def test_limite_lignes_bilan_incomplet_honnete_termine(self):
        politique = dict(_valid_policy(), max_rows=1)
        metadata, _ = _metadonnees(_CSV)
        fournisseur = _Fournisseur(dict(metadata), [_CSV])
        resolveur = _Resolveur(fournisseur)
        bundle, _, _ = _composer_limites(politique)
        parseur, _ = _fabrique_parseur(politique=politique)
        args = _args_prepare(metadata, politique, parseur, bundle, storage_resolver=resolveur)
        bilan, diagnostics = await lecteur_prepare(**args)
        self.assertEqual(diagnostics, [])
        self.assertTrue(bilan.complete)
        resume = bilan.parser_summary.as_values()
        self.assertFalse(resume["complete"])
        self.assertLessEqual(len(bilan.units), 1)
        with self.assertRaises(ValueError):
            parseur.feed(b"bob,2\n")


def _unites_csv():
    parseur, _ = _fabrique_parseur()
    emises = parseur.feed(_CSV)
    queue, resume = parseur.finish()
    assert resume.complete
    return tuple(emises) + tuple(queue)


class _Proprietaire:
    """Port de commande : validate réel, autres méthodes piégées."""

    def __init__(self, verdicts):
        self.calls = []
        self.execute_calls = []
        self.canonical_calls = []
        self.verdicts = dict(verdicts)

    async def validate(self, contexte, entree, references):
        self.calls.append((contexte, dict(entree), references))
        ligne = entree["line_index"]
        if ligne in self.verdicts:
            resultat = self.verdicts[ligne]
            if isinstance(resultat, Exception):
                raise resultat
            return resultat
        return {"accepted": True, "diagnostics": ()}

    def execute(self, *args, **kwargs):
        self.execute_calls.append((args, kwargs))
        raise AssertionError("owner execute must never be invoked")

    def canonical_bytes(self, *args, **kwargs):
        self.canonical_calls.append((args, kwargs))
        raise AssertionError("owner canonical_bytes must never be invoked")


def _rejet(ligne, code="REJECTED", champ="name"):
    return {"accepted": False, "diagnostics": ({"code": code, "field_reference": champ, "line_index": ligne},)}


def _args_verdicts(unites, proprietaire, politique=None, garde=None, restant=60.0, echeance=None):
    politique = _valid_policy() if politique is None else dict(politique)
    if echeance is None:
        echeance = datetime.now(timezone.utc) + timedelta(seconds=60)
    return {
        "validate_fn": proprietaire.validate,
        "server_context": object(),
        "units": tuple(unites),
        "references": ("operation-test", "owner-test", "mapping-test", "1.2.3-rc.1+build"),
        "policy_owned": dict(politique),
        "owner_codes": frozenset(_CODES_ETENDUS),
        "owner_fields": frozenset(_CHAMPS),
        "max_diagnostics": int(politique["max_diagnostics"]),
        "remaining_fn": (lambda: restant) if not callable(restant) else restant,
        "cancel_event": asyncio.Event(),
        "effective": echeance,
        "transfer_guard": (lambda: None) if garde is None else garde,
        "scratch": [],
    }


class VerdictsParUniteTests(unittest.IsolatedAsyncioTestCase):
    async def test_verdicts_separes_contexte_et_references(self):
        unites = _unites_csv()
        self.assertEqual(len(unites), 2)
        seconde = unites[1].line_index
        proprietaire = _Proprietaire({seconde: _rejet(seconde)})
        args = _args_verdicts(unites, proprietaire)
        contexte = args["server_context"]
        valides, invalides, diags = await orch._validate_units_one_by_one(**args)
        self.assertEqual((valides, invalides), (2, 1), msg="compteurs examinés et rejetés exacts attendus")
        self.assertEqual(len(diags), 1)
        self.assertEqual(len(proprietaire.calls), 2, msg="un transfert par unité réelle attendu")
        for contexte_appel, _, _ in proprietaire.calls:
            self.assertIs(contexte_appel, contexte)
        self.assertIs(proprietaire.calls[0][2], proprietaire.calls[1][2])
        self.assertIsNot(proprietaire.calls[0][1], proprietaire.calls[1][1])
        self.assertEqual(proprietaire.execute_calls, [])
        self.assertEqual(proprietaire.canonical_calls, [])
        self.assertEqual(args["scratch"], [])

    async def test_diagnostics_ligne_none_et_multiples_rejet_unique(self):
        unites = _unites_csv()
        seconde = unites[1].line_index
        verdict = {
            "accepted": False,
            "diagnostics": (
                {"code": "REJECTED", "field_reference": "name", "line_index": seconde},
                {"code": "REJECTED", "field_reference": None, "line_index": None},
            ),
        }
        proprietaire = _Proprietaire({seconde: verdict})
        args = _args_verdicts(unites, proprietaire)
        valides, invalides, diags = await orch._validate_units_one_by_one(**args)
        self.assertEqual((valides, invalides), (2, 1), msg="rejet unique malgré diagnostics multiples attendu")
        self.assertEqual(len(diags), 2)
        self.assertEqual(args["scratch"], [])

    async def test_ligne_etrangere_refusee(self):
        unites = _unites_csv()
        premiere = unites[0].line_index
        proprietaire = _Proprietaire({premiere: _rejet(9999)})
        args = _args_verdicts(unites[:1], proprietaire)
        with self.assertRaises(orch._OrchestrationRefused):
            await orch._validate_units_one_by_one(**args)
        self.assertEqual(len(proprietaire.calls), 1)
        self.assertEqual(args["scratch"], [])

    async def test_verdicts_hostiles_refuses_sans_crash(self):
        unites = _unites_csv()
        premiere = unites[0].line_index
        for verdict in (
            _Hostile(),
            {"accepted": "oui", "diagnostics": ()},
            {"accepted": True, "diagnostics": [{"code": "REJECTED", "field_reference": "name", "line_index": premiere}]},
            {"accepted": False, "diagnostics": ({"code": "INCONNU", "field_reference": "name", "line_index": premiere},)},
            {"accepted": False},
        ):
            proprietaire = _Proprietaire({premiere: verdict})
            args = _args_verdicts(unites[:1], proprietaire)
            with self.subTest(verdict=type(verdict).__name__):
                with self.assertRaises(orch._OrchestrationRefused):
                    await orch._validate_units_one_by_one(**args)
                self.assertEqual(args["scratch"], [])

    async def test_garde_revoquee_entre_unites(self):
        unites = _unites_csv()
        appels = []

        def garde():
            appels.append(1)
            if len(appels) == 2:
                raise orch._OrchestrationRefused([orch._refusal("transfert", "revoque")])

        proprietaire = _Proprietaire({})
        args = _args_verdicts(unites, proprietaire, garde=garde)
        with self.assertRaises(orch._OrchestrationRefused):
            await orch._validate_units_one_by_one(**args)
        self.assertEqual(len(proprietaire.calls), 1, msg="révocation avant second transfert attendue")
        self.assertEqual(len(appels), 2, msg="garde avant chaque transfert attendue")
        self.assertEqual(args["scratch"], [])

    async def test_event_annule_avant_transfert(self):
        unites = _unites_csv()
        appels = []
        proprietaire = _Proprietaire({})
        args = _args_verdicts(unites, proprietaire, garde=lambda: appels.append(1))
        args["cancel_event"].set()
        with self.assertRaises(orch._OrchestrationRefused):
            await orch._validate_units_one_by_one(**args)
        self.assertEqual(proprietaire.calls, [])
        self.assertEqual(appels, [])
        self.assertEqual(args["scratch"], [])

    async def test_echeance_avant_transfert(self):
        unites = _unites_csv()
        proprietaire = _Proprietaire({})
        args = _args_verdicts(unites, proprietaire, echeance=datetime.now(timezone.utc) - timedelta(seconds=1))
        with self.assertRaises(orch._OrchestrationRefused):
            await orch._validate_units_one_by_one(**args)
        self.assertEqual(proprietaire.calls, [])
        self.assertEqual(args["scratch"], [])

    async def test_proprietaire_en_panne_sans_transfert_suivant(self):
        unites = _unites_csv()
        seconde = unites[1].line_index
        proprietaire = _Proprietaire({seconde: TimeoutError("panne synthetique")})
        args = _args_verdicts(unites + unites[:1], proprietaire)
        with self.assertRaises(orch._OrchestrationRefused):
            await orch._validate_units_one_by_one(**args)
        self.assertEqual(len(proprietaire.calls), 2, msg="aucun transfert suivant après panne attendu")
        self.assertEqual(args["scratch"], [])

    async def test_borne_diagnostics_arrete_avant_unite_suivante(self):
        # Norme arrêt sur borne : borne atteinte après la première unité
        # rejetée, aucun transfert suivant, refus d'incomplétude annoncé.
        unites = _unites_csv()
        lignes = [unite.line_index for unite in unites]
        verdicts = {ligne: _rejet(ligne) for ligne in lignes}
        proprietaire = _Proprietaire(verdicts)
        politique = dict(_valid_policy(), max_diagnostics=1)
        args = _args_verdicts(unites + unites[:1], proprietaire, politique=politique)
        with self.assertRaises(orch._OrchestrationRefused):
            await orch._validate_units_one_by_one(**args)
        self.assertEqual(len(proprietaire.calls), 1, msg="arrêt dès borne atteinte attendu")
        self.assertEqual(args["scratch"], [])


class ExamenEtRapportTests(unittest.TestCase):
    def _examen_csv(self, politique=None):
        politique = _valid_policy() if politique is None else dict(politique)
        parseur, _ = _fabrique_parseur(politique=politique)
        emises = parseur.feed(_CSV)
        queue, resume = parseur.finish()
        unites = tuple(emises) + tuple(queue)
        qualifie = self._qualifie(unites, resume)
        instantane = declare_bulk_mapping_descriptor(_mapping())
        return orch._check_parser_exam(qualifie, _declaration(), instantane)

    def _qualifie(self, unites, resume):
        from pixs.backend.bulk_private_object_reader import _QualifiedImportUnits

        return _QualifiedImportUnits(
            complete=True,
            accepted_size=len(_CSV),
            sha256=hashlib.sha256(_CSV).hexdigest(),
            units=tuple(unites),
            parser_summary=resume,
        )

    def test_examen_complet_coherent_catalogues_immuables(self):
        examen = self._examen_csv()
        self.assertTrue(examen["full"])
        self.assertEqual(examen["emitted"], 2)
        self.assertEqual(examen["refused"], 0)
        self.assertEqual(examen["warnings"], [])
        self.assertIs(type(examen["report_codes"]), frozenset)
        self.assertIs(type(examen["report_fields"]), frozenset)
        self.assertTrue(set(_CODES) <= set(examen["report_codes"]))
        self.assertTrue({"name", "count", "source_name", "source_count"} <= set(examen["report_fields"]))

    def test_examen_incomplet_honnete_termine_stable(self):
        politique = dict(_valid_policy(), max_rows=1)
        parseur, _ = _fabrique_parseur(politique=politique)
        emises = parseur.feed(_CSV)
        queue, resume = parseur.finish()
        valeurs = resume.as_values()
        self.assertFalse(valeurs["complete"])
        qualifie = self._qualifie(tuple(emises) + tuple(queue), resume)
        examen = orch._check_parser_exam(qualifie, _declaration(), declare_bulk_mapping_descriptor(_mapping()))
        self.assertFalse(examen["full"])
        self.assertTrue(examen["warnings"])
        for averti in examen["warnings"]:
            self.assertIn(averti["code"], set(examen["report_codes"]))
        with self.assertRaises(ValueError):
            parseur.feed(b"bob,2\n")
        relus = resume.as_values()["diagnostics"]
        if relus:
            relus[0]["code"] = "appelant-modifie"
        self.assertNotIn("appelant-modifie", [item["code"] for item in resume.as_values()["diagnostics"]])

    def test_rapport_incomplet_total_none_valide(self):
        from pixs.backend.bulk_validation_report_values import validate_bulk_validation_report_values

        avertis = [{"code": "LIMIT_ROWS", "field_reference": None, "line_index": None}]
        diags = [{"code": "REJECTED", "field_reference": "name", "line_index": 1}]
        valeurs = orch._build_report_values(
            operation_id="operation-test",
            mapping_version="1.2.3-rc.1+build",
            source_version="version-test",
            total_rows=None,
            validated_rows=1,
            invalid_rows=1,
            complete=False,
            parser_warnings=avertis,
            owner_diagnostics=diags,
            max_diagnostics=100,
        )
        self.assertIsNone(valeurs["progress"]["total_rows"])
        self.assertFalse(valeurs["complete"])
        self.assertEqual(
            valeurs["progress"],
            {"total_rows": None, "validated_rows": 1, "invalid_rows": 1, "applied_rows": 0,
             "execution_rejected_rows": 0, "exported_rows": 0},
        )
        examen = self._examen_csv()
        self.assertEqual(
            validate_bulk_validation_report_values(
                valeurs,
                policy=_valid_policy(),
                declared_codes=examen["report_codes"],
                declared_fields=examen["report_fields"],
            ),
            [],
        )

    def test_rapport_borne_depassee_refusee(self):
        diags = [
            {"code": "REJECTED", "field_reference": "name", "line_index": 1},
            {"code": "REJECTED", "field_reference": "name", "line_index": 2},
        ]
        with self.assertRaises(orch._OrchestrationRefused):
            orch._build_report_values(
                operation_id="operation-test",
                mapping_version="1.2.3-rc.1+build",
                source_version=None,
                total_rows=2,
                validated_rows=2,
                invalid_rows=2,
                complete=True,
                parser_warnings=[],
                owner_diagnostics=diags,
                max_diagnostics=1,
            )

    def test_rapport_deduplique(self):
        diag = {"code": "REJECTED", "field_reference": "name", "line_index": 1}
        valeurs = orch._build_report_values(
            operation_id="operation-test",
            mapping_version="1.2.3-rc.1+build",
            source_version=None,
            total_rows=2,
            validated_rows=2,
            invalid_rows=1,
            complete=True,
            parser_warnings=[dict(diag)],
            owner_diagnostics=[dict(diag)],
            max_diagnostics=100,
        )
        self.assertEqual(len(valeurs["diagnostics"]), 1)

    def test_rapport_compteurs_incoherents_refuses_par_contrat(self):
        from pixs.backend.bulk_validation_report_values import validate_bulk_validation_report_values

        valeurs = orch._build_report_values(
            operation_id="operation-test",
            mapping_version="1.2.3-rc.1+build",
            source_version=None,
            total_rows=3,
            validated_rows=1,
            invalid_rows=2,
            complete=True,
            parser_warnings=[],
            owner_diagnostics=[],
            max_diagnostics=100,
        )
        examen = self._examen_csv()
        refus = validate_bulk_validation_report_values(
            valeurs,
            policy=_valid_policy(),
            declared_codes=examen["report_codes"],
            declared_fields=examen["report_fields"],
        )
        self.assertTrue(refus)


def _base_validation_kwargs(**surcharge):
    bundle, _, _ = _compose_reel()
    metadata, debut = _metadonnees(_CSV)
    args = {
        "trusted_ports": bundle,
        "runtime_repository": object(),
        "report_repository": object(),
        "server_context": object(),
        "operation_id": "operation-test",
        "job_id": "job-test",
        "owner_reference": "owner-test",
        "lease_owner": "worker-test",
        "expected_metadata": dict(metadata),
        "storage_resolver": object(),
        "deadline": debut + timedelta(seconds=60),
        "now": debut,
        "cancel_event": asyncio.Event(),
        "expected_schedule_revision": 1,
    }
    args.update(surcharge)
    return args


class GardesPrimitivesTests(unittest.IsolatedAsyncioTestCase):
    async def test_gardes_primitives_avant_chargeur_depots(self):
        echeance_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        cas = [
            ({"trusted_ports": None}, "bulk_import_validate.trusted_ports"),
            ({"operation_id": ""}, "bulk_import_validate.references"),
            ({"operation_id": _Hostile()}, "bulk_import_validate.references"),
            ({"deadline": echeance_naive}, "bulk_import_validate.deadline"),
            ({"cancel_event": object()}, "bulk_import_validate.cancel_event"),
            ({"expected_schedule_revision": 0}, "bulk_import_validate.expected_schedule_revision"),
            ({"expected_metadata": {"inconnu": True}}, ("prefixe", "bulk_object_metadata.")),
            ({"storage_resolver": None}, "bulk_import_validate.storage_resolver"),
        ]
        for index, (surcharge, attendu) in enumerate(cas):
            with self.subTest(cas=index):
                with mock.patch.object(orch, "_load_repository_classes") as chargeur:
                    bilan, diagnostics = await orch.validate_import_only(**_base_validation_kwargs(**surcharge))
                self.assertIsNone(bilan)
                self.assertTrue(diagnostics, msg="refus explicite de la garde visée attendu")
                for item in diagnostics:
                    self.assertIs(type(item), Diagnostic)
                    self.assertEqual(item.step, VALIDATE)
                elements = [item.element for item in diagnostics]
                if isinstance(attendu, tuple):
                    self.assertTrue(
                        all(element.startswith(attendu[1]) for element in elements),
                        msg="diagnostics issus du contrat métadonnées attendu",
                    )
                else:
                    self.assertIn(attendu, elements, msg="élément de la garde visée attendu")
                chargeur.assert_not_called()

    async def test_garde_metadata_profonde_avant_methodes(self):
        metadata, _ = _metadonnees(_CSV)
        corrompu = dict(metadata, media_type="inexistant")
        with mock.patch.object(orch, "_load_repository_classes") as chargeur:
            with mock.patch.object(orch, "_capture_python_method", side_effect=AssertionError("capture précoce")) as capture:
                bilan, diagnostics = await orch.validate_import_only(**_base_validation_kwargs(expected_metadata=corrompu))
        self.assertIsNone(bilan)
        self.assertTrue(
            any(item.element.startswith("bulk_object_metadata.") for item in diagnostics),
            msg="refus métadonnées profondes avant captures attendu",
        )
        chargeur.assert_not_called()
        capture.assert_not_called()


class ImportPurIsoleTests(unittest.TestCase):
    def test_import_pur_sans_django_sous_processus(self):
        racine = pathlib.Path(__file__).resolve().parents[2]
        env = {
            "PATH": "/usr/bin:/bin",
            "LANG": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": ":".join((str(racine / "src"), str(racine / "tests"))),
        }
        termine = subprocess.run(
            [sys.executable, "-c", _PUR],
            cwd=str(racine),
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(termine.returncode, 0, msg="import pur en échec : " + termine.stderr[-2000:])
        self.assertIn("PUR", termine.stdout)


if __name__ == "__main__":
    unittest.main()
