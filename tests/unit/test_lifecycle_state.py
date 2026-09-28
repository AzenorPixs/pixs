"""Tests unitaires du cycle de vie mécanique (tâche 5.1, spec lifecycle).

Contrôles : les cinq dimensions sont littéralement séparées et leurs
implications normatives sont vérifiées (un activé-sans-installation, un
configuré-sans-installation, un prêt-incohérent sont refusés) ; les opérations
mécaniques sont idempotentes, ordonnées et diagnostiquées ; la désactivation
conserve les données ; ``migrate``, ``upgrade``, ``uninstall``, ``purge`` sont
refusés explicitement (hors périmètre), jamais silencieusement.
"""

import unittest

from pixs.kernel.diagnostics import VALIDATE
from pixs.kernel.lifecycle.state import (
    LIFECYCLE_OPERATIONS,
    OUT_OF_SCOPE_OPERATIONS,
    LifecycleState,
    apply_operation,
    validate_lifecycle_state,
)


class TestDimensionsIndependantes(unittest.TestCase):
    def test_attente_vide_valide(self) -> None:
        self.assertEqual(validate_lifecycle_state(LifecycleState()), ())

    def test_active_sans_installe_refuse(self) -> None:
        refusals = validate_lifecycle_state(
            LifecycleState(enabled=True, ready=False)
        )
        self.assertTrue(
            any(
                diagnostic.step == VALIDATE
                and diagnostic.element == "lifecycle.enabled"
                for diagnostic in refusals
            ),
            f"aucun diagnostic d'activation sans installation : {refusals}",
        )

    def test_configure_sans_installe_refuse(self) -> None:
        refusals = validate_lifecycle_state(
            LifecycleState(configured=True)
        )
        self.assertTrue(
            any(
                diagnostic.element == "lifecycle.configured"
                for diagnostic in refusals
            ),
            f"aucun diagnostic de configuration sans installation : {refusals}",
        )

    def test_pret_incoherent_refuse(self) -> None:
        refusals = validate_lifecycle_state(LifecycleState(ready=True))
        self.assertTrue(
            any(
                diagnostic.element == "lifecycle.ready"
                for diagnostic in refusals
            ),
            f"aucun diagnostic d'état prêt incohérent : {refusals}",
        )

    def test_pret_complet_valide(self) -> None:
        etat = LifecycleState(
            installed=True,
            enabled=True,
            configured=True,
            healthy=True,
            ready=True,
        )
        self.assertEqual(validate_lifecycle_state(etat), ())

    def test_installe_desactive_non_confondu_avec_pret(self) -> None:
        desactive = LifecycleState(installed=True, enabled=False)
        pret = LifecycleState(
            installed=True,
            enabled=True,
            configured=True,
            healthy=True,
            ready=True,
        )
        self.assertNotEqual(desactive, pret)
        self.assertNotEqual(pret, desactive)
        self.assertEqual(validate_lifecycle_state(desactive), ())

    def test_dimension_non_booleenne_refusee(self) -> None:
        refusals = validate_lifecycle_state(LifecycleState(installed=1))
        self.assertTrue(
            any(
                "installed" in diagnostic.element
                and "non booléenne" in diagnostic.message
                for diagnostic in refusals
            ),
            f"aucun diagnostic de dimension non booléenne : {refusals}",
        )


class TestOperationsRefuseesExplicitement(unittest.TestCase):
    def test_monde_clos_des_operations(self) -> None:
        self.assertEqual(len(LIFECYCLE_OPERATIONS), 11)
        self.assertTrue(
            OUT_OF_SCOPE_OPERATIONS.issubset(set(LIFECYCLE_OPERATIONS))
        )

    def test_operations_hors_perimetre_refusees_sans_mutation(self) -> None:
        for operation in ("migrate", "upgrade", "uninstall", "purge"):
            with self.subTest(operation=operation):
                etat = LifecycleState()
                apres, refusals = apply_operation(etat, operation)
                self.assertEqual(apres, etat)
                self.assertEqual(len(refusals), 1)
                self.assertEqual(refusals[0].step, VALIDATE)
                self.assertIn("hors périmètre", refusals[0].message)
                self.assertIn(operation, refusals[0].message)

    def test_operation_inconnue_refusee_sans_mutation(self) -> None:
        etat = LifecycleState(installed=True)
        apres, refusals = apply_operation(etat, "rencontre")
        self.assertEqual(apres, etat)
        self.assertEqual(len(refusals), 1)
        self.assertIn("inconnue", refusals[0].message)

    def test_refus_ne_reproduit_aucune_valeur(self) -> None:
        etat = LifecycleState(installed=True)
        _, refusals = apply_operation(etat, "rencontre")
        for diagnostic in refusals:
            self.assertNotIn("True", diagnostic.message)
            self.assertNotIn("False", diagnostic.message)


class TestTransitionsMechaniques(unittest.TestCase):
    def test_install_idempotent_et_valide(self) -> None:
        etat = LifecycleState()
        apres, refusals = apply_operation(etat, "install")
        self.assertEqual(refusals, ())
        self.assertTrue(apres.installed)
        self.assertFalse(apres.ready)
        self.assertEqual(validate_lifecycle_state(apres), ())
        # idempotence : une seconde application ne change rien
        rejeu, refusals_rejeu = apply_operation(apres, "install")
        self.assertEqual(rejeu, apres)
        self.assertEqual(refusals_rejeu, ())

    def test_enable_refuse_sans_install(self) -> None:
        etat = LifecycleState()
        apres, refusals = apply_operation(etat, "enable")
        self.assertEqual(apres, etat)
        self.assertEqual(len(refusals), 1)
        self.assertIn("antériorité", refusals[0].message)

    def test_enable_apres_install_ok(self) -> None:
        etat = LifecycleState(installed=True)
        apres, refusals = apply_operation(etat, "enable")
        self.assertEqual(refusals, ())
        self.assertTrue(apres.installed)
        self.assertTrue(apres.enabled)
        self.assertFalse(apres.ready)
        self.assertEqual(validate_lifecycle_state(apres), ())

    def test_configure_refuse_sans_install(self) -> None:
        etat = LifecycleState()
        _, refusals = apply_operation(etat, "configure")
        self.assertEqual(len(refusals), 1)
        self.assertIn("antériorité", refusals[0].message)

    def test_start_exige_install_active_et_configure(self) -> None:
        installe_active = LifecycleState(installed=True, enabled=True)
        _, refusals = apply_operation(installe_active, "start")
        self.assertEqual(len(refusals), 1)
        self.assertIn("démarrage", refusals[0].message)
        # après configure, start réussit et rend prêt
        configure, _ = apply_operation(installe_active, "configure")
        demarre, refusals = apply_operation(configure, "start")
        self.assertEqual(refusals, ())
        self.assertTrue(demarre.ready)
        self.assertTrue(demarre.healthy)
        self.assertEqual(validate_lifecycle_state(demarre), ())

    def test_disable_conserve_donnees_et_eteint_pret(self) -> None:
        pret = LifecycleState(
            installed=True,
            enabled=True,
            configured=True,
            healthy=True,
            ready=True,
        )
        desactive, refusals = apply_operation(pret, "disable")
        self.assertEqual(refusals, ())
        # désactivation sans perte : installé et configuré conservés
        self.assertTrue(desactive.installed)
        self.assertTrue(desactive.configured)
        # prêt, activé, sain éteints
        self.assertFalse(desactive.enabled)
        self.assertFalse(desactive.healthy)
        self.assertFalse(desactive.ready)
        self.assertNotEqual(desactive, pret)
        self.assertEqual(validate_lifecycle_state(desactive), ())

    def test_chaine_complete_deterministe(self) -> None:
        operations = (
            "discover",
            "validate",
            "install",
            "enable",
            "configure",
            "start",
        )
        etat_a = LifecycleState()
        etat_b = LifecycleState()
        refusals_a: list = []
        refusals_b: list = []
        for operation in operations:
            etat_a, refus_a = apply_operation(etat_a, operation)
            refusals_a.extend(refus_a)
            etat_b, refus_b = apply_operation(etat_b, operation)
            refusals_b.extend(refus_b)
        self.assertEqual(etat_a, etat_b)
        self.assertEqual(refusals_a, refusals_b)
        self.assertEqual(refusals_a, [])
        self.assertTrue(etat_a.ready)


if __name__ == "__main__":
    unittest.main()
