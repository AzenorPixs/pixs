'''Recette service Agent 26 cas, Core/C05 reels, fixtures synthetiques.'''
from __future__ import annotations
import datetime
import json
import sys
sys.path.insert(0, 'src')
sys.path.insert(0, 'tests/integration')
import agent_pg_test_support as harness
ROOT = '/home/devops/datas/pixs'
EXPECTED_CASES = ('empty_query_without_desired','persist_normal','query_snapshot','replay_immutable','divergence_refused_audited','deny_current_replay_audited','root_waiver_none','root_policy_waiver','root_ungranted_denied','dispatch_denied_audited','governance_missing','metadata_unknown','policy_state_inaccessible','governance_drift_final','revoked_replay','programming_error_propagates','origin_boolean_refused','origin_reference_only_refused','observation_fixture_admitted','confirmation_postcondition_refused','confirmation_fixture_admitted','root_tenant_granted_service','sql_failure_before_commit_real','c05_failure_rolls_back_real','core_before_agent_mutex_real','commit_response_lost_reconciled_real')
TA = 'agent:target-a'
TB = 'agent:target-b'
APPLY = 'agent.apply'
READ = 'agent.read'
OBS = 'agent.observe'
CONF = 'agent.confirm'
def _cases(refs, failures, tracked_threads, cases):
    from dataclasses import replace, FrozenInstanceError
    from django.db import connections, transaction
    from pixs.agent import models as am
    from pixs.agent.contracts import AgentManagementState, AgentManagementInstruction, AgentManagementResult, AgentParam, AgentParamSpec, AgentValidationContext, AllowedCatalogEntry
    from pixs.agent.ports import AgentOperationalProfile
    from pixs.agent.service import AgentServiceError, PostgresAgentManagementService
    from pixs.agent.audit_adapter import AgentAuditAdapter
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.policy import AuthenticationAssurance, Effect, FederationTrust, IdentityAssurance, Obligation, Policy, ScopeSelector, Selector
    from pixs.core.authz.ports import AuthenticationContext, PortError, Request, RevocationStatus, TrustedFacts
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.dto import GovernanceAttestation
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.persistence.models_identity import CoreIdentity, CoreSuperAdminBinding, CoreSuperAdminTenantGrant
    from pixs.core.persistence.models_scope import CoreTenant
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.scope.ownership import ResourceOwnership
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider, RuntimeWaiverRequest
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from pixs.kernel.data_governance_profile import DataGovernanceProfile
    from pixs.kernel.diagnostics import Diagnostic
    plat = ScopeContext(ScopeType.PLATFORM)
    tA = CoreTenant.objects.create(tenant_id='tenant-a-m9')
    tB = CoreTenant.objects.create(tenant_id='tenant-b-m9')
    cA = ScopeContext(ScopeType.TENANT, tA.pk)
    cB = ScopeContext(ScopeType.TENANT, tB.pk)
    ord1 = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type='HUMAN', state='ACTIVE')
    root = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type='DEVICE', state='ACTIVE')
    def aref(i):
        return 'pixs.core.identity:' + str(i.pk)
    CoreSuperAdminBinding.objects.create(installation_ref='install-m9', identity=root)
    CoreSuperAdminTenantGrant.objects.create(binding=CoreSuperAdminBinding.objects.get(installation_ref='install-m9'), tenant=tA)
    lim = Limits(128, 8192, 10, 20, 20, 128, 256, 256, 100000000, 60, 3600)
    cat = Catalog((aref(ord1), aref(root)), (TA, TB), (APPLY, OBS, CONF, READ), (plat, cA, cB), ())
    base = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    class Clock:
        def now(self):
            return base
    clock = Clock()
    class Src:
        revoked = False
        def resolve(self, req):
            n = clock.now()
            a = AuthenticationContext(req.subject_id, 'syn.c03.m9', 'syn.iss', 'syn.sub', n - datetime.timedelta(seconds=30), n + datetime.timedelta(seconds=3600), ('syn.pw',), IdentityAssurance.CLAIMED, AuthenticationAssurance.SINGLE_FACTOR, FederationTrust.UNTRUSTED, req.context, None, None)
            status = RevocationStatus.REVOKED if self.revoked is True else RevocationStatus.ACTIVE
            return TrustedFacts(req.subject_id, req.resource_id, req.action_id, a, ResourceOwnership(req.resource_id, req.context), req.context, status, (), ())
    src = Src()
    class Bound:
        def __init__(self, request, alias, op):
            self.request = request
            self.al = alias
            self.op = op
        def revalidate(self, req, *, alias, operation_id):
            if type(req) is not Request or req != self.request or alias != self.al or operation_id != self.op:
                raise PortError()
            facts = src.resolve(req)
            return facts.auth, facts.revocation_status
    def store():
        return CoreAuthorizationStore(alias='default', installation_ref='install-m9', base_epoch='epoch-m9', catalog=cat, limits=lim)
    class Fact:
        def __init__(self, w=False):
            self.w = w
        def decider_for(self, *, request, alias, operation_id, purpose):
            if alias != 'default':
                raise PortError()
            wr = RuntimeWaiverRequest(request, alias, operation_id, True, True) if self.w else None
            return RuntimeAuthorizationDecider(store=store(), facts_provider=src, clock=clock, request=request, operation_id=operation_id, waiver_request=wr)
        def authentication_for(self, *, request, alias, operation_id, purpose):
            if alias != 'default':
                raise PortError()
            return Bound(request, alias, operation_id)
    def prof():
        e = AllowedCatalogEntry('agent.apply', '1.0.0', (AgentParamSpec('message', 'str', 16, None, None, True),))
        m = (('desired.persist', ('agent.apply',)), ('observation.append', ('agent.observe',)), ('confirmation.confirm', ('agent.confirm',)), ('state.query', ('agent.read',)),)
        return AgentOperationalProfile((e,), m, 128, 8192, 8, 8, 3600)
    pr = prof()
    def allow(pid, actor, ctx, res, act):
        return Policy(pid, 'v1', 'syn.own', Effect.ALLOW, Selector('subject', (actor,)), Selector('resource', (res,)), Selector('action', (act,)), ScopeSelector((ctx,)), obligations=(Obligation('AUDIT'),))
    def deny(pid, actor, ctx, res, act):
        return Policy(pid, 'v1', 'syn.own', Effect.DENY, Selector('subject', (actor,)), Selector('resource', (res,)), Selector('action', (act,)), ScopeSelector((ctx,)))
    for p in [allow('a1', aref(ord1), plat, TA, APPLY), allow('a2', aref(ord1), plat, TA, READ), allow('a3', aref(ord1), plat, TA, OBS), allow('a4', aref(ord1), plat, TA, CONF)]:
        CorePolicy.objects.create(policy_id=p.policy_id, policy_version=p.policy_version, owner=p.owner, effect=p.effect.value, definition=encode_policy(p))
    gprof = DataGovernanceProfile('1.0.0', 'asset-m9', 'pixs.agent', 'truth-m9', frozenset(['c1']), ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE, frozenset(['p1']), 'ret-m9', 'del-m9', frozenset(['r1']), frozenset(['csvc']), frozenset(['psvc']), 'exp-m9', 'lin-m9')
    class Gov:
        def __init__(self):
            self.reads = []
            self.last_refs = ()
            self.mode = 'ok'
            self.attest_calls = 0
        def attest(self, req, *, alias, operation_id, transaction_token):
            self.attest_calls += 1
            rows = [req.resource_id]
            filt = dict(scope_type=req.context.scope_type.value, tenant_id=req.context.tenant_id, scope_id=req.context.scope_id, target_id=req.resource_id)
            for model in (am.AgentHead, am.AgentOperation, am.AgentFact):
                rows.extend(str(value) for value in model.objects.using(alias).filter(**filt).values_list('id', flat=True))
            self.last_refs = tuple(rows)
            prof = gprof
            if self.mode == 'drift' and self.attest_calls >= 2:
                local_head = am.AgentHead.objects.using(alias).get(**filt)
                local_op = am.AgentOperation.objects.using(alias).get(request_operation_id=operation_id, **filt)
                local_audits = CoreAuditEvent.objects.using(alias).filter(operation_id=operation_id).count()
                peer_op = am.AgentOperation.objects.using('peer').filter(request_operation_id=operation_id, **filt).exists()
                peer_audits = CoreAuditEvent.objects.using('peer').filter(operation_id=operation_id).count()
                self.drift_observed = (local_head.current_generation, local_op.generation, local_audits, peer_op, peer_audits)
                prof = replace(gprof, profile_version='2.0.0')
            return GovernanceAttestation(prof, prof.profile_version, req.context, self.last_refs, clock.now())
        def stage_read(self, req, *, resource_refs, alias, operation_id, transaction_token):
            from pixs.core.ports import StagedRef
            from pixs.core.services_authorization_guard import transaction_identity
            assert type(resource_refs) is tuple and resource_refs
            assert set(resource_refs).issubset(self.last_refs)
            pin = transaction_identity(alias)
            ref = StagedRef(operation_id, alias, transaction_token, req.context, 'fixture.governance')
            self.reads.append((operation_id, alias, transaction_token, req.context, resource_refs, pin, ref))
            return ref
        def verify_staged(self, proof):
            from pixs.core.ports import TransactionProof
            from pixs.core.services_authorization_guard import transaction_identity
            assert type(proof) is TransactionProof
            proof.__post_init__()
            op, alias, token, context, refs, pin, ref = self.reads[-1]
            assert (proof.operation_id, proof.alias, proof.transaction_token, proof.context) == (op, alias, token, context)
            assert proof.staged == (ref,) and transaction_identity(alias) == pin
            assert set(refs).issubset(self.last_refs) and proof.prepared_at == clock.now()
            return None
    gov = Gov()
    # Registre de mandats synthetiques du test : aucun mandat PA reel qualifie.
    mandates = {}
    def mandate_binding(instruction):
        return (instruction.initial_actor, instruction.scope_context, instruction.pa_target, instruction.expected_generation, instruction.operation_id, instruction.catalog_operation, instruction.catalog_version, instruction.mandate_ref, instruction.expires_at, instruction.idempotency_key, instruction.correlation_ids, instruction.causation_ids)
    class Mand:
        def verify_mandate(self, *, instruction, context):
            binding = mandate_binding(instruction)
            valid = mandates.get(instruction.mandate_ref) == binding
            valid = valid and (instruction.initial_actor, instruction.scope_context, instruction.pa_target, instruction.expected_generation, instruction.operation_id, instruction.catalog_operation, instruction.catalog_version, instruction.mandate_ref, instruction.idempotency_key, instruction.correlation_ids) == (context.expected_actor, context.expected_scope, context.expected_target, context.expected_generation, context.expected_operation_id, context.expected_operation, context.expected_version, context.mandate_proof, context.expected_idempotency_key, context.expected_correlation_ids)
            valid = valid and clock.now().strftime('%Y-%m-%dT%H:%M:%SZ') < instruction.expires_at
            # Le mandat fixture couvre les deux valeurs de parametre de ce test.
            valid = valid and len(instruction.params) == 1 and instruction.params[0].str_value in ('hi', 'bye')
            if not valid:
                return (Diagnostic(step='validate', element='mandate', constraint='fixture_refused', message='Mandat fixture refuse.'),)
            return ()
    mand = Mand()
    def auditp():
        pol = AuditPolicy('fx-m9', '1', 'fx', 1, 65536, 50, (), 'fx-asset', ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE)
        class PS:
            def resolve(self, *, context, alias):
                assert context in (plat, cA, cB)
                return pol
        from pixs.core.audit_sink import PostgresAuditParticipant
        from pixs.agent.audit_adapter import AgentAuditAdapter
        return AgentAuditAdapter(PostgresAuditParticipant(PS(), clock, 'peer'))
    def svc(*, aud, gv, wav):
        return PostgresAgentManagementService(profile=pr, decider_factory=Fact(wav), clock=clock, audit_adapter=aud, governance_port=gv, mandate_port=mand, origin_port=None, confirmation_port=None, alias='default')
    def ctx(actor, scope, target, op, gen):
        iso = clock.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        return AgentValidationContext(actor, scope, target, gen, APPLY, '1.0.0', op, 'key:' + op, ('corr:' + op,), iso, 'mandat:' + op, None, None, 128, 8192, 8, 8, 3600)
    def req(dec, actor, target, act, scope, op):
        return Request(dec, actor, target, act, scope, 'corr:' + op)
    def ins(op, actor, scope, target, gen):
        exp = (clock.now() + datetime.timedelta(seconds=600)).strftime('%Y-%m-%dT%H:%M:%SZ')
        instruction = AgentManagementInstruction('1.0.0', op, APPLY, '1.0.0', actor, scope, target, gen, 'mandat:' + op, exp, ('corr:' + op,), ('cause:' + op,), 'key:' + op, (AgentParam('message', 'str', 'hi', None, None),))
        mandates[instruction.mandate_ref] = mandate_binding(instruction)
        return instruction
    def agent_rows():
        return tuple(list(model.objects.using('peer').order_by('id').values()) for model in (am.AgentHead, am.AgentOperation, am.AgentFact))
    def audit_ids():
        return set(CoreAuditEvent.objects.using('peer').values_list('record_id', flat=True))
    def assert_denial(previous_ids, actor, scope, target, correlation, code):
        added = list(CoreAuditEvent.objects.using('peer').exclude(record_id__in=previous_ids))
        assert len(added) == 1
        row = added[0]
        assert row.kind == 'GENERIC_AUDIT' and row.pdp_payload is None
        assert (row.scope_type, row.tenant_id, row.scope_id) == (scope.scope_type.value, scope.tenant_id, scope.scope_id)
        payload = row.generic_payload
        assert payload['result'] == 'DENIED' and payload['reason_or_error'] == code
        assert payload['actor_reference'] == actor and payload['resource_id'] == target
        assert payload['correlation_ids'] == [correlation] and payload['component_version'] == '0.1.0'
    def counts():
        return (am.AgentHead.objects.using('default').count(), am.AgentOperation.objects.using('default').count(), am.AgentFact.objects.using('default').count(), CoreAuditEvent.objects.using('peer').count())
    def need(c, m):
        assert c, m
    def refused(fn, code):
        try:
            fn()
        except AgentServiceError as e:
            assert e.code == code
            assert e.__cause__ is None
            return
        raise AssertionError('REFUS:' + code)
    from pixs.agent.service import AgentServiceError
    s = svc(aud=auditp(), gv=gov, wav=False)
    empty_op = 'op:m9-empty'
    empty_context = replace(ctx(aref(ord1), plat, TA, empty_op, 0), expected_operation=READ)
    empty_request = req('dec:m9-empty', aref(ord1), TA, READ, plat, empty_op)
    empty_rows, empty_audits = agent_rows(), audit_ids()
    empty_snapshot = s.query_state(request=empty_request, context=empty_context, limit=8)
    assert (empty_snapshot.target_id, empty_snapshot.scope_context, empty_snapshot.head_generation) == (TA, plat, 0)
    assert empty_snapshot.desired_doc is None and empty_snapshot.desired_request_op is None
    assert empty_snapshot.operations == () and empty_snapshot.facts == ()
    assert agent_rows() == empty_rows and all(not rows for rows in empty_rows)
    assert gov.reads[-1][4] == (TA,)
    empty_added = list(CoreAuditEvent.objects.using('peer').exclude(record_id__in=empty_audits))
    assert len(empty_added) == 2 and {row.kind for row in empty_added} == {'GENERIC_AUDIT', 'PDP_AUDIT'}
    empty_generic = next(row.generic_payload for row in empty_added if row.generic_payload is not None)
    assert empty_generic['result'] == 'READ' and empty_generic['actor_reference'] == aref(ord1)
    assert empty_generic['resource_id'] == TA and empty_generic['correlation_ids'] == [empty_request.correlation_id]
    cases['empty_query_without_desired'] = True
    op1 = 'op:m9-p1'
    r1 = req('dec:m9-p1', aref(ord1), TA, APPLY, plat, op1)
    c1 = ctx(aref(ord1), plat, TA, op1, 0)
    i1 = ins(op1, aref(ord1), plat, TA, 0)
    b0 = counts()
    initial_audits = audit_ids()
    rc = s.persist_desired(request=r1, context=c1, instruction=i1)
    need(rc.local_issue == 'PERSISTED' and rc.replay is False and type(rc.replay) is bool, 'p1')
    need(rc.generation == 1, 'g1')
    h = am.AgentHead.objects.using('default').get(target_id=TA)
    need((h.governance_ref, h.confidentiality, h.personal) == (gprof.data_asset_id, gprof.confidentiality.value, gprof.personal_data.value), 'meta')
    need(h.persistence_state == 'ACTIVE' and h.retention_state == 'RETAINED', 'st')
    prws = list(CoreAuditEvent.objects.using('peer').filter(operation_id=op1))
    need(len(prws) == 2, '2aud')
    gg = [x for x in prws if x.generic_payload is not None][0]
    need(gg.generic_payload['actor_reference'] == aref(ord1), 'actor')
    need(gg.generic_payload['correlation_ids'] == ['corr:' + op1], 'corr')
    need(gg.generic_payload['component_version'] == '0.1.0', 'man')
    need(gg.generic_payload['result'] == 'PERSISTED', 'res')
    operation = am.AgentOperation.objects.using('peer').get(pk=rc.local_ref)
    peer_head = am.AgentHead.objects.using('peer').get(pk=h.id)
    assert peer_head.desired_entry_id == operation.id and operation.subject_id == aref(ord1)
    assert counts()[:3] == (1, 1, 0) and len(audit_ids() - initial_audits) == 2
    assert (operation.governance_ref, operation.confidentiality, operation.personal) == (gprof.data_asset_id, gprof.confidentiality.value, gprof.personal_data.value)
    assert {row.kind for row in prws} == {'GENERIC_AUDIT', 'PDP_AUDIT'}
    need(am.AgentFact.objects.using('default').count() == 0, 'nf')
    cases['persist_normal'] = True
    qop = 'op:m9-q1'
    qc = AgentValidationContext(aref(ord1), plat, TA, 1, READ, '1.0.0', qop, 'key:' + qop, ('corr:' + qop,), clock.now().strftime('%Y-%m-%dT%H:%M:%SZ'), 'mandat:' + qop, None, None, 128, 8192, 8, 8, 3600)
    qr = req('dec:m9-q1', aref(ord1), TA, READ, plat, qop)
    query_audits = audit_ids()
    query_gov_reads = len(gov.reads)
    sn = s.query_state(request=qr, context=qc, limit=8)
    assert len(audit_ids() - query_audits) == 2 and len(gov.reads) == query_gov_reads + 1
    assert type(sn.facts) is tuple and sn.facts == ()
    assert all(type(item) is tuple for item in sn.operations)
    need(sn.head_generation == 1 and sn.desired_doc == am.AgentOperation.objects.using('default').get(request_operation_id=op1).content_canonical, 'snap')
    need(sn.desired_request_op == op1 and type(sn.operations) is tuple and len(sn.operations) == 1, 'ops')
    try:
        sn.head_generation = 9
        raise AssertionError('FROZEN')
    except FrozenInstanceError:
        pass
    cases['query_snapshot'] = True
    before = agent_rows()
    replay_audits = audit_ids()
    rc2 = s.persist_desired(request=r1, context=c1, instruction=i1)
    need(rc2.local_issue == 'REPLAY' and rc2.replay is True and type(rc2.replay) is bool, 'replay')
    need(rc2.local_ref == rc.local_ref, 'ref')
    assert agent_rows() == before
    assert len(audit_ids() - replay_audits) == 2
    cases['replay_immutable'] = True
    bad = replace(i1, params=(AgentParam('message', 'str', 'bye', None, None),))
    n0, a0 = agent_rows(), audit_ids()
    refused(lambda: s.persist_desired(request=r1, context=c1, instruction=bad), 'DEPOT_IMPOSSIBLE')
    assert agent_rows() == n0
    assert_denial(a0, aref(ord1), plat, TA, r1.correlation_id, 'DEPOT_IMPOSSIBLE')
    cases['divergence_refused_audited'] = True
    dp = deny('d-cur', aref(ord1), plat, TA, APPLY)
    CorePolicy.objects.create(policy_id=dp.policy_id, policy_version=dp.policy_version, owner=dp.owner, effect=dp.effect.value, definition=encode_policy(dp))
    try:
        n1, a1 = agent_rows(), audit_ids()
        refused(lambda: s.persist_desired(request=r1, context=c1, instruction=i1), 'ACTE_IMPOSSIBLE')
        assert agent_rows() == n1
        assert_denial(a1, aref(ord1), plat, TA, r1.correlation_id, 'ACTE_IMPOSSIBLE')
    finally:
        CorePolicy.objects.filter(policy_id='d-cur').delete()
    cases['deny_current_replay_audited'] = True
    sw = svc(aud=None, gv=None, wav=True)
    ow = 'op:m9-w1'
    rw = req('dec:' + ow, aref(root), TB, APPLY, plat, ow)
    cw = ctx(aref(root), plat, TB, ow, 0)
    iw = ins(ow, aref(root), plat, TB, 0)
    dp2 = deny('d-rb', aref(root), plat, TB, APPLY)
    CorePolicy.objects.create(policy_id=dp2.policy_id, policy_version=dp2.policy_version, owner=dp2.owner, effect=dp2.effect.value, definition=encode_policy(dp2))
    na = counts()[3]
    rrw = sw.persist_desired(request=rw, context=cw, instruction=iw)
    need(rrw.audit_disposition == 'WAIVED' and counts()[3] == na, 'waived')
    hw = am.AgentHead.objects.using('default').get(target_id=TB)
    need(hw.governance_ref is None and hw.confidentiality is None and hw.personal is None, 'nullmeta')
    cases['root_waiver_none'] = True
    hw.persistence_state = 'ARCHIVED'
    hw.retention_state = 'LEGAL_HOLD'
    hw.save(using='default')
    qw = AgentValidationContext(aref(root), plat, TB, 1, READ, '1.0.0', 'op:m9-wq', 'key:op:m9-wq', ('corr:op:m9-wq',), clock.now().strftime('%Y-%m-%dT%H:%M:%SZ'), 'mandat:op:m9-wq', None, None, 128, 8192, 8, 8, 3600)
    snw = sw.query_state(request=req('dec:m9-wq', aref(root), TB, READ, plat, 'op:m9-wq'), context=qw, limit=8)
    need(snw.head_generation == 1 and snw.desired_doc is not None, 'wquery')
    hw2 = am.AgentHead.objects.using('default').get(target_id=TB)
    need(hw2.persistence_state == 'ARCHIVED' and hw2.retention_state == 'LEGAL_HOLD' and hw2.governance_ref is None and hw2.confidentiality is None and hw2.personal is None, 'noreclass')
    assert counts()[3] == na
    cases['root_policy_waiver'] = True
    CorePolicy.objects.create(policy_id='a-grant-b', policy_version='v1', owner='syn.own', effect='ALLOW', definition=encode_policy(allow('a-grant-b', aref(root), cB, TB, APPLY)))
    ob = 'op:m9-ug'
    ungranted_before, ungranted_audit = agent_rows(), audit_ids()
    refused(lambda: svc(aud=auditp(), gv=gov, wav=True).persist_desired(request=req('dec:' + ob, aref(root), TB, APPLY, cB, ob), context=ctx(aref(root), cB, TB, ob, 0), instruction=ins(ob, aref(root), cB, TB, 0)), 'ACTE_IMPOSSIBLE')
    need(am.AgentHead.objects.using('default').filter(scope_type='TENANT', tenant_id=tB.pk, target_id=TB).count() == 0, 'noungranted')
    assert agent_rows() == ungranted_before
    assert_denial(ungranted_audit, aref(root), cB, TB, 'corr:' + ob, 'ACTE_IMPOSSIBLE')
    cases['root_ungranted_denied'] = True
    n5, a5 = agent_rows(), audit_ids()
    refused(lambda: s.dispatch(request=r1, context=c1, instruction=i1), 'PZT_TRANSPORT_UNAVAILABLE')
    assert agent_rows() == n5
    assert_denial(a5, aref(ord1), plat, TA, r1.correlation_id, 'PZT_TRANSPORT_UNAVAILABLE')
    cases['dispatch_denied_audited'] = True
    gm_op = 'op:m9-gm'
    gm_c = AgentValidationContext(aref(ord1), plat, TA, 1, READ, '1.0.0', gm_op, 'key:' + gm_op, ('corr:' + gm_op,), clock.now().strftime('%Y-%m-%dT%H:%M:%SZ'), 'mandat:' + gm_op, None, None, 128, 8192, 8, 8, 3600)
    gm_r = req('dec:m9-gm', aref(ord1), TA, READ, plat, gm_op)
    gm_reads = len(gov.reads)
    n_gm, a_gm = agent_rows(), audit_ids()
    refused(lambda: svc(aud=auditp(), gv=None, wav=False).query_state(request=gm_r, context=gm_c, limit=8), 'GOUVERNANCE_REFUSEE')
    assert agent_rows() == n_gm
    assert len(gov.reads) == gm_reads
    assert_denial(a_gm, aref(ord1), plat, TA, 'corr:' + gm_op, 'GOUVERNANCE_REFUSEE')
    cases['governance_missing'] = True
    hm_mu = am.AgentHead.objects.using('default').get(target_id=TA)
    old_mu = hm_mu.governance_ref
    hm_mu.governance_ref = None
    hm_mu.save(using='default')
    try:
        n_mu, a_mu = agent_rows(), audit_ids()
        mu_op = 'op:m9-mu'
        mu_c = AgentValidationContext(aref(ord1), plat, TA, 1, READ, '1.0.0', mu_op, 'key:' + mu_op, ('corr:' + mu_op,), clock.now().strftime('%Y-%m-%dT%H:%M:%SZ'), 'mandat:' + mu_op, None, None, 128, 8192, 8, 8, 3600)
        mu_r = req('dec:m9-mu', aref(ord1), TA, READ, plat, mu_op)
        refused(lambda: s.query_state(request=mu_r, context=mu_c, limit=8), 'METADONNEES_DIVERGENTES')
        assert agent_rows() == n_mu
        assert am.AgentHead.objects.using('default').get(target_id=TA).governance_ref is None
        assert_denial(a_mu, aref(ord1), plat, TA, 'corr:' + mu_op, 'METADONNEES_DIVERGENTES')
    finally:
        hm_mu.governance_ref = old_mu
        hm_mu.save(using='default')
    cases['metadata_unknown'] = True
    hs_ps = am.AgentHead.objects.using('default').get(target_id=TA)
    hs_ps.persistence_state = 'ARCHIVED'
    hs_ps.retention_state = 'LEGAL_HOLD'
    hs_ps.save(using='default')
    try:
        n_ps, a_ps = agent_rows(), audit_ids()
        ps_op = 'op:m9-ps'
        ps_c = AgentValidationContext(aref(ord1), plat, TA, 1, READ, '1.0.0', ps_op, 'key:' + ps_op, ('corr:' + ps_op,), clock.now().strftime('%Y-%m-%dT%H:%M:%SZ'), 'mandat:' + ps_op, None, None, 128, 8192, 8, 8, 3600)
        ps_r = req('dec:m9-ps', aref(ord1), TA, READ, plat, ps_op)
        refused(lambda: s.query_state(request=ps_r, context=ps_c, limit=8), 'ETAT_INACCESSIBLE')
        assert agent_rows() == n_ps
        assert_denial(a_ps, aref(ord1), plat, TA, 'corr:' + ps_op, 'ETAT_INACCESSIBLE')
    finally:
        hs_ps.persistence_state = 'ACTIVE'
        hs_ps.retention_state = 'RETAINED'
        hs_ps.save(using='default')
    cases['policy_state_inaccessible'] = True
    gov.mode = 'drift'
    gov.attest_calls = 0
    try:
        gd_op = 'op:m9-gd'
        gd_r = req('dec:' + gd_op, aref(ord1), TA, APPLY, plat, gd_op)
        gd_c = ctx(aref(ord1), plat, TA, gd_op, 1)
        gd_i = ins(gd_op, aref(ord1), plat, TA, 1)
        n_gd, a_gd = agent_rows(), audit_ids()
        base_gd = gov.attest_calls
        refused(lambda: s.persist_desired(request=gd_r, context=gd_c, instruction=gd_i), 'GOUVERNANCE_REFUSEE')
        assert gov.attest_calls - base_gd >= 2
        assert gov.drift_observed == (2, 2, 2, False, 0)
        assert agent_rows() == n_gd
        assert_denial(a_gd, aref(ord1), plat, TA, 'corr:' + gd_op, 'GOUVERNANCE_REFUSEE')
    finally:
        gov.mode = 'ok'
        gov.attest_calls = 0
    cases['governance_drift_final'] = True
    src.revoked = True
    try:
        n_rv, a_rv = agent_rows(), audit_ids()
        refused(lambda: s.persist_desired(request=r1, context=c1, instruction=i1), 'ACTE_IMPOSSIBLE')
        assert agent_rows() == n_rv
        added_rv = list(CoreAuditEvent.objects.using('peer').exclude(record_id__in=a_rv))
        assert len(added_rv) == 1
        row_rv = added_rv[0]
        assert row_rv.kind == 'GENERIC_AUDIT' and row_rv.pdp_payload is None
        assert (row_rv.scope_type, row_rv.tenant_id, row_rv.scope_id) == (plat.scope_type.value, plat.tenant_id, plat.scope_id)
        pay_rv = row_rv.generic_payload
        assert pay_rv['result'] == 'DENIED' and pay_rv['reason_or_error'] == 'ACTE_IMPOSSIBLE'
        assert pay_rv['actor_reference'] == 'UNVERIFIED' and pay_rv['resource_id'] == 'pixs.agent'
        assert type(pay_rv['correlation_ids']) is list and len(pay_rv['correlation_ids']) == 1 and pay_rv['correlation_ids'] != [r1.correlation_id]
        assert pay_rv['action'] == 'agent.management.refused' and pay_rv['component_id'] == 'pixs.agent'
        assert pay_rv['component_version'] == '0.1.0' and pay_rv['tenant_reference'] is None
        assert pay_rv['correlation_ids'] == [row_rv.operation_id]
        rendered = json.dumps(pay_rv, ensure_ascii=False)
        assert aref(ord1) not in rendered and r1.correlation_id not in rendered and TA not in rendered
    finally:
        src.revoked = False
    cases['revoked_replay'] = True
    class BadFact(Fact):
        def decider_for(self, *, request, alias, operation_id, purpose):
            raise TypeError('fixture decider boom')
    bad_svc = PostgresAgentManagementService(profile=pr, decider_factory=BadFact(False), clock=clock, audit_adapter=auditp(), governance_port=gov, mandate_port=mand, origin_port=None, confirmation_port=None, alias='default')
    n_pe, a_pe = agent_rows(), audit_ids()
    try:
        bad_svc.query_state(request=qr, context=qc, limit=8)
    except AgentServiceError:
        raise AssertionError('CONVERSION_REFUSEE')
    except TypeError as e:
        assert type(e) is TypeError and str(e) == 'fixture decider boom'
    else:
        raise AssertionError('TYPEERROR_ATTENDUE')
    assert agent_rows() == n_pe and audit_ids() == a_pe
    cases['programming_error_propagates'] = True
    DOC_OBS = 'fixture:applied-document-1'
    AT_OBS = clock.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    SRC_OBS = 'fixture:executor-a'
    ORIGIN_OBS = 'fixture:origin:' + op1
    CONF_ORIGIN = 'fixture:confirmation-origin:' + op1
    CONF_PROOF = 'fixture:confirmation-proof:' + op1
    POST_OK = 'fixture:postcondition:' + op1
    canon_op1 = am.AgentOperation.objects.using('default').get(request_operation_id=op1).content_canonical
    class OriginFx:
        def __init__(self):
            self.calls = []
            self.bool_mode = False
        def verify_origin(self, *, result, context, observed_document, observed_at, source_ref, target_id, scope):
            self.calls.append((result, context, observed_document, observed_at, source_ref, target_id, scope))
            if self.bool_mode is True:
                return True
            diags = []
            if not (type(result) is AgentManagementResult and result.operation_id == op1 and result.pa_target == TA and result.generation == 1 and result.scope_context == plat and result.outcome == 'ack' and result.correlation_ids == i1.correlation_ids and result.origin_proof == ORIGIN_OBS and result.occurred_at == AT_OBS):
                diags.append(Diagnostic(step='validate', element='origin.result', constraint='fixture_refused', message='Resultat fixture refuse.'))
            if not (type(context) is AgentValidationContext and context.expected_actor == aref(ord1) and context.expected_scope == plat and context.expected_target == TA and context.expected_generation == 1 and context.expected_operation_id == op1 and context.expected_operation == APPLY and context.expected_version == '1.0.0' and context.expected_origin_proof == ORIGIN_OBS):
                diags.append(Diagnostic(step='validate', element='origin.context', constraint='fixture_refused', message='Contexte fixture refuse.'))
            if not (observed_document == DOC_OBS and observed_at == AT_OBS and source_ref == SRC_OBS and target_id == TA and scope == plat):
                diags.append(Diagnostic(step='validate', element='origin.evidence', constraint='fixture_refused', message='Preuve fixture refusee.'))
            return tuple(diags)
    origin_fx = OriginFx()
    class ConfirmFx:
        def __init__(self):
            self.calls = []
        def verify_confirmation(self, *, state, result, observed_fact_id, observed_source_ref, observed_origin_proof, postcondition_ref, context, target_id, scope):
            self.calls.append((state, result, observed_fact_id, observed_source_ref, observed_origin_proof, postcondition_ref, context, target_id, scope))
            diags = []
            if not (type(result) is AgentManagementResult and result.operation_id == op1 and result.pa_target == TA and result.generation == 1 and result.scope_context == plat and result.outcome == 'confirmed' and result.correlation_ids == i1.correlation_ids and result.origin_proof == CONF_ORIGIN and result.occurred_at == AT_OBS):
                diags.append(Diagnostic(step='validate', element='confirm.result', constraint='fixture_refused', message='Resultat confirmation refuse.'))
            if not (type(context) is AgentValidationContext and context.expected_actor == aref(ord1) and context.expected_scope == plat and context.expected_target == TA and context.expected_generation == 1 and context.expected_operation_id == op1 and context.expected_operation == APPLY and context.expected_origin_proof == CONF_ORIGIN and context.expected_confirmation_proof == CONF_PROOF):
                diags.append(Diagnostic(step='validate', element='confirm.context', constraint='fixture_refused', message='Contexte confirmation refuse.'))
            if not (observed_source_ref == SRC_OBS and observed_origin_proof == ORIGIN_OBS and str(observed_fact_id) == str(parent_fact_id) and target_id == TA and scope == plat):
                diags.append(Diagnostic(step='validate', element='confirm.refs', constraint='fixture_refused', message='References confirmation refusees.'))
            if postcondition_ref != POST_OK:
                diags.append(Diagnostic(step='validate', element='confirm.postcondition', constraint='fixture_refused', message='Postcondition refusee.'))
            ok_state = (type(state) is AgentManagementState and state.confirmation_proof == CONF_PROOF and state.desired_doc == canon_op1 and state.observed_doc == DOC_OBS and state.observed_at == AT_OBS and state.operation_id == op1 and state.pa_target == TA and state.generation == 1 and state.scope_context == plat)
            if ok_state is not True:
                diags.append(Diagnostic(step='validate', element='confirm.state', constraint='fixture_refused', message='Etat confirmation refuse.'))
            return tuple(diags)
    confirm_fx = ConfirmFx()
    def svc_oc():
        return PostgresAgentManagementService(profile=pr, decider_factory=Fact(False), clock=clock, audit_adapter=auditp(), governance_port=gov, mandate_port=mand, origin_port=origin_fx, confirmation_port=confirm_fx, alias='default')
    obs_ctx = replace(ctx(aref(ord1), plat, TA, op1, 1), expected_origin_proof=ORIGIN_OBS)
    obs_res = AgentManagementResult(op1, TA, 1, plat, 'ack', i1.correlation_ids, AT_OBS, ORIGIN_OBS)
    conf_ctx = replace(ctx(aref(ord1), plat, TA, op1, 1), expected_origin_proof=CONF_ORIGIN, expected_confirmation_proof=CONF_PROOF)
    conf_res = AgentManagementResult(op1, TA, 1, plat, 'confirmed', i1.correlation_ids, AT_OBS, CONF_ORIGIN)
    origin_fx.bool_mode = True
    n_b1, a_b1 = agent_rows(), audit_ids()
    refused(lambda: svc_oc().append_observation(request=req('dec:obs-b1', aref(ord1), TA, OBS, plat, op1), context=obs_ctx, result=obs_res, observed_document=DOC_OBS, observed_at=AT_OBS, source_ref=SRC_OBS), 'ACTE_IMPOSSIBLE')
    assert len(origin_fx.calls) == 1
    full_b1 = origin_fx.calls[0]
    assert full_b1[0] == obs_res and full_b1[1] == obs_ctx and full_b1[2] == DOC_OBS and full_b1[3] == AT_OBS and full_b1[4] == SRC_OBS and full_b1[5] == TA and full_b1[6] == plat
    assert agent_rows() == n_b1
    assert_denial(a_b1, aref(ord1), plat, TA, 'corr:' + op1, 'ACTE_IMPOSSIBLE')
    origin_fx.calls.clear()
    origin_fx.bool_mode = False
    cases['origin_boolean_refused'] = True
    n_b2, a_b2 = agent_rows(), audit_ids()
    refused(lambda: svc_oc().append_observation(request=req('dec:obs-b2', aref(ord1), TA, OBS, plat, op1), context=obs_ctx, result=obs_res, observed_document=None, observed_at=None, source_ref=SRC_OBS), 'ORIGINE_REFUSEE')
    assert agent_rows() == n_b2
    assert am.AgentFact.objects.using('peer').count() == 0
    assert_denial(a_b2, aref(ord1), plat, TA, 'corr:' + op1, 'ORIGINE_REFUSEE')
    origin_fx.calls.clear()
    cases['origin_reference_only_refused'] = True
    n_b3, a_b3 = agent_rows(), audit_ids()
    head_b3 = am.AgentHead.objects.using('default').get(target_id=TA)
    op_b3 = am.AgentOperation.objects.using('default').get(request_operation_id=op1)
    rc_obs = svc_oc().append_observation(request=req('dec:obs-b3', aref(ord1), TA, OBS, plat, op1), context=obs_ctx, result=obs_res, observed_document=DOC_OBS, observed_at=AT_OBS, source_ref=SRC_OBS)
    need(rc_obs.local_issue == 'OBSERVED' and rc_obs.replay is False and rc_obs.audit_disposition == 'STAGED' and rc_obs.generation == 1, 'obs')
    assert am.AgentHead.objects.using('default').get(pk=head_b3.id).current_generation == head_b3.current_generation
    assert am.AgentOperation.objects.using('default').get(pk=op_b3.id).generation == 1
    new_b3 = list(CoreAuditEvent.objects.using('peer').exclude(record_id__in=a_b3))
    assert len(new_b3) == 2
    assert {x.kind for x in new_b3} == {'GENERIC_AUDIT', 'PDP_AUDIT'}
    assert [x for x in new_b3 if x.generic_payload is not None][0].generic_payload['result'] == 'OBSERVED'
    facts_b3 = list(am.AgentFact.objects.using('peer').exclude(pk__in=[r['id'] for r in n_b3[2]]))
    assert len(facts_b3) == 1
    f_b3 = facts_b3[0]
    assert f_b3.kind == 'OBSERVED' and f_b3.outcome == 'ack' and f_b3.generation == 1 and f_b3.scope_type == 'PLATFORM' and f_b3.tenant_id is None and f_b3.scope_id is None and f_b3.target_id == TA and f_b3.operation_id == op_b3.id and f_b3.observed_document == DOC_OBS and f_b3.observed_at == AT_OBS and f_b3.source_ref == SRC_OBS and f_b3.origin_proof == ORIGIN_OBS
    assert am.AgentFact.objects.using('peer').filter(kind='CONFIRMED').count() == 0
    assert agent_rows()[0] == n_b3[0] and agent_rows()[1] == n_b3[1]
    parent_fact_id = f_b3.id
    origin_fx.calls.clear()
    confirm_fx.calls.clear()
    cases['observation_fixture_admitted'] = True
    n_b4, a_b4 = agent_rows(), audit_ids()
    refused(lambda: svc_oc().confirm_observation(request=req('dec:conf-b4', aref(ord1), TA, CONF, plat, op1), context=conf_ctx, result=conf_res, observed_fact_id=parent_fact_id, proof_ref=CONF_PROOF, postcondition_ref='wrong'), 'DEPOT_IMPOSSIBLE')
    assert len(confirm_fx.calls) == 1
    assert str(confirm_fx.calls[0][2]) == str(parent_fact_id) and confirm_fx.calls[0][5] == 'wrong' and confirm_fx.calls[0][3] == SRC_OBS and confirm_fx.calls[0][4] == ORIGIN_OBS
    assert agent_rows() == n_b4
    assert am.AgentFact.objects.using('peer').filter(kind='CONFIRMED').count() == 0
    assert_denial(a_b4, aref(ord1), plat, TA, 'corr:' + op1, 'DEPOT_IMPOSSIBLE')
    confirm_fx.calls.clear()
    cases['confirmation_postcondition_refused'] = True
    n_b5, a_b5 = agent_rows(), audit_ids()
    rc_conf = svc_oc().confirm_observation(request=req('dec:conf-b5', aref(ord1), TA, CONF, plat, op1), context=conf_ctx, result=conf_res, observed_fact_id=parent_fact_id, proof_ref=CONF_PROOF, postcondition_ref=POST_OK)
    need(rc_conf.local_issue == 'CONFIRMED_LOCAL' and rc_conf.generation == 1 and rc_conf.audit_disposition == 'STAGED', 'conf')
    all_facts = list(am.AgentFact.objects.using('peer').order_by('id'))
    assert len(all_facts) == 2
    f_conf = [x for x in all_facts if x.kind == 'CONFIRMED'][0]
    assert str(f_conf.observed_fact_id) == str(parent_fact_id) and str(f_conf.operation_id) == str(op_b3.id) and f_conf.outcome == 'confirmed' and f_conf.generation == 1 and f_conf.scope_type == 'PLATFORM' and f_conf.tenant_id is None and f_conf.scope_id is None and f_conf.target_id == TA and f_conf.observed_document == DOC_OBS and f_conf.observed_at == AT_OBS and f_conf.source_ref == SRC_OBS and f_conf.origin_proof == CONF_ORIGIN and f_conf.proof_ref == CONF_PROOF and f_conf.postcondition_ref == POST_OK
    new_b5 = list(CoreAuditEvent.objects.using('peer').exclude(record_id__in=a_b5))
    assert len(new_b5) == 2 and {x.kind for x in new_b5} == {'GENERIC_AUDIT', 'PDP_AUDIT'}
    assert agent_rows()[0] == n_b5[0] and agent_rows()[1] == n_b5[1]
    assert am.AgentFact.objects.using('peer').filter(pk=parent_fact_id).values().get() == next(row for row in n_b5[2] if str(row['id']) == str(parent_fact_id))
    assert [x for x in new_b5 if x.generic_payload is not None][0].generic_payload['result'] == 'CONFIRMED_LOCAL'
    rendered_b5 = json.dumps([x.generic_payload for x in new_b5 if x.generic_payload is not None], ensure_ascii=False)
    assert all(value not in rendered_b5 for value in (DOC_OBS, ORIGIN_OBS, CONF_ORIGIN, CONF_PROOF, POST_OK))
    cases['confirmation_fixture_admitted'] = True
    dp_ta = deny('d-root-ta', aref(root), cA, TA, APPLY)
    CorePolicy.objects.create(policy_id=dp_ta.policy_id, policy_version=dp_ta.policy_version, owner=dp_ta.owner, effect=dp_ta.effect.value, definition=encode_policy(dp_ta))
    sw_ta = PostgresAgentManagementService(profile=pr, decider_factory=Fact(True), clock=clock, audit_adapter=None, governance_port=None, mandate_port=mand, origin_port=None, confirmation_port=None, alias='default')
    g6_op = 'op:m9-rta'
    g6_r = req('dec:' + g6_op, aref(root), TA, APPLY, cA, g6_op)
    g6_c = ctx(aref(root), cA, TA, g6_op, 0)
    g6_i = ins(g6_op, aref(root), cA, TA, 0)
    n6a = counts()[3]
    r6 = sw_ta.persist_desired(request=g6_r, context=g6_c, instruction=g6_i)
    need(r6.local_issue == 'PERSISTED' and r6.generation == 1 and r6.audit_disposition == 'WAIVED', 'rta')
    h6 = am.AgentHead.objects.using('default').get(scope_type='TENANT', tenant_id=tA.pk, scope_id=None, target_id=TA)
    op6 = am.AgentOperation.objects.using('peer').get(pk=r6.local_ref)
    assert op6.subject_id == aref(root) and op6.request_operation_id == g6_op and h6.desired_entry_id == op6.id
    assert (op6.scope_type, op6.tenant_id, op6.scope_id, op6.target_id) == ('TENANT', tA.pk, None, TA)
    assert (op6.governance_ref, op6.confidentiality, op6.personal) == (None, None, None)
    need((h6.governance_ref, h6.confidentiality, h6.personal) == (None, None, None), 'rta-meta')
    assert counts()[3] == n6a
    hp_after = am.AgentHead.objects.using('default').get(scope_type='PLATFORM', tenant_id=None, scope_id=None, target_id=TA)
    need(hp_after.current_generation == 1, 'plat-kept')
    cases['root_tenant_granted_service'] = True
    tbl_op = am.AgentOperation._meta.db_table
    fired1 = []
    conn1 = connections['default']
    def wrap1(execute, sql, params, many, context):
        txt = str(sql)
        if not fired1 and txt.strip().upper().startswith('INSERT') and tbl_op in txt:
            fired1.append(True)
            return execute('SELECT 1 / 0', None, False, context)
        return execute(sql, params, many, context)
    s1_op = 'op:m9-sq1'
    s1_r = req('dec:' + s1_op, aref(ord1), TA, APPLY, plat, s1_op)
    s1_c = ctx(aref(ord1), plat, TA, s1_op, 1)
    s1_i = ins(s1_op, aref(ord1), plat, TA, 1)
    n_sq1, a_sq1 = agent_rows(), audit_ids()
    with conn1.execute_wrapper(wrap1):
        refused(lambda: s.persist_desired(request=s1_r, context=s1_c, instruction=s1_i), 'DEPOT_IMPOSSIBLE')
    assert fired1 == [True]
    assert agent_rows() == n_sq1
    assert_denial(a_sq1, aref(ord1), plat, TA, 'corr:' + s1_op, 'DEPOT_IMPOSSIBLE')
    assert am.AgentHead.objects.using('default').filter(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True, target_id=TA).count() == 1
    cases['sql_failure_before_commit_real'] = True
    tbl_au = CoreAuditEvent._meta.db_table
    fired2 = []
    seen2 = {}
    conn2 = connections['default']
    c2_op = 'op:m9-au1'
    def wrap2(execute, sql, params, many, context):
        txt = str(sql)
        if not fired2 and txt.strip().upper().startswith('INSERT') and tbl_au in txt:
            fired2.append(True)
            seen2['op_local'] = am.AgentOperation.objects.using('default').filter(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True, target_id=TA, request_operation_id=c2_op).first()
            seen2['head_local'] = am.AgentHead.objects.using('default').filter(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True, target_id=TA).first()
            seen2['peer_op'] = am.AgentOperation.objects.using('peer').filter(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True, target_id=TA, request_operation_id=c2_op).first()
            seen2['peer_audits'] = CoreAuditEvent.objects.using('peer').filter(operation_id=c2_op).count()
            return execute('SELECT 1 / 0', None, False, context)
        return execute(sql, params, many, context)
    c2_r = req('dec:' + c2_op, aref(ord1), TA, APPLY, plat, c2_op)
    c2_c = ctx(aref(ord1), plat, TA, c2_op, 1)
    c2_i = ins(c2_op, aref(ord1), plat, TA, 1)
    n_au, a_au = agent_rows(), audit_ids()
    with conn2.execute_wrapper(wrap2):
        refused(lambda: s.persist_desired(request=c2_r, context=c2_c, instruction=c2_i), 'AUDIT_IMPOSSIBLE')
    assert fired2 == [True]
    assert seen2['op_local'] is not None and seen2['op_local'].generation == 2
    assert seen2['head_local'] is not None and seen2['head_local'].current_generation == 2
    assert seen2['peer_op'] is None and seen2['peer_audits'] == 0
    assert agent_rows() == n_au
    assert CoreAuditEvent.objects.using('peer').filter(operation_id=c2_op).count() == 0
    assert_denial(a_au, aref(ord1), plat, TA, 'corr:' + c2_op, 'AUDIT_IMPOSSIBLE')
    cases['c05_failure_rolls_back_real'] = True
    from pixs.agent.service import _advisory_key
    key3 = _advisory_key(plat, TA)
    probes3 = []
    base_factory3 = Fact(False)
    class SpyFactory3:
        def decider_for(self, *, request, alias, operation_id, purpose):
            inner = base_factory3.decider_for(request=request, alias=alias, operation_id=operation_id, purpose=purpose)
            outer = probes3
            k = key3
            class SpyDecider3:
                def revalidate_under_locks(self, req2, *, alias, operation_id):
                    dec = inner.revalidate_under_locks(req2, alias=alias, operation_id=operation_id)
                    from django.db import connections as conns3
                    peer3 = conns3['peer']
                    with peer3.cursor() as cur3:
                        cur3.execute('SELECT pg_try_advisory_lock(%s);', [k])
                        got3 = cur3.fetchone()[0]
                    try:
                        assert type(got3) is bool
                        outer.append(got3)
                    finally:
                        if got3 is True:
                            with peer3.cursor() as cur4:
                                cur4.execute('SELECT pg_advisory_unlock(%s);', [k])
                                assert cur4.fetchone()[0] is True
                    return dec
                def audit_waived(self, *a3, **k3):
                    return inner.audit_waived(*a3, **k3)
                def governance_waived(self, *a3, **k3):
                    return inner.governance_waived(*a3, **k3)
            return SpyDecider3()
        def authentication_for(self, *, request, alias, operation_id, purpose):
            return base_factory3.authentication_for(request=request, alias=alias, operation_id=operation_id, purpose=purpose)
    svc3 = PostgresAgentManagementService(profile=pr, decider_factory=SpyFactory3(), clock=clock, audit_adapter=auditp(), governance_port=gov, mandate_port=mand, origin_port=None, confirmation_port=None, alias='default')
    q3_op = 'op:m9-mx'
    q3_c = AgentValidationContext(aref(ord1), plat, TA, 1, READ, '1.0.0', q3_op, 'key:' + q3_op, ('corr:' + q3_op,), clock.now().strftime('%Y-%m-%dT%H:%M:%SZ'), 'mandat:' + q3_op, None, None, 128, 8192, 8, 8, 3600)
    q3_r = req('dec:m9-mx', aref(ord1), TA, READ, plat, q3_op)
    n_mx, a_mx = agent_rows(), audit_ids()
    sn3 = svc3.query_state(request=q3_r, context=q3_c, limit=8)
    assert len(probes3) >= 3 and probes3[0] is True and all(p is False for p in probes3[1:])
    need(sn3.head_generation == 1 and len(sn3.facts) == 2, 'mx-snap')
    assert agent_rows() == n_mx
    assert len(audit_ids() - a_mx) == 2
    cases['core_before_agent_mutex_real'] = True
    c4_op = 'op:m9-cl'
    c4_r = req('dec:' + c4_op, aref(ord1), TA, APPLY, plat, c4_op)
    c4_c = ctx(aref(ord1), plat, TA, c4_op, 1)
    c4_i = ins(c4_op, aref(ord1), plat, TA, 1)
    n_cl, a_cl = agent_rows(), audit_ids()
    from django.db import InterfaceError as DjangoInterfaceError
    calls4 = []
    holder4 = connections['default']
    real_commit4 = holder4.commit
    def fake_commit4(*a4, **k4):
        calls4.append(True)
        out4 = real_commit4(*a4, **k4)
        if len(calls4) == 1:
            raise DjangoInterfaceError('fixture:commit-response-lost')
        return out4
    holder4.commit = fake_commit4
    try:
        refused(lambda: s.persist_desired(request=c4_r, context=c4_c, instruction=c4_i), 'ISSUE_INCONNUE')
    finally:
        holder4.commit = real_commit4
    assert len(calls4) == 1
    assert len(agent_rows()[1]) == len(n_cl[1]) + 1 and agent_rows()[2] == n_cl[2]
    op_cl = am.AgentOperation.objects.using('peer').filter(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True, target_id=TA, request_operation_id=c4_op).first()
    assert op_cl is not None and op_cl.generation == 2
    head_cl = am.AgentHead.objects.using('peer').filter(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True, target_id=TA).first()
    assert head_cl is not None and head_cl.current_generation == 2 and head_cl.desired_entry_id == op_cl.id
    new_cl = list(CoreAuditEvent.objects.using('peer').exclude(record_id__in=a_cl))
    assert len(new_cl) == 2 and {x.kind for x in new_cl} == {'GENERIC_AUDIT', 'PDP_AUDIT'}
    assert [x for x in new_cl if x.generic_payload is not None][0].generic_payload['result'] == 'PERSISTED'
    assert am.AgentFact.objects.using('peer').filter(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True, target_id=TA).count() == 2
    r2_op = 'op:m9-clq'
    r2_c = AgentValidationContext(aref(ord1), plat, TA, 2, READ, '1.0.0', r2_op, 'key:' + r2_op, ('corr:' + r2_op,), clock.now().strftime('%Y-%m-%dT%H:%M:%SZ'), 'mandat:' + r2_op, None, None, 128, 8192, 8, 8, 3600)
    r2_r = req('dec:m9-clq', aref(ord1), TA, READ, plat, r2_op)
    n_cl3, a_cl3 = agent_rows(), audit_ids()
    sn_cl = s.query_state(request=r2_r, context=r2_c, limit=8)
    need(sn_cl.head_generation == 2 and sn_cl.desired_request_op == c4_op and len(sn_cl.facts) == 2, 'reconcile')
    assert sn_cl.desired_doc == op_cl.content_canonical and all(fact[4] == 1 for fact in sn_cl.facts)
    assert agent_rows() == n_cl3
    assert len(audit_ids() - a_cl3) == 2
    cases['commit_response_lost_reconciled_real'] = True
    assert set(cases) == set(EXPECTED_CASES)
    return cases
def main():
    import json
    r = harness.run_in_agent_schema(ROOT, _cases, EXPECTED_CASES, with_core=True)
    print(json.dumps(r, sort_keys=True, ensure_ascii=False))
    return 0 if (r['real_pg'] is True and set(r['cases']) == set(EXPECTED_CASES) and all(v is True for v in r['cases'].values())) else 1
if __name__ == '__main__':
    raise SystemExit(main())
