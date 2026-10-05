"""Tests unitaires de la résolution déclarative de candidats (tâche 3.1, C2).

Contrôlent le contexte figé à cinq champs, la fermeture des types avant toute
itération, comparaison ou accès d'attribut, l'adéquation exacte des seules
dimensions déclarées, la fenêtre semi-ouverte sur instant injecté, la priorité
par niveaux sans ordre relatif inventé, le refus d'ambiguïté et l'absence
d'écho des diagnostics. Aucune horloge système, aucune E/S et aucun callback ne
sont déclenchés ni patchés.
"""

from __future__ import annotations

import dataclasses
import itertools
import unittest
from dataclasses import replace

from pixs.kernel.diagnostics import VALIDATE
from pixs.kernel.feature_flags import (
    FeatureFlagAssignment,
    FeatureFlagDefinition,
    FeatureFlagEvaluationContext,
    FeatureFlagResolution,
    resolve_feature_flag_assignment,
)

CONTEXT_FIELDS = (
    "installation",
    "environment",
    "tenant",
    "scope",
    "as_of",
)

EQ_CALLS: list[str] = []
HASH_CALLS: list[str] = []
ITER_CALLS: list[str] = []
CALL_CALLS: list[str] = []
ATTR_READS: list[str] = []


class _TrapStr(str):
    def __eq__(self, other):
        EQ_CALLS.append("str")
        return str.__eq__(self, other)

    def __hash__(self):
        HASH_CALLS.append("str")
        return str.__hash__(self)


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
        return 3


class _IterTrap:
    def __iter__(self):
        ITER_CALLS.append("iter")
        return iter(())


class _AttributeTrap:
    def __getattribute__(self, name):
        ATTR_READS.append(name)
        return object.__getattribute__(self, name)


class _SubDefinition(FeatureFlagDefinition):
    pass


class _SubAssignment(FeatureFlagAssignment):
    pass


class _SubContext(FeatureFlagEvaluationContext):
    pass


_DEFINITION = FeatureFlagDefinition(
    flag_id="web.dark_mode",
    flag_version="2026.10-r1",
    owner_component="web-main",
    purpose="Déclarer l'option sombre du thème web.",
    value_schema="BOOLEAN",
    default_value=False,
    targeting_dimensions=("INSTALLATION", "TENANT", "SCOPE"),
    cohort_key=None,
    prerequisites=("web-main",),
    fallback_policy="fail_closed",
    expires_at="2028-01-01T00:00:00Z",
    audit_policy="standard_audit",
)

_CONTEXT = FeatureFlagEvaluationContext(
    installation="installation-principale",
    environment=None,
    tenant=None,
    scope=None,
    as_of="2026-06-01T00:00:00Z",
)


def _definition(**overrides) -> FeatureFlagDefinition:
    return replace(_DEFINITION, **overrides)


def _context(**overrides) -> FeatureFlagEvaluationContext:
    return replace(_CONTEXT, **overrides)


def _assignment(**overrides) -> FeatureFlagAssignment:
    fields = {
        "flag_id": "web.dark_mode",
        "selector": "INSTALLATION",
        "selector_value": "installation-principale",
        "value": False,
        "valid_from": "2026-01-01T00:00:00Z",
        "valid_until": "2027-01-01T00:00:00Z",
        "configuration_version": "cfg-1",
        "updated_by": "administrateur.1",
    }
    fields.update(overrides)
    return FeatureFlagAssignment(**fields)


def _elements(result: FeatureFlagResolution) -> set[str]:
    return {diagnostic.element for diagnostic in result.diagnostics}


def _texts(result: FeatureFlagResolution) -> list[str]:
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


class FeatureFlagEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        for calls in (EQ_CALLS, HASH_CALLS, ITER_CALLS, CALL_CALLS, ATTR_READS):
            calls.clear()

    def test_contexte_cinq_champs_obligatoires_sans_defaut(self) -> None:
        fields = dataclasses.fields(FeatureFlagEvaluationContext)
        self.assertEqual(tuple(field.name for field in fields), CONTEXT_FIELDS)
        for field in fields:
            self.assertIs(field.default, dataclasses.MISSING)
            self.assertIs(field.default_factory, dataclasses.MISSING)
        full = {name: getattr(_CONTEXT, name) for name in CONTEXT_FIELDS}
        FeatureFlagEvaluationContext(**full)
        for name in CONTEXT_FIELDS:
            partial = dict(full)
            partial.pop(name)
            with self.assertRaises(TypeError):
                FeatureFlagEvaluationContext(**partial)
        for unknown in ("installation_alias", "now", "clock", "cohort"):
            with self.assertRaises(TypeError):
                FeatureFlagEvaluationContext(**{**full, unknown: "x"})
        context = _context()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            context.as_of = "2027-01-01T00:00:00Z"

    def test_resolution_gelee_a_trois_champs(self) -> None:
        fields = dataclasses.fields(FeatureFlagResolution)
        self.assertEqual(
            tuple(field.name for field in fields),
            ("status", "assignment", "diagnostics"),
        )
        result = resolve_feature_flag_assignment(_DEFINITION, [], _CONTEXT)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            result.status = "SELECTED"
        self.assertEqual(result.status, "NO_MATCH")
        self.assertIsNone(result.assignment)
        self.assertEqual(result.diagnostics, ())

    def test_selection_unique_conserve_false_et_determinisme(self) -> None:
        assignment = _assignment()
        first = resolve_feature_flag_assignment(_DEFINITION, [assignment], _CONTEXT)
        second = resolve_feature_flag_assignment(_DEFINITION, [assignment], _CONTEXT)
        self.assertEqual(first.status, "SELECTED")
        self.assertIs(first.assignment, assignment)
        self.assertIs(first.assignment.value, False)
        self.assertEqual(second, first)
        self.assertEqual(first.diagnostics, ())

    def test_permutations_du_lot_produisent_la_meme_decision(self) -> None:
        general = _assignment()
        tenant = _assignment(
            selector="TENANT", selector_value="tenant-a", configuration_version="cfg-2"
        )
        scope = _assignment(
            selector="SCOPE",
            selector_value="scope-a",
            configuration_version="cfg-3",
        )
        context = _context(tenant="tenant-a", scope="scope-a")
        baseline = resolve_feature_flag_assignment(
            _DEFINITION, [general, tenant, scope], context
        )
        self.assertEqual(baseline.status, "SELECTED")
        self.assertEqual(baseline.assignment.configuration_version, "cfg-3")
        for order in itertools.permutations((general, tenant, scope)):
            self.assertEqual(
                resolve_feature_flag_assignment(_DEFINITION, list(order), context),
                baseline,
            )

    def test_niveau_suivant_prend_le_dessus_et_general_egal(self) -> None:
        general = _assignment()
        tenant = _assignment(selector="TENANT", selector_value="tenant-a")
        scoped = _assignment(selector="SCOPE", selector_value="scope-a")
        self.assertEqual(
            resolve_feature_flag_assignment(
                _DEFINITION, [general], _context(tenant="tenant-a")
            ).assignment,
            general,
        )
        self.assertEqual(
            resolve_feature_flag_assignment(
                _DEFINITION, [general, tenant], _context(tenant="tenant-a")
            ).assignment,
            tenant,
        )
        self.assertEqual(
            resolve_feature_flag_assignment(
                _DEFINITION, [scoped, tenant], _context(tenant="tenant-a", scope="scope-a")
            ).assignment,
            scoped,
        )
        four = _definition(
            targeting_dimensions=("INSTALLATION", "ENVIRONMENT", "TENANT", "SCOPE")
        )
        installation = _assignment()
        environment = _assignment(
            selector="ENVIRONMENT", selector_value="prod", configuration_version="cfg-e"
        )
        context = _context(environment="prod")
        refused = resolve_feature_flag_assignment(
            four, [installation, environment], context
        )
        self.assertEqual(refused.status, "REFUSED")
        self.assertIsNone(refused.assignment)
        self.assertEqual(_elements(refused), {"feature_flags.evaluation.candidats"})
        only_general = resolve_feature_flag_assignment(four, [installation], context)
        self.assertEqual(only_general.assignment, installation)

    def test_ambiguite_refusee_meme_a_valeurs_egales_sans_ordre(self) -> None:
        first = _assignment(configuration_version="cfg-a")
        twin = _assignment(configuration_version="cfg-b", value=False)
        for order in itertools.permutations((first, twin)):
            result = resolve_feature_flag_assignment(
                _DEFINITION, list(order), _CONTEXT
            )
            self.assertEqual(result.status, "REFUSED")
            self.assertIsNone(result.assignment)
            self.assertEqual(
                _elements(result), {"feature_flags.evaluation.candidats"}
            )
            self.assertEqual(len(result.diagnostics), 1)

    def test_dimension_hors_declaration_ignoree_et_adéquation_exacte(self) -> None:
        hidden = _assignment(selector="ENVIRONMENT", selector_value="prod")
        self.assertEqual(
            resolve_feature_flag_assignment(
                _DEFINITION, [hidden], _context(environment="prod")
            ).status,
            "NO_MATCH",
        )
        for overrides in (
            dict(flag_id="other.flag"),
            dict(selector_value="installation-secondaire"),
            dict(selector_value="Installation-principale"),
            dict(selector_value=" installation-principale"),
        ):
            result = resolve_feature_flag_assignment(
                _DEFINITION, [_assignment(**overrides)], _CONTEXT
            )
            self.assertEqual(result.status, "NO_MATCH", overrides)
        for context, expected in (
            (_context(installation=None), "NO_MATCH"),
            (_context(installation=""), "REFUSED"),
            (_context(installation=_TrapStr("installation-principale")), "REFUSED"),
        ):
            result = resolve_feature_flag_assignment(_DEFINITION, [_assignment()], context)
            self.assertEqual(result.status, expected)

    def test_fenetre_semieouverte_et_horodatages_invalides(self) -> None:
        windows = (
            ("2026-06-01T00:00:00Z", "2027-01-01T00:00:00Z", "SELECTED"),
            ("2026-01-01T00:00:00Z", "2027-01-01T00:00:00Z", "SELECTED"),
            ("2026-01-01T00:00:00Z", "2026-06-01T00:00:00Z", "NO_MATCH"),
            ("2025-01-01T00:00:00Z", "2026-01-01T00:00:00Z", "NO_MATCH"),
            ("2027-01-01T00:00:00Z", "2028-01-01T00:00:00Z", "NO_MATCH"),
        )
        for valid_from, valid_until, expected in windows:
            result = resolve_feature_flag_assignment(
                _DEFINITION,
                [_assignment(valid_from=valid_from, valid_until=valid_until)],
                _CONTEXT,
            )
            self.assertEqual(result.status, expected, (valid_from, valid_until))
        for refused in (
            dict(valid_from="2026-01-01T00:00:00"),
            dict(valid_until="2027-01-01T00:00:00+02:00"),
            dict(valid_from="naif", valid_until="garbage"),
            dict(valid_from="2027-01-01T00:00:00Z", valid_until="2026-01-01T00:00:00Z"),
        ):
            result = resolve_feature_flag_assignment(
                _DEFINITION, [_assignment(**refused)], _CONTEXT
            )
            self.assertEqual(result.status, "REFUSED", refused)
            self.assertTrue(result.diagnostics)

    def test_instant_injecte_aucune_horloge_lue(self) -> None:
        assignment = _assignment()
        far_past = resolve_feature_flag_assignment(
            _DEFINITION, [assignment], _context(as_of="2020-01-01T00:00:00Z")
        )
        self.assertEqual(far_past.status, "NO_MATCH")
        inside = resolve_feature_flag_assignment(
            _DEFINITION, [assignment], _context(as_of="2026-12-31T23:59:59Z")
        )
        self.assertEqual(inside.status, "SELECTED")
        for refused_as_of in ("2026-06-01T00:00:00", "2026-06-01 00:00:00Z", "x"):
            result = resolve_feature_flag_assignment(
                _DEFINITION, [assignment], _context(as_of=refused_as_of)
            )
            self.assertEqual(result.status, "REFUSED", refused_as_of)
            self.assertIn("feature_flags.evaluation.as_of", _elements(result))

    def test_scope_sans_tenant_refuse_en_forme_seulement(self) -> None:
        result = resolve_feature_flag_assignment(
            _definition(targeting_dimensions=("INSTALLATION", "TENANT", "SCOPE")),
            [_assignment()],
            _context(scope="scope-a"),
        )
        self.assertEqual(result.status, "REFUSED")
        self.assertIn("feature_flags.evaluation.scope", _elements(result))
        self.assertIsNone(result.assignment)

    def test_compatibilite_de_valeur_avec_le_schema(self) -> None:
        variant = _definition(
            value_schema="VARIANT", default_value="sombre", expires_at="2028-01-01T00:00:00Z"
        )
        selected = resolve_feature_flag_assignment(
            variant, [_assignment(value="sombre")], _CONTEXT
        )
        self.assertEqual(selected.status, "SELECTED")
        self.assertEqual(selected.assignment.value, "sombre")
        wrong = resolve_feature_flag_assignment(
            variant, [_assignment(value=True)], _CONTEXT
        )
        self.assertEqual(wrong.status, "REFUSED")
        self.assertIn("feature_flags.evaluation.value", _elements(wrong))
        bool_wrong = resolve_feature_flag_assignment(
            _DEFINITION, [_assignment(value="clair")], _CONTEXT
        )
        self.assertEqual(bool_wrong.status, "REFUSED")
        self.assertIn("feature_flags.evaluation.value", _elements(bool_wrong))

    def test_types_exactes_fermees_avant_toute_operation(self) -> None:
        definition_cases = (
            _SubDefinition(**dataclasses.asdict(_DEFINITION)),
            _AttributeTrap(),
            _CallableTrap(),
            None,
        )
        for hostile in definition_cases:
            result = resolve_feature_flag_assignment(hostile, [_assignment()], _CONTEXT)
            self.assertEqual(result.status, "REFUSED", type(hostile))
            self.assertIn("feature_flags.evaluation.definition", _elements(result))
        self.assertEqual(ATTR_READS, [])
        for hostile in (
            _SubContext(**{name: getattr(_CONTEXT, name) for name in CONTEXT_FIELDS}),
            _AttributeTrap(),
            _CallableTrap(),
            None,
        ):
            result = resolve_feature_flag_assignment(_DEFINITION, [_assignment()], hostile)
            self.assertEqual(result.status, "REFUSED", type(hostile))
            self.assertIn("feature_flags.evaluation.contexte", _elements(result))
        self.assertEqual(ATTR_READS, [])
        for container in (_IterTrap(), {"a": 1}, iter(()), None, _CallableTrap()):
            result = resolve_feature_flag_assignment(_DEFINITION, container, _CONTEXT)
            self.assertEqual(result.status, "REFUSED", type(container))
        self.assertEqual(ITER_CALLS, [])
        for item in (
            _SubAssignment(**dataclasses.asdict(_assignment())),
            _AttributeTrap(),
            _CallableTrap(),
        ):
            result = resolve_feature_flag_assignment(_DEFINITION, [item], _CONTEXT)
            self.assertEqual(result.status, "REFUSED", type(item))
            self.assertIn("feature_flags.assignments.entree", _elements(result))
        self.assertEqual(ATTR_READS + EQ_CALLS + HASH_CALLS + CALL_CALLS, [])

    def test_objet_hostile_ne_declenche_aucun_callback(self) -> None:
        trap = _CallableTrap()
        for overrides in (
            dict(value=trap),
            dict(selector_value=trap),
            dict(valid_from=trap),
            dict(updated_by=trap),
        ):
            result = resolve_feature_flag_assignment(
                _DEFINITION, [_assignment(**overrides)], _CONTEXT
            )
            self.assertEqual(result.status, "REFUSED", overrides)
        self.assertEqual(CALL_CALLS, [])

    def test_definition_hote_refusee_par_validateur_existants(self) -> None:
        result = resolve_feature_flag_assignment(
            _definition(flag_id="dark", expires_at="2028-01-01T00:00:00z"),
            [_assignment()],
            _CONTEXT,
        )
        self.assertEqual(result.status, "REFUSED")
        self.assertIn("feature_flags.flag_id", _elements(result))
        self.assertIn("feature_flags.expires_at", _elements(result))
        self.assertIsNone(result.assignment)

    def test_diagnostics_sans_echo_et_invariants(self) -> None:
        sentinel = "SENTINELLE-valeur"
        result = resolve_feature_flag_assignment(
            _definition(flag_id=f"bad space {sentinel}"),
            [_assignment(selector_value=sentinel, updated_by=sentinel)],
            _CONTEXT,
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
            len(ordered),
            len({(d.element, d.constraint, d.message) for d in ordered}),
        )
        self.assertEqual(
            EQ_CALLS + HASH_CALLS + ITER_CALLS + CALL_CALLS + ATTR_READS, []
        )


if __name__ == "__main__":
    unittest.main()
