"""Fixtures Agent partagees : Core/C05 PG reels, Auth et confiance synthetiques.

A appeler uniquement apres configuration du schema prive par le harnais PG.
Aucune lecture env ni qualification PA/PZT/C03 dans ce module.
"""
from __future__ import annotations
import datetime
from types import SimpleNamespace
TA = 'agent:target-a'
TB = 'agent:target-b'
APPLY = 'agent.apply'
READ = 'agent.read'
OBS = 'agent.observe'
CONF = 'agent.confirm'

def build_agent_service_fixture():
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
    return SimpleNamespace(
        plat=plat, cA=cA, cB=cB, tA=tA, tB=tB, ord1=ord1, root=root,
        aref=aref, clock=clock, pr=pr, Fact=Fact, src=src, gov=gov,
        gprof=gprof, mand=mand, prof=prof, auditp=auditp, svc=svc,
        ctx=ctx, req=req, ins=ins, agent_rows=agent_rows, audit_ids=audit_ids,
        assert_denial=assert_denial, counts=counts, refused=refused,
        TA=TA, TB=TB, APPLY=APPLY, READ=READ, OBS=OBS, CONF=CONF,
    )
