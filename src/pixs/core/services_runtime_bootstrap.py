"""Autorisation R01 disjointe, sans session ni identité applicative fabriquée.

C03 prouve la signature et la confiance ; C08 prouve le plan réel. La décision
C04 autorise seulement l'acte fermé. Le commit et la consommation effective
restent aux propriétaires, dans la transaction Core.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from dataclasses import fields

from django.db import DatabaseError, InterfaceError, connections, transaction

from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect, Obligation
from pixs.core.authz.ports import PortError, Request
from pixs.core.bootstrap_operator import BootstrapOperatorFacts
from pixs.core.dto import BootstrapActInput, BootstrapTargetSpec, CommandEnvelope, CoreInputInvalid
from pixs.core.ports import CorePortError
from pixs.core.services_authorization_guard import acquire_catalog_guard, transaction_identity
from pixs.core.services_bootstrap import _validate_act
from pixs.core.services_bootstrap_facts import (
    BootstrapBindingError, check_act_binding, check_request_binding,
    check_consumed_policy, require_current_window,
)
from pixs.core.services_common import CoreServiceError, lock_scopes


class RuntimeBootstrapDecider:
    """Une instance par acte et invocation serveur ; aucun privilège Super Admin."""

    def __init__(self, *, act: BootstrapActInput, envelope: CommandEnvelope,
                 alias: str, operator, plans, clock) -> None:
        if type(act) is not BootstrapActInput or type(envelope) is not CommandEnvelope:
            raise CorePortError()
        identity, tenant = _validate_act(act, envelope)
        if type(alias) is not str or not alias:
            raise CorePortError()
        for owner, names in ((operator, ("verify",)),
                             (plans, ("verify_plan", "verify_operator_binding",
                                      "get_closed_effects", "resolve_targets", "inspect_confirmed")),
                             (clock, ("now",))):
            if any(not callable(getattr(owner, name, None)) for name in names):
                raise CorePortError()
        self._act, self._envelope, self._alias = act, envelope, alias
        self._operator, self._plans, self._clock = operator, plans, clock
        self._identity, self._tenant = identity, tenant

    def _bound(self, request, alias, operation_id):
        if (type(request) is not Request or request != self._envelope.request
                or type(alias) is not str or alias != self._alias
                or type(operation_id) is not str or operation_id != self._act.operation_id):
            raise CorePortError()

    def _now(self):
        value = self._clock.now()
        if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
            raise CorePortError()
        return value

    def _guards(self):
        transaction_identity(self._alias)
        acquire_catalog_guard(self._alias, False)
        act = self._act
        scopes = ["installation:" + act.installation_ref, "binding:" + act.installation_ref,
                  "uuid:" + uuid.UUID(self._identity).hex, "operation:" + act.operation_id]
        if self._tenant is not None:
            scopes.append("tenant:" + self._tenant)
        lock_scopes(self._alias, tuple(sorted(scopes)))

    def _facts(self, request):
        act = self._act
        if self._plans.verify_plan(act, alias=self._alias) is not None:
            raise CorePortError()
        actual_effects = self._plans.get_closed_effects(
            plan_version=act.plan_version, installation_ref=act.installation_ref)
        if type(actual_effects) is not tuple or actual_effects != act.closed_effects:
            raise CorePortError()
        spec = self._plans.resolve_targets(act, alias=self._alias)
        if type(spec) is not BootstrapTargetSpec:
            raise CorePortError()
        spec.__post_init__()
        if str(spec.identity_id) != self._identity or spec.tenant_id != self._tenant:
            raise CorePortError()
        if "REUSE_EXISTING" in act.closed_effects:
            if spec.expected_binding_version is None or spec.expected_identity_version is None:
                raise CorePortError()
        elif spec.expected_binding_version is not None or spec.expected_identity_version is not None:
            raise CorePortError()
        if "CREATE_IDENTITY" in act.closed_effects:
            operator_id = act.operator_subject_ref.removeprefix("pixs.core.identity:")
            try:
                operator_uuid = uuid.UUID(operator_id)
            except ValueError:
                operator_uuid = None
            if operator_uuid == spec.identity_id:
                raise CorePortError()
        if "CREATE_TENANT" in act.closed_effects and spec.expected_tenant_version is not None:
            raise CorePortError()
        if ("CREATE_TENANT" not in act.closed_effects and spec.tenant_id is not None
                and spec.expected_tenant_version is None):
            raise CorePortError()
        facts = self._operator.verify(
            operator_subject_ref=act.operator_subject_ref,
            operator_proof_ref=act.operator_proof_ref, plan_version=act.plan_version,
            installation_ref=act.installation_ref, context=request.context)
        # Une AuthenticationContext ou une structure prétendue ne prouve jamais R01.
        if type(facts) is not BootstrapOperatorFacts:
            raise CorePortError()
        check_act_binding(act, facts)
        check_request_binding(facts, request, operation_id=act.operation_id)
        require_current_window(facts, self._now())
        if self._plans.verify_operator_binding(act, facts, alias=self._alias) is not None:
            raise CorePortError()
        if facts.consumed_operation_id is not None:
            check_consumed_policy(facts, act.operation_id, self._plans.inspect_confirmed(act))
        return facts

    def _version(self, facts):
        material = {}
        for field in fields(BootstrapOperatorFacts):
            value = getattr(facts, field.name)
            if field.name == "context":
                value = (value.scope_type.value, value.tenant_id, value.scope_id)
            elif type(value) is datetime.datetime:
                value = value.isoformat()
            material[field.name] = value
        digest = hashlib.sha256(json.dumps(
            material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        return digest, ((facts.trust_policy_version, facts.plan_version),)

    def _decide_locked(self, request, alias, operation_id):
        self._bound(request, alias, operation_id)
        self._guards()
        now = self._now()
        try:
            facts = self._facts(request)
            now = self._now()
            require_current_window(facts, now)
        except (BootstrapBindingError, CorePortError, CoreInputInvalid, PortError,
                CoreServiceError, DatabaseError, InterfaceError):
            return Decision(request.decision_id, Effect.DENY, "DENIED", None, (), now, now)
        return Decision(request.decision_id, Effect.ALLOW, "ALLOWED", self._version(facts),
                        (Obligation("AUDIT"),), now, facts.expires_at)

    def decide(self, request):
        self._bound(request, self._alias, self._act.operation_id)
        if connections[self._alias].in_atomic_block:
            return self._decide_locked(request, self._alias, self._act.operation_id)
        with transaction.atomic(using=self._alias):
            return self._decide_locked(request, self._alias, self._act.operation_id)

    def revalidate_under_locks(self, request, *, alias, operation_id):
        return self._decide_locked(request, alias, operation_id)

    def audit_waived(self, request, decision, *, alias, operation_id):
        return False

    def governance_waived(self, request, decision, *, alias, operation_id):
        return False
