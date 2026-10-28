'''Recette autorisation Agent sur C04 PostgreSQL reel, sans autre service.

Le harness Auth sert seulement a l isolation PG et aux migrations Core.
Source Auth synthetique explicite, sans preuve C03 ; fabrique privee liee
qui renvoie le VRAI RuntimeAuthorizationDecider. Aucun faux decideur pour
les cas nominaux et SA. Aucune fabrication de permission par DTO client.
'''
from __future__ import annotations
import datetime
import json
import sys
from dataclasses import replace
sys.path.insert(0, 'src')
sys.path.insert(0, 'tests/integration')
import auth_pg_test_support as harness
ROOT = '/home/devops/datas/pixs'
EXPECTED_CASES = (
    'ordinary_allow_puis_deny_prioritaire',
    'preuve_version_source_publique',
    'root_platform_malgre_deny',
    'root_tenant_a_accorde_malgre_deny',
    'root_tenant_b_non_accorde_meme_acl_allow',
    'service_pas_root_aucune_derogation',
    'derogations_root_permitted_seulement',
    'revocation_ferme_derogation_sans_transfert',
    'expiration_ferme_derogation',
    'autorisation_nominale_puis_verification_finale',
    'liaisons_toutes_refusees',
    'catalogue_version_type_invalides',
    'bornes_contexte_differentes_refusees',
    'operation_action_divergente_refusee',
    'instruction_expiree_clock_actuelle_refusee',
    'sujet_uuid_brut_decision_invalide',
    'tx_absente_refusee_avant_fabrique',
    'helper_apres_commit_nouvelle_tx_refuse',
    'remplacement_connexion_nouvelle_tx_refuse',
    'preuve_copiee_forgee_refusee',
    'preuve_autre_helper_refusee',
    'pin_stable_savepoint_sans_fuite',
    'mock_obligation_inconnue_refusee_distinct_c04',
    'defaut_prog_propage_sans_masque',
    'refus_exact_pas_autre_cause',
    'texte_invalide_chr_refuse',
)
ACTION = 'agent.apply'
TARGET_A = 'agent:target-a'
TARGET_B = 'agent:target-b'
def _cases():
    from django.db import connections, transaction
    from pixs.agent.authorization import AgentAuthorization, AgentAuthorizationError, _SealedAuthorization
    from pixs.agent.contracts import AgentManagementInstruction, AgentParam, AgentParamSpec, AgentValidationContext, AllowedCatalogEntry
    from pixs.agent.ports import AgentOperationalProfile
    from pixs.core.audit_contracts import encode_policy_version
    from pixs.core.authz.decision import Decision
    from pixs.core.authz.policy import AuthenticationAssurance, Effect, FederationTrust, IdentityAssurance, Obligation, Policy, ScopeSelector, Selector
    from pixs.core.authz.ports import AuthenticationContext, PortError, Request, RevocationStatus, TrustedFacts
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.persistence.models_identity import CoreIdentity, CoreSuperAdminBinding, CoreSuperAdminTenantGrant
    from pixs.core.persistence.models_scope import CoreTenant
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.scope.ownership import ResourceOwnership
    from pixs.core.services_authorization_guard import transaction_identity
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider, RuntimeWaiverRequest
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    platform = ScopeContext(ScopeType.PLATFORM)
    tenant_a = CoreTenant.objects.create(tenant_id='tenant-a-agent')
    tenant_b = CoreTenant.objects.create(tenant_id='tenant-b-agent')
    ca = ScopeContext(ScopeType.TENANT, tenant_a.pk)
    cb = ScopeContext(ScopeType.TENANT, tenant_b.pk)
    ordinary = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type='HUMAN', state='ACTIVE')
    root = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type='DEVICE', state='ACTIVE')
    service = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type='SERVICE', state='ACTIVE')
    binding = CoreSuperAdminBinding.objects.create(installation_ref='synthetic-install-agent', identity=root)
    CoreSuperAdminTenantGrant.objects.create(binding=binding, tenant=tenant_a)
    def ref(identity):
        return 'pixs.core.identity:' + str(identity.pk)
    limits = Limits(128, 128, 10, 20, 20, 128, 256, 256, 100000000, 60, 3600)
    catalog = Catalog((ref(ordinary), ref(root), ref(service)), (TARGET_A, TARGET_B), (ACTION,), (platform, ca, cb), ())
    class Clock:
        def __init__(self, instant):
            self.instant = instant
        def now(self):
            return self.instant
    base_now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    class SyntheticAuth:
        def __init__(self, clock):
            self.clock = clock
            self.revoked = False
        def resolve(self, request):
            now = self.clock.now()
            auth = AuthenticationContext(request.subject_id, 'synthetic.c03.agent', 'synthetic.issuer', 'synthetic.subject', now - datetime.timedelta(seconds=30), now + datetime.timedelta(hours=1), ('synthetic.password',), IdentityAssurance.CLAIMED, AuthenticationAssurance.SINGLE_FACTOR, FederationTrust.UNTRUSTED, request.context, None, None)
            return TrustedFacts(request.subject_id, request.resource_id, request.action_id, auth, ResourceOwnership(request.resource_id, request.context), request.context, RevocationStatus.REVOKED if self.revoked else RevocationStatus.ACTIVE, (), ())
    def make_store():
        return CoreAuthorizationStore(alias='default', installation_ref='synthetic-install-agent', base_epoch='synthetic-epoch-agent', catalog=catalog, limits=limits)
    def profile():
        apply_entry = AllowedCatalogEntry('agent.apply', '1.0.0', (AgentParamSpec('message', 'str', 16, None, None, True),))
        noop_entry = AllowedCatalogEntry('agent.noop', '1.0.0', ())
        mapping = (('desired.persist', ('agent.apply',)), ('observation.append', ('agent.noop',)), ('confirmation.confirm', ('agent.noop',)), ('state.query', ('agent.noop',)))
        return AgentOperationalProfile((apply_entry, noop_entry), mapping, 128, 256, 8, 8, 60)
    def evaluate(req, *, store=None):
        clock = Clock(base_now)
        source = SyntheticAuth(clock)
        obj = RuntimeAuthorizationDecider(store=make_store() if store is None else store, facts_provider=source, clock=clock, request=req, operation_id='operation:' + req.decision_id)
        return obj.revalidate_under_locks(req, alias='default', operation_id='operation:' + req.decision_id)
    def agent_context_for(actor_ref, context, target, op, key, corr, clock):
        now_iso = clock.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        return AgentValidationContext(expected_actor=actor_ref, expected_scope=context, expected_target=target, expected_generation=0, expected_operation=ACTION, expected_version='1.0.0', expected_operation_id=op, expected_idempotency_key=key, expected_correlation_ids=(corr,), now_iso=now_iso, mandate_proof='mandate:agent:' + op, expected_origin_proof=None, expected_confirmation_proof=None, max_id_len=128, max_doc_len=256, max_ids=8, max_params=8, max_observation_age_seconds=60)
    class _AgentFactory:
        def __init__(self, store, source, clock, request, alias, operation_id, purpose, waiver=None):
            self._store = store
            self._source = source
            self._clock = clock
            self._request = request
            self._alias = alias
            self._operation_id = operation_id
            self._purpose = purpose
            self._waiver = waiver
        def decider_for(self, *, request, alias, operation_id, purpose):
            if request != self._request or alias != self._alias or operation_id != self._operation_id or purpose != self._purpose:
                raise PortError()
            return RuntimeAuthorizationDecider(store=self._store, facts_provider=self._source, clock=self._clock, request=request, operation_id=operation_id, waiver_request=self._waiver)
    def make_helper(actor_ref, context, suffix, *, store=None, source=None, clock=None, target=TARGET_A, purpose='desired.persist', alias='default', waiver=False):
        store = make_store() if store is None else store
        clock = Clock(base_now) if clock is None else clock
        source = SyntheticAuth(clock) if source is None else source
        tag = 'h:' + suffix
        req = Request('decision:agent:' + tag, actor_ref, target, ACTION if purpose == 'desired.persist' else 'agent.noop', context, 'corr:agent:' + tag)
        op = 'op:agent:' + tag
        ctx = agent_context_for(actor_ref, context, target, op, 'key:agent:' + tag, 'corr:agent:' + tag, clock)
        intent = RuntimeWaiverRequest(req, alias, op, True, True) if waiver else None
        factory = _AgentFactory(store, source, clock, req, alias, op, purpose, intent)
        helper = AgentAuthorization(profile=profile(), request=req, agent_context=ctx, alias=alias, operation_id=op, purpose=purpose, decider_factory=factory, clock=clock)
        return (helper, req, ctx, op, store, source, clock, factory)
    def refused(fn, expected):
        try:
            fn()
        except AgentAuthorizationError as error:
            assert error.code == expected
            assert error.__cause__ is None
            return
        raise AssertionError('REFUS_ATTENDU')
    def propagates(fn, exc_type):
        try:
            fn()
        except exc_type as error:
            assert type(error) is exc_type
            assert not isinstance(error, AgentAuthorizationError)
            return
        raise AssertionError('PROPAGATION_ATTENDUE')
    def allow_policy(pid, actor, context=platform, resource=TARGET_A):
        return Policy(pid, 'v1', 'synthetic.owner', Effect.ALLOW, Selector('subject', (actor,)), Selector('resource', (resource,)), Selector('action', (ACTION,)), ScopeSelector((context,)), obligations=(Obligation('AUDIT'),))
    def deny_policy(pid, actor, context=platform, resource=TARGET_A):
        return Policy(pid, 'v1', 'synthetic.owner', Effect.DENY, Selector('subject', (actor,)), Selector('resource', (resource,)), Selector('action', (ACTION,)), ScopeSelector((context,)))
    def persist(policy_obj):
        return CorePolicy.objects.create(policy_id=policy_obj.policy_id, policy_version=policy_obj.policy_version, owner=policy_obj.owner, effect=policy_obj.effect.value, definition=encode_policy(policy_obj))
    def rollback():
        transaction.set_rollback(True, using='default')
    def instruction_for(op, subject, context, target, key, corr, clock, catalog_operation=ACTION, catalog_version='1.0.0', expires_in_seconds=60, params=None):
        expires = (clock.now() + datetime.timedelta(seconds=expires_in_seconds)).strftime('%Y-%m-%dT%H:%M:%SZ')
        return AgentManagementInstruction(schema_version='1.0.0', operation_id=op, catalog_operation=catalog_operation, catalog_version=catalog_version, initial_actor=subject, scope_context=context, pa_target=target, expected_generation=0, mandate_ref='mandate:agent:' + op, expires_at=expires, correlation_ids=(corr,), causation_ids=('cause:agent:' + op,), idempotency_key=key, params=(AgentParam('message', 'str', 'hello', None, None),) if params is None else params)
    cases = {}
    def agent_request(actor_ref, context, suffix, resource=TARGET_A):
        return Request('decision:agent:' + suffix, actor_ref, resource, ACTION, context, 'corr:agent:' + suffix)
    refused(lambda: make_helper(ref(ordinary), platform, 'hors-tx')[0], 'TX_ABSENTE')
    cases['tx_absente_refusee_avant_fabrique'] = True
    with transaction.atomic(using='default', durable=True):
        assert evaluate(agent_request(ref(ordinary), platform, 'ordinary-1')).effect is Effect.DENY
        persist(allow_policy('allow-ordinary-agent', ref(ordinary)))
        assert evaluate(agent_request(ref(ordinary), platform, 'ordinary-2')).effect is Effect.ALLOW
        persist(deny_policy('deny-ordinary-agent', ref(ordinary)))
        assert evaluate(agent_request(ref(ordinary), platform, 'ordinary-3')).effect is Effect.DENY
        rollback()
    cases['ordinary_allow_puis_deny_prioritaire'] = True
    with transaction.atomic(using='default', durable=True):
        store = make_store()
        persist(allow_policy('allow-version-src-agent', ref(ordinary)))
        snapshot = store.pinned_snapshot(context=platform, actor_ref=ref(ordinary))[0]
        decision = evaluate(agent_request(ref(ordinary), platform, 'version-src'), store=store)
        assert decision.effect is Effect.ALLOW
        assert decision.policy_version == snapshot.version
        assert encode_policy_version(decision.policy_version)['encoded_policy_version'] is not None
        rollback()
    cases['preuve_version_source_publique'] = True
    with transaction.atomic(using='default', durable=True):
        persist(deny_policy('deny-root-agent', ref(root)))
        assert evaluate(agent_request(ref(root), platform, 'root-platform')).effect is Effect.ALLOW
        rollback()
    cases['root_platform_malgre_deny'] = True
    with transaction.atomic(using='default', durable=True):
        persist(deny_policy('deny-root-a-agent', ref(root), ca))
        assert evaluate(agent_request(ref(root), ca, 'root-a')).effect is Effect.ALLOW
        rollback()
    cases['root_tenant_a_accorde_malgre_deny'] = True
    with transaction.atomic(using='default', durable=True):
        persist(allow_policy('allow-root-b-agent', ref(root), cb))
        assert evaluate(agent_request(ref(root), cb, 'root-b')).effect is Effect.DENY
        rollback()
    cases['root_tenant_b_non_accorde_meme_acl_allow'] = True
    with transaction.atomic(using='default', durable=True):
        persist(allow_policy('allow-service-agent', ref(service)))
        clock = Clock(base_now)
        source = SyntheticAuth(clock)
        req = agent_request(ref(service), platform, 'service-1')
        op = 'op:agent:service-1'
        waiver = RuntimeWaiverRequest(req, 'default', op, True, True)
        decider = RuntimeAuthorizationDecider(store=make_store(), facts_provider=source, clock=clock, request=req, operation_id=op, waiver_request=waiver)
        decision = decider.revalidate_under_locks(req, alias='default', operation_id=op)
        assert decision.effect is Effect.ALLOW
        assert decider.audit_waived(req, decision, alias='default', operation_id=op) is False
        assert decider.governance_waived(req, decision, alias='default', operation_id=op) is False
        rollback()
    cases['service_pas_root_aucune_derogation'] = True
    with transaction.atomic(using='default', durable=True):
        clock = Clock(base_now)
        source = SyntheticAuth(clock)
        req = agent_request(ref(root), platform, 'waiver-root')
        op = 'op:agent:waiver-root'
        decider = RuntimeAuthorizationDecider(store=make_store(), facts_provider=source, clock=clock, request=req, operation_id=op, waiver_request=RuntimeWaiverRequest(req, 'default', op, True, True))
        decision = decider.revalidate_under_locks(req, alias='default', operation_id=op)
        assert decision.effect is Effect.ALLOW
        assert decider.audit_waived(req, decision, alias='default', operation_id=op) is True
        assert decider.governance_waived(req, decision, alias='default', operation_id=op) is True
        oreq = agent_request(ref(ordinary), platform, 'waiver-ord')
        oop = 'op:agent:waiver-ord'
        persist(allow_policy('allow-waiver-ord-agent', ref(ordinary)))
        odecider = RuntimeAuthorizationDecider(store=make_store(), facts_provider=source, clock=clock, request=oreq, operation_id=oop, waiver_request=RuntimeWaiverRequest(oreq, 'default', oop, True, True))
        odecision = odecider.revalidate_under_locks(oreq, alias='default', operation_id=oop)
        assert odecision.effect is Effect.ALLOW
        assert odecider.audit_waived(oreq, odecision, alias='default', operation_id=oop) is False
        nreq = agent_request(ref(root), platform, 'waiver-none')
        noop = 'op:agent:waiver-none'
        ndecider = RuntimeAuthorizationDecider(store=make_store(), facts_provider=source, clock=clock, request=nreq, operation_id=noop)
        ndecision = ndecider.revalidate_under_locks(nreq, alias='default', operation_id=noop)
        assert ndecision.effect is Effect.ALLOW
        assert ndecider.audit_waived(nreq, ndecision, alias='default', operation_id=noop) is False
        rollback()
    cases['derogations_root_permitted_seulement'] = True
    with transaction.atomic(using='default', durable=True):
        clock = Clock(base_now)
        source = SyntheticAuth(clock)
        req = agent_request(ref(root), platform, 'rev-1')
        op = 'op:agent:rev-1'
        decider = RuntimeAuthorizationDecider(store=make_store(), facts_provider=source, clock=clock, request=req, operation_id=op, waiver_request=RuntimeWaiverRequest(req, 'default', op, True, True))
        decision = decider.revalidate_under_locks(req, alias='default', operation_id=op)
        assert decider.audit_waived(req, decision, alias='default', operation_id=op) is True
        source.revoked = True
        assert decider.audit_waived(req, decision, alias='default', operation_id=op) is False
        assert decider.revalidate_under_locks(req, alias='default', operation_id=op).effect is Effect.DENY
        source.revoked = False
    cases['revocation_ferme_derogation_sans_transfert'] = True
    with transaction.atomic(using='default', durable=True):
        clock = Clock(base_now)
        source = SyntheticAuth(clock)
        req = agent_request(ref(root), platform, 'exp-1')
        op = 'op:agent:exp-1'
        decider = RuntimeAuthorizationDecider(store=make_store(), facts_provider=source, clock=clock, request=req, operation_id=op, waiver_request=RuntimeWaiverRequest(req, 'default', op, True, True))
        decision = decider.revalidate_under_locks(req, alias='default', operation_id=op)
        assert decider.audit_waived(req, decision, alias='default', operation_id=op) is True
        clock.instant = decision.expires_at
        assert decider.audit_waived(req, decision, alias='default', operation_id=op) is False
    cases['expiration_ferme_derogation'] = True
    with transaction.atomic(using='default', durable=True):
        persist(allow_policy('allow-nominal-agent', ref(ordinary)))
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'nominal-1')
        instruction = instruction_for(op, ref(ordinary), platform, TARGET_A, 'key:agent:h:nominal-1', 'corr:agent:h:nominal-1', clock)
        assert helper.bind_instruction(instruction) is None
        proof = helper.authorize()
        assert proof.decision.effect is Effect.ALLOW
        assert helper.verify_final(proof) is None
        rollback()
    cases['autorisation_nominale_puis_verification_finale'] = True
    with transaction.atomic(using='default', durable=True):
        helper0, req0, ctx0, op0, store0, source0, clock0, factory0 = make_helper(ref(ordinary), platform, 'liaison-base')
        prof0 = helper0.profile
        def build(req=None, ctx=None, alias='default', op=None, purpose='desired.persist'):
            return AgentAuthorization(profile=prof0, request=req0 if req is None else req, agent_context=ctx0 if ctx is None else ctx, alias=alias, operation_id=op0 if op is None else op, purpose=purpose, decider_factory=factory0, clock=clock0)
        refused(lambda: build(req=Request(req0.decision_id, 'autre-acteur', req0.resource_id, req0.action_id, req0.context, req0.correlation_id)), 'LIAISON_ACTEUR_INVALIDE')
        refused(lambda: build(req=Request(req0.decision_id, req0.subject_id, req0.resource_id, req0.action_id, ca, req0.correlation_id)), 'LIAISON_CONTEXTE_INVALIDE')
        refused(lambda: build(req=Request(req0.decision_id, req0.subject_id, TARGET_B, req0.action_id, req0.context, req0.correlation_id)), 'LIAISON_CIBLE_INVALIDE')
        refused(lambda: build(req=Request(req0.decision_id, req0.subject_id, req0.resource_id, req0.action_id, req0.context, 'corr:autre')), 'LIAISON_CORRELATION_INVALIDE')
        refused(lambda: build(req=Request(req0.decision_id, req0.subject_id, req0.resource_id, 'agent.noop', req0.context, req0.correlation_id)), 'ACTION_NON_AUTORISEE')
        refused(lambda: build(purpose='etat.inconnu'), 'INTENTION_INVALIDE')
        refused(lambda: build(purpose='state.query'), 'ACTION_NON_AUTORISEE')
        refused(lambda: build(op='op:agent:autre'), 'LIAISON_OPERATION_INVALIDE')
        refused(lambda: build(alias='peer'), 'TX_ABSENTE')
    cases['liaisons_toutes_refusees'] = True
    with transaction.atomic(using='default', durable=True):
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'catalogue-1')
        key = 'key:agent:h:catalogue-1'
        corr = 'corr:agent:h:catalogue-1'
        refused(lambda: helper.bind_instruction(instruction_for(op, ref(ordinary), platform, TARGET_A, key, corr, clock, catalog_version='x')), 'INSTRUCTION_INVALIDE')
        refused(lambda: helper.bind_instruction(instruction_for(op, ref(ordinary), platform, TARGET_A, key, corr, clock, catalog_operation='pa.inconnu')), 'INSTRUCTION_INVALIDE')
        refused(lambda: helper.bind_instruction(instruction_for(op, ref(ordinary), platform, TARGET_A, key, corr, clock, params=(AgentParam('message', 'int', None, 5, None),))), 'INSTRUCTION_INVALIDE')
        refused(lambda: helper.bind_instruction(instruction_for(op, ref(ordinary), platform, TARGET_A, key, corr, clock, params=())), 'INSTRUCTION_INVALIDE')
        refused(lambda: helper.bind_instruction(instruction_for(op, ref(ordinary), platform, TARGET_A, key, corr, clock, params=(AgentParam('message', 'str', 'a', None, None), AgentParam('message', 'str', 'b', None, None)))), 'INSTRUCTION_INVALIDE')
    cases['catalogue_version_type_invalides'] = True
    with transaction.atomic(using='default', durable=True):
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'bornes-1')
        from dataclasses import replace as _replace
        for field in ('max_id_len', 'max_params'):
            kwargs = {field: getattr(ctx, field) + 1}
            bad = _replace(ctx, **kwargs)
            refused(lambda badctx=bad: AgentAuthorization(profile=helper.profile, request=req, agent_context=badctx, alias='default', operation_id=op, purpose='desired.persist', decider_factory=factory, clock=clock), 'BORNES_DIVERGENTES')
    cases['bornes_contexte_differentes_refusees'] = True
    with transaction.atomic(using='default', durable=True):
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'diverge-1', purpose='state.query')
        key = 'key:agent:h:diverge-1'
        corr = 'corr:agent:h:diverge-1'
        refused(lambda: helper.bind_instruction(instruction_for(op, ref(ordinary), platform, TARGET_A, key, corr, clock, catalog_operation='agent.apply')), 'LIAISON_OPERATION_INVALIDE')
    cases['operation_action_divergente_refusee'] = True
    with transaction.atomic(using='default', durable=True):
        old = Clock(base_now - datetime.timedelta(seconds=300))
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'expiree-1', clock=old)
        key = 'key:agent:h:expiree-1'
        corr = 'corr:agent:h:expiree-1'
        clock.instant = base_now
        refused(lambda: helper.bind_instruction(instruction_for(op, ref(ordinary), platform, TARGET_A, key, corr, clock, expires_in_seconds=-120)), 'INSTRUCTION_INVALIDE')
    cases['instruction_expiree_clock_actuelle_refusee'] = True
    with transaction.atomic(using='default', durable=True):
        raw = str(ordinary.pk)
        tag = 'h:raw-1'
        req = Request('decision:agent:' + tag, raw, TARGET_A, ACTION, platform, 'corr:agent:' + tag)
        op = 'op:agent:' + tag
        ctx = agent_context_for(raw, platform, TARGET_A, op, 'key:agent:' + tag, 'corr:agent:' + tag, Clock(base_now))
        store = make_store()
        source = SyntheticAuth(Clock(base_now))
        factory = _AgentFactory(store, source, Clock(base_now), req, 'default', op, 'desired.persist')
        helper = AgentAuthorization(profile=profile(), request=req, agent_context=ctx, alias='default', operation_id=op, purpose='desired.persist', decider_factory=factory, clock=Clock(base_now))
        refused(lambda: helper.authorize(), 'DECISION_INVALIDE')
    cases['sujet_uuid_brut_decision_invalide'] = True
    held = {}
    with transaction.atomic(using='default', durable=True):
        held['helper'] = make_helper(ref(ordinary), platform, 'commit-1')[0]
    with transaction.atomic(using='default', durable=True):
        refused(lambda: held['helper'].authorize(), 'TX_MODIFIEE')
    cases['helper_apres_commit_nouvelle_tx_refuse'] = True
    with transaction.atomic(using='default', durable=True):
        held['conn'] = make_helper(ref(ordinary), platform, 'conn-1')[0]
        old_physical = connections['default'].connection
        assert old_physical is not None
        held['physical'] = old_physical
    assert connections['default'].connection is held['physical']
    connections['default'].close()
    assert connections['default'].connection is None
    with transaction.atomic(using='default', durable=True):
        assert connections['default'].connection is not held['physical']
        refused(lambda: held['conn'].authorize(), 'TX_MODIFIEE')
    cases['remplacement_connexion_nouvelle_tx_refuse'] = True
    with transaction.atomic(using='default', durable=True):
        persist(allow_policy('allow-forge-agent', ref(ordinary)))
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'forge-1')
        proof = helper.authorize()
        twin = _SealedAuthorization(decision=proof.decision, alias=proof.alias, operation_id=proof.operation_id, tx_pin=proof.tx_pin, audit_waived=proof.audit_waived, governance_waived=proof.governance_waived, decider=proof.decider)
        refused(lambda: helper.verify_final(twin), 'PREUVE_INVALIDE')
        forged_decision = replace(proof.decision)
        forged = _SealedAuthorization(decision=forged_decision, alias=proof.alias, operation_id=proof.operation_id, tx_pin=proof.tx_pin, audit_waived=proof.audit_waived, governance_waived=proof.governance_waived, decider=proof.decider)
        refused(lambda: helper.verify_final(forged), 'PREUVE_INVALIDE')
        refused(lambda: helper.verify_final({'decision': proof.decision}), 'PREUVE_INVALIDE')
        rollback()
    cases['preuve_copiee_forgee_refusee'] = True
    with transaction.atomic(using='default', durable=True):
        persist(allow_policy('allow-other-agent', ref(ordinary)))
        ha, reqa, ctxa, opa, _, _, _, _ = make_helper(ref(ordinary), platform, 'other-a')
        hb, reqb, ctxb, opb, _, _, _, _ = make_helper(ref(ordinary), platform, 'other-b')
        pa = ha.authorize()
        refused(lambda: hb.verify_final(pa), 'PREUVE_INVALIDE')
        rollback()
    cases['preuve_autre_helper_refusee'] = True
    with transaction.atomic(using='default', durable=True):
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'save-1')
        pin_before = transaction_identity('default')
        raised = False
        try:
            with transaction.atomic(using='default'):
                persist(allow_policy('allow-rolled-back-agent', ref(ordinary)))
                inner = helper.authorize()
                assert inner.decision.effect is Effect.ALLOW
                raise LookupError('SYNTHETIC_ROLLBACK')
        except LookupError:
            raised = True
        assert raised is True
        refused(lambda: helper.authorize(), 'AUTORISATION_REFUSEE')
        assert transaction_identity('default') == pin_before
        assert CorePolicy.objects.filter(policy_id='allow-rolled-back-agent').count() == 0
        rollback()
    cases['pin_stable_savepoint_sans_fuite'] = True
    with transaction.atomic(using='default', durable=True):
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'mock-1')
        class _MockDecider:
            def revalidate_under_locks(self, request, alias, operation_id):
                now = clock.now()
                return Decision(request.decision_id, Effect.ALLOW, 'ALLOWED', ('epoch',), ('PAS_UNE_OBLIGATION',), now, now + datetime.timedelta(seconds=60))
            def audit_waived(self, request, decision, *, alias, operation_id):
                return False
            def governance_waived(self, request, decision, *, alias, operation_id):
                return False
        class _MockFactory:
            def decider_for(self, *, request, alias, operation_id, purpose):
                return _MockDecider()
        mhelper = AgentAuthorization(profile=profile(), request=req, agent_context=ctx, alias='default', operation_id=op, purpose='desired.persist', decider_factory=_MockFactory(), clock=clock)
        refused(lambda: mhelper.authorize(), 'OBLIGATIONS_INVALIDES')
    cases['mock_obligation_inconnue_refusee_distinct_c04'] = True
    with transaction.atomic(using='default', durable=True):
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'prog-1')
        class _BuggyFactory:
            def decider_for(self, *, request, alias, operation_id, purpose):
                raise TypeError('defaut de programmation fixture')
        buggy = AgentAuthorization(profile=profile(), request=req, agent_context=ctx, alias='default', operation_id=op, purpose='desired.persist', decider_factory=_BuggyFactory(), clock=clock)
        propagates(lambda: buggy.authorize(), TypeError)
    cases['defaut_prog_propage_sans_masque'] = True
    with transaction.atomic(using='default', durable=True):
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'exact-1')
        key = 'key:agent:h:exact-1'
        corr = 'corr:agent:h:exact-1'
        try:
            helper.bind_instruction(instruction_for(op, ref(ordinary), platform, TARGET_A, key, corr, clock, catalog_version='x'))
        except AgentAuthorizationError as error:
            assert error.code == 'INSTRUCTION_INVALIDE'
            assert error.code != 'LIAISON_OPERATION_INVALIDE'
            assert error.__cause__ is None
        else:
            raise AssertionError('REFUS_ATTENDU')
    cases['refus_exact_pas_autre_cause'] = True
    with transaction.atomic(using='default', durable=True):
        helper, req, ctx, op, store, source, clock, factory = make_helper(ref(ordinary), platform, 'chr-1')
        for invalid in ('x' + chr(0), 'x' + chr(55296)):
            refused(lambda bad=invalid: AgentAuthorization(profile=profile(), request=req, agent_context=ctx, alias=bad, operation_id=op, purpose='desired.persist', decider_factory=factory, clock=clock), 'LIAISON_INVALIDE')
            refused(lambda bad=invalid: AgentAuthorization(profile=profile(), request=req, agent_context=ctx, alias='default', operation_id=bad, purpose='desired.persist', decider_factory=factory, clock=clock), 'LIAISON_OPERATION_INVALIDE')
    cases['texte_invalide_chr_refuse'] = True
    assert set(cases) == set(EXPECTED_CASES)
    return cases
def main():
    result = harness.run_in_auth_schema(ROOT, _cases, EXPECTED_CASES, with_core=True, core_target='0002_core_audit')
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0 if (result['real_pg'] is True and set(result['cases']) == set(EXPECTED_CASES) and all(value is True for value in result['cases'].values())) else 1
if __name__ == '__main__':
    raise SystemExit(main())
