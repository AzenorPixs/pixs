"""Frontières 2.1a : nominal, liaisons, horodatages canoniques, fraîcheur, bornes, étrangers, bool/int, catalogue, fuites."""
import unittest
from dataclasses import replace

from pixs.agent.contracts import (
    AgentManagementInstruction,
    AgentManagementResult,
    AgentManagementState,
    AgentParam,
    AgentParamSpec,
    AgentValidationContext,
    AllowedCatalogEntry,
    validate_agent_instruction,
    validate_agent_result,
    validate_agent_state,
)
from pixs.core.scope import ScopeContext, ScopeType


class Evil:
    def __eq__(self, other):
        raise AssertionError("appel hostile eq")

    def __hash__(self):
        raise AssertionError("appel hostile hash")


def _scope():
    return ScopeContext(ScopeType.TENANT, "tenant-synth-1", "scope-synth-1")


def _catalog():
    return (
        AllowedCatalogEntry(
            operation="synth.sys.nop",
            version="1.0.0",
            params=(
                AgentParamSpec(name="message", kind="str", max_len=32, int_min=None, int_max=None, required=True),
                AgentParamSpec(name="retries", kind="int", max_len=None, int_min=0, int_max=100, required=False),
                AgentParamSpec(name="force", kind="bool", max_len=None, int_min=None, int_max=None, required=False),
            ),
        ),
    )


def _context(**over):
    fields = {
        "expected_actor": "actor-synth-1",
        "expected_scope": _scope(),
        "expected_target": "pa-synth-1",
        "expected_generation": 7,
        "expected_operation": "synth.sys.nop",
        "expected_version": "1.0.0",
        "expected_operation_id": "op-synth-1",
        "expected_idempotency_key": "key-synth-1",
        "expected_correlation_ids": ("corr-1",),
        "now_iso": "2030-01-01T00:00:00Z",
        "mandate_proof": "mandate-synth-1",
        "expected_origin_proof": "origin-synth-1",
        "expected_confirmation_proof": "confirm-synth-1",
        "max_id_len": 64,
        "max_doc_len": 1024,
        "max_ids": 8,
        "max_params": 8,
        "max_observation_age_seconds": 3600,
    }
    fields.update(over)
    return AgentValidationContext(**fields)


def _kwargs(**over):
    fields = {
        "schema_version": "1.0.0",
        "operation_id": "op-synth-1",
        "catalog_operation": "synth.sys.nop",
        "catalog_version": "1.0.0",
        "initial_actor": "actor-synth-1",
        "scope_context": _scope(),
        "pa_target": "pa-synth-1",
        "expected_generation": 7,
        "mandate_ref": "mandate-synth-1",
        "expires_at": "2030-01-01T01:00:00Z",
        "correlation_ids": ("corr-1",),
        "causation_ids": (),
        "idempotency_key": "key-synth-1",
        "params": (
            AgentParam(name="message", kind="str", str_value="bonjour", int_value=None, bool_value=None),
        ),
    }
    fields.update(over)
    return fields


class InstructionCases(unittest.TestCase):
    def test_nominal_sans_diagnostic(self):
        inst = AgentManagementInstruction(**_kwargs())
        self.assertEqual(validate_agent_instruction(inst, _catalog(), _context()), [])

    def test_schema_kind_outcome_avant_comparaison_sans_appel_hostile(self):
        inst = AgentManagementInstruction(**_kwargs(schema_version=Evil()))
        self.assertTrue(validate_agent_instruction(inst, _catalog(), _context()))
        inst = AgentManagementInstruction(**_kwargs(params=(AgentParam(name="message", kind=Evil(), str_value="x", int_value=None, bool_value=None),)))
        self.assertTrue(validate_agent_instruction(inst, _catalog(), _context()))
        res = AgentManagementResult(scope_context=_scope(), operation_id="op-synth-1", pa_target="pa-synth-1", generation=7, outcome=Evil(), correlation_ids=("corr-1",), occurred_at="2029-12-31T23:00:00Z", origin_proof="origin-synth-1")
        self.assertTrue(validate_agent_result(res, _context()))

    def test_nom_non_hashable_et_sous_classe_refusés_sans_typeerror(self):
        inst = AgentManagementInstruction(**_kwargs(params=(AgentParam(name=["liste"], kind="str", str_value="x", int_value=None, bool_value=None),)))
        diags = validate_agent_instruction(inst, _catalog(), _context())
        self.assertTrue(any("param.name" in d.element for d in diags))

        class SubStr(str):
            pass

        inst = AgentManagementInstruction(**_kwargs(operation_id=SubStr("op-synth-1")))
        diags = validate_agent_instruction(inst, _catalog(), _context())
        self.assertTrue(any("operation_id" in d.element for d in diags))

    def test_liaisons_opération_version_idempotence_corrélation(self):
        for field, ctx_field in (("catalog_operation", "expected_operation"), ("catalog_version", "expected_version"), ("operation_id", "expected_operation_id"), ("idempotency_key", "expected_idempotency_key")):
            inst = AgentManagementInstruction(**_kwargs(**{field: "autre"}))
            diags = validate_agent_instruction(inst, _catalog(), _context(**{ctx_field: "autre-ctx-lié"}))
            self.assertTrue(diags)
        inst = AgentManagementInstruction(**_kwargs(correlation_ids=("autre",)))
        diags = validate_agent_instruction(inst, _catalog(), _context())
        self.assertTrue(any("binding.correlation" in d.element for d in diags))
        inst = AgentManagementInstruction(**_kwargs(initial_actor="autre"))
        self.assertTrue(any("binding.actor" in d.element for d in validate_agent_instruction(inst, _catalog(), _context())))
        other_scope = ScopeContext(ScopeType.TENANT, "tenant-synth-1", "autre")
        inst = AgentManagementInstruction(**_kwargs(scope_context=other_scope))
        self.assertTrue(any("binding.scope" in d.element for d in validate_agent_instruction(inst, _catalog(), _context())))

    def test_expiré_et_non_canonique_refusés(self):
        inst = AgentManagementInstruction(**_kwargs(expires_at="2029-12-31T23:59:59Z"))
        self.assertTrue(any("expires_at" in d.element for d in validate_agent_instruction(inst, _catalog(), _context())))
        inst = AgentManagementInstruction(**_kwargs(expires_at="2030-1-01T01:00:00Z"))
        self.assertTrue(any("expires_at" in d.element for d in validate_agent_instruction(inst, _catalog(), _context())))
        inst = AgentManagementInstruction(**_kwargs(expires_at="pas-une-date"))
        self.assertTrue(any("expires_at" in d.element for d in validate_agent_instruction(inst, _catalog(), _context())))

    def test_catalogue_inconnu_et_champ_étranger(self):
        inst = AgentManagementInstruction(**_kwargs(catalog_operation="inconnu"))
        self.assertTrue(any(d.element == "agent.instruction.catalog" for d in validate_agent_instruction(inst, _catalog(), _context())))
        foreign = (
            AgentParam(name="message", kind="str", str_value="x", int_value=None, bool_value=None),
            AgentParam(name="intrus", kind="str", str_value="x", int_value=None, bool_value=None),
        )
        inst = AgentManagementInstruction(**_kwargs(params=foreign))
        self.assertTrue(any("param.name" in d.element for d in validate_agent_instruction(inst, _catalog(), _context())))
        with self.assertRaises(TypeError):
            AgentManagementInstruction(**{**_kwargs(), "extra": "champ-étranger"})

    def test_bornes_fournies_sans_plafond_4096(self):
        ctx = _context(max_id_len=10000)
        big_catalog = (AllowedCatalogEntry(operation="synth.sys.nop", version="1.0.0", params=(AgentParamSpec(name="message", kind="str", max_len=5000, int_min=None, int_max=None, required=True),)),)
        big = AgentParam(name="message", kind="str", str_value="x" * 5000, int_value=None, bool_value=None)
        inst = AgentManagementInstruction(**_kwargs(params=(big,)))
        self.assertEqual(validate_agent_instruction(inst, big_catalog, ctx), [])
        too = AgentParam(name="message", kind="str", str_value="x" * 5001, int_value=None, bool_value=None)
        inst = AgentManagementInstruction(**_kwargs(params=(too,)))
        self.assertTrue(validate_agent_instruction(inst, big_catalog, ctx))

    def test_bool_int_et_représentation_sans_fuite(self):
        bad = AgentParam(name="force", kind="bool", str_value=None, int_value=1, bool_value=None)
        base = (AgentParam(name="message", kind="str", str_value="x", int_value=None, bool_value=None), bad)
        inst = AgentManagementInstruction(**_kwargs(params=base))
        self.assertTrue(validate_agent_instruction(inst, _catalog(), _context()))
        inst = AgentManagementInstruction(**_kwargs(expected_generation=True))
        self.assertTrue(any("expected_generation" in d.element for d in validate_agent_instruction(inst, _catalog(), _context())))
        text = repr(AgentManagementInstruction(**_kwargs())) + str(AgentManagementInstruction(**_kwargs()))
        self.assertIn("<redacted>", text)
        self.assertNotIn("actor-synth-1", text)
        self.assertNotIn("mandate-synth-1", text)


class ParameterBoundaryCases(unittest.TestCase):
    def test_entiers_et_booleens_nominaux_et_refus_aux_limites(self):
        message = AgentParam("message", "str", "x", None, None)
        for value in (0, 100):
            params = (message, AgentParam("retries", "int", None, value, None))
            self.assertEqual(validate_agent_instruction(AgentManagementInstruction(**_kwargs(params=params)), _catalog(), _context()), [])
        for value in (-1, 101, True, "1"):
            with self.subTest(value=value):
                params = (message, AgentParam("retries", "int", None, value, None))
                self.assertTrue(validate_agent_instruction(AgentManagementInstruction(**_kwargs(params=params)), _catalog(), _context()))
        for value in (True, False):
            params = (message, AgentParam("force", "bool", None, None, value))
            self.assertEqual(validate_agent_instruction(AgentManagementInstruction(**_kwargs(params=params)), _catalog(), _context()), [])

    def test_catalogue_hostile_manquant_duplique_et_requis(self):
        inst = AgentManagementInstruction(**_kwargs())
        for catalog in (None, (), (_catalog()[0], _catalog()[0])):
            self.assertTrue(validate_agent_instruction(inst, catalog, _context()))
        spec = replace(_catalog()[0].params[0], kind=Evil())
        self.assertTrue(validate_agent_instruction(inst, (replace(_catalog()[0], params=(spec,)),), _context()))
        self.assertTrue(validate_agent_instruction(AgentManagementInstruction(**_kwargs(params=())), _catalog(), _context()))
        duplicated = AgentManagementInstruction(**_kwargs(params=(inst.params[0], inst.params[0])))
        self.assertTrue(validate_agent_instruction(duplicated, _catalog(), _context()))

    def test_operation_valide_du_catalogue_hors_mandat_et_echeance_exacte(self):
        catalog = _catalog() + (AllowedCatalogEntry("synth.other", "1.0.0", ()),)
        other = AgentManagementInstruction(**_kwargs(catalog_operation="synth.other", params=()))
        self.assertTrue(any(d.element == "agent.instruction.binding.operation" for d in validate_agent_instruction(other, catalog, _context())))
        expired = AgentManagementInstruction(**_kwargs(expires_at=_context().now_iso))
        self.assertTrue(any("expires_at" in d.element for d in validate_agent_instruction(expired, _catalog(), _context())))


class StateResultCases(unittest.TestCase):
    def _state(self, **over):
        fields = {
            "operation_id": "op-synth-1",
            "pa_target": "pa-synth-1",
            "generation": 7,
            "scope_context": _scope(),
            "desired_doc": "souhait-synth",
            "observed_doc": "appliqué-synth",
            "observed_at": "2029-12-31T23:00:00Z",
            "last_known_doc": "connu-synth",
            "last_known_at": "2029-12-31T23:30:00Z",
            "confirmation_proof": None,
        }
        fields.update(over)
        return AgentManagementState(**fields)

    def test_confirmation_exige_preuve_attendue_fraîche(self):
        self.assertEqual(validate_agent_state(self._state(), _context()), [])
        ok = self._state(confirmation_proof="confirm-synth-1")
        self.assertEqual(validate_agent_state(ok, _context()), [])
        arbitraire = self._state(confirmation_proof="quelconque")
        self.assertTrue(any("confirmation" in d.element for d in validate_agent_state(arbitraire, _context())))
        périmée = self._state(observed_at="2029-12-30T00:00:00Z", last_known_at="2029-12-30T01:00:00Z", confirmation_proof="confirm-synth-1")
        self.assertTrue(any("confirmation" in d.element for d in validate_agent_state(périmée, _context())))
        sans_observé = self._state(observed_doc=None, observed_at=None, last_known_doc=None, last_known_at=None, confirmation_proof="confirm-synth-1")
        self.assertTrue(any("confirmation" in d.element for d in validate_agent_state(sans_observé, _context())))

    def test_historique_accepté_et_futur_refusé(self):
        vieux = self._state(observed_at="2020-01-01T00:00:00Z", last_known_at="2020-01-02T00:00:00Z")
        self.assertEqual(validate_agent_state(vieux, _context()), [])
        futur = self._state(observed_at="2031-01-01T00:00:00Z")
        self.assertTrue(any("observed_at" in d.element for d in validate_agent_state(futur, _context())))
        non_canonique = self._state(observed_at="2029-12-31T23:00:00")
        self.assertTrue(any("observed_at" in d.element for d in validate_agent_state(non_canonique, _context())))

    def test_résultat_autre_opération_refusé_et_unknown_distinct(self):
        base = {"operation_id": "op-synth-1", "pa_target": "pa-synth-1", "generation": 7, "scope_context": _scope(), "correlation_ids": ("corr-1",), "occurred_at": "2029-12-31T23:00:00Z"}
        unknown = AgentManagementResult(outcome="unknown", origin_proof=None, **base)
        self.assertEqual(validate_agent_result(unknown, _context()), [])
        self.assertTrue(validate_agent_result(AgentManagementResult(outcome="unknown", origin_proof="preuve", **base), _context()))
        confirmé = AgentManagementResult(outcome="confirmed", origin_proof="origin-synth-1", **base)
        self.assertEqual(validate_agent_result(confirmé, _context()), [])
        self.assertTrue(validate_agent_result(AgentManagementResult(outcome="confirmed", origin_proof="quelconque", **base), _context()))
        autre_op = AgentManagementResult(outcome="confirmed", origin_proof="origin-synth-1", **{**base, "operation_id": "op-autre"})
        self.assertTrue(any("binding.operation_id" in d.element for d in validate_agent_result(autre_op, _context())))
        futur = AgentManagementResult(outcome="ack", origin_proof="origin-synth-1", **{**base, "occurred_at": "2031-01-01T00:00:00Z"})
        self.assertTrue(any("occurred_at" in d.element for d in validate_agent_result(futur, _context())))


    def test_tenant_distinct_et_types_hostiles_des_observations_refuses(self):
        other_scope = ScopeContext(ScopeType.TENANT, "autre-tenant", "scope-synth-1")
        state = self._state(scope_context=other_scope)
        self.assertTrue(any("binding.scope" in d.element for d in validate_agent_state(state, _context())))
        result = AgentManagementResult(
            "op-synth-1", "pa-synth-1", 7, other_scope, "confirmed",
            ("corr-1",), "2029-12-31T23:00:00Z", "origin-synth-1",
        )
        self.assertTrue(any("binding.scope" in d.element for d in validate_agent_result(result, _context())))
        for field in ("operation_id", "pa_target", "generation"):
            with self.subTest(field=field):
                self.assertTrue(validate_agent_state(self._state(**{field: Evil()}), _context()))
                self.assertTrue(validate_agent_result(replace(result, **{field: Evil()}), _context()))

    def test_absence_de_preuve_observee_ne_force_pas_une_preuve_inventee(self):
        context = _context(expected_origin_proof=None, expected_confirmation_proof=None)
        desired_only = self._state(
            observed_doc=None, observed_at=None, last_known_doc=None, last_known_at=None,
        )
        self.assertEqual(validate_agent_state(desired_only, context), [])
        self.assertTrue(validate_agent_state(self._state(confirmation_proof="arbitraire"), context))
        unknown = AgentManagementResult(
            "op-synth-1", "pa-synth-1", 7, _scope(), "unknown",
            ("corr-1",), "2029-12-31T23:00:00Z", None,
        )
        self.assertEqual(validate_agent_result(unknown, context), [])
        self.assertTrue(validate_agent_result(replace(unknown, outcome="confirmed", origin_proof="arbitraire"), context))

    def test_nom_parametre_borne_et_contexte_sans_borne_refuses(self):
        inst = AgentManagementInstruction(**_kwargs(params=(AgentParam("x" * 65, "str", "x", None, None),)))
        self.assertTrue(validate_agent_instruction(inst, _catalog(), _context()))
        for key in ("max_id_len", "max_doc_len", "max_ids", "max_params", "max_observation_age_seconds"):
            with self.subTest(key=key):
                self.assertTrue(validate_agent_instruction(AgentManagementInstruction(**_kwargs()), _catalog(), _context(**{key: 0})))


    def test_mandat_absent_ou_incoherent_refuse(self):
        instruction = AgentManagementInstruction(**_kwargs(mandate_ref="mandat-different"))
        self.assertTrue(any(d.element == "agent.instruction.binding.mandate" for d in validate_agent_instruction(instruction, _catalog(), _context())))
        for proof in (None, "", Evil()):
            with self.subTest(proof_type=type(proof).__name__):
                self.assertTrue(any(d.element == "agent.context" for d in validate_agent_instruction(AgentManagementInstruction(**_kwargs()), _catalog(), _context(mandate_proof=proof))))

    def test_immutabilite_et_diagnostics_sans_valeurs(self):
        from dataclasses import FrozenInstanceError

        instruction = AgentManagementInstruction(**_kwargs())
        with self.assertRaises(FrozenInstanceError):
            setattr(instruction, "expected_generation", 9)
        with self.assertRaises(FrozenInstanceError):
            setattr(instruction.params[0], "str_value", "modification")
        self.assertFalse(hasattr(instruction, "__dict__"))
        marker = "valeur-synthetique-ne-pas-exposer"
        invalid = AgentManagementInstruction(**_kwargs(initial_actor=marker))
        diagnostics = validate_agent_instruction(invalid, _catalog(), _context())
        self.assertTrue(diagnostics)
        text = " ".join(d.element + d.constraint + d.message for d in diagnostics)
        self.assertNotIn(marker, text)
        self.assertNotIn(marker, repr(invalid))


if __name__ == "__main__":
    unittest.main()
