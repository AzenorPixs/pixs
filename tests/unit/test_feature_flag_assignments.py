"""Tests unitaires des affectations déclaratives de fanions (tâche 2.2, C1a).

Contrôlent le modèle figé à huit champs obligatoires sans défaut, le refus
fermé du validateur (types exacts, agrégation déterministe, diagnostics
constants sans écho), la fenêtre structurelle entre deux bornes UTC déjà
validées et l'invoquabilité nulle des objets hostiles.
"""

from __future__ import annotations

import dataclasses
import itertools
import unittest
from dataclasses import replace

from pixs.kernel.diagnostics import VALIDATE
from pixs.kernel.feature_flags import (
    FLAG_TARGETING_DIMENSIONS,
    FeatureFlagAssignment,
    validate_feature_flag_assignments,
)

CANONICAL_FIELDS = (
    "flag_id",
    "selector",
    "selector_value",
    "value",
    "valid_from",
    "valid_until",
    "configuration_version",
    "updated_by",
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


class _TrapAssignment(FeatureFlagAssignment):
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


_WITNESS = FeatureFlagAssignment(
    flag_id="web.dark_mode",
    selector="INSTALLATION",
    selector_value="installation-principale",
    value=False,
    valid_from="2026-10-03T00:00:00Z",
    valid_until="2027-01-01T00:00:00Z",
    configuration_version="cfg-2026-10-03",
    updated_by="administrateur.1",
)


def _assignment(**overrides) -> FeatureFlagAssignment:
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


class FeatureFlagAssignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        for calls in (
            EQ_CALLS, HASH_CALLS, STR_CALLS, REPR_CALLS,
            BOOL_CALLS, ITER_CALLS, META_CALLS,
        ):
            calls.clear()

    def test_huit_champs_canoniques_sans_defaut(self) -> None:
        fields = dataclasses.fields(FeatureFlagAssignment)
        self.assertEqual(tuple(field.name for field in fields), CANONICAL_FIELDS)
        for field in fields:
            self.assertIs(field.default, dataclasses.MISSING)
            self.assertIs(field.default_factory, dataclasses.MISSING)

    def test_chaque_champ_oublie_refuse_construction(self) -> None:
        full = {
            field.name: getattr(_WITNESS, field.name)
            for field in dataclasses.fields(_WITNESS)
        }
        FeatureFlagAssignment(**full)
        for name in CANONICAL_FIELDS:
            partial = dict(full)
            partial.pop(name)
            with self.assertRaises(TypeError):
                FeatureFlagAssignment(**partial)

    def test_kwargs_inconnus_refuses_a_construction(self) -> None:
        full = {
            field.name: getattr(_WITNESS, field.name)
            for field in dataclasses.fields(_WITNESS)
        }
        for unknown in ("expression", "rule", "code", "callback", "extra", "variant"):
            with self.assertRaises(TypeError):
                FeatureFlagAssignment(**{**full, unknown: "x"})

    def test_affectation_gelee(self) -> None:
        assignment = _assignment()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            assignment.selector = "TENANT"

    def test_value_booleenne_exacte_jeton_litteral_acceptes(self) -> None:
        for accepted in (False, True, "bleu", "var-1", "x.y"):
            self.assertEqual(
                validate_feature_flag_assignments([_assignment(value=accepted)]),
                (),
                accepted,
            )

    def test_value_hostiles_refusees_sans_callback(self) -> None:
        callable_trap = _CallableTrap()
        hostile = _Hostile()
        for refused in (
            0, 1, "", "a b", "lambda: x", "1 + 1", 5, None, callable_trap, hostile,
            _TrapStr("bleu"),
        ):
            diagnostics = validate_feature_flag_assignments(
                [_assignment(value=refused)]
            )
            self.assertIn(
                "feature_flags.assignments.value", _elements(diagnostics), refused
            )
        self.assertEqual(callable_trap.calls, [])
        self.assertEqual(
            EQ_CALLS + HASH_CALLS + STR_CALLS + REPR_CALLS + BOOL_CALLS + ITER_CALLS,
            [],
        )

    def test_selector_unique_dans_whitelist_exacte(self) -> None:
        for accepted in sorted(FLAG_TARGETING_DIMENSIONS):
            self.assertEqual(
                validate_feature_flag_assignments([_assignment(selector=accepted)]),
                (),
                accepted,
            )
        for refused in (
            "installation", "INSTALLATION ", "", "INSTALLATION,TENANT",
            ("INSTALLATION",), ["INSTALLATION"], None, 7, _TrapStr("INSTALLATION"),
        ):
            diagnostics = validate_feature_flag_assignments(
                [_assignment(selector=refused)]
            )
            self.assertIn(
                "feature_flags.assignments.selector", _elements(diagnostics), refused
            )
        self.assertEqual(EQ_CALLS + HASH_CALLS + ITER_CALLS + BOOL_CALLS, [])

    def test_metadonnees_opaques_non_vides_sans_grammaire_imposee(self) -> None:
        for field in ("selector_value", "configuration_version", "updated_by"):
            for accepted in (
                "web-main >=1.2.3", "0.0.0-pas-semver", "a b c",
                "cfg/2026#1", "v1 v2 v3", "1 + 1", " ", "dark",
            ):
                self.assertEqual(
                    validate_feature_flag_assignments([_assignment(**{field: accepted})]),
                    (),
                    (field, accepted),
                )
            for refused in ("", None, 7):
                diagnostics = validate_feature_flag_assignments(
                    [_assignment(**{field: refused})]
                )
                self.assertIn(
                    f"feature_flags.assignments.{field}",
                    _elements(diagnostics),
                    (field, refused),
                )
        self.assertEqual(
            EQ_CALLS + HASH_CALLS + STR_CALLS + REPR_CALLS + BOOL_CALLS + ITER_CALLS,
            [],
        )

    def test_flag_id_namespace(self) -> None:
        for accepted in ("web.dark_mode", "WEB-2.prod_x", "a.b.c"):
            self.assertEqual(
                validate_feature_flag_assignments([_assignment(flag_id=accepted)]),
                (),
                accepted,
            )
        for refused in (
            "dark", "", "web.", ".web", "web..x", "bad space", "flag x.y",
        ):
            diagnostics = validate_feature_flag_assignments(
                [_assignment(flag_id=refused)]
            )
            self.assertIn(
                "feature_flags.assignments.flag_id", _elements(diagnostics), refused
            )

    def test_bornes_utc_acceptees(self) -> None:
        for accepted in (
            "2026-10-03T00:00:00Z",
            "2026-10-03T00:00:00+00:00",
            "2026-10-03T00:00:00.1Z",
        ):
            self.assertEqual(
                validate_feature_flag_assignments([_assignment(valid_from=accepted)]),
                (),
                accepted,
            )
        for accepted in (
            "2027-01-01T00:00:00+00:00",
            "2027-01-01T00:00:00.5Z",
            "2027-01-01T23:59:59.123456Z",
        ):
            self.assertEqual(
                validate_feature_flag_assignments([_assignment(valid_until=accepted)]),
                (),
                accepted,
            )

    def test_bornes_utc_refusees(self) -> None:
        for refused in (
            "", "2026-10-03T00:00:00", "2026-10-03T00:00:00+02:00",
            "2026-10-03T00:00:00-00:00", "2025-02-29T00:00:00Z",
            "2026-13-01T00:00:00Z", "2026-10-03T24:00:00Z",
            "2026-10-03 00:00:00Z", "20261003T00:00:00Z",
            "2026-W40-1T00:00:00Z", "2026-10-03T00:00:00.1234567Z",
            "2026-10-03T00:00:00.Z", "٢٠٢٦-10-03T00:00:00Z",
            "2026-10-03T00:00:00z", None, 7,
        ):
            for field in ("valid_from", "valid_until"):
                diagnostics = validate_feature_flag_assignments(
                    [_assignment(**{field: refused})]
                )
                self.assertIn(
                    f"feature_flags.assignments.{field}",
                    _elements(diagnostics),
                    (field, refused),
                )

    def test_fenetre_structurelle_strictement_positive(self) -> None:
        diagnostics = validate_feature_flag_assignments(
            [_assignment(valid_until="2026-10-03T00:00:00Z")]
        )
        self.assertEqual(
            _elements(diagnostics), {"feature_flags.assignments.valid_window"}
        )
        diagnostics = validate_feature_flag_assignments(
            [_assignment(valid_until="2026-10-03T00:00:00+00:00")]
        )
        self.assertEqual(
            _elements(diagnostics), {"feature_flags.assignments.valid_window"}
        )
        diagnostics = validate_feature_flag_assignments(
            [_assignment(valid_from="2027-06-01T00:00:00Z")]
        )
        self.assertEqual(
            _elements(diagnostics), {"feature_flags.assignments.valid_window"}
        )
        self.assertEqual(
            validate_feature_flag_assignments(
                [_assignment(
                    valid_from="2027-01-01T00:00:00Z",
                    valid_until="2027-01-01T00:00:00.000001Z",
                )]
            ),
            (),
        )
        diagnostics = validate_feature_flag_assignments(
            [_assignment(valid_from="naif")]
        )
        self.assertEqual(
            _elements(diagnostics), {"feature_flags.assignments.valid_from"}
        )
        self.assertNotIn(
            "feature_flags.assignments.valid_window", _elements(diagnostics)
        )
        self.assertEqual(
            EQ_CALLS + HASH_CALLS + STR_CALLS + REPR_CALLS + BOOL_CALLS + ITER_CALLS,
            [],
        )

    def test_agregation_dedup_permutations_etapes_valide(self) -> None:
        bad_a = _assignment(flag_id="dark", valid_from="naif")
        bad_b = _assignment(selector="", configuration_version="")
        good = _assignment(flag_id="test.good")
        baseline = validate_feature_flag_assignments([bad_a, bad_b, good])
        self.assertTrue(baseline)
        self.assertEqual(
            _elements(baseline),
            {
                "feature_flags.assignments.flag_id",
                "feature_flags.assignments.valid_from",
                "feature_flags.assignments.selector",
                "feature_flags.assignments.configuration_version",
            },
        )
        for order in itertools.permutations((bad_a, bad_b, good)):
            self.assertEqual(validate_feature_flag_assignments(list(order)), baseline)
        duplicate_bad_a = replace(bad_a, flag_id="other.bad")
        self.assertEqual(
            validate_feature_flag_assignments([bad_a, duplicate_bad_a, bad_b, good]),
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
        diagnostics = validate_feature_flag_assignments(
            [_assignment(flag_id=f"bad space {sentinel}", configuration_version="")]
        )
        self.assertTrue(diagnostics)
        for text in _texts(diagnostics):
            self.assertNotIn(sentinel, text)

    def test_conteneur_exact_exige_list_ou_tuple_sans_invocation(self) -> None:
        container = _ContainerTrap([_assignment()])
        diagnostics = validate_feature_flag_assignments(container)
        self.assertEqual(
            _elements(diagnostics), {"feature_flags.assignments.conteneur"}
        )
        self.assertEqual(EQ_CALLS + HASH_CALLS + ITER_CALLS + BOOL_CALLS, [])
        self.assertEqual(validate_feature_flag_assignments(tuple([_assignment()])), ())
        self.assertEqual(validate_feature_flag_assignments([]), ())
        trap = _AttributeTrap()
        diagnostics = validate_feature_flag_assignments(trap)
        self.assertEqual(
            _elements(diagnostics), {"feature_flags.assignments.conteneur"}
        )
        self.assertEqual(trap.reads, [])

    def test_entree_non_affectation_jamais_lue(self) -> None:
        trap = _AttributeTrap()
        diagnostics = validate_feature_flag_assignments([trap, _assignment()])
        self.assertEqual(_elements(diagnostics), {"feature_flags.assignments.entree"})
        self.assertEqual(trap.reads, [])

    def test_sousclasses_refusees_sans_eq_hash(self) -> None:
        cases = (
            dict(flag_id=_TrapStr("trap.flag")),
            dict(selector=_TrapStr("INSTALLATION")),
            dict(selector_value=_TrapStr("site")),
            dict(value=_TrapStr("bleu")),
            dict(valid_from=_TrapStr("2026-10-03T00:00:00Z")),
            dict(updated_by=_TrapStr("operateur")),
        )
        for overrides in cases:
            diagnostics = validate_feature_flag_assignments([_assignment(**overrides)])
            self.assertTrue(diagnostics, overrides)
        diagnostics = validate_feature_flag_assignments(
            [_TrapAssignment(**dataclasses.asdict(_WITNESS))]
        )
        self.assertEqual(_elements(diagnostics), {"feature_flags.assignments.entree"})
        self.assertEqual(EQ_CALLS + HASH_CALLS, [])

    def test_primitives_hostiles_champ_par_champ_sans_appel(self) -> None:
        hostile = _Hostile()
        for field in CANONICAL_FIELDS:
            diagnostics = validate_feature_flag_assignments(
                [_assignment(**{field: hostile})]
            )
            self.assertIn(
                f"feature_flags.assignments.{field}",
                _elements(diagnostics),
                field,
            )
        self.assertEqual(
            EQ_CALLS + HASH_CALLS + STR_CALLS + REPR_CALLS + BOOL_CALLS + ITER_CALLS,
            [],
        )

    def test_metadonnees_hostiles_refusees_sans_touch_partout(self) -> None:
        hostile = _MetaHostile()
        for field in CANONICAL_FIELDS:
            diagnostics = validate_feature_flag_assignments(
                [_assignment(**{field: hostile})]
            )
            self.assertIn(
                f"feature_flags.assignments.{field}",
                _elements(diagnostics),
                field,
            )
        container = _MetaHostileList([_assignment()])
        self.assertEqual(
            _elements(validate_feature_flag_assignments(container)),
            {"feature_flags.assignments.conteneur"},
        )
        self.assertEqual(
            _elements(validate_feature_flag_assignments([_MetaHostile()])),
            {"feature_flags.assignments.entree"},
        )
        self.assertEqual(META_CALLS, [])


if __name__ == "__main__":
    unittest.main()
