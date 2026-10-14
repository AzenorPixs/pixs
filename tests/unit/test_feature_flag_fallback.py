"""Tests unitaires de l'application déclarative du repli R3 (tâche 3.1).

Contrôlent le résultat figé à trois champs obligatoires, la fermeture des types
avant tout accès d'attribut, comparaison ou hachage, la matrice des politiques,
des usages et des causes, la préservation littérale de ``False`` et du jeton de
variante, le refus d'une référence héritée sans alias ni normalisation et
l'absence d'écho des diagnostics. Aucune horloge, E/S ni callback n'est lu ou
déclenché.
"""

from __future__ import annotations

import dataclasses
import unittest
from dataclasses import replace

from pixs.kernel.diagnostics import VALIDATE
from pixs.kernel.feature_flags import (
    FeatureFlagDefinition,
    FeatureFlagFallback,
    resolve_feature_flag_fallback,
)

USE_KINDS = ("NON_SENSITIVE", "PERMISSION", "MUTATION", "PROTECTED_DATA", "CONTRACT")
SENSITIVE_USE_KINDS = ("PERMISSION", "MUTATION", "PROTECTED_DATA", "CONTRACT")
FAILURE_KINDS = ("ABSENT", "INVALID", "STALE")

EQ_CALLS: list[str] = []
HASH_CALLS: list[str] = []
ATTR_READS: list[str] = []
CALL_CALLS: list[str] = []


class _TrapStr(str):
    def __eq__(self, other):
        EQ_CALLS.append("str")
        return str.__eq__(self, other)

    def __hash__(self):
        HASH_CALLS.append("str")
        return str.__hash__(self)


class _AttributeTrap:
    def __getattribute__(self, name):
        ATTR_READS.append(name)
        return object.__getattribute__(self, name)


class _CallableTrap:
    def __call__(self, *args, **kwargs):
        CALL_CALLS.append("call")
        return True

    def __bool__(self):
        CALL_CALLS.append("bool")
        return True

    def __eq__(self, other):
        EQ_CALLS.append("callable")
        return False

    def __hash__(self):
        HASH_CALLS.append("callable")
        return 5


class _SubDefinition(FeatureFlagDefinition):
    pass


class _TrapFallback(FeatureFlagFallback):
    def __eq__(self, other):
        EQ_CALLS.append("dto")
        return False

    def __hash__(self):
        HASH_CALLS.append("dto")
        return 0


def _definition(**overrides) -> FeatureFlagDefinition:
    fields = {
        "flag_id": "web.dark_mode",
        "flag_version": "2026.10-r1",
        "owner_component": "web-main",
        "purpose": "Déclarer l'option sombre du thème web.",
        "value_schema": "BOOLEAN",
        "default_value": True,
        "targeting_dimensions": ("INSTALLATION",),
        "cohort_key": None,
        "prerequisites": ("web-main",),
        "fallback_policy": "fail_closed",
        "expires_at": "2028-01-01T00:00:00Z",
        "audit_policy": "standard_audit",
    }
    fields.update(overrides)
    return FeatureFlagDefinition(**fields)


def _elements(result: FeatureFlagFallback) -> set[str]:
    return {diagnostic.element for diagnostic in result.diagnostics}


def _texts(result: FeatureFlagFallback) -> list[str]:
    return [
        text
        for diagnostic in result.diagnostics
        for text in (
            str(diagnostic),
            diagnostic.element,
            diagnostic.constraint,
            diagnostic.message,
        )
    ]


class FeatureFlagFallbackTests(unittest.TestCase):
    def setUp(self) -> None:
        for calls in (EQ_CALLS, HASH_CALLS, ATTR_READS, CALL_CALLS):
            calls.clear()

    def test_resultat_gele_trois_champs_obligatoires_sans_defaut(self) -> None:
        fields = dataclasses.fields(FeatureFlagFallback)
        self.assertEqual(
            tuple(field.name for field in fields),
            ("status", "value", "diagnostics"),
        )
        for field in fields:
            self.assertIs(field.default, dataclasses.MISSING)
            self.assertIs(field.default_factory, dataclasses.MISSING)
        with self.assertRaises(TypeError):
            FeatureFlagFallback(status="REFUSED")
        with self.assertRaises(TypeError):
            FeatureFlagFallback("REFUSED", None, (), alias="x")
        result = resolve_feature_flag_fallback(
            _definition(fallback_policy="DENY"), "NON_SENSITIVE", "ABSENT"
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            result.status = "DEFAULT"

    def test_matrice_politiques_usages_et_causes(self) -> None:
        for policy in ("DENY", "DEFAULT", "fail_closed"):
            for use_kind in USE_KINDS:
                for failure_kind in FAILURE_KINDS:
                    definition = _definition(fallback_policy=policy)
                    result = resolve_feature_flag_fallback(
                        definition, use_kind, failure_kind
                    )
                    self.assertIn(result.status, ("DEFAULT", "REFUSED"))
                    self.assertEqual(
                        resolve_feature_flag_fallback(
                            definition, use_kind, failure_kind
                        ),
                        result,
                    )
                    if policy == "DENY":
                        self.assertEqual(
                            (result.status, result.value, result.diagnostics),
                            ("REFUSED", None, ()),
                        )
                    elif policy == "DEFAULT" and use_kind == "NON_SENSITIVE":
                        self.assertEqual(
                            (result.status, result.value, result.diagnostics),
                            ("DEFAULT", True, ()),
                        )
                    else:
                        self.assertEqual(result.status, "REFUSED")
                        self.assertIsNone(result.value)
                        self.assertTrue(result.diagnostics)
        self.assertEqual(EQ_CALLS + HASH_CALLS + ATTR_READS + CALL_CALLS, [])

    def test_default_booleen_et_variante_conservés_litteralement(self) -> None:
        for failure_kind in FAILURE_KINDS:
            result = resolve_feature_flag_fallback(
                _definition(
                    fallback_policy="DEFAULT", default_value=False
                ),
                "NON_SENSITIVE",
                failure_kind,
            )
            self.assertEqual(result.status, "DEFAULT")
            self.assertIs(result.value, False)
            self.assertEqual(result.diagnostics, ())
        variant = resolve_feature_flag_fallback(
            _definition(
                value_schema="VARIANT",
                default_value="sombre",
                fallback_policy="DEFAULT",
            ),
            "NON_SENSITIVE",
            "STALE",
        )
        self.assertEqual(variant.status, "DEFAULT")
        self.assertEqual(variant.value, "sombre")
        not_a_bool = resolve_feature_flag_fallback(
            _definition(
                value_schema="VARIANT",
                default_value="sombre",
                fallback_policy="DEFAULT",
            ),
            "NON_SENSITIVE",
            "ABSENT",
        )
        self.assertNotIsInstance(not_a_bool.value, bool)

    def test_usage_sensible_refuse_sous_default_et_value_true_prouve_la_fermeture(
        self,
    ) -> None:
        for use_kind in SENSITIVE_USE_KINDS:
            result = resolve_feature_flag_fallback(
                _definition(fallback_policy="DEFAULT", default_value=True),
                use_kind,
                "INVALID",
            )
            self.assertEqual(result.status, "REFUSED", use_kind)
            self.assertIsNone(result.value)
            self.assertEqual(
                _elements(result), {"feature_flags.fallback.sensible"}, use_kind
            )

    def test_reference_heritee_opaque_jamais_aliee_ni_normalisee(self) -> None:
        for policy in ("deny", "Deny", "fail_closed", "retry_later", "DEFAULT_x"):
            result = resolve_feature_flag_fallback(
                _definition(fallback_policy=policy), "NON_SENSITIVE", "ABSENT"
            )
            self.assertEqual(result.status, "REFUSED", policy)
            self.assertIsNone(result.value)
            self.assertEqual(
                _elements(result), {"feature_flags.fallback.policy"}, policy
            )

    def test_arguments_hors_vocabulaire_refuses_sans_normalisation(self) -> None:
        for use_kind in ("non_sensitive", "", "INCONNU", "INSTALLATION"):
            result = resolve_feature_flag_fallback(_definition(), use_kind, "ABSENT")
            self.assertEqual(result.status, "REFUSED", use_kind)
            self.assertIn("feature_flags.fallback.use_kind", _elements(result))
            self.assertIsNone(result.value)
        for failure_kind in ("absent", "", "EXPIRED", "NA"):
            result = resolve_feature_flag_fallback(
                _definition(), "NON_SENSITIVE", failure_kind
            )
            self.assertEqual(result.status, "REFUSED", failure_kind)
            self.assertIn("feature_flags.fallback.failure_kind", _elements(result))
            self.assertIsNone(result.value)
        self.assertEqual(EQ_CALLS + HASH_CALLS + CALL_CALLS + ATTR_READS, [])

    def test_types_non_exacts_fermes_avant_toute_operation(self) -> None:
        for hostile in (
            _SubDefinition(**dataclasses.asdict(_definition())),
            _AttributeTrap(),
            _CallableTrap(),
            _TrapStr("web.dark_mode"),
            None,
        ):
            result = resolve_feature_flag_fallback(
                hostile, "NON_SENSITIVE", "ABSENT"
            )
            self.assertEqual(result.status, "REFUSED", type(hostile))
            self.assertIsNone(result.value)
            self.assertEqual(
                _elements(result), {"feature_flags.fallback.definition"}
            )
        for hostile in (_TrapStr("NON_SENSITIVE"), 1, None, ("NON_SENSITIVE",)):
            result = resolve_feature_flag_fallback(_definition(), hostile, "ABSENT")
            self.assertEqual(result.status, "REFUSED", type(hostile))
        for hostile in (_TrapStr("ABSENT"), 0, None, ["ABSENT"]):
            result = resolve_feature_flag_fallback(
                _definition(), "NON_SENSITIVE", hostile
            )
            self.assertEqual(result.status, "REFUSED", type(hostile))
        self.assertEqual(ATTR_READS + EQ_CALLS + HASH_CALLS + CALL_CALLS, [])

    def test_definition_hote_refusee_par_le_validateur_existant(self) -> None:
        trap = _CallableTrap()
        for overrides in (
            dict(flag_id="dark", fallback_policy="DENY"),
            dict(expires_at="2028-01-01T00:00:00", fallback_policy="DEFAULT"),
            dict(default_value=trap, fallback_policy="DEFAULT"),
            dict(fallback_policy=7),
        ):
            result = resolve_feature_flag_fallback(
                _definition(**overrides), "NON_SENSITIVE", "ABSENT"
            )
            self.assertEqual(result.status, "REFUSED", overrides)
            self.assertIsNone(result.value)
            self.assertTrue(result.diagnostics)
            self.assertNotIn("feature_flags.fallback.definition", _elements(result))
        self.assertEqual(CALL_CALLS, [])

    def test_diagnostics_sans_echo_tri_et_deduplication(self) -> None:
        sentinel = "SENTINELLE-repli"
        result = resolve_feature_flag_fallback(
            _definition(
                flag_id=f"bad space {sentinel}",
                fallback_policy=sentinel,
            ),
            _TrapStr("NON_SENSITIVE"),
            "ABSENT",
        )
        self.assertEqual(result.status, "REFUSED")
        self.assertTrue(result.diagnostics)
        for text in _texts(result):
            self.assertNotIn(sentinel, text)
        ordered = list(result.diagnostics)
        self.assertEqual(
            ordered,
            sorted(
                ordered,
                key=lambda item: (item.element, item.constraint, item.message),
            ),
        )
        for diagnostic in ordered:
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
        self.assertEqual(
            len(ordered), len({(d.element, d.constraint) for d in ordered})
        )
        refused = resolve_feature_flag_fallback(
            _TrapFallback("REFUSED", None, ()), "NON_SENSITIVE", "ABSENT"
        )
        self.assertEqual(_elements(refused), {"feature_flags.fallback.definition"})
        self.assertEqual(EQ_CALLS + HASH_CALLS, [])


if __name__ == "__main__":
    unittest.main()
