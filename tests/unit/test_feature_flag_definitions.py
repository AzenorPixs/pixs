"""Tests unitaires des définitions déclaratives de fanions (tâche 2.2, R1).

Contrôlent le modèle figé à douze champs canoniques sans défaut, le refus
fermé du validateur (types exacts, agrégation déterministe, diagnostics
constants sans écho) et l'invoquabilité nulle des objets hostiles.
"""

from __future__ import annotations

import dataclasses
import itertools
import unittest
from dataclasses import replace

from pixs.kernel.diagnostics import VALIDATE
from pixs.kernel.feature_flags import (
    FLAG_TARGETING_DIMENSIONS,
    FeatureFlagDefinition,
    validate_feature_flag_definitions,
)

CANONICAL_FIELDS = (
    "flag_id",
    "flag_version",
    "owner_component",
    "purpose",
    "value_schema",
    "default_value",
    "targeting_dimensions",
    "cohort_key",
    "prerequisites",
    "fallback_policy",
    "expires_at",
    "audit_policy",
)

EQ_CALLS: list[str] = []
HASH_CALLS: list[str] = []
STR_CALLS: list[str] = []
REPR_CALLS: list[str] = []
BOOL_CALLS: list[str] = []
ITER_CALLS: list[str] = []
META_CALLS: list[str] = []


class _TrapStr(str):
    def __eq__(self, other):
        EQ_CALLS.append("str")
        return str.__eq__(self, other)

    def __hash__(self):
        HASH_CALLS.append("str")
        return str.__hash__(self)

    def __str__(self):
        STR_CALLS.append("str")
        return str.__str__(self)

    def __repr__(self):
        REPR_CALLS.append("str")
        return str.__repr__(self)


class _TrapTuple(tuple):
    def __eq__(self, other):
        EQ_CALLS.append("tuple")
        return tuple.__eq__(self, other)

    def __hash__(self):
        HASH_CALLS.append("tuple")
        return tuple.__hash__(self)

    def __iter__(self):
        ITER_CALLS.append("tuple")
        return tuple.__iter__(self)


class _TrapList(list):
    def __eq__(self, other):
        EQ_CALLS.append("list")
        return list.__eq__(self, other)

    def __hash__(self):
        HASH_CALLS.append("list")
        return 0

    def __iter__(self):
        ITER_CALLS.append("list")
        return list.__iter__(self)


class _TrapDto(FeatureFlagDefinition):
    def __eq__(self, other):
        EQ_CALLS.append("dto")
        return False

    def __hash__(self):
        HASH_CALLS.append("dto")
        return 0


class _TrapMeta(type):
    def __eq__(cls, other):
        META_CALLS.append("meta_eq")
        return type.__eq__(cls, other)

    def __hash__(cls):
        META_CALLS.append("meta_hash")
        return type.__hash__(cls)


class _MetaHostile(metaclass=_TrapMeta):
    pass


class _MetaHostileList(list, metaclass=_TrapMeta):
    pass


class _Hostile:
    def __eq__(self, other):
        EQ_CALLS.append("hostile")
        return False

    def __hash__(self):
        HASH_CALLS.append("hostile")
        return 1

    def __str__(self):
        STR_CALLS.append("hostile")
        return "hostile"

    def __repr__(self):
        REPR_CALLS.append("hostile")
        return "<hostile>"

    def __bool__(self):
        BOOL_CALLS.append("hostile")
        return True

    def __iter__(self):
        ITER_CALLS.append("hostile")
        return iter(())


class _AttributeTrap:
    def __init__(self) -> None:
        object.__setattr__(self, "reads", [])

    def __getattribute__(self, name):
        if name != "reads":
            object.__getattribute__(self, "reads").append(name)
        return object.__getattribute__(self, name)


class _CallableTrap:
    def __init__(self) -> None:
        object.__setattr__(self, "calls", [])

    def __call__(self, *args, **kwargs):
        object.__getattribute__(self, "calls").append("call")


class _ContainerTrap(list):
    def __eq__(self, other):
        EQ_CALLS.append("container")
        return list.__eq__(self, other)

    def __hash__(self):
        HASH_CALLS.append("container")
        return 0

    def __bool__(self):
        BOOL_CALLS.append("container")
        return True

    def __iter__(self):
        ITER_CALLS.append("container")
        return list.__iter__(self)

    def __repr__(self):
        REPR_CALLS.append("container")
        return list.__repr__(self)


_WITNESS = FeatureFlagDefinition(
    flag_id="web.dark_mode",
    flag_version="2026.10-r1",
    owner_component="web-main",
    purpose="Déclarer l'option sombre du thème web.",
    value_schema="BOOLEAN",
    default_value=False,
    targeting_dimensions=("INSTALLATION",),
    cohort_key=None,
    prerequisites=("web-main",),
    fallback_policy="fail_closed",
    expires_at="2027-01-01T00:00:00Z",
    audit_policy="standard_audit",
)


def _definition(**overrides) -> FeatureFlagDefinition:
    return replace(_WITNESS, **overrides)


def _elements(diagnostics) -> set[str]:
    return {diagnostic.element for diagnostic in diagnostics}


def _texts(diagnostics) -> list[str]:
    return [
        text
        for diagnostic in diagnostics
        for text in (
            str(diagnostic),
            diagnostic.element,
            diagnostic.constraint,
            diagnostic.message,
        )
    ]


class FeatureFlagDefinitionTests(unittest.TestCase):
    def setUp(self) -> None:
        for calls in (
            EQ_CALLS, HASH_CALLS, STR_CALLS, REPR_CALLS,
            BOOL_CALLS, ITER_CALLS, META_CALLS,
        ):
            calls.clear()

    def test_douze_champs_canoniques_sans_defaut(self) -> None:
        fields = dataclasses.fields(FeatureFlagDefinition)
        self.assertEqual(tuple(field.name for field in fields), CANONICAL_FIELDS)
        for field in fields:
            self.assertIs(field.default, dataclasses.MISSING)
            self.assertIs(field.default_factory, dataclasses.MISSING)

    def test_chaque_champ_oublie_refuse_construction(self) -> None:
        full = {
            field.name: getattr(_WITNESS, field.name)
            for field in dataclasses.fields(_WITNESS)
        }
        FeatureFlagDefinition(**full)
        for name in CANONICAL_FIELDS:
            partial = dict(full)
            partial.pop(name)
            with self.assertRaises(TypeError):
                FeatureFlagDefinition(**partial)

    def test_champs_expression_rule_code_callback_refuses(self) -> None:
        full = {
            field.name: getattr(_WITNESS, field.name)
            for field in dataclasses.fields(_WITNESS)
        }
        for unknown in ("expression", "rule", "code", "callback", "extra"):
            with self.assertRaises(TypeError):
                FeatureFlagDefinition(**{**full, unknown: "x"})

    def test_definition_gelee(self) -> None:
        definition = _definition()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            definition.flag_version = "autre"

    def test_boolean_bool_exact_int_refuses(self) -> None:
        self.assertEqual(validate_feature_flag_definitions([_definition()]), ())
        for refused in (0, 1):
            diagnostics = validate_feature_flag_definitions(
                [_definition(default_value=refused)]
            )
            self.assertIn("feature_flags.default_value", _elements(diagnostics))

    def test_variant_token_accepte_expressions_refusees(self) -> None:
        callable_trap = _CallableTrap()
        for accepted in ("bleu", "var-1", "x.y"):
            diagnostics = validate_feature_flag_definitions(
                [_definition(value_schema="VARIANT", default_value=accepted)]
            )
            self.assertEqual(diagnostics, ())
        for refused in ("", "a b", "lambda: x", "1 + 1", 5, None, callable_trap):
            diagnostics = validate_feature_flag_definitions(
                [_definition(value_schema="VARIANT", default_value=refused)]
            )
            self.assertIn("feature_flags.default_value", _elements(diagnostics))
        self.assertEqual(callable_trap.calls, [])

    def test_none_admis_seulement_pour_cohort_key(self) -> None:
        self.assertEqual(
            _elements(validate_feature_flag_definitions([_definition(cohort_key=None)])),
            set(),
        )
        for field in CANONICAL_FIELDS:
            if field == "cohort_key":
                continue
            diagnostics = validate_feature_flag_definitions(
                [_definition(**{field: None})]
            )
            self.assertIn(f"feature_flags.{field}", _elements(diagnostics))

    def test_version_opaque_et_prose_contenant_code_acceptees(self) -> None:
        for version in ("toute-valeur#2026!", "0.0.0-pas-semver", "v1 v2 v3"):
            self.assertEqual(
                validate_feature_flag_definitions([_definition(flag_version=version)]),
                (),
            )
        prose = "Si flag_id == 'web.dark_mode' : run('reboot') — finalité rédigée."
        self.assertEqual(
            validate_feature_flag_definitions([_definition(purpose=prose)]), ()
        )

    def test_bare_ids_acceptes_flag_id_namespaces_exiges(self) -> None:
        for accepted in ("WEB-2", "composant.9_x", "web-main"):
            self.assertEqual(
                validate_feature_flag_definitions(
                    [_definition(owner_component=accepted)]
                ),
                (),
            )
        for accepted in ("web.dark_mode", "WEB-2.prod_x", "a.b.c"):
            self.assertEqual(
                validate_feature_flag_definitions([_definition(flag_id=accepted)]),
                (),
            )
        for refused in (
            "dark", "", "web.", ".web", "web..x", "bad space", "flag x.y",
        ):
            diagnostics = validate_feature_flag_definitions(
                [_definition(flag_id=refused)]
            )
            self.assertIn("feature_flags.flag_id", _elements(diagnostics))

    def test_dimensions_whitelist_tuple_exact_sans_doublon(self) -> None:
        for accepted in ((), tuple(sorted(FLAG_TARGETING_DIMENSIONS))):
            self.assertEqual(
                validate_feature_flag_definitions(
                    [_definition(targeting_dimensions=accepted)]
                ),
                (),
            )
        for refused in (
            ("fanion",), ("installation",), ("INSTALLATION", "INSTALLATION"),
            ["INSTALLATION"], ("INSTALLATION", None),
        ):
            diagnostics = validate_feature_flag_definitions(
                [_definition(targeting_dimensions=refused)]
            )
            self.assertIn(
                "feature_flags.targeting_dimensions", _elements(diagnostics)
            )

    def test_prerequis_references_tuple_sans_doublon(self) -> None:
        self.assertEqual(
            validate_feature_flag_definitions(
                [_definition(prerequisites=("web-main", "api.v2"))]
            ),
            (),
        )
        for refused in (
            ("web-main", "web-main"), ("bad space",), ["web-main"], (None,),
        ):
            diagnostics = validate_feature_flag_definitions(
                [_definition(prerequisites=refused)]
            )
            self.assertIn("feature_flags.prerequisites", _elements(diagnostics))

    def test_cohorte_politiques_declares(self) -> None:
        for accepted in ("beta.cohorte-x", "FAIL-CLOSED", "audit_v2"):
            field = (
                "cohort_key" if accepted == "beta.cohorte-x"
                else "fallback_policy" if accepted == "FAIL-CLOSED"
                else "audit_policy"
            )
            self.assertEqual(
                validate_feature_flag_definitions([_definition(**{field: accepted})]),
                (),
            )
        for field, refused in (
            ("cohort_key", "cohorte 1"), ("cohort_key", ""),
            ("fallback_policy", "fail open"), ("audit_policy", 7),
        ):
            diagnostics = validate_feature_flag_definitions(
                [_definition(**{field: refused})]
            )
            self.assertIn(f"feature_flags.{field}", _elements(diagnostics))

    def test_expirations_acceptees(self) -> None:
        for accepted in (
            "2027-01-01T00:00:00Z",
            "2027-01-01T00:00:00+00:00",
            "2024-02-29T12:00:00Z",
            "2027-01-01T00:00:00.1Z",
            "2027-01-01T00:00:00.12+00:00",
            "2027-01-01T23:59:59.123456Z",
        ):
            self.assertEqual(
                validate_feature_flag_definitions([_definition(expires_at=accepted)]),
                (),
                accepted,
            )

    def test_expirations_refusees(self) -> None:
        for refused in (
            "", "2027-01-01T00:00:00", "2027-01-01T00:00:00+02:00",
            "2027-01-01T00:00:00-00:00", "2025-02-29T00:00:00Z",
            "2027-13-01T00:00:00Z", "2027-01-01T24:00:00Z",
            "2027-01-01 00:00:00Z", "20270101T00:00:00Z",
            "2027-W01-1T00:00:00Z", "2027-01-01T00:00:00.1234567Z",
            "2027-01-01T00:00:00.Z", "٢٠٢٧-01-01T00:00:00Z",
            "2027-01-01T00:00:00z", None, 7,
        ):
            diagnostics = validate_feature_flag_definitions(
                [_definition(expires_at=refused)]
            )
            self.assertIn("feature_flags.expires_at", _elements(diagnostics), refused)

    def test_drapeau_declare_une_seule_fois_meme_version_diff(self) -> None:
        diagnostics = validate_feature_flag_definitions(
            [
                _definition(flag_id="dup.flag", flag_version="v1"),
                _definition(flag_id="dup.flag", flag_version="v2"),
            ]
        )
        self.assertIn(
            "drapeau déclaré une seule fois",
            [diagnostic.constraint for diagnostic in diagnostics],
        )

    def test_agregation_dedup_permutations_etapes_valide(self) -> None:
        bad_a = _definition(
            flag_id="test.bad_a", flag_version="", expires_at="naif"
        )
        bad_b = _definition(
            flag_id="test.bad_b", value_schema="AUTRE", purpose=""
        )
        good = _definition(flag_id="test.good")
        baseline = validate_feature_flag_definitions([bad_a, bad_b, good])
        self.assertTrue(baseline)
        self.assertEqual(
            _elements(baseline),
            {
                "feature_flags.flag_version",
                "feature_flags.expires_at",
                "feature_flags.value_schema",
                "feature_flags.purpose",
            },
        )
        for order in itertools.permutations((bad_a, bad_b, good)):
            self.assertEqual(
                validate_feature_flag_definitions(list(order)),
                baseline,
            )
        duplicate_bad_a = replace(bad_a, flag_id="test.bad_a_again")
        self.assertEqual(
            validate_feature_flag_definitions(
                [bad_a, duplicate_bad_a, bad_b, good]
            ),
            baseline,
        )
        ordered = list(baseline)
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

    def test_diagnostics_ne_reproduisent_aucune_valeur(self) -> None:
        sentinel = "SENTINELLE-id"
        diagnostics = validate_feature_flag_definitions(
            [_definition(flag_id=f"bad space {sentinel}", flag_version="")]
        )
        self.assertTrue(diagnostics)
        for text in _texts(diagnostics):
            self.assertNotIn(sentinel, text)

    def test_conteneur_exact_exige_list_ou_tuple_sans_invocation(self) -> None:
        container = _ContainerTrap([_definition()])
        diagnostics = validate_feature_flag_definitions(container)
        self.assertEqual(_elements(diagnostics), {"feature_flags.conteneur"})
        self.assertEqual(EQ_CALLS + HASH_CALLS + ITER_CALLS + BOOL_CALLS, [])
        self.assertEqual(
            validate_feature_flag_definitions(tuple([_definition()])), ()
        )
        self.assertEqual(validate_feature_flag_definitions([]), ())
        trap = _AttributeTrap()
        diagnostics = validate_feature_flag_definitions(trap)
        self.assertEqual(_elements(diagnostics), {"feature_flags.conteneur"})
        self.assertEqual(trap.reads, [])

    def test_entree_non_definition_jamais_lue(self) -> None:
        trap = _AttributeTrap()
        diagnostics = validate_feature_flag_definitions([trap, _definition()])
        self.assertEqual(_elements(diagnostics), {"feature_flags.entree"})
        self.assertEqual(trap.reads, [])

    def test_sousclasses_refusees_sans_eq_hash(self) -> None:
        cases = (
            dict(flag_id=_TrapStr("trap.flag")),
            dict(targeting_dimensions=_TrapTuple(("INSTALLATION",))),
            dict(prerequisites=_TrapList(("a.b",))),
            dict(expires_at=_TrapStr("2027-01-01T00:00:00Z")),
        )
        for overrides in cases:
            diagnostics = validate_feature_flag_definitions(
                [_definition(**overrides)]
            )
            self.assertTrue(diagnostics, overrides)
        diagnostics = validate_feature_flag_definitions(
            [_TrapDto(**dataclasses.asdict(_WITNESS))]
        )
        self.assertEqual(_elements(diagnostics), {"feature_flags.entree"})
        self.assertEqual(EQ_CALLS + HASH_CALLS, [])

    def test_primitives_hostiles_champ_par_champ_sans_appel(self) -> None:
        hostile = _Hostile()
        for field in CANONICAL_FIELDS:
            diagnostics = validate_feature_flag_definitions(
                [_definition(**{field: hostile})]
            )
            self.assertIn(
                f"feature_flags.{field}", _elements(diagnostics), field
            )
        self.assertEqual(
            EQ_CALLS + HASH_CALLS + STR_CALLS + REPR_CALLS + BOOL_CALLS + ITER_CALLS,
            [],
        )

    def test_metadonnees_hostiles_refusees_sans_touch_partout(self) -> None:
        hostile = _MetaHostile()
        for field in CANONICAL_FIELDS:
            diagnostics = validate_feature_flag_definitions(
                [_definition(**{field: hostile})]
            )
            self.assertIn(
                f"feature_flags.{field}", _elements(diagnostics), field
            )
        container = _MetaHostileList([_definition()])
        self.assertEqual(
            _elements(validate_feature_flag_definitions(container)),
            {"feature_flags.conteneur"},
        )
        self.assertEqual(
            _elements(validate_feature_flag_definitions([_MetaHostile()])),
            {"feature_flags.entree"},
        )
        self.assertEqual(META_CALLS, [])

    def test_references_a_comparateurs_valides_refusees(self) -> None:
        for field in (
            "owner_component",
            "cohort_key",
            "fallback_policy",
            "audit_policy",
        ):
            for entry in (
                "web-main >=1.2.3",
                "web-main ==1.2.3",
                "web-main >2.0.0",
            ):
                diagnostics = validate_feature_flag_definitions(
                    [_definition(**{field: entry})]
                )
                self.assertIn(
                    f"feature_flags.{field}", _elements(diagnostics), entry
                )
        for entry in ("web-main >=1.2.3", "api.v2 <=2.0.0"):
            diagnostics = validate_feature_flag_definitions(
                [_definition(prerequisites=(entry,))]
            )
            self.assertIn("feature_flags.prerequisites", _elements(diagnostics))
        diagnostics = validate_feature_flag_definitions(
            [_definition(value_schema="VARIANT", default_value="bleu >=1.0.0")]
        )
        self.assertIn("feature_flags.default_value", _elements(diagnostics))
        hostile = _Hostile()
        diagnostics = validate_feature_flag_definitions(
            [
                _definition(targeting_dimensions=(hostile,)),
                _definition(targeting_dimensions=_TrapTuple((hostile,))),
                _definition(prerequisites=_TrapList((hostile,))),
                _definition(prerequisites=(hostile,)),
            ]
        )
        self.assertIn(
            "feature_flags.targeting_dimensions", _elements(diagnostics)
        )
        self.assertIn("feature_flags.prerequisites", _elements(diagnostics))
        self.assertEqual(
            EQ_CALLS
            + HASH_CALLS
            + STR_CALLS
            + REPR_CALLS
            + BOOL_CALLS
            + ITER_CALLS,
            [],
            "aucun crochet étranger ni itération de tuple piégé",
        )

    def test_schemas_hors_whitelist_refuses_avec_premier_defaut_valide(self) -> None:
        for refused in ("boolean", "INTEGER", "", "CODE"):
            diagnostics = validate_feature_flag_definitions(
                [_definition(value_schema=refused)]
            )
            self.assertIn("feature_flags.value_schema", _elements(diagnostics))


if __name__ == "__main__":
    unittest.main()
