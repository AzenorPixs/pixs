"""Recette supervision sur Agent/Core/C05 PostgreSQL reels.

Les ports Auth, gouvernance, mandat et preuves d'executant sont des fixtures
explicites. Aucun transport, binaire PA/PZT ou preuve cryptographique qualifie.
"""
from __future__ import annotations
import datetime
import json
import sys
sys.path.insert(0, 'src')
sys.path.insert(0, 'tests/integration')
import agent_pg_test_support as harness
ROOT = '/home/devops/datas/pixs'
EXPECTED_CASES = (
    'empty_authorized_read', 'desired_is_not_observed', 'readonly_reconciliation',
    'fresh_observation', 'verified_fixture_confirmation', 'bounded_confirmation_window',
    'stale_observation_and_confirmation', 'unknown_overrides_confirmation',
    'failure_overrides_confirmation', 'new_generation_keeps_history',
    'restart_reads_persisted_state', 'new_generation_observation',
    'revoked_authority_refused', 'tenant_isolation', 'corrupt_projection_refused',
    'programming_error_propagates',
)
def _cases(refs, failures, threads, cases):
    from dataclasses import FrozenInstanceError, replace
    from unittest.mock import patch
    from pixs.agent import models as am
    from pixs.agent.contracts import AgentManagementResult
    from pixs.agent.service import PostgresAgentManagementService, AgentServiceError
    from pixs.agent.supervision import AgentSupervisor, AgentSupervisionError, AgentSupervisionView
    from pixs.kernel.diagnostics import Diagnostic
    from agent_service_test_support import build_agent_service_fixture
    fx = build_agent_service_fixture()
    actor = fx.aref(fx.ord1)
    base_now = fx.clock.now()
    now_box = [base_now]
    fx.clock.now = lambda: now_box[0]
    profile = replace(fx.pr, max_observation_age_seconds=2)
    sequence = [0]
    expected_origin = {}
    expected_confirmation = {}
    def bad():
        return (Diagnostic(step='validate', element='fixture', constraint='fixture_refused', message='Preuve fixture refusee.'),)
    class OriginFixture:
        calls = 0
        def verify_origin(self, **kw):
            self.calls += 1
            result, context = kw['result'], kw['context']
            wanted = expected_origin.get(result.origin_proof)
            if wanted is None:
                return bad()
            bound = (result, kw['observed_document'], kw['observed_at'], kw['source_ref'], kw['target_id'], kw['scope'])
            valid = bound == wanted
            valid = valid and (context.expected_actor, context.expected_scope, context.expected_target, context.expected_generation, context.expected_operation_id, context.expected_origin_proof) == (actor, fx.plat, fx.TA, result.generation, result.operation_id, result.origin_proof)
            return () if valid else bad()
    class ConfirmationFixture:
        calls = 0
        def verify_confirmation(self, **kw):
            self.calls += 1
            result, state, context = kw['result'], kw['state'], kw['context']
            wanted = expected_confirmation.get(state.confirmation_proof)
            if wanted is None:
                return bad()
            bound = (result, str(kw['observed_fact_id']), kw['observed_source_ref'], kw['observed_origin_proof'], kw['postcondition_ref'], kw['target_id'], kw['scope'], state.observed_doc, state.observed_at, state.desired_doc)
            valid = bound == wanted
            valid = valid and (context.expected_actor, context.expected_scope, context.expected_target, context.expected_generation, context.expected_operation_id, context.expected_origin_proof, context.expected_confirmation_proof) == (actor, fx.plat, fx.TA, result.generation, result.operation_id, result.origin_proof, state.confirmation_proof)
            return () if valid else bad()
    origin, confirmation = OriginFixture(), ConfirmationFixture()
    def service():
        return PostgresAgentManagementService(profile=profile, decider_factory=fx.Fact(False), clock=fx.clock, audit_adapter=fx.auditp(), governance_port=fx.gov, mandate_port=fx.mand, origin_port=origin, confirmation_port=confirmation, alias='default')
    management = service()
    supervisor = AgentSupervisor(management=management)
    def context(op, gen, scope=None, who=None):
        return replace(fx.ctx(actor if who is None else who, fx.plat if scope is None else scope, fx.TA, op, gen), max_observation_age_seconds=2)
    def read(*, chosen=None, limit=8, scope=None, who=None):
        sequence[0] += 1
        op = 'supervision.read.' + str(sequence[0])
        scope = fx.plat if scope is None else scope
        who = actor if who is None else who
        req = fx.req('decision:' + op, who, fx.TA, fx.READ, scope, op)
        ctx = replace(context(op, 0, scope, who), expected_operation=fx.READ)
        rows_before, audit_before = fx.agent_rows(), fx.audit_ids()
        value = (supervisor if chosen is None else chosen).reconcile(request=req, context=ctx, limit=limit)
        assert type(value) is AgentSupervisionView
        assert value.target == fx.TA and value.scope == scope
        assert value.transport_status == 'PZT_NOT_BOUND' and value.executor_status == 'UNKNOWN'
        assert fx.agent_rows() == rows_before
        assert len(fx.audit_ids() - audit_before) == 2
        assert fx.TA in fx.gov.last_refs
        return value
    def persist(op, previous_generation):
        ins = fx.ins(op, actor, fx.plat, fx.TA, previous_generation)
        receipt = management.persist_desired(request=fx.req('decision:' + op, actor, fx.TA, fx.APPLY, fx.plat, op), context=context(op, previous_generation), instruction=ins)
        assert receipt.generation == previous_generation + 1 and receipt.local_issue == 'PERSISTED'
        return ins
    def observe(ins, gen, outcome='ack', doc='fixture:observed'):
        now_box[0] += datetime.timedelta(seconds=1)
        at = fx.clock.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        proof = None if outcome == 'unknown' else 'fixture:origin:' + str(sequence[0]) + ':' + outcome + ':' + at
        result = AgentManagementResult(ins.operation_id, fx.TA, gen, fx.plat, outcome, ins.correlation_ids, at, proof)
        seen_at = at if doc is not None else None
        if proof is not None:
            expected_origin[proof] = (result, doc, seen_at, 'fixture:executor', fx.TA, fx.plat)
        # Unknown is deliberately admitted only as an unproven result.
        if outcome == 'unknown':
            expected_origin[None] = (result, doc, seen_at, 'fixture:executor', fx.TA, fx.plat)
        before = set(am.AgentFact.objects.values_list('id', flat=True))
        management.append_observation(request=fx.req('decision:observe:' + at, actor, fx.TA, fx.OBS, fx.plat, ins.operation_id), context=replace(context(ins.operation_id, gen), expected_origin_proof=proof), result=result, observed_document=doc, observed_at=seen_at, source_ref='fixture:executor')
        fact = am.AgentFact.objects.exclude(pk__in=before).get()
        assert fact.kind == 'OBSERVED' and fact.outcome == outcome
        return fact
    def confirm(ins, gen, observed):
        now_box[0] += datetime.timedelta(seconds=1)
        at = fx.clock.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        proof = 'fixture:confirmation:' + at
        origin_proof = 'fixture:confirmation-origin:' + at
        post = 'fixture:postcondition:' + at
        result = AgentManagementResult(ins.operation_id, fx.TA, gen, fx.plat, 'confirmed', ins.correlation_ids, at, origin_proof)
        desired = am.AgentOperation.objects.get(request_operation_id=ins.operation_id).content_canonical
        expected_confirmation[proof] = (result, str(observed.id), observed.source_ref, observed.origin_proof, post, fx.TA, fx.plat, observed.observed_document, observed.observed_at, desired)
        receipt = management.confirm_observation(request=fx.req('decision:confirm:' + at, actor, fx.TA, fx.CONF, fx.plat, ins.operation_id), context=replace(context(ins.operation_id, gen), expected_origin_proof=origin_proof, expected_confirmation_proof=proof), result=result, observed_fact_id=observed.id, proof_ref=proof, postcondition_ref=post)
        assert receipt.local_issue == 'CONFIRMED_LOCAL'
        return proof
    empty = read()
    assert empty.desired_doc is None and empty.state is None and empty.desired_generation is None
    assert empty.observation_status == 'ABSENT' and empty.confirmation_status == 'NONE'
    assert empty.last_result is None and empty.last_known_generation is None
    cases['empty_authorized_read'] = True
    ins1 = persist('supervision.desired.1', 0)
    desired = read()
    assert desired.desired_generation == 1 and desired.state.observed_doc is None
    assert desired.state.last_known_doc is None and desired.state.confirmation_proof is None
    assert desired.last_result is None and desired.observation_status == 'ABSENT'
    assert desired.confirmation_status == 'NONE'
    cases['desired_is_not_observed'] = True
    def forbidden(*args, **kwargs):
        raise AssertionError('MUTATION_SUPERVISION_INTERDITE')
    with patch.object(PostgresAgentManagementService, 'persist_desired', forbidden), patch.object(PostgresAgentManagementService, 'append_observation', forbidden), patch.object(PostgresAgentManagementService, 'confirm_observation', forbidden), patch.object(PostgresAgentManagementService, 'dispatch', forbidden):
        again = read()
        assert again == desired
    try:
        desired.desired_generation = 99
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError('VUE_NON_FIGEE')
    assert desired.desired_doc not in repr(desired) and actor not in str(desired)
    cases['readonly_reconciliation'] = True
    obs1 = observe(ins1, 1)
    fresh = read()
    assert fresh.observation_status == 'CURRENT' and fresh.state.observed_doc == obs1.observed_document
    assert fresh.last_known_generation == 1 and fresh.last_known_stale is False
    assert fresh.last_result.outcome == 'ack' and fresh.confirmation_status == 'NONE'
    assert fresh.state.confirmation_proof is None and fresh.desired_doc != fresh.state.observed_doc
    cases['fresh_observation'] = True
    proof1 = confirm(ins1, 1, obs1)
    current = read()
    assert current.confirmation_status == 'CURRENT' and current.state.confirmation_proof == proof1
    assert current.last_result.outcome == 'confirmed' and current.last_confirmation_generation == 1
    assert origin.calls >= 2 and confirmation.calls == 1
    cases['verified_fixture_confirmation'] = True
    narrow = read(limit=1)
    assert narrow.history_limit == 1 and narrow.confirmation_status == 'CURRENT'
    assert narrow.state.observed_doc == obs1.observed_document and narrow.state.confirmation_proof == proof1
    cases['bounded_confirmation_window'] = True
    now_box[0] += datetime.timedelta(seconds=3)
    stale = read()
    assert stale.observation_status == 'STALE' and stale.confirmation_status == 'STALE'
    assert stale.state.observed_doc is None and stale.state.observed_at is None
    assert stale.state.last_known_doc == obs1.observed_document and stale.last_known_stale is True
    assert stale.state.confirmation_proof is None and stale.last_confirmation_ref == proof1
    cases['stale_observation_and_confirmation'] = True
    observe(ins1, 1, outcome='unknown', doc=None)
    unknown = read()
    assert unknown.last_result.outcome == 'unknown' and unknown.last_result.origin_proof is None
    assert unknown.state.observed_doc is None and unknown.state.confirmation_proof is None
    assert unknown.confirmation_status == 'HISTORICAL' and unknown.last_confirmation_ref == proof1
    cases['unknown_overrides_confirmation'] = True
    observe(ins1, 1, outcome='failed', doc=None)
    failed = read()
    assert failed.last_result.outcome == 'failed' and failed.state.confirmation_proof is None
    assert failed.confirmation_status == 'HISTORICAL' and failed.state.observed_doc is None
    cases['failure_overrides_confirmation'] = True
    ins2 = persist('supervision.desired.2', 1)
    new = read()
    assert new.desired_generation == 2 and new.desired_operation_id == ins2.operation_id
    assert new.last_result is None and new.state.observed_doc is None
    assert new.last_known_generation == 1 and new.confirmation_status == 'HISTORICAL'
    assert new.state.confirmation_proof is None
    cases['new_generation_keeps_history'] = True
    restarted = AgentSupervisor(management=service())
    restart_view = read(chosen=restarted)
    assert restart_view == new
    cases['restart_reads_persisted_state'] = True
    obs2 = observe(ins2, 2, doc='fixture:observed-generation-2')
    new_observation = read()
    assert new_observation.observation_status == 'CURRENT' and new_observation.last_known_generation == 2
    assert new_observation.state.observed_doc == obs2.observed_document
    assert new_observation.confirmation_status == 'HISTORICAL' and new_observation.state.confirmation_proof is None
    cases['new_generation_observation'] = True
    before = fx.agent_rows()
    fx.src.revoked = True
    try:
        try:
            read()
        except AgentServiceError:
            pass
        else:
            raise AssertionError('REVOCATION_IGNOREe')
        assert fx.agent_rows() == before
    finally:
        fx.src.revoked = False
    cases['revoked_authority_refused'] = True
    try:
        read(scope=fx.cB)
    except AgentServiceError:
        pass
    else:
        raise AssertionError('FUITE_TENANT')
    assert fx.agent_rows() == before
    cases['tenant_isolation'] = True
    original_query = PostgresAgentManagementService.query_state
    def corrupted(self, **kw):
        snapshot = original_query(self, **kw)
        return replace(snapshot, head_generation=True)
    with patch.object(PostgresAgentManagementService, 'query_state', corrupted):
        try:
            read()
        except AgentSupervisionError as error:
            assert error.code == 'PROJECTION_INCOHERENTE'
        else:
            raise AssertionError('PROJECTION_CORROMPUE_ACCEPTEE')
    assert fx.agent_rows() == before
    cases['corrupt_projection_refused'] = True
    with patch.object(PostgresAgentManagementService, 'query_state', side_effect=TypeError('FIXTURE_PROGRAMMING')):
        try:
            read()
        except TypeError as error:
            assert str(error) == 'FIXTURE_PROGRAMMING'
        else:
            raise AssertionError('ERREUR_PROGRAMMATION_MASQUEE')
    assert fx.agent_rows() == before
    cases['programming_error_propagates'] = True
    assert set(cases) == set(EXPECTED_CASES)
    return cases
def main():
    result = harness.run_in_agent_schema(ROOT, _cases, EXPECTED_CASES, with_core=True)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['real_pg'] else 1
if __name__ == '__main__':
    raise SystemExit(main())
