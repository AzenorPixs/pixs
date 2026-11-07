"""Agent contracts v2.0.0 purs D-A3, unittest stdlib uniquement."""
from __future__ import annotations
import dataclasses
import unittest
from pixs.agent import contracts as c1
from pixs.agent import contracts_v2 as c2
from pixs.agent.contracts import AgentManagementInstruction, AgentManagementResult, AgentManagementState, AgentParam, AgentParamSpec, AgentValidationContext, AllowedCatalogEntry
from pixs.core.scope import ScopeContext, ScopeType

SCOPE = ScopeContext(scope_type=ScopeType.PLATFORM, tenant_id=None, scope_id=None)
TENANT_SCOPE = ScopeContext(scope_type=ScopeType.TENANT, tenant_id="tenant-a", scope_id="scope-a")
NOW = "2026-10-27T12:00:00.000000Z"
PLUS1 = "2026-10-27T12:00:00.000001Z"
MINUS1 = "2026-10-27T11:59:59.999999Z"
NOW_V1 = "2026-10-27T12:00:00Z"
PLUS1_V1 = "2026-10-27T12:00:01Z"
EXP_PLUS1 = "2026-10-27T12:00:01.000001Z"
EMPTY_CAT = (AllowedCatalogEntry(operation="op.a", version="1.2.3", params=()),)

def _ctx(now=NOW, **kw):
    base = dict(expected_actor="actor-a", expected_scope=SCOPE, expected_target="target-a", expected_generation=3, expected_operation="op.a", expected_version="1.2.3", expected_operation_id="opid-1", expected_idempotency_key="idem-1", expected_correlation_ids=("corr-1",), now_iso=now, mandate_proof="mandate-1", expected_origin_proof="origin-1", expected_confirmation_proof="confirm-1", max_id_len=128, max_doc_len=4096, max_ids=8, max_params=8, max_observation_age_seconds=60)
    base.update(kw)
    return AgentValidationContext(**base)

def _instr(expires=PLUS1, schema="2.0.0", **kw):
    base = dict(schema_version=schema, operation_id="opid-1", catalog_operation="op.a", catalog_version="1.2.3", initial_actor="actor-a", scope_context=SCOPE, pa_target="target-a", expected_generation=3, mandate_ref="mandate-1", expires_at=expires, correlation_ids=("corr-1",), causation_ids=(), idempotency_key="idem-1", params=())
    base.update(kw)
    return AgentManagementInstruction(**base)

def _state(obs_doc=None, obs_at=None, last_doc=None, last_at=None, proof=None, **kw):
    base = dict(operation_id="opid-1", pa_target="target-a", generation=3, scope_context=SCOPE, desired_doc="d", observed_doc=obs_doc, observed_at=obs_at, last_known_doc=last_doc, last_known_at=last_at, confirmation_proof=proof)
    base.update(kw)
    return AgentManagementState(**base)

def _result(outcome="ack", occurred=NOW, proof="origin-1", **kw):
    base = dict(operation_id="opid-1", pa_target="target-a", generation=3, scope_context=SCOPE, outcome=outcome, correlation_ids=("corr-1",), occurred_at=occurred, origin_proof=proof)
    base.update(kw)
    return AgentManagementResult(**base)

class DescriptorsTest(unittest.TestCase):
    def test_ids_and_version(self):
        self.assertEqual(c2.CONTRACT_VERSION_V2, "2.0.0")
        self.assertEqual(c2.COMMAND_DESCRIPTOR_V2.contract_id, "pixs.agent.management.command")
        self.assertEqual(c2.QUERY_DESCRIPTOR_V2.contract_id, "pixs.agent.management.query")
        self.assertEqual(c2.SERVICE_DESCRIPTOR_V2.contract_id, "pixs.agent.management.service")
        for d in c2.ALL_AGENT_CONTRACTS_V2:
            self.assertEqual(d.version, "2.0.0")
        self.assertEqual(len(c2.ALL_AGENT_CONTRACTS_V2), 3)
    def test_v1_tuple_unchanged_schema_isolated(self):
        self.assertEqual(c1.CONTRACT_VERSION, "1.0.0")
        self.assertEqual(len(tuple(c1.ALL_AGENT_CONTRACTS)), 3)
        for d in c1.ALL_AGENT_CONTRACTS:
            self.assertEqual(d.version, "1.0.0")
        bad = _instr(schema="1.0.0", expires=EXP_PLUS1)
        diags = c2.validate_agent_instruction_v2(bad, EMPTY_CAT, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.schema_version" for d in diags))

class InstructionExpiryTest(unittest.TestCase):
    def test_nominal_plus1us(self):
        self.assertEqual(c2.validate_agent_instruction_v2(_instr(PLUS1), EMPTY_CAT, _ctx(NOW)), [])
    def test_expires_equal_now_refused(self):
        diags = c2.validate_agent_instruction_v2(_instr(NOW), EMPTY_CAT, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.expires_at" for d in diags))
    def test_minus1us_refused(self):
        diags = c2.validate_agent_instruction_v2(_instr(MINUS1), EMPTY_CAT, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.expires_at" for d in diags))
    def test_context_now_grammar_invalid(self):
        bad_ctx = _ctx(now="2026-10-27T12:00:00Z")
        diags = c2.validate_agent_instruction_v2(_instr(PLUS1), EMPTY_CAT, bad_ctx)
        self.assertTrue(any(d.element == "agent.context" for d in diags))

class GrammarTest(unittest.TestCase):
    def test_strict6_instruction_isolated_from_expiry(self):
        ctx = _ctx("2026-10-27T12:00:00.000000Z")
        for bad in ("2026-10-27T12:00:01Z", "2026-10-27T12:00:01.00000Z", "2026-10-27T12:00:01.0000001Z", "2026-10-27T12:00:01.000001+00:00", "2026-10-27 12:00:01.000001Z"):
            diags = c2.validate_agent_instruction_v2(_instr(bad), EMPTY_CAT, ctx)
            self.assertTrue(any(d.element == "agent.instruction.expires_at" for d in diags), msg=bad)
    def test_result_occurred_grammar_isolated(self):
        self.assertEqual(c2.validate_agent_result_v2(_result(occurred=NOW), _ctx(NOW)), [])
        for bad in ("2026-10-27T12:00:00Z", "2026-10-27T12:00:00.00000Z", "2026-10-27T12:00:00.0000001Z", "2026-10-27T12:00:00.000000+00:00"):
            diags = c2.validate_agent_result_v2(_result(occurred=bad), _ctx(NOW))
            self.assertTrue(any(d.element == "agent.result.occurred_at" for d in diags), msg=bad)
    def test_state_observed_lastknown_valid_then_invalid(self):
        self.assertEqual(c2.validate_agent_state_v2(_state(obs_doc="o", obs_at=NOW, last_doc="k", last_at=NOW), _ctx(NOW)), [])
        for bad in ("2026-10-27T12:00:00Z", "2026-10-27T12:00:00.00000Z", "2026-10-27T12:00:00.0000001Z", "2026-10-27T12:00:00.000000+00:00"):
            d1 = c2.validate_agent_state_v2(_state(obs_doc="o", obs_at=bad), _ctx(NOW))
            self.assertTrue(any(d.element == "agent.state.observed_at" for d in d1), msg=bad)
            d2 = c2.validate_agent_state_v2(_state(last_doc="k", last_at=bad), _ctx(NOW))
            self.assertTrue(any(d.element == "agent.state.last_known_at" for d in d2), msg=bad)
    def test_calendar(self):
        self.assertEqual(c2.validate_agent_instruction_v2(_instr("2024-02-29T12:00:01.000001Z"), EMPTY_CAT, _ctx("2024-02-29T12:00:00.000001Z")), [])
        diags = c2.validate_agent_instruction_v2(_instr("2025-02-29T12:00:01.000001Z"), EMPTY_CAT, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.expires_at" for d in diags))
    def test_v1_in_v2_isolated(self):
        diags = c2.validate_agent_instruction_v2(_instr("2026-10-27T12:00:01Z"), EMPTY_CAT, _ctx("2026-10-27T12:00:00.000000Z"))
        self.assertTrue(any(d.element == "agent.instruction.expires_at" for d in diags))
    def test_v2_in_v1_isolated(self):
        ctx1 = _ctx(now=NOW_V1)
        ins_schema = _instr("2026-10-27T12:00:01.000001Z", schema="2.0.0")
        d1 = c1.validate_agent_instruction(ins_schema, EMPTY_CAT, ctx1)
        self.assertTrue(any(d.element == "agent.instruction.schema_version" for d in d1))
        ins_fmt = _instr("2026-10-27T12:00:01.000001Z", schema="1.0.0")
        d2 = c1.validate_agent_instruction(ins_fmt, EMPTY_CAT, ctx1)
        self.assertTrue(any(d.element == "agent.instruction.expires_at" for d in d2))

class StateFutureFreshnessTest(unittest.TestCase):
    def test_observed_future_plus1us_refused(self):
        st = _state(obs_doc="o", obs_at=PLUS1)
        diags = c2.validate_agent_state_v2(st, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.state.observed_at" for d in diags))
    def test_last_known_future_plus1us_refused(self):
        st = _state(last_doc="k", last_at=PLUS1)
        diags = c2.validate_agent_state_v2(st, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.state.last_known_at" for d in diags))
    def test_freshness_exact_accept_then_plus1us_stale(self):
        ctx = _ctx(now="2026-10-27T12:00:01.000000Z", max_observation_age_seconds=1)
        ok = _state(obs_doc="o", obs_at="2026-10-27T12:00:00.000000Z", proof="confirm-1")
        self.assertEqual(c2.validate_agent_state_v2(ok, ctx), [])
        ctx2 = _ctx(now="2026-10-27T12:00:01.000001Z", max_observation_age_seconds=1)
        stale = _state(obs_doc="o", obs_at="2026-10-27T12:00:00.000000Z", proof="confirm-1")
        diags = c2.validate_agent_state_v2(stale, ctx2)
        self.assertTrue(any(d.element == "agent.state.confirmation" for d in diags))
    def test_unknown_absence_separated(self):
        diags = c2.validate_agent_state_v2(_state(obs_doc=None, obs_at=NOW), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.state.observed" for d in diags))
        self.assertEqual(c2.validate_agent_state_v2(_state(), _ctx(NOW)), [])

class ResultProofTest(unittest.TestCase):
    def test_confirmed_requires_exact_proof(self):
        self.assertEqual(c2.validate_agent_result_v2(_result(outcome="confirmed", proof="origin-1"), _ctx(NOW)), [])
        diags = c2.validate_agent_result_v2(_result(outcome="confirmed", proof="other"), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.result.origin" for d in diags))
    def test_unknown_forbids_proof(self):
        self.assertEqual(c2.validate_agent_result_v2(_result(outcome="unknown", proof=None), _ctx(NOW)), [])
        diags = c2.validate_agent_result_v2(_result(outcome="unknown", proof="origin-1"), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.result.origin" for d in diags))

class BindingTest(unittest.TestCase):
    def test_instruction_bad_bindings_by_element(self):
        cases = [
            (dict(initial_actor="other"), "agent.instruction.binding.actor"),
            (dict(pa_target="other"), "agent.instruction.binding.target"),
            (dict(expected_generation=4), "agent.instruction.binding.generation"),
            (dict(catalog_operation="other"), "agent.instruction.binding.operation"),
            (dict(catalog_version="9.9.9"), "agent.instruction.binding.version"),
            (dict(correlation_ids=("other",)), "agent.instruction.binding.correlation"),
            (dict(mandate_ref="other"), "agent.instruction.binding.mandate"),
            (dict(idempotency_key="other"), "agent.instruction.binding.idempotence"),
            (dict(operation_id="other"), "agent.instruction.binding.operation_id"),
        ]
        for kw, element in cases:
            with self.subTest(kw=kw):
                diags = c2.validate_agent_instruction_v2(_instr(**kw), EMPTY_CAT, _ctx(NOW))
                self.assertTrue(any(d.element == element for d in diags))
    def test_instruction_scope_binding_separate_from_actor(self):
        ctx = _ctx(NOW)
        ins = dataclasses.replace(_instr(), scope_context=TENANT_SCOPE)
        diags = c2.validate_agent_instruction_v2(ins, EMPTY_CAT, ctx)
        self.assertTrue(any(d.element == "agent.instruction.binding.scope" for d in diags))
        self.assertFalse(any(d.element == "agent.instruction.binding.actor" for d in diags))
    def test_result_state_bad_bindings(self):
        diags = c2.validate_agent_result_v2(_result(operation_id="other"), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.result.binding.operation_id" for d in diags))
        diags = c2.validate_agent_result_v2(_result(pa_target="other"), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.result.binding.target" for d in diags))
        diags = c2.validate_agent_result_v2(_result(generation=9), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.result.binding.generation" for d in diags))
        scoped = dataclasses.replace(_result(), scope_context=TENANT_SCOPE)
        diags = c2.validate_agent_result_v2(scoped, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.result.binding.scope" for d in diags))
        diags = c2.validate_agent_state_v2(_state(operation_id="other"), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.state.binding.operation_id" for d in diags))
        stated = dataclasses.replace(_state(), pa_target="other")
        diags = c2.validate_agent_state_v2(stated, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.state.binding.target" for d in diags))
        statesc = dataclasses.replace(_state(), scope_context=TENANT_SCOPE)
        diags = c2.validate_agent_state_v2(statesc, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.state.binding.scope" for d in diags))
        diags = c2.validate_agent_state_v2(_state(generation=True), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.state.generation" for d in diags))
        diags = c2.validate_agent_result_v2(_result(generation=True), _ctx(NOW))
        self.assertTrue(any(d.element == "agent.result.generation" for d in diags))

class CatalogParamsTest(unittest.TestCase):
    def test_catalog_duplicates_and_bounds(self):
        spec = AgentParamSpec(name="p", kind="int", max_len=None, int_min=0, int_max=5, required=True)
        cat = (AllowedCatalogEntry(operation="op.a", version="1.2.3", params=(spec,)),)
        okp = AgentParam(name="p", kind="int", str_value=None, int_value=3, bool_value=None)
        self.assertEqual(c2.validate_agent_instruction_v2(_instr(params=(okp,)), cat, _ctx(NOW)), [])
        dup_cat = (AllowedCatalogEntry(operation="op.a", version="1.2.3", params=()), AllowedCatalogEntry(operation="op.a", version="1.2.3", params=()))
        diags = c2.validate_agent_instruction_v2(_instr(), dup_cat, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.catalog.entry" for d in diags))
        dup_param = (AllowedCatalogEntry(operation="op.a", version="1.2.3", params=(spec, spec)),)
        diags = c2.validate_agent_instruction_v2(_instr(), dup_param, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.catalog.param" for d in diags))
        low = AgentParam(name="p", kind="int", str_value=None, int_value=-1, bool_value=None)
        diags = c2.validate_agent_instruction_v2(_instr(params=(low,)), cat, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.param.int" for d in diags))
        high = AgentParam(name="p", kind="int", str_value=None, int_value=6, bool_value=None)
        diags = c2.validate_agent_instruction_v2(_instr(params=(high,)), cat, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.param.int" for d in diags))
        asbool = AgentParam(name="p", kind="int", str_value=None, int_value=True, bool_value=None)
        diags = c2.validate_agent_instruction_v2(_instr(params=(asbool,)), cat, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.param.int" for d in diags))
    def test_required_foreign_strmaxlen(self):
        spec = AgentParamSpec(name="p", kind="str", max_len=2, int_min=None, int_max=None, required=True)
        cat = (AllowedCatalogEntry(operation="op.a", version="1.2.3", params=(spec,)),)
        diags = c2.validate_agent_instruction_v2(_instr(params=()), cat, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.param.required" for d in diags))
        foreign = (AgentParam(name="q", kind="str", str_value="x", int_value=None, bool_value=None),)
        diags = c2.validate_agent_instruction_v2(_instr(params=foreign), cat, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.param.name" for d in diags))
        toolong = (AgentParam(name="p", kind="str", str_value="abc", int_value=None, bool_value=None),)
        diags = c2.validate_agent_instruction_v2(_instr(params=toolong), cat, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.param.str" for d in diags))
        boolspec = AgentParamSpec(name="b", kind="bool", max_len=None, int_min=None, int_max=None, required=False)
        cat2 = (AllowedCatalogEntry(operation="op.a", version="1.2.3", params=(boolspec,)),)
        badb = (AgentParam(name="b", kind="bool", str_value=None, int_value=1, bool_value=None),)
        diags = c2.validate_agent_instruction_v2(_instr(params=badb), cat2, _ctx(NOW))
        self.assertTrue(any(d.element == "agent.instruction.param.bool" for d in diags))

class V1CompatTest(unittest.TestCase):
    def test_v1_guards_unchanged(self):
        self.assertEqual(c1.CONTRACT_VERSION, "1.0.0")
        ctx1 = _ctx(now=NOW_V1)
        ins1 = _instr(expires=PLUS1_V1, schema="1.0.0")
        self.assertEqual(c1.validate_agent_instruction(ins1, EMPTY_CAT, ctx1), [])

if __name__ == "__main__":
    unittest.main()
