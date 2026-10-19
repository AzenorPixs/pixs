"""Intégration fraîche B04 lecteur privé, mémoire pure.

PostgreSQL N/A motivé : processus mémoire frais sous interdiction DB/ORM
(sqlite3, psycopg, psycopg2, Django, pixs.core), sans SQL, persistance,
migration ni fournisseur de production. Elle ne qualifie aucune base.
"""

import subprocess
import sys
import unittest
from pathlib import Path


_CHILD = r'''
import asyncio
import builtins
import contextlib
import hashlib
import importlib
import importlib.abc
import io
import os
import socket
import subprocess as _sp
import sys
import unittest.mock as _mock
from datetime import datetime, timedelta, timezone

# Stdlib et boucle AVANT gardes pour ne pas confondre self-pipe avec réseau.
_boucle = asyncio.new_event_loop()
asyncio.set_event_loop(_boucle)

class _GuardBlocked(Exception):
    pass

_compteurs = {"lecture": 0, "ecriture": 0, "reseau": 0, "sousprocessus": 0, "systeme": 0, "environ": 0, "import_db": 0}
_lecture_bloquee = {"actif": False}
_INTERDITS = ("sqlite3", "psycopg", "psycopg2", "django", "pixs.core")
for _m in ("sqlite3", "psycopg", "psycopg2", "django", "pixs.core"):
    assert _m not in sys.modules, _m

_ouvrir_origine = builtins.open
_socket_origine = socket.socket
_popen_origine = _sp.Popen
_system_origine = os.system

def _faux_open(*a, **k):
    mode = "r"
    if len(a) >= 2 and isinstance(a[1], str):
        mode = a[1]
    mode = k.get("mode", mode)
    ecrit = any(c in mode for c in ("w", "a", "x", "+"))
    if ecrit:
        _compteurs["ecriture"] += 1
        raise _GuardBlocked("ecriture interdite")
    if _lecture_bloquee["actif"]:
        _compteurs["lecture"] += 1
        raise _GuardBlocked("lecture interdite")
    return _ouvrir_origine(*a, **k)

def _faux_socket(*a, **k):
    _compteurs["reseau"] += 1
    raise _GuardBlocked("reseau interdit")

def _faux_popen(*a, **k):
    _compteurs["sousprocessus"] += 1
    raise _GuardBlocked("sous-processus interdit")

def _faux_system(*a, **k):
    _compteurs["systeme"] += 1
    raise _GuardBlocked("systeme interdit")

def _faux_getitem(self, cle):
    _compteurs["environ"] += 1
    raise _GuardBlocked("environnement interdit")

def _faux_get(self, cle, *a, **k):
    _compteurs["environ"] += 1
    raise _GuardBlocked("environnement interdit")

def _faux_getenv(cle, *a, **k):
    _compteurs["environ"] += 1
    raise _GuardBlocked("environnement interdit")

class _GardeImport(importlib.abc.MetaPathFinder):
    def find_spec(self, nom, chemin=None, cible=None):
        base = nom.split(".")[0]
        if nom in _INTERDITS or base in ("sqlite3", "psycopg", "psycopg2", "django") or nom == "pixs.core" or nom.startswith("pixs.core."):
            _compteurs["import_db"] += 1
            raise _GuardBlocked("import interdit " + nom)
        return None

def _attend_bloque(fonction, *a, **k):
    try:
        fonction(*a, **k)
    except _GuardBlocked:
        return
    raise AssertionError("garde inactive")

try:
    with contextlib.ExitStack() as _pile:
        _pile.enter_context(_mock.patch("builtins.open", side_effect=_faux_open))
        _pile.enter_context(_mock.patch("io.open", side_effect=_faux_open))
        _pile.enter_context(_mock.patch("socket.socket", side_effect=_faux_socket))
        _pile.enter_context(_mock.patch("subprocess.Popen", side_effect=_faux_popen))
        _pile.enter_context(_mock.patch("os.system", side_effect=_faux_system))
        _pile.enter_context(_mock.patch.object(os.environ.__class__, "__getitem__", _faux_getitem))
        _pile.enter_context(_mock.patch.object(os.environ.__class__, "get", _faux_get))
        _pile.enter_context(_mock.patch("os.getenv", side_effect=_faux_getenv))
        _garde = _GardeImport()
        sys.meta_path.insert(0, _garde)
        try:
            # Contrôles positifs AVANT imports applicatifs (lecture source encore permise).
            _avant = dict(_compteurs)
            _attend_bloque(builtins.open, "fichier-inexistant-b04.tmp", "wb")
            assert _compteurs["ecriture"] == _avant["ecriture"] + 1
            _attend_bloque(socket.socket)
            assert _compteurs["reseau"] == _avant["reseau"] + 1
            _attend_bloque(_sp.Popen, ["/usr/bin/true"])
            assert _compteurs["sousprocessus"] == _avant["sousprocessus"] + 1
            _attend_bloque(os.system, "/usr/bin/true")
            assert _compteurs["systeme"] == _avant["systeme"] + 1
            _attend_bloque(os.environ.__getitem__, "cle-test-b04")
            assert _compteurs["environ"] >= _avant["environ"] + 1
            _attend_bloque(importlib.import_module, "sqlite3")
            assert _compteurs["import_db"] >= _avant["import_db"] + 1
            _attend_bloque(importlib.import_module, "pixs.core")
            assert _compteurs["import_db"] >= _avant["import_db"] + 2

            # Imports applicatifs sous garde écriture/DB/Core, lecture source permise.
            from pixs.backend import bulk_private_object_reader as lecteur
            from pixs.backend import bulk_trusted_ports as ports
            from unit.test_bulk_execution_values import _valid_policy
            from unit.test_bulk_trusted_ports import _Authority, _GovernanceResolve3, _kwargs, _resolved_response

            # Après imports, activer aussi garde lecture puis remettre compteurs à zéro.
            _lecture_bloquee["actif"] = True
            for _cle in _compteurs:
                _compteurs[_cle] = 0
            # Contrôles positifs lecture/écriture/environnement après activation.
            _attend_bloque(builtins.open, sys.executable, "rb")
            assert _compteurs["lecture"] == 1
            _attend_bloque(io.open, sys.executable, "rb")
            assert _compteurs["lecture"] == 2
            _attend_bloque(builtins.open, "fichier-inexistant-b04.tmp", "wb")
            assert _compteurs["ecriture"] == 1
            _attend_bloque(os.environ.get, "cle-test-b04")
            assert _compteurs["environ"] == 1
            _attend_bloque(os.getenv, "cle-test-b04")
            assert _compteurs["environ"] == 2
            _attend_bloque(importlib.import_module, "sqlite3")
            _attend_bloque(importlib.import_module, "pixs.core")
            for _cle in _compteurs:
                _compteurs[_cle] = 0

            class _Iterateur:
                def __init__(self, morceaux):
                    self._morceaux = list(morceaux)
                    self.ferme = False
                async def __anext__(self):
                    if not self._morceaux:
                        raise StopAsyncIteration
                    return self._morceaux.pop(0)
                async def aclose(self):
                    self.ferme = True

            class _Fournisseur:
                def __init__(self, meta, morceaux):
                    self.metadata = dict(meta)
                    self._morceaux = list(morceaux)
                    self.stat_appels = 0
                    self.iter_appels = 0
                    self.dernier = None
                async def stat_private(self, contexte, objet, version):
                    self.stat_appels += 1
                    return dict(self.metadata)
                async def iter_bytes(self, contexte, objet, version):
                    self.iter_appels += 1
                    it = _Iterateur(list(self._morceaux))
                    self.dernier = it
                    return it

            class _Resolveur:
                def __init__(self, fourn):
                    self.fourn = fourn
                    self.qualify_appels = 0
                async def qualify(self, contexte, objet, version):
                    self.qualify_appels += 1
                    b = lecteur._make_qualified_storage_binding(provider=self.fourn, object_reference=objet, version_reference=version, provider_reference="provider-test")
                    assert b is not None
                    return b

            def _compose(autorite=None, reponse=None):
                aut = autorite if autorite is not None else _Authority()
                gov = _GovernanceResolve3(response=reponse)
                kw = _kwargs(authority=aut)
                kw["governance_adapter"] = gov
                bundle = ports.compose_bulk_trusted_ports(**kw)
                assert isinstance(bundle, ports._BulkTrustedPorts)
                if reponse is None:
                    gov.response = _resolved_response()
                return bundle, gov, aut

            async def _corps():
                donnees = b"entree privee synthetique\n"
                debut = datetime.now(timezone.utc)
                vraie = {"object_reference": "object-test", "version_reference": "version-test", "tenant_reference": "tenant-test", "scope_reference": None, "classification_reference": "classification-test", "size_bytes": len(donnees), "sha256": hashlib.sha256(donnees).hexdigest(), "media_type": "text/csv", "is_private": True, "expires_at": debut + timedelta(hours=1), "retention_policy_reference": "retention-test"}
                assert len(vraie) == 11
                pol = _valid_policy()
                ech = debut + timedelta(seconds=60)
                fourn = _Fournisseur(dict(vraie), [donnees])
                res = _Resolveur(fourn)
                bundle, gov, _ = _compose()
                assert len(gov.response.keys()) == 6
                args = {"trusted_ports": bundle, "server_context": object(), "operation_reference": "operation-test", "expected_metadata": dict(vraie), "policy_reference": "policy-test", "policy_version": "1.0.0", "storage_resolver": res, "expected_policy": dict(pol), "deadline": ech, "now": debut, "cancel_event": asyncio.Event()}
                bilan, diags = await lecteur.read_private_object_once(**args)
                assert diags == [], diags
                assert bilan.complete
                assert bilan.accepted_size == len(donnees)
                assert bilan.sha256 == hashlib.sha256(donnees).hexdigest()
                assert res.qualify_appels == 1
                assert fourn.stat_appels == 2
                assert fourn.iter_appels == 1
                assert fourn.dernier.ferme
                assert len(gov.calls) == 1
                _, contrat, refs = gov.calls[0]
                assert len(contrat.keys()) == 11
                assert refs == ("policy-test", "1.0.0")
                assert "entree" not in repr(bilan)
                aut = _Authority({"decision": "DENY", "resolved_context": None})
                bundle2, _, _ = _compose(autorite=aut)
                fourn2 = _Fournisseur(dict(vraie), [donnees])
                res2 = _Resolveur(fourn2)
                args2 = dict(args, trusted_ports=bundle2, expected_metadata=dict(vraie), storage_resolver=res2, cancel_event=asyncio.Event())
                b2, d2 = await lecteur.read_private_object_once(**args2)
                assert b2 is None and d2
                assert res2.qualify_appels == 0
                assert fourn2.stat_appels == 0 and fourn2.iter_appels == 0
                faux_sha = "a" * 64
                assert faux_sha != hashlib.sha256(donnees).hexdigest()
                meta_fausse = dict(vraie, sha256=faux_sha)
                fourn3 = _Fournisseur(dict(meta_fausse), [donnees])
                res3 = _Resolveur(fourn3)
                bundle3, _, _ = _compose()
                args3 = dict(args, trusted_ports=bundle3, expected_metadata=dict(meta_fausse), storage_resolver=res3, cancel_event=asyncio.Event())
                b3, d3 = await lecteur.read_private_object_once(**args3)
                assert b3 is None and d3
                assert fourn3.stat_appels == 2 and fourn3.iter_appels == 1
                assert fourn3.dernier.ferme
                for _m in ("sqlite3", "psycopg", "psycopg2", "django", "pixs.core"):
                    assert _m not in sys.modules, _m
                assert all(v == 0 for v in _compteurs.values()), _compteurs
                print("intégration fraîche B04 mémoire OK")
                print("compteurs zéros applicatifs confirmés")
                print("étapes succès refus-autorité refus-intégrité validées")

            _boucle.run_until_complete(_corps())
        finally:
            sys.meta_path.remove(_garde)
finally:
    _boucle.close()
'''


class IntegrationFraicheB04Tests(unittest.TestCase):
    def test_fraiche_memoire_b04(self):
        racine = Path(__file__).resolve().parents[2]
        env = {
            "PATH": "/usr/bin:/bin",
            "PYTHONPATH": str(racine / "src") + ":" + str(racine / "tests"),
            "PYTHONDONTWRITEBYTECODE": "1",
            "LC_ALL": "C.UTF-8",
        }
        proc = None
        try:
            proc = subprocess.Popen(
                [sys.executable, "-B", "-c", _CHILD],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
            )
            try:
                sortie, erreur = proc.communicate(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
                sortie, erreur = proc.communicate()
                self.fail("délai processus frais dépassé")
            self.assertEqual(proc.returncode, 0, msg=erreur)
            self.assertIn("intégration fraîche B04 mémoire OK", sortie)
            self.assertIn("compteurs zéros applicatifs confirmés", sortie)
        finally:
            if proc is not None and proc.poll() is None:
                proc.kill()
                try:
                    proc.communicate(timeout=5)
                except Exception:
                    pass


if __name__ == "__main__":
    unittest.main()
