"""Tests unitaires des diagnostics de composition typés (tâche 3.4).

Chaque classe d'échec normée (kernel : erreur explicite et diagnostiquable ;
modules : diagnostic nommant le champ, le cycle et l'ambiguïté ; providers :
diagnostic d'ambiguïté ; secrets-providers : aucune valeur sensible) doit
produire un ``Diagnostic`` portant l'étape, l'élément en cause et la contrainte
violée, avec un rendu texte identique aux chaînes émises en 2.x–3.3.

Fixtures synthétiques stdlib ``unittest``, sans secret réel ni donnée de
production : la « valeur sensible » embarquée est un placeholder documentaire
AWS, utilisée uniquement pour prouver que le diagnostic ne la reproduit pas.
"""

import unittest

from pixs.kernel.composition import compose, resolve
from pixs.kernel.diagnostics import RESOLVE, VALIDATE, Diagnostic
from pixs.kernel.manifest.models import ComponentManifest

BASE_TOML = """
schema_version = "1"
id = "acme.app"
type = "MODULE"
version = "1.0.0"
"""

MISSING_TYPE_TOML = """
schema_version = "1"
id = "acme.app"
version = "1.0.0"
"""

WRONG_ID_TYPE_TOML = """
schema_version = "1"
id = 42
type = "MODULE"
version = "1.0.0"
"""

BAD_TYPE_TOML = """
schema_version = "1"
id = "acme.app"
type = "APPLICATION"
version = "1.0.0"
"""

BAD_VERSION_TOML = """
schema_version = "1"
id = "acme.app"
type = "MODULE"
version = "1.0"
"""

UNKNOWN_SCHEMA_TOML = """
schema_version = "2"
id = "acme.app"
type = "MODULE"
version = "1.0.0"
"""

SECRET_TOML = """
schema_version = "1"
id = "acme.app"
type = "MODULE"
version = "1.0.0"
name = "AKIAIOSFODNN7EXAMPLE"
"""

EXECUTABLE_TOML = """
schema_version = "1"
id = "acme.app"
type = "MODULE"
version = "1.0.0"
name = "${DEPLOIEMENT_TOKEN}"
"""

USURPER_TOML = """
schema_version = "1"
id = "pixs.usurpe"
type = "MODULE"
version = "1.0.0"
"""

DUP_TOML = """
schema_version = "1"
id = "acme.dup"
type = "MODULE"
version = "1.0.0"
"""


def _manifest(
    component_id: str,
    dependency_components: tuple[str, ...] = (),
    dependency_capabilities: tuple[str, ...] = (),
    provided_capabilities: tuple[str, ...] = (),
) -> ComponentManifest:
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version="1.0.0",
        dependency_components=dependency_components,
        dependency_capabilities=dependency_capabilities,
        provided_capabilities=provided_capabilities,
    )


AMBIGUITY_COMPOSITION = (
    _manifest("t.web", dependency_capabilities=("audit >=1.0.0",)),
    _manifest("t.p1", provided_capabilities=("audit",)),
    _manifest("t.p2", provided_capabilities=("audit",)),
)


def _un_seul(diagnostics, element):
    """Retourne l'unique diagnostic d'une classe pour l'élément attendu."""
    matches = [d for d in diagnostics if d.element == element]
    assert len(matches) == 1, (
        f"diagnostic attendu exactement un element={element!r} : {diagnostics}"
    )
    return matches[0]


class TestModeleDiagnostic(unittest.TestCase):
    def test_rendu_texte_herite(self) -> None:
        diagnostic = Diagnostic(
            step=VALIDATE, element="id", constraint="chaîne attendue", message="m"
        )
        self.assertIsInstance(diagnostic, str)
        self.assertEqual(str(diagnostic), "id : m")
        self.assertEqual(diagnostic, "id : m")

    def test_from_legacy_decoupe_au_premier_separateur(self) -> None:
        diagnostic = Diagnostic.from_legacy(VALIDATE, "a : b : c")
        self.assertEqual(diagnostic.element, "a")
        self.assertEqual(diagnostic.constraint, "b : c")
        self.assertEqual(str(diagnostic), "a : b : c")

    def test_from_legacy_repli_sans_separateur(self) -> None:
        diagnostic = Diagnostic.from_legacy(VALIDATE, "texte brut")
        self.assertEqual(diagnostic.element, "manifest")
        self.assertEqual(diagnostic.constraint, "texte brut")
        self.assertEqual(str(diagnostic), "manifest : texte brut")

    def test_etape_inconnue_refusee(self) -> None:
        with self.assertRaises(ValueError):
            Diagnostic(step="activate", element="a", constraint="b", message="c")
        with self.assertRaises(ValueError):
            Diagnostic.from_legacy("inconnue", "a : b")

    def test_champs_vides_refuses(self) -> None:
        with self.assertRaises(ValueError):
            Diagnostic(step=VALIDATE, element="", constraint="b", message="c")
        with self.assertRaises(ValueError):
            Diagnostic(step=VALIDATE, element="a", constraint="", message="c")
        with self.assertRaises(ValueError):
            Diagnostic(step=VALIDATE, element="a", constraint="b", message="")

    def test_immutabilite_des_attributs(self) -> None:
        diagnostic = Diagnostic.from_legacy(RESOLVE, "a : b")
        with self.assertRaises(AttributeError):
            diagnostic.step = VALIDATE
        with self.assertRaises(AttributeError):
            diagnostic.element = "autre"
        with self.assertRaises(AttributeError):
            diagnostic.nouvel_attribut = 1


class TestDiagnosticsValidate(unittest.TestCase):
    def test_champ_obligatoire_manquant(self) -> None:
        result = compose([MISSING_TYPE_TOML])
        self.assertEqual(result.stage, "validate")
        diagnostic = _un_seul(result.diagnostics, "type")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.constraint, "champ obligatoire manquant")
        self.assertEqual(str(diagnostic), "type : champ obligatoire manquant")

    def test_type_de_champ_fautif(self) -> None:
        result = compose([WRONG_ID_TYPE_TOML])
        diagnostic = _un_seul(result.diagnostics, "id")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.constraint, "une chaîne est attendue")

    def test_type_hors_enumeration(self) -> None:
        result = compose([BAD_TYPE_TOML])
        diagnostic = _un_seul(result.diagnostics, "type")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertIn("valeur hors des six types attendue", diagnostic.constraint)

    def test_version_non_semver(self) -> None:
        result = compose([BAD_VERSION_TOML])
        diagnostic = _un_seul(result.diagnostics, "version")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(
            diagnostic.constraint, "SemVer attendu (majeure.mineure.correctif)"
        )

    def test_version_de_schema_inconnue(self) -> None:
        result = compose([UNKNOWN_SCHEMA_TOML])
        matches = [
            d
            for d in result.diagnostics
            if "version de schéma non supportée" in str(d) and "'2'" in str(d)
        ]
        self.assertEqual(len(matches), 1, f"diagnostic de schéma absent : {result.diagnostics}")
        diagnostic = matches[0]
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertTrue(diagnostic.element)
        self.assertTrue(diagnostic.constraint)

    def test_secret_embarque_refuse_sans_reproduction(self) -> None:
        result = compose([SECRET_TOML])
        diagnostic = _un_seul(result.diagnostics, "name")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertIn("secret embarqué refusé", diagnostic.constraint)
        rendu = "".join(str(d) for d in result.diagnostics)
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", rendu)

    def test_expression_executable_refusee_sans_reproduction(self) -> None:
        result = compose([EXECUTABLE_TOML])
        diagnostic = _un_seul(result.diagnostics, "name")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertIn("expression exécutable refusée", diagnostic.constraint)
        rendu = "".join(str(d) for d in result.diagnostics)
        self.assertNotIn("DEPLOIEMENT_TOKEN", rendu)

    def test_namespace_reserve(self) -> None:
        result = compose([USURPER_TOML, BASE_TOML])
        diagnostic = _un_seul(result.diagnostics, "id")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertIn("namespace réservé", diagnostic.constraint)

    def test_collision_d_identifiants(self) -> None:
        result = compose([DUP_TOML, DUP_TOML])
        diagnostic = _un_seul(result.diagnostics, "id 'acme.dup'")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertIn("identifiant dupliqué", diagnostic.constraint)

    def test_entree_non_texte(self) -> None:
        result = compose([42])
        diagnostic = _un_seul(result.diagnostics, "manifestes[0]")
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.constraint, "un texte TOML est attendu")


class TestDiagnosticsResolve(unittest.TestCase):
    def test_composant_requis_absent(self) -> None:
        _edges, _order, diagnostics = resolve(
            (_manifest("acme.orphan", dependency_components=("acme.absent >=1.0.0",)),)
        )
        diagnostic = _un_seul(diagnostics, "dependencies.components")
        self.assertEqual(diagnostic.step, RESOLVE)
        self.assertEqual(
            diagnostic.constraint, "composant requis présent dans la composition"
        )
        self.assertEqual(
            str(diagnostic),
            "dependencies.components : composant requis absent de la "
            "composition ('acme.absent')",
        )

    def test_fournisseur_configure_hors_candidats(self) -> None:
        _edges, _order, diagnostics = resolve(
            AMBIGUITY_COMPOSITION, configured_providers={"audit": "t.absent"}
        )
        diagnostic = _un_seul(diagnostics, "dependencies.capabilities")
        self.assertEqual(diagnostic.step, RESOLVE)
        self.assertEqual(
            diagnostic.constraint, "fournisseur configuré parmi les candidats"
        )
        self.assertIn("'audit'", str(diagnostic))

    def test_ambiguite_de_fournisseurs(self) -> None:
        _edges, _order, diagnostics = resolve(AMBIGUITY_COMPOSITION)
        diagnostic = _un_seul(diagnostics, "dependencies.capabilities")
        self.assertEqual(diagnostic.step, RESOLVE)
        self.assertEqual(diagnostic.constraint, "fournisseur unique ou configuré")
        self.assertEqual(
            str(diagnostic),
            "dependencies.capabilities : ambiguïté de fournisseur pour la "
            "capacité ('audit') entre : 't.p1', 't.p2'",
        )

    def test_capacite_sans_fournisseur(self) -> None:
        _edges, _order, diagnostics = resolve(
            (_manifest("t.client", dependency_capabilities=("audit",)),)
        )
        diagnostic = _un_seul(diagnostics, "dependencies.capabilities")
        self.assertEqual(diagnostic.step, RESOLVE)
        self.assertEqual(diagnostic.constraint, "capacité requise fournie")
        self.assertIn("'audit'", str(diagnostic))

    def test_cycle_identifie_element_et_contrainte(self) -> None:
        _edges, _order, diagnostics = resolve(
            (
                _manifest("t.a", dependency_components=("t.b",)),
                _manifest("t.b", dependency_components=("t.a",)),
            )
        )
        diagnostic = _un_seul(diagnostics, "dependencies")
        self.assertEqual(diagnostic.step, RESOLVE)
        self.assertEqual(diagnostic.constraint, "graphe de dépendances acyclique")
        self.assertIn("'t.a'", str(diagnostic))
        self.assertIn("'t.b'", str(diagnostic))

    def test_tous_les_diagnostics_sont_tipes(self) -> None:
        for diagnostics in (
            compose([MISSING_TYPE_TOML]).diagnostics,
            resolve(AMBIGUITY_COMPOSITION)[2],
            resolve(
                (_manifest("t.client", dependency_capabilities=("audit",)),)
            )[2],
        ):
            self.assertTrue(diagnostics)
            for diagnostic in diagnostics:
                self.assertIsInstance(diagnostic, Diagnostic)
                self.assertIn(diagnostic.step, {VALIDATE, RESOLVE})
                self.assertTrue(diagnostic.element)
                self.assertTrue(diagnostic.constraint)

    def test_diagnostics_identiques_entre_deux_executions(self) -> None:
        first = compose([BAD_VERSION_TOML])
        second = compose([BAD_VERSION_TOML])
        self.assertEqual(first.diagnostics, second.diagnostics)


if __name__ == "__main__":
    unittest.main()
