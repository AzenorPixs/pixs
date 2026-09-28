"""Tests d'intégration des hooks de cycle de vie ordonnés (tâche 5.2, spec lifecycle).

Garantie normative contrôlée : à composants, versions et configuration
identiques, deux exécutions complètes (pipeline puis hooks) produisent un
ordre de chargement et une suite de hooks strictement identiques, sans
dépendre du système de fichiers ni de l'ordre de construction des mappings.
Fixtures synthétiques sans secret ni donnée de production, sur le motif de
``test_composition_pipeline`` (acme.app dépend de pixs.core et acme.lib).
"""

import unittest

from pixs.kernel.composition import compose
from pixs.kernel.lifecycle.hooks import HOOK_POINTS, HookCall, run_hooks

APP_TOML = """
schema_version = "1"
id = "acme.app"
type = "MODULE"
version = "1.0.0"

[dependencies]
components = ["pixs.core >=1.0.0 <2.0.0", "acme.lib"]
"""

CORE_TOML = """
schema_version = "1"
id = "pixs.core"
type = "KERNEL"
version = "1.0.0"
"""

LIB_TOML = """
schema_version = "1"
id = "acme.lib"
type = "MODULE"
version = "0.1.0"
"""

VALID_TEXTS = [APP_TOML, CORE_TOML, LIB_TOML]
OFFICIAL_IDS = ("pixs.core",)


def _build_hooks(
    log: list,
    component_ids,
    hook_names=HOOK_POINTS,
) -> dict:
    """Construit des tables de hooks hôtes qui tracent leurs appels dans ``log``."""
    return {
        component_id: {
            hook_name: (
                lambda component_id=component_id, hook_name=hook_name: log.append(
                    (component_id, hook_name)
                )
            )
            for hook_name in hook_names
        }
        for component_id in component_ids
    }


class TestDoubleExecutionReproductible(unittest.TestCase):
    def test_double_execution_complete_ordres_identiques(self) -> None:
        first = compose(VALID_TEXTS, official_ids=OFFICIAL_IDS)
        second = compose(VALID_TEXTS, official_ids=OFFICIAL_IDS)
        self.assertEqual(first, second)
        self.assertTrue(first.activated)
        self.assertEqual(first.order, second.order)

        log_first: list = []
        log_second: list = []
        calls_first, diagnostics_first = run_hooks(
            first.order, _build_hooks(log_first, first.order)
        )
        calls_second, diagnostics_second = run_hooks(
            second.order, _build_hooks(log_second, second.order)
        )
        self.assertEqual(diagnostics_first, ())
        self.assertEqual(diagnostics_second, ())
        self.assertEqual(calls_first, calls_second)
        self.assertEqual(log_first, log_second)
        self.assertEqual(
            [(call.component_id, call.hook) for call in calls_first], log_first
        )


class TestOrdreDuGraphe(unittest.TestCase):
    def test_suite_des_composants_egale_ordre_resolu(self) -> None:
        result = compose(VALID_TEXTS, official_ids=OFFICIAL_IDS)
        log: list = []
        calls, diagnostics = run_hooks(result.order, _build_hooks(log, result.order))
        self.assertEqual(diagnostics, ())
        distinct: list = []
        for call in calls:
            if not distinct or distinct[-1] != call.component_id:
                distinct.append(call.component_id)
        self.assertEqual(tuple(distinct), result.order)

    def test_hooks_par_composant_dans_l_ordre_des_points(self) -> None:
        result = compose(VALID_TEXTS, official_ids=OFFICIAL_IDS)
        log: list = []
        calls, diagnostics = run_hooks(result.order, _build_hooks(log, result.order))
        self.assertEqual(diagnostics, ())
        self.assertEqual(
            calls,
            tuple(
                HookCall(component_id, hook_name)
                for component_id in result.order
                for hook_name in HOOK_POINTS
            ),
        )


class TestInvarianceDInsertion(unittest.TestCase):
    def test_constructions_divergentes_meme_sequence(self) -> None:
        result = compose(VALID_TEXTS, official_ids=OFFICIAL_IDS)
        log_canonique: list = []
        calls_canoniques, _ = run_hooks(
            result.order, _build_hooks(log_canonique, result.order)
        )
        log_inversé: list = []
        calls_inversés, _ = run_hooks(
            result.order,
            _build_hooks(
                log_inversé,
                tuple(reversed(result.order)),
                hook_names=tuple(reversed(HOOK_POINTS)),
            ),
        )
        self.assertEqual(calls_canoniques, calls_inversés)
        self.assertEqual(log_canonique, log_inversé)


class TestMondeClosSansEffet(unittest.TestCase):
    def test_composant_inconnu_refuse_aucun_callback(self) -> None:
        result = compose(VALID_TEXTS, official_ids=OFFICIAL_IDS)
        log: list = []
        hooks = _build_hooks(log, result.order)
        hooks["acme.ghost"] = {"install": lambda: log.append(("acme.ghost", "install"))}
        calls, diagnostics = run_hooks(result.order, hooks)
        self.assertEqual(calls, ())
        self.assertEqual(log, [])
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].step, "validate")
        self.assertIn("acme.ghost", diagnostics[0].element)
        self.assertIn("acme.ghost", diagnostics[0].message)

    def test_hook_hors_ensemble_refuse_aucun_callback(self) -> None:
        result = compose(VALID_TEXTS, official_ids=OFFICIAL_IDS)
        log: list = []
        hooks = _build_hooks(log, result.order)
        hooks["acme.lib"] = {
            "install": lambda: log.append(("acme.lib", "install")),
            "disable": lambda: log.append(("acme.lib", "disable")),
        }
        calls, diagnostics = run_hooks(result.order, hooks)
        self.assertEqual(calls, ())
        self.assertEqual(log, [])
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].step, "validate")
        self.assertIn("acme.lib.disable", diagnostics[0].element)
        self.assertIn("disable", diagnostics[0].message)


if __name__ == "__main__":
    unittest.main()
