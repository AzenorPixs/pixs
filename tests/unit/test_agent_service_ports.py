"""Unittest pure ports Agent 2.1d : profil serveur explicite seul."""
import unittest
from pixs.agent.contracts import AgentParamSpec, AllowedCatalogEntry
from pixs.agent.ports import PURPOSES, AgentOperationalProfile, AgentPortsError


def _spec(name="p1"):
    return AgentParamSpec(name=name, kind="str", max_len=16, int_min=None, int_max=None, required=True)


def _entry(op="pa.apply", ver="1.0.0"):
    return AllowedCatalogEntry(operation=op, version=ver, params=(_spec(),))


def _mapping():
    return (("desired.persist", ("core.a",)), ("observation.append", ("core.b",)), ("confirmation.confirm", ("core.c",)), ("state.query", ("core.d",)))


def _profile(**kw):
    base = dict(allowed_catalog=(_entry(),), allowed_core_actions=_mapping(), max_id_len=64, max_doc_len=256, max_ids=8, max_params=8, max_observation_age_seconds=60)
    base.update(kw)
    return AgentOperationalProfile(**base)


def _code(fn):
    try:
        fn()
    except AgentPortsError as e:
        return e.code
    return None


class PortsProfileTest(unittest.TestCase):
    def test_purposes_exact(self):
        self.assertEqual(PURPOSES, ("desired.persist", "observation.append", "confirmation.confirm", "state.query"))
    def test_profil_valide(self):
        self.assertEqual(_code(_profile), None)
    def test_bornes_bool_refuse(self):
        self.assertEqual(_code(lambda: _profile(max_id_len=True)), "BORNE_INVALIDE")
    def test_bornes_zero_refuse(self):
        self.assertEqual(_code(lambda: _profile(max_params=0)), "BORNE_INVALIDE")
    def test_catalogue_vide_refuse(self):
        self.assertEqual(_code(lambda: _profile(allowed_catalog=())), "CATALOGUE_INVALIDE")
    def test_version_invalide(self):
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(_entry(ver="x"),))), "CATALOGUE_VERSION_INVALIDE")
    def test_doublon_operation_version(self):
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(_entry(), _entry()))), "CATALOGUE_DOUBLON")
    def test_doublon_parametre(self):
        dup = AllowedCatalogEntry(operation="pa.apply", version="1.0.0", params=(_spec("p1"), _spec("p1")))
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(dup,))), "CATALOGUE_PARAMETRE_DOUBLON")
    def test_spec_invalide(self):
        bad = AgentParamSpec(name="p1", kind="str", max_len=None, int_min=None, int_max=None, required=True)
        ent = AllowedCatalogEntry(operation="pa.apply", version="1.0.0", params=(bad,))
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(ent,))), "CATALOGUE_PARAMETRE_INVALIDE")
    def test_fausse_classe_refusee(self):
        class Faux:
            operation = "pa.apply"
            version = "1.0.0"
            params = ()
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(Faux(),))), "CATALOGUE_INVALIDE")
    def test_sous_classe_refusee(self):
        class Sous(AllowedCatalogEntry):
            pass
        e = Sous(operation="pa.apply", version="1.0.0", params=(_spec(),))
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(e,))), "CATALOGUE_INVALIDE")
    def test_nul_refuse(self):
        ent = AllowedCatalogEntry(operation="pa" + chr(0) + "x", version="1.0.0", params=(_spec(),))
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(ent,))), "CATALOGUE_INVALIDE")
    def test_surrogate_refuse(self):
        ent = AllowedCatalogEntry(operation="pa" + chr(55296), version="1.0.0", params=(_spec(),))
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(ent,))), "CATALOGUE_INVALIDE")
    def test_mapping_incomplet_refuse(self):
        m = (("desired.persist", ("core.a",)), ("observation.append", ("core.b",)), ("confirmation.confirm", ("core.c",)))
        self.assertEqual(_code(lambda: _profile(allowed_core_actions=m)), "ACTIONS_CORE_INCOMPLETES")
    def test_mapping_purpose_duplique(self):
        m = (("desired.persist", ("core.a",)), ("desired.persist", ("core.b",)), ("confirmation.confirm", ("core.c",)), ("state.query", ("core.d",)))
        self.assertEqual(_code(lambda: _profile(allowed_core_actions=m)), "INTENTION_INVALIDE")
    def test_mapping_action_vide(self):
        m = (("desired.persist", ()), ("observation.append", ("core.b",)), ("confirmation.confirm", ("core.c",)), ("state.query", ("core.d",)))
        self.assertEqual(_code(lambda: _profile(allowed_core_actions=m)), "ACTIONS_CORE_INVALIDES")
    def test_mapping_action_doublon(self):
        m = (("desired.persist", ("core.a", "core.a")), ("observation.append", ("core.b",)), ("confirmation.confirm", ("core.c",)), ("state.query", ("core.d",)))
        self.assertEqual(_code(lambda: _profile(allowed_core_actions=m)), "ACTION_CORE_INVALIDE")
    def test_valeurs_serveur_explicites(self):
        m = (("desired.persist", ("srv.desired.v1",)), ("observation.append", ("srv.obs.v1",)), ("confirmation.confirm", ("srv.conf.v1",)), ("state.query", ("srv.query.v1",)))
        self.assertEqual(_code(lambda: _profile(allowed_core_actions=m)), None)
    def test_repr_confidentiel(self):
        p = _profile()
        self.assertIn("<confidentiel>", repr(p))
        self.assertIn("<confidentiel>", str(p))
        self.assertNotIn("pa.apply", repr(p))
    def test_champs_erreur(self):
        try:
            _profile(max_ids=0)
        except AgentPortsError as e:
            self.assertEqual(e.element, "agent_ports")
            self.assertEqual(e.step, "validate_server_port")
        else:
            self.fail("refus attendu")
    def test_import_frontiere_processus_frais(self):
        import subprocess
        import sys
        script = """import sys, importlib.abc
sys.path.insert(0, "src")
class Guard(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in ("django", "psycopg", "socket", "requests") or fullname.startswith(("pixs.pzt", "pixs.pa.", "urllib.request", "urllib3", "http.client")):
            raise AssertionError("import interdit")
sys.meta_path.insert(0, Guard())
import pixs.agent.ports
print("IMPORT_BOUNDARY_OK")
"""
        result = subprocess.run([sys.executable, "-B", "-c", script], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "IMPORT_BOUNDARY_OK")

    def test_preversion_et_parametres_explicites(self):
        self.assertIsInstance(_profile(allowed_catalog=(_entry(ver="1.0.0-rc.1+test"),)), AgentOperationalProfile)

    def test_types_hostiles_sans_conversion(self):
        class Hostile:
            def __bool__(self):
                raise AssertionError("conversion interdite")
            def __eq__(self, other):
                raise AssertionError("comparaison interdite")
            def __str__(self):
                raise AssertionError("conversion interdite")
        for field in ("max_id_len", "max_doc_len", "max_ids", "max_params", "max_observation_age_seconds"):
            for value in (True, False, 0, -1, None, 1.5, "8", Hostile()):
                with self.subTest(field=field, kind=type(value).__name__):
                    self.assertEqual(_code(lambda: _profile(**{field: value})), "BORNE_INVALIDE")

    def test_usurpation_nom_et_action_invalide(self):
        Faux = type("AllowedCatalogEntry", (), {})
        self.assertEqual(_code(lambda: _profile(allowed_catalog=(Faux(),))), "CATALOGUE_INVALIDE")
        for invalid in ("", "x" + chr(0), "x" + chr(55296), True):
            mapping = tuple((purpose, (invalid,)) for purpose in PURPOSES)
            self.assertEqual(_code(lambda: _profile(allowed_core_actions=mapping)), "ACTION_CORE_INVALIDE")


if __name__ == "__main__":
    unittest.main()
