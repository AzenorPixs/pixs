"""Tests unitaires du tri topologique et de la détection de cycles (tâche 3.2)."""

import unittest

from pixs.kernel.composition import resolve
from pixs.kernel.manifest.models import ComponentManifest


def _manifest(
    component_id: str,
    dependency_components: tuple[str, ...] = (),
) -> ComponentManifest:
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version="1.0.0",
        dependency_components=dependency_components,
    )


CHAIN_A_TO_C = (
    _manifest("t.a", ("t.b",)),
    _manifest("t.b", ("t.c",)),
    _manifest("t.c"),
)


class TestTriTopologique(unittest.TestCase):
    def test_chaine_a_b_c_ordre_dependances_dabord(self) -> None:
        _edges, order, diagnostics = resolve(CHAIN_A_TO_C)
        self.assertEqual(diagnostics, ())
        self.assertEqual(order, ("t.c", "t.b", "t.a"))

    def test_double_execution_ordre_identique(self) -> None:
        first = resolve(CHAIN_A_TO_C)
        second = resolve(CHAIN_A_TO_C)
        self.assertEqual(first, second)

    def test_departage_par_identifiant_canonique(self) -> None:
        composition = (
            _manifest("t.z", ("t.x", "t.y")),
            _manifest("t.y"),
            _manifest("t.x"),
        )
        _edges, order, diagnostics = resolve(composition)
        self.assertEqual(diagnostics, ())
        self.assertEqual(order, ("t.x", "t.y", "t.z"))


class TestDetectionCycles(unittest.TestCase):
    def test_cycle_a_b_refuse_avec_membres_nommes(self) -> None:
        composition = (
            _manifest("t.a", ("t.b",)),
            _manifest("t.b", ("t.a",)),
        )
        _edges, order, diagnostics = resolve(composition)
        self.assertEqual(order, ())
        self.assertTrue(
            any(
                "cycle" in d and "'t.a'" in d and "'t.b'" in d
                for d in diagnostics
            ),
            f"aucun diagnostic ne nomme les membres du cycle : {diagnostics}",
        )

    def test_auto_cycle_refuse(self) -> None:
        composition = (_manifest("t.a", ("t.a",)),)
        _edges, order, diagnostics = resolve(composition)
        self.assertEqual(order, ())
        self.assertTrue(
            any("cycle" in d and "'t.a'" in d for d in diagnostics),
            f"aucun diagnostic ne nomme l'auto-cycle : {diagnostics}",
        )


class TestCibleAbsenteRegression(unittest.TestCase):
    def test_cible_absente_sans_ordre(self) -> None:
        composition = (_manifest("t.solo", ("t.absent >=1.0.0",)),)
        _edges, order, diagnostics = resolve(composition)
        self.assertEqual(order, ())
        self.assertTrue(
            any(
                "composant requis absent" in d and "'t.absent'" in d
                for d in diagnostics
            ),
            f"aucun diagnostic ne nomme la cible absente : {diagnostics}",
        )


class TestDependanceOptionnelleAbsente(unittest.TestCase):
    """Scénario dependencies « Optionnelle absente tolérée » (tâche 6.1).

    Une dépendance optionnelle (composant ou capacité) dont la cible est absente
    ne doit invalider ni la composition ni l'ordre de chargement : aucun
    diagnostic n'est émis et la cible n'entre jamais dans le graphe. Contraste
    avec la dépendance obligatoire absente, qui, elle, refuse
    (TestCibleAbsenteRegression).
    """

    def test_composant_optionnel_absent_composition_valide(self) -> None:
        app = ComponentManifest(
            schema_version="1",
            id="t.app",
            type="MODULE",
            version="1.0.0",
            optional_dependency_components=("t.ghost >=1.0.0",),
        )
        edges, order, diagnostics = resolve((app,))
        self.assertEqual(diagnostics, ())
        self.assertEqual(order, ("t.app",))
        self.assertNotIn(("t.app", "t.ghost"), edges)

    def test_capacite_optionnelle_absente_composition_valide(self) -> None:
        app = ComponentManifest(
            schema_version="1",
            id="t.app",
            type="MODULE",
            version="1.0.0",
            optional_dependency_capabilities=("audit >=1.0.0 <2.0.0",),
        )
        _edges, order, diagnostics = resolve((app,))
        self.assertEqual(diagnostics, ())
        self.assertEqual(order, ("t.app",))

    def test_optionnelle_absente_ordre_stable_entre_ordinnees(self) -> None:
        core = _manifest("t.core")
        app = ComponentManifest(
            schema_version="1",
            id="t.app",
            type="MODULE",
            version="1.0.0",
            dependency_components=("t.core",),
            optional_dependency_components=("t.ghost",),
        )
        first = resolve((app, core))
        second = resolve((core, app))
        self.assertEqual(first, second)
        _edges, order, diagnostics = first
        self.assertEqual(diagnostics, ())
        self.assertEqual(order, ("t.core", "t.app"))


if __name__ == "__main__":
    unittest.main()
