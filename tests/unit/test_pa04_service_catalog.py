"""Unite locale catalogue PA04 : nominaux puis refus integres, valeurs synthetiques."""
from __future__ import annotations

import unittest
from dataclasses import replace

from pixs.agent.contracts import AgentManagementInstruction, AgentParam, AgentValidationContext
from pixs.agent.pa04_service_catalog import PA04_OPERATIONS, build_pa04_catalog, validate_pa04_instruction
from pixs.core.scope import ScopeContext, ScopeType

ALLOW = ("service-livre-synth-1",)
VERSION = "1.0.0"
B = {"max_service_ref_len": 64, "max_plan_ref_len": 64, "max_operation_ref_len": 64, "max_action_len": 32}


def _scope():
    return ScopeContext(ScopeType.TENANT, "tenant-synth-1", "scope-synth-1")


def _params(operation):
    if operation == "OBSERVE":
        return (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None),)
    if operation == "PREPARE_PLAN":
        return (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="action", kind="str", str_value="START", int_value=None, bool_value=None))
    if operation in ("START", "STOP"):
        return (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="plan-synth-1", int_value=None, bool_value=None))
    return (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="operation_ref", kind="str", str_value="op-cible-1", int_value=None, bool_value=None))


def _context(operation="START"):
    return AgentValidationContext(expected_actor="actor-synth-1", expected_scope=_scope(), expected_target="pa-synth-1", expected_generation=7, expected_operation=operation, expected_version=VERSION, expected_operation_id="op-synth-1", expected_idempotency_key="key-synth-1", expected_correlation_ids=("corr-1",), now_iso="2030-01-01T00:00:00Z", mandate_proof="mandate-synth-1", expected_origin_proof="origin-synth-1", expected_confirmation_proof="confirm-synth-1", max_id_len=64, max_doc_len=1024, max_ids=8, max_params=8, max_observation_age_seconds=3600)


def _instruction(operation="START", **over):
    fields = {"schema_version": "1.0.0", "operation_id": "op-synth-1", "catalog_operation": operation, "catalog_version": VERSION, "initial_actor": "actor-synth-1", "scope_context": _scope(), "pa_target": "pa-synth-1", "expected_generation": 7, "mandate_ref": "mandate-synth-1", "expires_at": "2030-01-01T01:00:00Z", "correlation_ids": ("corr-1",), "causation_ids": (), "idempotency_key": "key-synth-1", "params": _params(operation)}
    fields.update(over)
    return AgentManagementInstruction(**fields)


def _check(operation="START", **over):
    return validate_pa04_instruction(instruction=_instruction(operation, **over), context=_context(operation), allowlist=ALLOW, catalog_version=VERSION, **B)


class Pa04NominalCases(unittest.TestCase):
    def test_nominaux_cinq_operations_sans_diagnostic(self):
        for operation in PA04_OPERATIONS:
            with self.subTest(operation=operation):
                self.assertEqual(_check(operation), ())


class Pa04RefusCases(unittest.TestCase):
    def test_action_interdite_refusee(self):
        for action in ("CONFIGURE", "RESTART", "ENABLE", "DISABLE", "AUTRE"):
            with self.subTest(action=action):
                bad = (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="action", kind="str", str_value=action, int_value=None, bool_value=None))
                self.assertTrue(validate_pa04_instruction(instruction=_instruction("PREPARE_PLAN", params=bad), context=_context("PREPARE_PLAN"), allowlist=ALLOW, catalog_version=VERSION, **B))

    def test_service_inconnu_operation_version_inconnues(self):
        bad = (AgentParam(name="service_ref", kind="str", str_value="libre", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="plan-synth-1", int_value=None, bool_value=None))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction("START", params=bad), context=_context("START"), allowlist=ALLOW, catalog_version=VERSION, **B))
        inst = _instruction(catalog_operation="INCONNU")
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context("INCONNU"), allowlist=ALLOW, catalog_version=VERSION, **B))
        inst = _instruction(catalog_version="9.9.9")
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))

    def test_champs_manquants_etrangers_types_bornes(self):
        inst = _instruction(params=())
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        inst = _instruction(params=_params("START") + (AgentParam(name="intrus", kind="str", str_value="x", int_value=None, bool_value=None),))
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        inst = _instruction(params=(AgentParam(name="service_ref", kind="int", str_value=None, int_value=1, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="plan-synth-1", int_value=None, bool_value=None)))
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        inst = _instruction(params=(AgentParam(name="service_ref", kind="str", str_value="x" * 65, int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="plan-synth-1", int_value=None, bool_value=None)))
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        inst = _instruction(params=(AgentParam(name="service_ref", kind="str", str_value="", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="plan-synth-1", int_value=None, bool_value=None)))
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        inst = _instruction(params=(AgentParam(name="service_ref", kind="str", str_value="a\x00b", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="plan-synth-1", int_value=None, bool_value=None)))
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))

    def test_read_result_reference_vide_ou_hors_borne(self):
        inst = _instruction("READ_RESULT", params=(AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="operation_ref", kind="str", str_value="", int_value=None, bool_value=None)))
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context("READ_RESULT"), allowlist=ALLOW, catalog_version=VERSION, **B))
        inst = _instruction("READ_RESULT", params=(AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="operation_ref", kind="str", str_value="x" * 65, int_value=None, bool_value=None)))
        self.assertTrue(validate_pa04_instruction(instruction=inst, context=_context("READ_RESULT"), allowlist=ALLOW, catalog_version=VERSION, **B))

    def test_mauvais_types_bornes_et_allowlist(self):
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist=ALLOW, catalog_version=VERSION, max_service_ref_len=None, max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=32)
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist=ALLOW, catalog_version=VERSION, max_service_ref_len=True, max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=32)
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist=None, catalog_version=VERSION, max_service_ref_len=64, max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=32)
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist=(), catalog_version=VERSION, max_service_ref_len=64, max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=32)
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist=("a", "a"), catalog_version=VERSION, max_service_ref_len=64, max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=32)
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist=(True,), catalog_version=VERSION, max_service_ref_len=64, max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=32)

    def test_bornes_limites_acceptees_au_dela_refusees(self):
        ok = (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="y" * 64, int_value=None, bool_value=None))
        self.assertEqual(validate_pa04_instruction(instruction=_instruction(params=ok), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B), ())
        bad = (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="y" * 65, int_value=None, bool_value=None))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(params=bad), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))

    def test_plan_ref_vide_et_prepare_stop_nominal(self):
        nominal = (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="action", kind="str", str_value="STOP", int_value=None, bool_value=None))
        self.assertEqual(validate_pa04_instruction(instruction=_instruction("PREPARE_PLAN", params=nominal), context=_context("PREPARE_PLAN"), allowlist=ALLOW, catalog_version=VERSION, **B), ())
        vide = (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="", int_value=None, bool_value=None))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(params=vide), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))

    def test_multioctets_local_refuse_generique_accepte(self):
        temoin = (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="\u00e9" * 32, int_value=None, bool_value=None))
        self.assertEqual(validate_pa04_instruction(instruction=_instruction(params=temoin), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B), ())
        depasse = (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value="\u00e9" * 33, int_value=None, bool_value=None))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(params=depasse), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))

    def test_c1_del_surrogate_plan_ref_refuses(self):
        for value in ("a\u0080", "a\x7f", "a\ud800"):
            with self.subTest(value=value):
                bad = (AgentParam(name="service_ref", kind="str", str_value="service-livre-synth-1", int_value=None, bool_value=None), AgentParam(name="plan_ref", kind="str", str_value=value, int_value=None, bool_value=None))
                self.assertTrue(validate_pa04_instruction(instruction=_instruction(params=bad), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))

    def test_profil_max_action_insuffisante_et_mauvais_profils(self):
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist=ALLOW, catalog_version=VERSION, max_service_ref_len=64, max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=4)
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist="service-livre-synth-1", catalog_version=VERSION, max_service_ref_len=64, max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=32)
        with self.assertRaises(ValueError):
            build_pa04_catalog(allowlist=ALLOW, catalog_version=VERSION, max_service_ref_len="64", max_plan_ref_len=64, max_operation_ref_len=64, max_action_len=32)

    def test_version_serveur_differente_concordante_nominale(self):
        other = "2.0.0"
        inst = _instruction(catalog_version=other)
        ctx = replace(_context(), expected_version=other)
        self.assertEqual(validate_pa04_instruction(instruction=inst, context=ctx, allowlist=ALLOW, catalog_version=other, **B), ())

    def test_expire_acteur_scope_generation_mandat_correlation_idempotence(self):
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(expires_at="2029-01-01T00:00:00Z"), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(initial_actor="autre"), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        other_scope = ScopeContext(ScopeType.TENANT, "tenant-synth-1", "autre-scope")
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(scope_context=other_scope), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(expected_generation=True), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(mandate_ref="autre"), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(correlation_ids=("autre",)), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))
        self.assertTrue(validate_pa04_instruction(instruction=_instruction(idempotency_key="autre"), context=_context(), allowlist=ALLOW, catalog_version=VERSION, **B))


if __name__ == "__main__":
    unittest.main()
