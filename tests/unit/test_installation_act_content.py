'''Recettes contrat acte C08, phase 2, sans execution.'''
import unittest
import uuid
from dataclasses import replace, fields
from pixs.backend.installation.act_content import ActContentFields, act_content_sha256, canonical_act_content, verify_act_plan_binding
from pixs.backend.installation.plan import InstallationPlan, PlanBindingInvalid, PlanInvalid, PlanLimits
from pixs.core.authz.ports import Request
from pixs.core.dto import BootstrapActInput, BootstrapTargetSpec, CommandEnvelope
from pixs.core.identity.models import IdentityState, IdentityType
from pixs.core.scope.context import ScopeContext, ScopeType
_FIX_ID = '01900000-0000-7000-8000-000000000001'
_FIX_OP = '01900000-0000-7000-8000-000000000002'
class ActContentCases(unittest.TestCase):
    def _limits(self) -> PlanLimits:
        return PlanLimits(65536, 64, 8, ('1',), ('1.0',))
    def _plan(self, limits: PlanLimits) -> InstallationPlan:
        itype = IdentityType.HUMAN
        istate = IdentityState.ACTIVE
        spec = BootstrapTargetSpec(uuid.UUID(_FIX_ID), itype, istate, None, None, None, None)
        return InstallationPlan('1', '1.0', 'op-qualif-0001', 'install-qualif-0001', 'db-qualif-0001', 'ABSENT', 'PREPARATION', 'pixs.core.identity:' + _FIX_OP, 'pixs.core.identity:' + _FIX_ID, None, spec, ('CREATE_IDENTITY', 'BIND_SUPER_ADMIN', 'STAMP_CREDENTIAL'), 'intent-qualif-0001', 'corr-qualif-0001', None, 'idem-qualif-0001')
    def _fields(self, plan: InstallationPlan) -> ActContentFields:
        ctx = ScopeContext(ScopeType.PLATFORM, None, None)
        return ActContentFields('op-qualif-0001', '1.0', 'install-qualif-0001', 'INSTALLER', 'proof-qualif-0001', 'pixs.core.identity:' + _FIX_OP, 'auth-qualif-0001', 'pixs.core.identity:' + _FIX_ID, None, ('CREATE_IDENTITY', 'BIND_SUPER_ADMIN', 'STAMP_CREDENTIAL'), ('conf-qualif-0001',), ctx, 'corr-qualif-0001', None, 'idem-qualif-0001', '1.0.0')
    def test_determinism(self) -> None:
        limits = self._limits()
        plan = self._plan(limits)
        content = self._fields(plan)
        first = canonical_act_content(plan, content, limits)
        second = canonical_act_content(plan, content, limits)
        self.assertEqual(first, second)
        self.assertEqual(act_content_sha256(plan, content, limits), __import__('hashlib').sha256(first).hexdigest())
    def test_envelope_binding(self) -> None:
        limits = self._limits()
        plan = self._plan(limits)
        content = self._fields(plan)
        digest = act_content_sha256(plan, content, limits)
        ctx = ScopeContext(ScopeType.PLATFORM, None, None)
        request = Request('auth-qualif-0001', 'pixs.core.identity:' + _FIX_OP, 'pixs.core.bootstrap:install-qualif-0001', 'pixs.core.bootstrap.apply', ctx, 'corr-qualif-0001')
        act = BootstrapActInput('op-qualif-0001', '1.0', 'install-qualif-0001', 'INSTALLER', 'proof-qualif-0001', 'pixs.core.identity:' + _FIX_OP, 'auth-qualif-0001', 'pixs.core.identity:' + _FIX_ID, None, ('CREATE_IDENTITY', 'BIND_SUPER_ADMIN', 'STAMP_CREDENTIAL'), ('conf-qualif-0001',), ctx, 'corr-qualif-0001', None, 'idem-qualif-0001', digest, '1.0.0')
        envelope = CommandEnvelope(request, 'op-qualif-0001', 'idem-qualif-0001', digest, '1.0.0', 'corr-qualif-0001', None)
        from pixs.backend.installation.plan import PlanConfirmationLink, bind_confirmation
        link = bind_confirmation(plan, 'conf-qualif-0001', limits)
        self.assertIsNone(verify_act_plan_binding(act, envelope, plan, (link,), limits))
    def test_refusals(self) -> None:
        limits = self._limits()
        plan = self._plan(limits)
        content = self._fields(plan)
        bad = ActContentFields(content.operation_id, content.plan_version, content.installation_ref, 'NORMAL', content.operator_proof_ref, content.operator_subject_ref, content.authorization_ref, content.target_identity_ref, content.target_tenant_ref, content.closed_effects, content.confirmations, content.context, content.correlation_id, content.causation_id, content.idempotency_key, content.serializer_version)
        with self.assertRaises(PlanInvalid):
            canonical_act_content(plan, bad, limits)

    def _packet(self):
        from pixs.backend.installation.plan import bind_confirmation
        limits = self._limits()
        plan = self._plan(limits)
        content = self._fields(plan)
        digest = act_content_sha256(plan, content, limits)
        act = BootstrapActInput(**{f.name:getattr(content,f.name) for f in fields(ActContentFields)},content_sha256=digest)
        request = Request(content.authorization_ref, content.operator_subject_ref,
                          'pixs.core.bootstrap:' + content.installation_ref,
                          'pixs.core.bootstrap.apply', content.context, content.correlation_id)
        envelope = CommandEnvelope(request, content.operation_id, content.idempotency_key,
                                   digest, content.serializer_version,content.correlation_id,content.causation_id)
        return limits,plan,act,envelope,(bind_confirmation(plan,content.confirmations[0],limits),)
    def test_unbound_extra_confirmation_refused(self):
        limits,plan,act,envelope,links=self._packet()
        with self.assertRaises(PlanInvalid):
            verify_act_plan_binding(replace(act,confirmations=act.confirmations+('unverified',)),envelope,plan,links,limits)
    def test_foreign_request_and_confirmation_refused(self):
        limits,plan,act,envelope,links=self._packet()
        for change in ({'subject_id':'foreign'},{'decision_id':'foreign'},{'action_id':'foreign'},{'resource_id':'foreign'}):
            with self.subTest(change=change):
                with self.assertRaises(PlanInvalid):
                    verify_act_plan_binding(act,replace(envelope,request=replace(envelope.request,**change)),plan,links,limits)
        with self.assertRaises(PlanInvalid):
            verify_act_plan_binding(act,envelope,plan,(replace(links[0],plan_sha256='f'*64),),limits)
    def test_plan_correlation_and_digest_binding(self):
        limits,plan,act,envelope,links=self._packet()
        for change in ({'correlation_id':'foreign'},{'idempotency_key':'foreign'},{'operation_id':'foreign'}):
            with self.subTest(change=change):
                with self.assertRaises(PlanInvalid):
                    verify_act_plan_binding(act,envelope,replace(plan,**change),links,limits)

if __name__ == '__main__':
    unittest.main()
