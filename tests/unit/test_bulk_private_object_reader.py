"""Lecteur privé B04 : contrat réel, refus fermés et bornes, sans production."""

import asyncio
import hashlib
import unittest
from datetime import datetime, timedelta, timezone

from pixs.backend import bulk_private_object_reader as lecteur
from pixs.backend.bulk_trusted_ports import _BulkTrustedPorts
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from unit.test_bulk_execution_values import _valid_policy
from unit.test_bulk_runtime_contracts import (
    _Hostile,
    _ForeignDict,
    _ForeignStr,
    _context,
)
from unit.test_bulk_trusted_ports import (
    _Authority,
    _GovernanceResolve3,
    _resolved_response,
)


_DONNEES = b"entree privee synthetique\n"
_VIDE = b""


def _maintenant():
    return datetime.now(timezone.utc)


def _metadonnees(donnees=_DONNEES, **surcharge):
    debut = _maintenant()
    valeurs = {
        "object_reference": "object-test",
        "version_reference": "version-test",
        "tenant_reference": "tenant-test",
        "scope_reference": None,
        "classification_reference": "classification-test",
        "size_bytes": len(donnees),
        "sha256": hashlib.sha256(donnees).hexdigest(),
        "media_type": "text/csv",
        "is_private": True,
        "expires_at": debut + timedelta(hours=1),
        "retention_policy_reference": "retention-test",
    }
    valeurs.update(surcharge)
    return valeurs, debut


def _appel_base(**surcharge):
    metadata, debut = _metadonnees()
    politique = _valid_policy()
    echeance = debut + timedelta(seconds=60)
    kwargs = {
        "trusted_ports": None,
        "server_context": object(),
        "operation_reference": "operation-test",
        "expected_metadata": metadata,
        "policy_reference": "policy-test",
        "policy_version": "1.0.0",
        "storage_resolver": None,
        "expected_policy": politique,
        "deadline": echeance,
        "now": debut,
        "cancel_event": asyncio.Event(),
    }
    kwargs.update(surcharge)
    return kwargs


class _Iterateur:
    """Itérateur coopératif réel, fermeture comptée par lui-même."""

    def __init__(self, morceaux, fail_close=False, entree_anext=None, entree_close=None):
        self._morceaux = list(morceaux)
        self.ferme = False
        self._fail_close = fail_close
        self._entree_anext = entree_anext
        self._entree_close = entree_close

    async def __anext__(self):
        if self._entree_anext is not None and not self._entree_anext.is_set():
            self._entree_anext.set()
        if not self._morceaux:
            raise StopAsyncIteration
        return self._morceaux.pop(0)

    async def aclose(self):
        if self._entree_close is not None and not self._entree_close.is_set():
            self._entree_close.set()
        self.ferme = True
        if self._fail_close:
            raise RuntimeError("fermeture synthetique en echec")


class _Fournisseur:
    """Fournisseur synthétique réel, méthodes async de classe liées."""

    def __init__(self, metadata, morceaux, fail_close=False):
        self.metadata = dict(metadata)
        self._morceaux = list(morceaux)
        self.stat_appels = 0
        self.iter_appels = 0
        self._fail_close = fail_close
        self.dernier_iterateur = None

    async def stat_private(self, contexte, objet, version):
        self.stat_appels += 1
        return dict(self.metadata)

    async def iter_bytes(self, contexte, objet, version):
        self.iter_appels += 1
        await asyncio.sleep(0)
        it = _Iterateur(list(self._morceaux), fail_close=self._fail_close)
        self.dernier_iterateur = it
        return it


class _FournisseurChangeant(_Fournisseur):
    """Sous-classe réelle : première stat originale, seconde divergente."""

    async def stat_private(self, contexte, objet, version):
        if self.stat_appels == 0:
            return await super().stat_private(contexte, objet, version)
        self.stat_appels += 1
        return dict(self.metadata, version_reference="version-apres")


class _Resolveur:
    """Résolveur serveur déclaré, qualify async vers binding exact."""

    def __init__(self, fournisseur=None, fail=False, exception=None):
        self.fournisseur = fournisseur
        self.fail = fail
        self.exception = exception
        self.appels = []

    async def qualify(self, contexte, objet, version):
        self.appels.append((contexte, objet, version))
        await asyncio.sleep(0)
        if self.fail:
            raise RuntimeError("qualification synthetique en echec")
        if self.exception is not None:
            raise self.exception
        fournisseur = self.fournisseur
        binding = lecteur._make_qualified_storage_binding(
            provider=fournisseur,
            object_reference=objet,
            version_reference=version,
            provider_reference="provider-test",
        )
        if binding is None:
            raise RuntimeError("fabrique serveur refusee")
        return binding


def _compose_reel(reponse=None, autorite=None):
    import pixs.backend.bulk_trusted_ports as ports
    from unit.test_bulk_trusted_ports import _kwargs

    autorite_reelle = autorite if autorite is not None else _Authority()
    gov = _GovernanceResolve3(response=reponse)
    kwargs = _kwargs(authority=autorite_reelle)
    kwargs["governance_adapter"] = gov
    bundle = ports.compose_bulk_trusted_ports(**kwargs)
    if reponse is None:
        gov.response = _resolved_response()
    return bundle, gov, autorite_reelle


def _succes_args(donnees=_DONNEES, **surcharge):
    metadata, _ = _metadonnees(donnees)
    fournisseur = _Fournisseur(metadata, [donnees] if donnees else [])
    resolveur = _Resolveur(fournisseur)
    bundle, gov, _ = _compose_reel()
    args = _appel_base(
        trusted_ports=bundle, expected_metadata=metadata, storage_resolver=resolveur, **surcharge
    )
    return args, bundle, fournisseur, gov


class LecteurPriveTests(unittest.IsolatedAsyncioTestCase):
    def assert_refus(self, resultat):
        bilan, diagnostics = resultat
        self.assertIsNone(bilan)
        self.assertIs(type(diagnostics), list)
        self.assertTrue(diagnostics)
        for item in diagnostics:
            self.assertIs(type(item), Diagnostic)
            self.assertEqual(item.step, VALIDATE)

    async def test_succes_non_vide_double_stat(self):
        args, _, fournisseur, _ = _succes_args()
        bilan, diagnostics = await lecteur.read_private_object_once(**args)
        self.assertEqual(diagnostics, [])
        self.assertTrue(bilan.complete)
        self.assertEqual(bilan.accepted_size, len(_DONNEES))
        self.assertEqual(bilan.sha256, hashlib.sha256(_DONNEES).hexdigest())
        self.assertEqual(fournisseur.stat_appels, 2)
        self.assertEqual(fournisseur.iter_appels, 1)
        self.assertTrue(fournisseur.dernier_iterateur.ferme)

    async def test_succes_vide_taille_zero(self):
        args, _, _, _ = _succes_args(donnees=_VIDE)
        bilan, diagnostics = await lecteur.read_private_object_once(**args)
        self.assertEqual(diagnostics, [])
        self.assertTrue(bilan.complete)
        self.assertEqual(bilan.accepted_size, 0)

    async def test_check_execute_reel_et_contrat_onze_cles(self):
        autorite = _Authority()
        bundle, gov, gardee = _compose_reel(autorite=autorite)
        self.assertIs(gardee, autorite)
        self.assertIs(type(bundle), _BulkTrustedPorts)
        metadata, _ = _metadonnees()
        fournisseur = _Fournisseur(metadata, [_DONNEES])
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=metadata,
            storage_resolver=_Resolveur(fournisseur),
        )
        bilan, _ = await lecteur.read_private_object_once(**args)
        self.assertTrue(bilan.complete)
        self.assertEqual(len(autorite.calls), 1)
        contexte, action, operation, ressource = autorite.calls[0]
        self.assertIs(contexte, args["server_context"])
        self.assertEqual(action, "EXECUTE")
        self.assertEqual(operation, "operation-test")
        self.assertEqual(ressource, "object-test")
        self.assertEqual(len(gov.calls), 1)
        _, contrat, references = gov.calls[0]
        self.assertEqual(len(contrat.keys()), 11)
        self.assertEqual(references, ("policy-test", "1.0.0"))

    async def test_sha_taille_chunk_surplus_refuses(self):
        for cas in ("sha", "taille", "chunk", "surplus", "tronque"):
            metadata, _ = _metadonnees()
            politique = _valid_policy()
            if cas == "sha":
                attendu = dict(metadata, sha256="a" * 64)
                base = dict(metadata, sha256="a" * 64)
                morceaux = [_DONNEES]
            elif cas == "taille":
                attendu = dict(metadata)
                base = dict(metadata)
                morceaux = [_DONNEES + b"octet-supplementaire"]
            elif cas == "chunk":
                attendu = dict(metadata)
                base = dict(metadata)
                morceaux = [b"x" * (politique["read_chunk_bytes"] + 1)]
            elif cas == "surplus":
                attendu = dict(metadata)
                base = dict(metadata)
                morceaux = [_DONNEES, b"surplus"]
            else:
                attendu = dict(metadata)
                base = dict(metadata)
                morceaux = [_DONNEES[:-1]]
            fournisseur = _Fournisseur(base, morceaux)
            bundle, _, _ = _compose_reel()
            args = _appel_base(
                trusted_ports=bundle, expected_metadata=attendu,
                storage_resolver=_Resolveur(fournisseur),
            )
            with self.subTest(cas=cas):
                bilan, diagnostics = await lecteur.read_private_object_once(**args)
                self.assert_refus((bilan, diagnostics))
                if cas in ("sha", "tronque"):
                    self.assertEqual(fournisseur.stat_appels, 2)
                    self.assertEqual(fournisseur.iter_appels, 1)
                    self.assertTrue(fournisseur.dernier_iterateur.ferme)
                if cas == "sha":
                    self.assertTrue(
                        any(
                            "sha256" in item.element
                            and "recalculée" in item.constraint
                            for item in diagnostics
                        )
                    )

    async def test_metadata_divergents_stat_avant_iter(self):
        base, _ = _metadonnees()
        for champ, valeur in (
            ("classification_reference", "autre-classe"),
            ("media_type", "application/x-ndjson"),
            ("version_reference", "autre-version"),
        ):
            attendu = dict(base, **{champ: valeur})
            fournisseur = _Fournisseur(dict(base), [_DONNEES])
            bundle, _, _ = _compose_reel()
            args = _appel_base(
                trusted_ports=bundle, expected_metadata=attendu,
                storage_resolver=_Resolveur(fournisseur),
            )
            with self.subTest(champ=champ):
                self.assert_refus(await lecteur.read_private_object_once(**args))
                self.assertEqual(fournisseur.stat_appels, 1)
                self.assertEqual(fournisseur.iter_appels, 0)
        # Tenant : refus pré-stockage.
        attendu = dict(base, tenant_reference="autre-tenant")
        fournisseur = _Fournisseur(dict(base), [_DONNEES])
        bundle, _, _ = _compose_reel()
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=attendu,
            storage_resolver=_Resolveur(fournisseur),
        )
        self.assert_refus(await lecteur.read_private_object_once(**args))
        self.assertEqual(fournisseur.stat_appels, 0)

    async def test_version_apres_flux_divergente(self):
        metadata, _ = _metadonnees()
        fournisseur = _FournisseurChangeant(dict(metadata), [_DONNEES])
        bundle, _, _ = _compose_reel()
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=dict(metadata),
            storage_resolver=_Resolveur(fournisseur),
        )
        self.assert_refus(await lecteur.read_private_object_once(**args))
        self.assertEqual(fournisseur.stat_appels, 2)
        self.assertEqual(fournisseur.iter_appels, 1)
        self.assertTrue(fournisseur.dernier_iterateur.ferme)

    async def test_authority_deny_unavailable_sans_stockage(self):
        for decision in ("DENY", "UNAVAILABLE"):
            autorite = _Authority({"decision": decision, "resolved_context": None})
            bundle, _, _ = _compose_reel(autorite=autorite)
            metadata, _ = _metadonnees()
            fournisseur = _Fournisseur(metadata, [_DONNEES])
            args = _appel_base(
                trusted_ports=bundle, expected_metadata=metadata,
                storage_resolver=_Resolveur(fournisseur),
            )
            with self.subTest(decision=decision):
                self.assert_refus(await lecteur.read_private_object_once(**args))
                self.assertEqual(len(autorite.calls), 1)
                self.assertEqual(fournisseur.stat_appels, 0)
                self.assertEqual(fournisseur.iter_appels, 0)

    async def test_gouvernance_contexte_policy_divergents(self):
        autre = dict(_context(), tenant_id="autre-tenant")
        limites = _valid_policy()
        reponse = {
            "resolution_version": "1.0.0", "decision": "RESOLVED",
            "resolved_context": autre,
            "policy": {"policy_reference": "policy-test", "policy_version": "1.0.0", "limits": limites},
            "profile": _resolved_response()["profile"], "obligations": ("obligation-test",),
        }
        bundle, _, _ = _compose_reel(reponse=reponse)
        metadata, _ = _metadonnees()
        fournisseur = _Fournisseur(metadata, [_DONNEES])
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=metadata,
            storage_resolver=_Resolveur(fournisseur),
        )
        self.assert_refus(await lecteur.read_private_object_once(**args))
        self.assertEqual(fournisseur.stat_appels, 0)
        limites2 = dict(_valid_policy(), max_input_bytes=1)
        reponse2 = _resolved_response()
        reponse2["policy"] = {"policy_reference": "policy-test", "policy_version": "1.0.0", "limits": limites2}
        bundle2, _, _ = _compose_reel(reponse=reponse2)
        fournisseur2 = _Fournisseur(metadata, [_DONNEES])
        args2 = _appel_base(
            trusted_ports=bundle2, expected_metadata=metadata,
            storage_resolver=_Resolveur(fournisseur2),
        )
        self.assert_refus(await lecteur.read_private_object_once(**args2))
        self.assertEqual(fournisseur2.stat_appels, 0)

    async def test_qualification_erreurs_au_stade_vise(self):
        metadata, _ = _metadonnees()
        # None : refus avant tout appel stockage.
        bundle, _, _ = _compose_reel()
        args = _appel_base(trusted_ports=bundle, expected_metadata=metadata, storage_resolver=None)
        self.assert_refus(await lecteur.read_private_object_once(**args))

        class _Sync:
            def qualify(self, *a, **k):
                return None

        bundle, _, _ = _compose_reel()
        args = _appel_base(trusted_ports=bundle, expected_metadata=metadata, storage_resolver=_Sync())
        self.assert_refus(await lecteur.read_private_object_once(**args))

        for mode in ("fail", "exception", "etrangere", "divergente"):
            bundle, _, _ = _compose_reel()
            fournisseur = _Fournisseur(dict(metadata), [_DONNEES])
            resolveur = _Resolveur(fournisseur)
            if mode == "fail":
                resolveur.fail = True
            elif mode == "exception":
                resolveur.exception = RuntimeError("brute-qualify")
            args = _appel_base(
                trusted_ports=bundle, expected_metadata=dict(metadata), storage_resolver=resolveur
            )
            if mode == "etrangere":
                async def _etrangere(contexte, objet, version):
                    return object()

                resolveur.qualify = _etrangere
            if mode == "divergente":
                async def _divergente(contexte, objet, version):
                    bon = await _Resolveur.qualify(resolveur, contexte, objet, version)
                    return lecteur._QualifiedStorageBinding(
                        provider_reference=bon.provider_reference,
                        object_reference="autre-objet",
                        version_reference=bon.version_reference,
                        provider=bon.provider, stat_private=bon.stat_private,
                        iter_bytes=bon.iter_bytes, immutability="IMMUTABLE",
                        cancellation_supported=True,
                    )

                resolveur.qualify = _divergente
            with self.subTest(mode=mode):
                bilan, diagnostics = await lecteur.read_private_object_once(**args)
                self.assert_refus((bilan, diagnostics))
                for item in diagnostics:
                    self.assertNotIn("brute", str(item))
                self.assertEqual(fournisseur.stat_appels, 0)

    async def test_bindings_libres_negatifs_distincts(self):
        metadata, _ = _metadonnees()
        fournisseur = _Fournisseur(dict(metadata), [_DONNEES])
        bundle, _, _ = _compose_reel()

        async def _stat_libre(contexte, objet, version):
            return dict(metadata)

        async def _iter_libre(contexte, objet, version):
            return _Iterateur([_DONNEES])

        binding = lecteur._QualifiedStorageBinding(
            provider_reference="provider-test", object_reference="object-test",
            version_reference="version-test", provider=fournisseur,
            stat_private=_stat_libre, iter_bytes=_iter_libre,
            immutability="IMMUTABLE", cancellation_supported=True,
        )

        class _R:
            async def qualify(self, *a, **k):
                return binding

        args = _appel_base(trusted_ports=bundle, expected_metadata=dict(metadata), storage_resolver=_R())
        self.assert_refus(await lecteur.read_private_object_once(**args))

    async def test_adversaires_jamais_invoques(self):
        class _Egal:
            def __eq__(self, autre):
                raise AssertionError("égalité étrangère invoquée")

            def __hash__(self):
                raise AssertionError("hash étranger invoqué")

        for candidat in (_Hostile(), _ForeignDict({}), _ForeignStr("x"), _Egal()):
            args, _, _, _ = _succes_args()
            args["operation_reference"] = candidat
            bilan, _ = await lecteur.read_private_object_once(**args)
            self.assertIsNone(bilan)

    async def test_capture_reelle_pendant_qualify_suspendu(self):
        metadata, _ = _metadonnees()
        politique = _valid_policy()
        bundle, _, _ = _compose_reel()
        entre = asyncio.Event()
        libere = asyncio.Event()
        fournisseur = _Fournisseur(dict(metadata), [_DONNEES])

        class _Suspensif(_Resolveur):
            async def qualify(self, contexte, objet, version):
                entre.set()
                await libere.wait()
                return await super().qualify(contexte, objet, version)

        resolveur = _Suspensif(fournisseur)
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=dict(metadata),
            expected_policy=dict(politique), storage_resolver=resolveur,
        )
        tâche = asyncio.ensure_future(lecteur.read_private_object_once(**args))
        try:
            await asyncio.wait_for(entre.wait(), timeout=1.0)
            args["expected_metadata"]["object_reference"] = "mutation-test"
            args["expected_policy"]["retry_delays_seconds"].append(999)
            libere.set()
            bilan, diagnostics = await asyncio.wait_for(tâche, timeout=2.0)
        finally:
            libere.set()
            if not tâche.done():
                tâche.cancel()
            try:
                await asyncio.wait_for(tâche, timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                pass
        self.assertEqual(diagnostics, [])
        self.assertTrue(bilan.complete)
        self.assertEqual(resolveur.appels[0][1], "object-test")

    async def test_event_pendant_qualify_stat_anext_fermeture(self):
        for moment in ("qualify", "stat", "anext", "fermeture"):
            metadata, _ = _metadonnees()
            bundle, _, _ = _compose_reel()
            cancel = asyncio.Event()
            entre_qualify, entre_stat = asyncio.Event(), asyncio.Event()
            entre_anext, entre_close = asyncio.Event(), asyncio.Event()

            class _Cible(_Fournisseur):
                async def stat_private(self, *a, **k):
                    entre_stat.set()
                    if moment == "stat":
                        await asyncio.sleep(0.2)
                    return await super().stat_private(*a, **k)

                async def iter_bytes(self, *a, **k):
                    it = await super().iter_bytes(*a, **k)
                    base_anext, base_close = it.__anext__, it.aclose

                    async def _anext():
                        entre_anext.set()
                        if moment == "anext":
                            await asyncio.sleep(0.2)
                        return await base_anext()

                    async def _close():
                        entre_close.set()
                        if moment == "fermeture":
                            await asyncio.sleep(0.02)
                        return await base_close()

                    it.__anext__ = _anext
                    it.aclose = _close
                    return it

            class _CibleR(_Resolveur):
                async def qualify(self, *a, **k):
                    entre_qualify.set()
                    if moment == "qualify":
                        await asyncio.sleep(0.2)
                    return await super().qualify(*a, **k)

            fournisseur = _Cible(dict(metadata), [_DONNEES])
            # Enveloppe iterator avec fail_close seulement pour fermeture : aclose atteint.
            args = _appel_base(
                trusted_ports=bundle, expected_metadata=dict(metadata),
                storage_resolver=_CibleR(fournisseur), cancel_event=cancel,
            )
            cibles = {"qualify": entre_qualify, "stat": entre_stat,
                      "anext": entre_anext, "fermeture": entre_close}

            async def _declenche():
                await asyncio.wait_for(cibles[moment].wait(), timeout=1.0)
                await asyncio.sleep(0)
                cancel.set()

            decl = asyncio.ensure_future(_declenche())
            try:
                bilan, diagnostics = await asyncio.wait_for(
                    lecteur.read_private_object_once(**args), timeout=2.0
                )
            finally:
                if not decl.done():
                    decl.cancel()
                try:
                    await asyncio.wait_for(decl, timeout=1.0)
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    pass
            with self.subTest(moment=moment):
                self.assertIsNone(bilan)
                self.assertTrue(diagnostics)
                if moment == "fermeture":
                    self.assertTrue(entre_close.is_set())
                    self.assertTrue(fournisseur.dernier_iterateur.ferme)

    async def test_deadline_courte_bornee(self):
        import time as _temps

        metadata, _ = _metadonnees()
        bundle, _, _ = _compose_reel()
        debut = _maintenant()

        class _Suspendu(_Fournisseur):
            async def stat_private(self, *a, **k):
                await asyncio.sleep(0.2)
                return await super().stat_private(*a, **k)

        args = _appel_base(
            trusted_ports=bundle, expected_metadata=dict(metadata),
            storage_resolver=_Resolveur(_Suspendu(dict(metadata), [_DONNEES])),
            deadline=debut + timedelta(seconds=0.05), now=debut,
        )
        top = _temps.monotonic()
        bilan, _ = await lecteur.read_private_object_once(**args)
        duree = _temps.monotonic() - top
        self.assertIsNone(bilan)
        self.assertLess(duree, 0.5)
        # max_runtime_seconds int valide accepté dans le budget.
        metadata2, debut2 = _metadonnees()
        politique2 = dict(_valid_policy(), max_runtime_seconds=3600)
        bundle2, gov2, _ = _compose_reel()
        gov2.response = _resolved_response()
        gov2.response["policy"] = {
            "policy_reference": "policy-test", "policy_version": "1.0.0", "limits": politique2,
        }
        args2 = _appel_base(
            trusted_ports=bundle2, expected_metadata=dict(metadata2),
            expected_policy=dict(politique2),
            storage_resolver=_Resolveur(_Fournisseur(dict(metadata2), [_DONNEES])),
        )
        bilan2, diagnostics2 = await lecteur.read_private_object_once(**args2)
        self.assertEqual(diagnostics2, [])
        self.assertTrue(bilan2.complete)

    async def test_max_runtime_resolu_refuse_avant_stockage(self):
        import time as vrai_temps

        metadata, _ = _metadonnees()
        politique = dict(_valid_policy(), max_runtime_seconds=1)
        bundle, gov, _ = _compose_reel()
        gov.response = _resolved_response()
        gov.response["policy"] = {
            "policy_reference": "policy-test", "policy_version": "1.0.0", "limits": dict(politique),
        }
        fournisseur = _Fournisseur(dict(metadata), [_DONNEES])
        vrai_monotonic = vrai_temps.monotonic
        temps_origine = lecteur.time
        entre_qualify = asyncio.Event()

        class _Decale:
            def __getattr__(self, nom):
                return getattr(vrai_temps, nom)

            def monotonic(self):
                return vrai_monotonic() + 2.0

        class _ResolveurDecalant(_Resolveur):
            async def qualify(self, contexte, objet, version):
                entre_qualify.set()
                lecteur.time = _Decale()
                return await super().qualify(contexte, objet, version)

        args = _appel_base(
            trusted_ports=bundle,
            expected_metadata=dict(metadata),
            expected_policy=dict(politique),
            storage_resolver=_ResolveurDecalant(fournisseur),
        )
        try:
            bilan, diagnostics = await lecteur.read_private_object_once(**args)
            self.assert_refus((bilan, diagnostics))
            self.assertTrue(entre_qualify.is_set())
            self.assertEqual(fournisseur.stat_appels, 0)
            self.assertEqual(fournisseur.iter_appels, 0)
        finally:
            lecteur.time = temps_origine

    async def test_retour_arriere_utc_n_prolonge_pas(self):
        metadata, _ = _metadonnees()
        bundle, _, _ = _compose_reel()
        debut = _maintenant()
        entre = asyncio.Event()
        libere = asyncio.Event()

        class _Lent(_Fournisseur):
            async def stat_private(self, *a, **k):
                entre.set()
                await asyncio.sleep(0.15)
                return await super().stat_private(*a, **k)

        resolveur = _Resolveur(_Lent(dict(metadata), [_DONNEES]))
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=dict(metadata),
            storage_resolver=resolveur,
            deadline=debut + timedelta(seconds=0.05), now=debut,
        )
        vrai_datetime = lecteur.datetime

        class _Reculee(vrai_datetime):
            @classmethod
            def now(cls, tz=None):
                base = vrai_datetime.now(tz)
                return base - timedelta(seconds=60)

        async def _patche():
            await asyncio.wait_for(entre.wait(), timeout=1.0)
            lecteur.datetime = _Reculee
            libere.set()

        patcheur = asyncio.ensure_future(_patche())
        try:
            libere.set()
            bilan, _ = await asyncio.wait_for(lecteur.read_private_object_once(**args), timeout=2.0)
        finally:
            lecteur.datetime = vrai_datetime
            if not patcheur.done():
                patcheur.cancel()
            try:
                await asyncio.wait_for(patcheur, timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
        self.assertIsNone(bilan)

    async def test_annulation_externe_apres_acquisition(self):
        metadata, _ = _metadonnees()
        bundle, _, _ = _compose_reel()
        entre_anext = asyncio.Event()
        libere_anext = asyncio.Event()

        class _Bloquant(_Fournisseur):
            async def iter_bytes(self, *a, **k):
                it = await super().iter_bytes(*a, **k)
                base = it.__anext__

                async def _bloquee():
                    entre_anext.set()
                    await libere_anext.wait()
                    return await base()

                it.__anext__ = _bloquee
                return it

        fournisseur = _Bloquant(dict(metadata), [_DONNEES])
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=dict(metadata),
            storage_resolver=_Resolveur(fournisseur),
        )
        avant = {t for t in asyncio.all_tasks() if t is not asyncio.current_task()}
        tâche = asyncio.ensure_future(lecteur.read_private_object_once(**args))
        try:
            await asyncio.wait_for(entre_anext.wait(), timeout=1.0)
            tâche.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(tâche, timeout=2.0)
        finally:
            libere_anext.set()
            if not tâche.done():
                tâche.cancel()
            try:
                await asyncio.wait_for(tâche, timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                pass
        await asyncio.sleep(0)
        self.assertTrue(fournisseur.dernier_iterateur.ferme)
        apres = {t for t in asyncio.all_tasks() if t is not asyncio.current_task()}
        residuelles = {t for t in apres - avant if not t.done()}
        self.assertEqual(residuelles, set())

    async def test_erreurs_ordinaires_et_fermeture(self):
        # qualify ordinaire déjà couverte ; stat/iter/anext/aclose ordinaires.
        for etape in ("stat", "iter", "anext", "aclose"):
            metadata, _ = _metadonnees()
            bundle, _, _ = _compose_reel()

            class _Fautif(_Fournisseur):
                async def stat_private(self, *a, **k):
                    if etape == "stat":
                        raise RuntimeError("brute-stat")
                    return await super().stat_private(*a, **k)

                async def iter_bytes(self, *a, **k):
                    if etape == "iter":
                        raise RuntimeError("brute-iter")
                    it = await super().iter_bytes(*a, **k)
                    if etape == "anext":
                        async def _ratee():
                            raise RuntimeError("brute-anext")

                        it.__anext__ = _ratee
                    if etape == "aclose":
                        async def _closee():
                            raise RuntimeError("brute-close")

                        it.aclose = _closee
                    return it

            fournisseur = _Fautif(dict(metadata), [_DONNEES])
            args = _appel_base(
                trusted_ports=bundle, expected_metadata=dict(metadata),
                storage_resolver=_Resolveur(fournisseur),
            )
            with self.subTest(etape=etape):
                bilan, diagnostics = await lecteur.read_private_object_once(**args)
                self.assertIsNone(bilan)
                self.assertTrue(diagnostics)
                for item in diagnostics:
                    self.assertNotIn("brute", str(item))
                if etape in ("stat",):
                    self.assertEqual(fournisseur.stat_appels, 0 if etape == "stat" else 1)
                if etape in ("anext", "aclose"):
                    self.assertEqual(fournisseur.stat_appels, 2 if etape == "aclose" else 1)
                    self.assertEqual(fournisseur.iter_appels, 1)

        # aclose absente vaut refus.
        class _SansClose:
            async def __anext__(self):
                raise StopAsyncIteration

        class _FournSansClose(_Fournisseur):
            async def iter_bytes(self, *a, **k):
                self.iter_appels += 1
                return _SansClose()

        metadata, _ = _metadonnees()
        bundle, _, _ = _compose_reel()
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=dict(metadata),
            storage_resolver=_Resolveur(_FournSansClose(dict(metadata), [])),
        )
        bilan, _ = await lecteur.read_private_object_once(**args)
        self.assertIsNone(bilan)

    async def test_annulation_externe_pendant_drainage_propagee(self):
        import unittest.mock as _mock

        metadata, _ = _metadonnees()
        bundle, _, _ = _compose_reel()
        fournisseur = _Fournisseur(dict(metadata), [_DONNEES])
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=dict(metadata),
            storage_resolver=_Resolveur(fournisseur),
        )
        vrai_wait = lecteur.asyncio.wait
        intercepte = {"atteint": False, "une_fois": False}

        async def _wait_provoquant(*a, **k):
            taches = list(a[0]) if a else list(k.get("fs", []))
            if (not intercepte["une_fois"] and len(taches) >= 2
                    and any(t.done() for t in taches)
                    and any(t.cancelling() for t in taches)):
                intercepte["une_fois"] = True
                intercepte["atteint"] = True
                asyncio.current_task().cancel()
            return await vrai_wait(*a, **k)

        avant = {t for t in asyncio.all_tasks() if t is not asyncio.current_task()}
        try:
            with _mock.patch.object(lecteur.asyncio, "wait", side_effect=_wait_provoquant):
                with self.assertRaises(asyncio.CancelledError):
                    await lecteur.read_private_object_once(**args)
        finally:
            await asyncio.sleep(0)
        self.assertTrue(intercepte["atteint"])
        self.assertEqual(fournisseur.stat_appels, 0)
        self.assertEqual(fournisseur.iter_appels, 0)
        apres = {t for t in asyncio.all_tasks()
                 if t is not asyncio.current_task() and not t.done()}
        self.assertEqual(apres - {t for t in avant if not t.done()}, set())

    async def test_fermeture_bloquee_cooperative_bornee(self):
        import time as _temps

        metadata, _ = _metadonnees()
        bundle, _, _ = _compose_reel()
        debut = _maintenant()

        class _LentFerme(_Fournisseur):
            async def iter_bytes(self, *a, **k):
                it = await super().iter_bytes(*a, **k)
                base = it.aclose

                async def _bloquee():
                    try:
                        await asyncio.sleep(0.2)
                    finally:
                        it.ferme = True

                it.aclose = _bloquee
                return it

        fournisseur = _LentFerme(dict(metadata), [_DONNEES])
        args = _appel_base(
            trusted_ports=bundle, expected_metadata=dict(metadata),
            storage_resolver=_Resolveur(fournisseur),
            deadline=debut + timedelta(seconds=0.05), now=debut,
        )
        avant = {t for t in asyncio.all_tasks() if t is not asyncio.current_task()}
        top = _temps.monotonic()
        try:
            bilan, diagnostics = await lecteur.read_private_object_once(**args)
        finally:
            await asyncio.sleep(0)
        duree = _temps.monotonic() - top
        self.assertIsNone(bilan)
        self.assertTrue(diagnostics)
        self.assertEqual(fournisseur.stat_appels, 2)
        self.assertEqual(fournisseur.iter_appels, 1)
        self.assertTrue(fournisseur.dernier_iterateur.ferme)
        self.assertLess(duree, 0.5)
        apres = {t for t in asyncio.all_tasks()
                 if t is not asyncio.current_task() and not t.done()}
        self.assertEqual(apres - {t for t in avant if not t.done()}, set())

    async def test_grand_entier_max_runtime_borne_utc(self):
        args, _, fournisseur, gov = _succes_args()
        args["expected_policy"] = dict(args["expected_policy"], max_runtime_seconds=10 ** 400)
        gov.response["policy"]["limits"] = dict(
            gov.response["policy"]["limits"], max_runtime_seconds=10 ** 400
        )
        bilan, diagnostics = await lecteur.read_private_object_once(**args)
        self.assertEqual(diagnostics, [])
        self.assertTrue(bilan.complete)
        self.assertEqual(fournisseur.stat_appels, 2)
        self.assertEqual(fournisseur.iter_appels, 1)
        self.assertTrue(fournisseur.dernier_iterateur.ferme)


if __name__ == "__main__":
    unittest.main()
