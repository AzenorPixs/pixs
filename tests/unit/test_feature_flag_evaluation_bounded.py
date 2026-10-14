"""Tests unitaires de l'évaluation bornée des affectations (tâche 3.1).

Contrôlent le résultat figé à trois champs obligatoires, la fermeture des types
avant tout accès d'attribut ou comparaison, la gate de politique avant toute
valeur, le refus terminal sans repli des entrées invalides, des configurations
non supportées et des ambiguïtés, la préservation de ``False`` et du jeton
``VARIANT``, le classement ``STALE``/``ABSENT`` et le constat ``INVALID`` par le
seul champ machine interne. Aucune horloge, E/S ni callback n'est lu ou déclenché.
"""

from __future__ import annotations

import dataclasses
import itertools
import unittest
from dataclasses import replace
from unittest import mock

from pixs.kernel import feature_flags
from pixs.kernel.diagnostics import VALIDATE
from pixs.kernel.feature_flags import (
    FeatureFlagAssignment,
    FeatureFlagDefinition,
    FeatureFlagEvaluation,
    FeatureFlagEvaluationContext,
    _classify_no_match,
    evaluate_feature_flag_assignments_bounded,
    validate_feature_flag_assignment_expiry,
)

USE_KINDS = ("NON_SENSITIVE", "PERMISSION", "MUTATION", "PROTECTED_DATA", "CONTRACT")
SENSITIVE_USE_KINDS = ("PERMISSION", "MUTATION", "PROTECTED_DATA", "CONTRACT")

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
        return 7


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


def _definition(**overrides) -> FeatureFlagDefinition:
    fields = {
        "flag_id": "web.dark_mode",
        "flag_version": "2026.10-r1",
        "owner_component": "web-main",
        "purpose": "Déclarer l'option sombre du thème web.",
        "value_schema": "BOOLEAN",
        "default_value": True,
        "targeting_dimensions": ("INSTALLATION", "TENANT", "SCOPE"),
        "cohort_key": None,
        "prerequisites": (),
        "fallback_policy": "DENY",
        "expires_at": "2028-01-01T00:00:00Z",
        "audit_policy": "standard_audit",
    }
    fields.update(overrides)
    return FeatureFlagDefinition(**fields)


def _context(**overrides) -> FeatureFlagEvaluationContext:
    return replace(
        FeatureFlagEvaluationContext(
            installation="installation-principale",
            environment=None,
            tenant=None,
            scope=None,
            as_of="2026-06-01T00:00:00Z",
        ),
        **overrides,
    )


def _assignment(**overrides) -> FeatureFlagAssignment:
    fields = {
        "flag_id": "web.dark_mode",
        "selector": "INSTALLATION",
        "selector_value": "installation-principale",
        "value": True,
        "valid_from": "2026-01-01T00:00:00Z",
        "valid_until": "2027-01-01T00:00:00Z",
        "configuration_version": "cfg-1",
        "updated_by": "administrateur.1",
    }
    fields.update(overrides)
    return FeatureFlagAssignment(**fields)


def _elements(result: FeatureFlagEvaluation) -> set[str]:
    return {diagnostic.element for diagnostic in result.diagnostics}


def _texts(result: FeatureFlagEvaluation) -> list[str]:
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


class FeatureFlagEvaluationBoundedTests(unittest.TestCase):
    def setUp(self) -> None:
        for calls in (EQ_CALLS, HASH_CALLS, ATTR_READS, CALL_CALLS):
            calls.clear()

    def test_evaluation_gelee_trois_champs_obligatoires(self) -> None:
        fields = dataclasses.fields(FeatureFlagEvaluation)
        self.assertEqual(
            tuple(field.name for field in fields),
            ("status", "value", "diagnostics"),
        )
        for field in fields:
            self.assertIs(field.default, dataclasses.MISSING)
            self.assertIs(field.default_factory, dataclasses.MISSING)
        with self.assertRaises(TypeError):
            FeatureFlagEvaluation(status="REFUSED")
        with self.assertRaises(TypeError):
            FeatureFlagEvaluation("REFUSED", None, (), alias="x")
        result = evaluate_feature_flag_assignments_bounded(
            _definition(), [], _context(), "NON_SENSITIVE"
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            result.status = "DEFAULT"
        self.assertEqual(_elements(result), set())

    def test_selected_conserve_false_variant_et_tous_usages(self) -> None:
        for use_kind in USE_KINDS:
            result = evaluate_feature_flag_assignments_bounded(
                _definition(fallback_policy="DEFAULT"),
                [_assignment()],
                _context(),
                use_kind,
            )
            self.assertEqual(result.status, "SELECTED", use_kind)
            self.assertIs(result.value, True)
            self.assertEqual(result.diagnostics, ())
        false_case = evaluate_feature_flag_assignments_bounded(
            _definition(fallback_policy="DEFAULT", default_value=False),
            [_assignment(value=False)],
            _context(),
            "PERMISSION",
        )
        self.assertIs(false_case.value, False)
        variant = evaluate_feature_flag_assignments_bounded(
            _definition(value_schema="VARIANT", default_value="clair"),
            [_assignment(value="sombre")],
            _context(),
            "PROTECTED_DATA",
        )
        self.assertEqual(variant.status, "SELECTED")
        self.assertEqual(variant.value, "sombre")

    def test_politique_inconnue_refuse_avant_toute_valeur(self) -> None:
        for policy in ("deny", "Deny", "fail_closed", "retry_later", "DEFAULT_x"):
            result = evaluate_feature_flag_assignments_bounded(
                _definition(fallback_policy=policy, default_value=True),
                [_assignment()],
                _context(),
                "NON_SENSITIVE",
            )
            self.assertEqual(result.status, "REFUSED", policy)
            self.assertIsNone(result.value)
            self.assertEqual(
                _elements(result), {"feature_flags.evaluation_bounded.policy"}, policy
            )

    def test_absence_replie_selon_politique_et_usage(self) -> None:
        for use_kind in USE_KINDS:
            refused = evaluate_feature_flag_assignments_bounded(
                _definition(fallback_policy="DENY", default_value=True),
                [],
                _context(),
                use_kind,
            )
            self.assertEqual(refused.status, "REFUSED", use_kind)
            self.assertIsNone(refused.value)
            default = evaluate_feature_flag_assignments_bounded(
                _definition(fallback_policy="DEFAULT", default_value=False),
                [_assignment(valid_from="2026-09-01T00:00:00Z")],
                _context(),
                use_kind,
            )
            if use_kind == "NON_SENSITIVE":
                self.assertEqual(default.status, "DEFAULT", use_kind)
                self.assertIs(default.value, False)
                self.assertEqual(default.diagnostics, ())
            else:
                self.assertEqual(default.status, "REFUSED", use_kind)
                self.assertIsNone(default.value)
                self.assertEqual(
                    _elements(default), {"feature_flags.fallback.sensible"}
                )
        mismatch = evaluate_feature_flag_assignments_bounded(
            _definition(fallback_policy="DEFAULT"),
            [_assignment(selector_value="autre-installation")],
            _context(),
            "NON_SENSITIVE",
        )
        self.assertEqual(mismatch.status, "DEFAULT")
        hidden = evaluate_feature_flag_assignments_bounded(
            _definition(targeting_dimensions=("TENANT",), fallback_policy="DEFAULT"),
            [_assignment(selector="INSTALLATION")],
            _context(tenant=None),
            "NON_SENSITIVE",
        )
        self.assertEqual(hidden.status, "DEFAULT")

    def test_fenetre_classe_stale_alors_que_futur_absent(self) -> None:
        definition = _definition()
        context = _context()
        reference = __import__("datetime").datetime.fromisoformat(context.as_of)
        stale = _classify_no_match(
            definition,
            [_assignment(valid_until="2026-06-01T00:00:00Z")],
            context,
            reference,
        )
        self.assertEqual(stale, "STALE")
        past = _classify_no_match(
            definition,
            [_assignment(
                valid_from="2025-01-01T00:00:00Z",
                valid_until="2025-06-01T00:00:00Z",
            )],
            context,
            reference,
        )
        self.assertEqual(past, "STALE")
        future = _classify_no_match(
            definition,
            [_assignment(valid_from="2026-09-01T00:00:00Z")],
            context,
            reference,
        )
        self.assertEqual(future, "ABSENT")
        other_dimension = _classify_no_match(
            definition,
            [_assignment(selector="TENANT", selector_value="tenant-a")],
            context,
            reference,
        )
        self.assertEqual(other_dimension, "ABSENT")

    def test_melange_expire_et_futur_classe_stale(self) -> None:
        context = _context()
        reference = __import__("datetime").datetime.fromisoformat(context.as_of)
        expired = _assignment(valid_until="2026-05-01T00:00:00Z")
        upcoming = _assignment(
            valid_from="2026-09-01T00:00:00Z",
            configuration_version="cfg-2",
        )
        for order in itertools.permutations((expired, upcoming)):
            self.assertEqual(
                _classify_no_match(_definition(), list(order), context, reference),
                "STALE",
            )
        public = evaluate_feature_flag_assignments_bounded(
            _definition(fallback_policy="DEFAULT", default_value=True),
            [upcoming, expired],
            context,
            "NON_SENSITIVE",
        )
        self.assertEqual(public.status, "DEFAULT")
        self.assertIs(public.value, True)

    def test_incompatibilite_de_valeur_constatee_invalid_replie(self) -> None:
        for use_kind, policy, expected in (
            ("NON_SENSITIVE", "DEFAULT", "DEFAULT"),
            ("NON_SENSITIVE", "DENY", "REFUSED"),
            ("PERMISSION", "DEFAULT", "REFUSED"),
        ):
            result = evaluate_feature_flag_assignments_bounded(
                _definition(
                    value_schema="BOOLEAN",
                    default_value=False,
                    fallback_policy=policy,
                ),
                [_assignment(value="clair")],
                _context(),
                use_kind,
            )
            self.assertEqual(result.status, expected, (use_kind, policy))
            if expected == "DEFAULT":
                self.assertIs(result.value, False)
            else:
                self.assertIsNone(result.value)
        refused = evaluate_feature_flag_assignments_bounded(
            _definition(value_schema="BOOLEAN", default_value=False),
            [_assignment(value="clair")],
            _context(),
            "NON_SENSITIVE",
        )
        self.assertEqual(refused.status, "REFUSED")
        self.assertIsNone(refused.value)
        self.assertNotIn("feature_flags.evaluation.value", _elements(refused))

    def test_ambiguite_refus_terminal_sans_repli(self) -> None:
        result = evaluate_feature_flag_assignments_bounded(
            _definition(fallback_policy="DEFAULT", default_value=True),
            [_assignment(), _assignment(configuration_version="cfg-2")],
            _context(),
            "NON_SENSITIVE",
        )
        self.assertEqual(result.status, "REFUSED")
        self.assertIsNone(result.value)
        self.assertEqual(
            _elements(result), {"feature_flags.evaluation.candidats"}
        )

    def test_configuration_non_supportee_refus_terminal_sans_defaut(self) -> None:
        for overrides in (
            dict(cohort_key="beta.cohorte-x"),
            dict(prerequisites=("web-main",)),
        ):
            result = evaluate_feature_flag_assignments_bounded(
                _definition(fallback_policy="DEFAULT", default_value=True, **overrides),
                [_assignment()],
                _context(),
                "NON_SENSITIVE",
            )
            self.assertEqual(result.status, "REFUSED", overrides)
            self.assertIsNone(result.value)
            self.assertEqual(
                _elements(result),
                {"feature_flags.evaluation_bounded.configuration"},
                overrides,
            )

    def test_entrees_hostiles_fermees_sans_callback_ni_repli(self) -> None:
        for hostile in (
            _SubDefinition(**dataclasses.asdict(_definition())),
            _AttributeTrap(),
            _CallableTrap(),
            None,
        ):
            result = evaluate_feature_flag_assignments_bounded(
                hostile, [_assignment()], _context(), "NON_SENSITIVE"
            )
            self.assertEqual(result.status, "REFUSED", type(hostile))
            self.assertIsNone(result.value)
            self.assertIn(
                "feature_flags.evaluation_bounded.definition", _elements(result)
            )
        self.assertEqual(ATTR_READS + EQ_CALLS + HASH_CALLS + CALL_CALLS, [])
        for hostile in (
            _SubContext(
                **{name: getattr(_context(), name) for name in (
                    "installation", "environment", "tenant", "scope", "as_of",
                )}
            ),
            _AttributeTrap(),
            None,
        ):
            result = evaluate_feature_flag_assignments_bounded(
                _definition(), [_assignment()], hostile, "NON_SENSITIVE"
            )
            self.assertEqual(result.status, "REFUSED", type(hostile))
            self.assertIn(
                "feature_flags.evaluation_bounded.contexte", _elements(result)
            )
        self.assertEqual(ATTR_READS + EQ_CALLS + HASH_CALLS + CALL_CALLS, [])
        for hostile in (_TrapStr("NON_SENSITIVE"), "non_sensitive", "", None, 7):
            result = evaluate_feature_flag_assignments_bounded(
                _definition(fallback_policy="DEFAULT"), [], _context(), hostile
            )
            self.assertEqual(result.status, "REFUSED", hostile)
            self.assertIn(
                "feature_flags.evaluation_bounded.use_kind", _elements(result)
            )
        self.assertEqual(EQ_CALLS + HASH_CALLS + CALL_CALLS + ATTR_READS, [])
        trap_item = _AttributeTrap()
        for container in (_TrapListTrap([_assignment()]), {"a": 1}, trap_item, None):
            result = evaluate_feature_flag_assignments_bounded(
                _definition(fallback_policy="DEFAULT", default_value=True),
                container,
                _context(),
                "NON_SENSITIVE",
            )
            self.assertEqual(result.status, "REFUSED", type(container))
            self.assertIsNone(result.value)
            self.assertNotIn("SELECTED", result.status)
        self.assertEqual(ATTR_READS + EQ_CALLS + HASH_CALLS + CALL_CALLS, [])

    def test_diagnostics_stables_sans_echo_et_sans_mutation(self) -> None:
        sentinel = "SENTINELLE-bornee"
        definition = _definition(fallback_policy="DEFAULT")
        assignments = [_assignment(selector_value="installation-principale")]
        context = _context()
        snapshot = (
            dataclasses.astuple(definition),
            tuple(dataclasses.astuple(item) for item in assignments),
            dataclasses.astuple(context),
        )
        result = evaluate_feature_flag_assignments_bounded(
            _definition(
                flag_id=f"bad space {sentinel}",
                fallback_policy="DEFAULT",
            ),
            assignments,
            context,
            "NON_SENSITIVE",
        )
        self.assertEqual(result.status, "REFUSED")
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
            snapshot,
            (
                dataclasses.astuple(definition),
                tuple(dataclasses.astuple(item) for item in assignments),
                dataclasses.astuple(context),
            ),
        )
        stable = evaluate_feature_flag_assignments_bounded(
            definition, assignments, context, "NON_SENSITIVE"
        )
        self.assertEqual(stable.status, "SELECTED")
        self.assertEqual(
            stable,
            evaluate_feature_flag_assignments_bounded(
                definition, assignments, context, "NON_SENSITIVE"
            ),
        )
        candidates = (
            assignments[0],
            _assignment(selector_value="autre-installation"),
            _assignment(valid_until="2026-05-01T00:00:00Z"),
        )
        for order in itertools.permutations(candidates):
            self.assertEqual(
                evaluate_feature_flag_assignments_bounded(
                    definition, list(order), context, "NON_SENSITIVE"
                ),
                stable,
            )
        duplicate = evaluate_feature_flag_assignments_bounded(
            definition, assignments * 2, context, "NON_SENSITIVE"
        )
        self.assertEqual(duplicate.status, "REFUSED")
        self.assertIsNone(duplicate.value)

    def test_gate_expiree_ne_produit_que_le_diagnostic_constant(self) -> None:
        for expired in (
            "2026-06-01T00:00:00Z",
            "2026-05-31T23:59:59.999999+00:00",
            "2026-01-01T00:00:00Z",
        ):
            diagnostics = validate_feature_flag_assignment_expiry(
                _definition(expires_at=expired), _context()
            )
            self.assertEqual(
                {d.element for d in diagnostics},
                {"feature_flags.expiry.expires_at"},
                expired,
            )
            for diagnostic in diagnostics:
                self.assertEqual(diagnostic.step, VALIDATE)
                self.assertEqual(diagnostic.message, diagnostic.constraint)
        for later in ("2026-06-01T00:00:00.000001Z", "2026-06-01T00:00:01+00:00"):
            self.assertEqual(
                validate_feature_flag_assignment_expiry(
                    _definition(expires_at=later), _context()
                ),
                (),
                later,
            )

    def test_gate_refuse_entree_invalide_sans_decision_d_expiration(self) -> None:
        diagnostics = validate_feature_flag_assignment_expiry(
            _definition(flag_id="dark", expires_at="2026-06-01T00:00:00Z"),
            _context(),
        )
        elements = {diagnostic.element for diagnostic in diagnostics}
        self.assertIn("feature_flags.flag_id", elements)
        self.assertNotIn("feature_flags.expiry.expires_at", elements)
        for as_of in ("2026-06-01T00:00:00", "2026-06-01T00:00:00+02:00", "x"):
            bad = validate_feature_flag_assignment_expiry(
                _definition(), _context(as_of=as_of)
            )
            self.assertEqual(
                {d.element for d in bad}, {"feature_flags.evaluation.as_of"}, as_of
            )
        for hostile in (
            _SubDefinition(**dataclasses.asdict(_definition())),
            _AttributeTrap(),
            _CallableTrap(),
            None,
        ):
            refused = validate_feature_flag_assignment_expiry(hostile, _context())
            self.assertIn(
                "feature_flags.expiry.definition",
                {d.element for d in refused},
            )
        for hostile in (_SubContext(**dataclasses.asdict(_context())), _AttributeTrap(), _CallableTrap(), None):
            refused = validate_feature_flag_assignment_expiry(_definition(), hostile)
            self.assertIn(
                "feature_flags.expiry.contexte", {d.element for d in refused}
            )
        sentinel = "SENTINELLE-expiry"
        invalid = validate_feature_flag_assignment_expiry(
            _definition(expires_at=sentinel), _context(as_of=sentinel)
        )
        self.assertNotIn("feature_flags.expiry.expires_at", {d.element for d in invalid})
        for diagnostic in invalid:
            self.assertNotIn(sentinel, str(diagnostic))
        self.assertEqual(ATTR_READS + EQ_CALLS + HASH_CALLS + CALL_CALLS, [])

    def test_definition_expiree_ne_restitue_jamais_la_valeur_selectionnee(self) -> None:
        for schema, default, assigned in (("BOOLEAN", False, True), ("VARIANT", "clair", "sombre")):
            for policy in ("DENY", "DEFAULT"):
                for use_kind in USE_KINDS:
                    with self.subTest(schema=schema, policy=policy, use_kind=use_kind):
                        result = evaluate_feature_flag_assignments_bounded(
                            _definition(value_schema=schema, default_value=default,
                                        fallback_policy=policy, expires_at="2026-06-01T00:00:00+00:00"),
                            [_assignment(value=assigned)], _context(), use_kind,
                        )
                        allowed_default = policy == "DEFAULT" and use_kind == "NON_SENSITIVE"
                        self.assertEqual(result.status, "DEFAULT" if allowed_default else "REFUSED")
                        if allowed_default:
                            if schema == "BOOLEAN":
                                self.assertIs(result.value, False)
                            else:
                                self.assertEqual(result.value, "clair")
                        else:
                            self.assertIsNone(result.value)
                        expected = {"feature_flags.expiry.expires_at"}
                        if policy == "DEFAULT" and use_kind in SENSITIVE_USE_KINDS:
                            expected.add("feature_flags.fallback.sensible")
                        self.assertEqual(_elements(result), expected)

    def test_no_match_et_incompatibilite_expirees_recoivent_stale(self) -> None:
        for assignments in (
            [_assignment()], [],
            [_assignment(valid_from="2026-09-01T00:00:00Z")],
            [_assignment(valid_until="2026-06-01T00:00:00Z")],
            [_assignment(value="clair")],
        ):
            with mock.patch.object(
                feature_flags, "resolve_feature_flag_fallback",
                wraps=feature_flags.resolve_feature_flag_fallback,
            ) as spy:
                result = evaluate_feature_flag_assignments_bounded(
                    _definition(fallback_policy="DEFAULT", default_value=False,
                                expires_at="2026-06-01T00:00:00Z"),
                    assignments, _context(), "NON_SENSITIVE",
                )
            self.assertEqual([call.args[2] for call in spy.call_args_list], ["STALE"])
            self.assertEqual(result.status, "DEFAULT")
            self.assertIs(result.value, False)
            self.assertEqual(_elements(result), {"feature_flags.expiry.expires_at"})

    def test_causes_du_repli_non_expire_restent_inchangees(self) -> None:
        context = _context()
        cases = (
            ([], "ABSENT"),
            ([_assignment(valid_until="2026-06-01T00:00:00Z")], "STALE"),
            ([_assignment(valid_from="2026-09-01T00:00:00Z")], "ABSENT"),
            ([_assignment(value="clair")], "INVALID"),
        )
        for assignments, expected in cases:
            with mock.patch.object(
                feature_flags,
                "resolve_feature_flag_fallback",
                wraps=feature_flags.resolve_feature_flag_fallback,
            ) as spy:
                evaluate_feature_flag_assignments_bounded(
                    _definition(fallback_policy="DEFAULT", default_value=False),
                    assignments,
                    context,
                    "NON_SENSITIVE",
                )
            self.assertEqual(
                [call.args[2] for call in spy.call_args_list], [expected], expected
            )

    def test_refus_terminal_preserve_meme_sur_definition_expiree(self) -> None:
        context = _context()
        expired = "2026-06-01T00:00:00Z"
        for overrides in (
            dict(cohort_key="beta.cohorte-x"),
            dict(prerequisites=("web-main",)),
        ):
            result = evaluate_feature_flag_assignments_bounded(
                _definition(
                    fallback_policy="DEFAULT", expires_at=expired, **overrides
                ),
                [_assignment()],
                context,
                "NON_SENSITIVE",
            )
            self.assertEqual(result.status, "REFUSED", overrides)
            self.assertIsNone(result.value)
            self.assertEqual(
                {d.element for d in result.diagnostics},
                {"feature_flags.evaluation_bounded.configuration"},
                overrides,
            )
        policy = evaluate_feature_flag_assignments_bounded(
            _definition(fallback_policy="fail_closed", expires_at=expired),
            [_assignment()],
            context,
            "NON_SENSITIVE",
        )
        self.assertEqual(
            {d.element for d in policy.diagnostics},
            {"feature_flags.evaluation_bounded.policy"},
        )
        ambiguous = evaluate_feature_flag_assignments_bounded(
            _definition(fallback_policy="DEFAULT", expires_at=expired),
            [_assignment(), _assignment(configuration_version="cfg-2")],
            context,
            "NON_SENSITIVE",
        )
        self.assertEqual(
            {d.element for d in ambiguous.diagnostics},
            {"feature_flags.evaluation.candidats"},
        )
        invalid = evaluate_feature_flag_assignments_bounded(
            _definition(flag_id="dark", expires_at=expired),
            [_assignment()],
            context,
            "NON_SENSITIVE",
        )
        invalid_elements = {d.element for d in invalid.diagnostics}
        self.assertIn("feature_flags.flag_id", invalid_elements)
        self.assertNotIn("feature_flags.expiry.expires_at", invalid_elements)
        self.assertEqual(ATTR_READS + EQ_CALLS + CALL_CALLS, [])

    def test_diagnostics_expirees_stables_tri_etsans_mutation(self) -> None:
        context = _context()
        definition = _definition(
            fallback_policy="DEFAULT", expires_at="2026-06-01T00:00:00Z"
        )
        assignments = [_assignment(), _assignment(flag_id="autre.drapeau")]
        snapshot = (
            dataclasses.astuple(definition),
            tuple(dataclasses.astuple(item) for item in assignments),
            dataclasses.astuple(context),
        )
        first = evaluate_feature_flag_assignments_bounded(
            definition, assignments, context, "PROTECTED_DATA"
        )
        self.assertEqual(
            first,
            evaluate_feature_flag_assignments_bounded(
                definition, assignments, context, "PROTECTED_DATA"
            ),
        )
        for order in itertools.permutations(assignments):
            self.assertEqual(
                evaluate_feature_flag_assignments_bounded(
                    definition, list(order), context, "PROTECTED_DATA"
                ),
                first,
            )
        ordered = list(first.diagnostics)
        self.assertEqual(
            ordered,
            sorted(ordered, key=lambda d: (d.element, d.constraint, d.message)),
        )
        self.assertEqual(
            len(ordered), len({(d.element, d.constraint) for d in ordered})
        )
        self.assertEqual(
            snapshot,
            (
                dataclasses.astuple(definition),
                tuple(dataclasses.astuple(item) for item in assignments),
                dataclasses.astuple(context),
            ),
        )
        self.assertEqual(
            {d.element for d in first.diagnostics},
            {"feature_flags.expiry.expires_at", "feature_flags.fallback.sensible"},
        )


    def test_borne_fractionnelle_equivalente_utc_avant_egal_apres(self) -> None:
        for suffix in ("Z", "+00:00"):
            for fraction, expired in (("123455", False), ("123456", True), ("123457", True)):
                with self.subTest(suffix=suffix, fraction=fraction):
                    definition = _definition(fallback_policy="DEFAULT", default_value=False,
                                             expires_at="2026-06-01T00:00:00.123456Z")
                    context = _context(as_of="2026-06-01T00:00:00." + fraction + suffix)
                    gate = validate_feature_flag_assignment_expiry(definition, context)
                    self.assertEqual(bool(gate), expired)
                    result = evaluate_feature_flag_assignments_bounded(
                        definition, [_assignment(value=True)], context, "NON_SENSITIVE"
                    )
                    self.assertEqual(result.status, "DEFAULT" if expired else "SELECTED")
                    self.assertIs(result.value, False if expired else True)
                    self.assertEqual(_elements(result), {"feature_flags.expiry.expires_at"} if expired else set())

class _TrapListTrap(list):
    def __eq__(self, other):
        EQ_CALLS.append("container")
        return list.__eq__(self, other)

    def __hash__(self):
        HASH_CALLS.append("container")
        return 0

    def __iter__(self):
        ATTR_READS.append("container_iter")
        return list.__iter__(self)


if __name__ == "__main__":
    unittest.main()
