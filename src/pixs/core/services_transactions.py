"""Transaction Core propriétaire : autorité fraîche, preuves et résultat après commit.

Les ports concrets restent fournis par leurs propriétaires. Les callbacks
sont fermés dans les services Core et ne font pas partie des contrats publics.
Une issue de commit inconnue ne relance jamais le callback de mutation.
"""
from __future__ import annotations

from django.db import DatabaseError, IntegrityError, InterfaceError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.core.authz.decision import Decision
from pixs.core.bootstrap_operator import BootstrapOperatorFacts
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent, PortError, TrustedFacts
from pixs.core.dto import CommandEnvelope, CoreInputInvalid, CoreMutationResult
from pixs.core.persistence.uuid7 import generate_uuid7
from pixs.core.ports import BootstrapServicePorts, CorePortError, CoreServicePorts, TransactionProof
from pixs.core.services_authorization_guard import acquire_catalog_guard
from pixs.core.services_common import CoreServiceError, allow, check_request, check_stage, lock_scopes, make_proof, published_profile, utc_now
from pixs.core.services_transaction_types import AppliedMutation, MutationContext

__all__ = ["execute_mutation"]

def _verify(method, proof) -> None:
    outcome = method(proof)
    if outcome is not None:
        raise CoreServiceError("PREUVE_INVALIDE") from None


def _audit_refusal(ports, *, envelope: CommandEnvelope, alias: str, token: str, facts: TrustedFacts | BootstrapOperatorFacts | None, decision: Decision | None, waived: bool) -> None:
    if type(waived) is not bool:
        raise CoreServiceError("DEROGATION_INVALIDE") from None
    if waived is True:
        return None
    if object.__getattribute__(ports, "audit") is None:
        raise CoreServiceError("AUDIT_ABSENT") from None
    if type(alias) is not str or alias == "":
        raise CoreServiceError("ALIAS_INVALIDE") from None
    if type(token) is not str or token == "":
        raise CoreServiceError("IDENTIFIANTS_INVALIDES") from None
    if decision is not None and type(decision) is not Decision:
        raise CoreServiceError("DECISION_INVALIDE") from None
    request = envelope.request
    subject = None
    if facts is not None and type(facts) is TrustedFacts and facts.subject_id == request.subject_id and facts.context == request.context:
        subject = facts.subject_id
    elif (type(facts) is BootstrapOperatorFacts
          and facts.operator_subject_ref == request.subject_id and facts.context == request.context):
        subject = facts.operator_subject_ref
    version = None
    if decision is not None and type(decision) is Decision:
        version = decision.policy_version
    now = utc_now(ports.clock)
    event = AuditEvent(request.decision_id, subject, request.resource_id, request.action_id, request.context, request.correlation_id, Effect.DENY, "DENIED", version, now)
    with transaction.atomic(using=alias, durable=True):
        ref = ports.audit.stage(event, alias=alias, operation_id=envelope.operation_id, transaction_token=token, context=request.context, decision=decision)
        checked = check_stage(ref, envelope, alias=alias, token=token)
        proof = make_proof(envelope, alias=alias, token=token, stages=(checked,), now=now)
        outcome = ports.audit.verify_staged(proof)
        if outcome is not None:
            raise CoreServiceError("AUDIT_CONTRAT_VIOLE") from None
    return None


def _refuse(principal: Exception, ports, *, envelope, alias, state) -> None:
    facts = state.get("facts")
    decision = state.get("decision")
    waived = False
    token = generate_uuid7().hex
    if type(principal) is CoreServiceError and principal.code == "DECISION_REFUSEE":
        if type(principal.facts) in (TrustedFacts, BootstrapOperatorFacts):
            facts = principal.facts
        if type(principal.decision) is Decision:
            decision = principal.decision
    try:
        current_facts, current_decision = allow(ports, envelope.request, under_locks=False, alias=alias, operation_id=envelope.operation_id, _facts_source=state.get("facts_source"))
        confirmed = ports.decider.audit_waived(envelope.request, current_decision, alias=alias, operation_id=envelope.operation_id)
        if type(confirmed) is bool and confirmed is True:
            waived = True
        facts, decision = current_facts, current_decision
    except (CoreServiceError, CorePortError, CoreInputInvalid, PortError, DatabaseError, InterfaceError):
        # Sans preuve actuelle de derogation, audit obligatoire.
        waived = False
    if facts is not None and type(facts) not in (TrustedFacts, BootstrapOperatorFacts):
        facts = None
    if decision is not None and type(decision) is not Decision:
        decision = None
    try:
        _audit_refusal(ports, envelope=envelope, alias=alias, token=token, facts=facts, decision=decision, waived=waived)
    except Exception as audit_error:
        group = ExceptionGroup("Refus Core et echec audit", [principal, audit_error])
        raise CoreServiceError("AUDIT_REFUS_INDISPONIBLE") from group
    raise principal


def _stage_result(ctx: MutationContext, applied: AppliedMutation, payload_refs: tuple[str, ...], *, state: dict) -> CoreMutationResult:
    if type(ctx) is not MutationContext:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    if type(applied) is not AppliedMutation:
        raise CoreServiceError("APPLICATION_INVALIDE") from None
    applied.__post_init__()
    if type(payload_refs) is not tuple or any(type(r) is not str or r == "" for r in payload_refs):
        raise CoreServiceError("PAYLOAD_INVALIDE") from None
    request = ctx.envelope.request
    decision = ctx.decision
    if ctx.governance_waived is not True:
        expected = ctx.classification()
        if applied.governance_ref != expected["governance_ref"]:
            raise CoreServiceError("GOUVERNANCE_DIVERGENTE") from None
        if applied.confidentiality != expected["confidentiality"]:
            raise CoreServiceError("GOUVERNANCE_DIVERGENTE") from None
        if applied.personal != expected["personal"]:
            raise CoreServiceError("GOUVERNANCE_DIVERGENTE") from None
        if applied.result_ref not in ctx.attestation.resource_refs:
            raise CoreServiceError("RESSOURCE_NON_COUVERTE") from None
        for ref in payload_refs:
            if ref not in ctx.attestation.resource_refs:
                raise CoreServiceError("PAYLOAD_NON_COUVERT") from None
    if ctx.audit_waived is not True:
        event = AuditEvent(request.decision_id, request.subject_id, request.resource_id, request.action_id, request.context, request.correlation_id, Effect.ALLOW, "ALLOWED", decision.policy_version, decision.evaluated_at)
        ctx.collect(ctx.ports.audit.stage(event, alias=ctx.alias, operation_id=ctx.envelope.operation_id, transaction_token=ctx.token, context=request.context, decision=decision))
    result = CoreMutationResult(ctx.envelope.operation_id, applied.result_ref, applied.version, applied.persistence_state, ctx.envelope.correlation_id)
    ctx.collect(ctx.ports.idempotence.stage_result(ctx.proof(), result=result))
    if len(payload_refs) > 0:
        if ctx.governance_waived is not True and len(ctx.attestation.outbound_declarations) == 0:
            raise CoreServiceError("OUTBOX_SANS_DECLARATION") from None
        declarations = () if ctx.attestation is None else ctx.attestation.outbound_declarations
        ctx.collect(ctx.ports.outbox.stage_envelope(alias=ctx.alias, operation_id=ctx.envelope.operation_id, transaction_token=ctx.token, context=request.context, correlation_id=ctx.envelope.correlation_id, request=request, decision=decision, causation_id=ctx.envelope.causation_id, governance_waived=ctx.governance_waived, governance_ref=applied.governance_ref, payload_refs=payload_refs, outbound_declarations=declarations))
    proof = ctx.proof()
    _verify(ctx.ports.idempotence.verify_staged, proof)
    if ctx.audit_waived is not True:
        _verify(ctx.ports.audit.verify_staged, proof)
    if len(payload_refs) > 0:
        _verify(ctx.ports.outbox.verify_staged, proof)
    if ctx.declarations_used is True:
        if type(ctx.ports) is not CoreServicePorts:
            raise CoreServiceError("DECLARATION_INCOHERENTE") from None
        _verify(ctx.ports.declarations.verify_staged, proof)
    if ctx.attestation is not None or ctx.governance_used is True:
        _verify(ctx.ports.governance.verify_staged, proof)
    if ctx.credential_used is True:
        if type(ctx.ports) is not BootstrapServicePorts:
            raise CoreServiceError("CREDENTIAL_INCOHERENT") from None
        _verify(ctx.ports.stamper.verify_staged, proof)
    if ctx.plans_used is True:
        if type(ctx.ports) is not BootstrapServicePorts:
            raise CoreServiceError("PLAN_INCOHERENT") from None
        _verify(ctx.ports.plans.verify_staged, proof)
    state["proof"] = proof
    return result


def _attempt(ports, *, envelope, alias, scopes, apply, payload_refs, facts_source, state, restore_only=False) -> CoreMutationResult:
    if type(restore_only) is not bool:
        raise CoreServiceError("MODE_INVALIDE") from None
    if type(scopes) is not tuple or len(scopes) == 0:
        raise CoreServiceError("SCOPES_INVALIDES") from None
    if type(payload_refs) is not tuple:
        raise CoreServiceError("PAYLOAD_INVALIDE") from None
    if type(state) is not dict:
        raise CoreServiceError("ETAT_INVALIDE") from None
    token = state["token"]
    command_type = state["command_type"]
    if type(token) is not str or token == "":
        raise CoreServiceError("JETON_INVALIDE") from None
    if type(command_type) is not str or command_type == "":
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    acquire_catalog_guard(alias, command_type.startswith("pixs.core.authz."))
    request = envelope.request
    lock_scopes(alias, scopes)
    facts, decision = allow(ports, request, under_locks=True, alias=alias, operation_id=envelope.operation_id, _facts_source=facts_source)
    state["facts"] = facts
    state["decision"] = decision
    attestation, audit_waived, governance_waived = published_profile(ports, request, decision, alias=alias, operation_id=envelope.operation_id, token=token)
    state["audit_waived"] = audit_waived
    ctx = MutationContext(ports, envelope, alias, token, decision, attestation, audit_waived, governance_waived)
    state["ctx"] = ctx
    staged = ports.idempotence.check_or_stage(alias=alias, operation_id=envelope.operation_id, transaction_token=token, context=request.context, subject_id=request.subject_id, command_type=command_type, idempotency_key=envelope.idempotency_key, content_sha256=envelope.content_sha256, serializer_version=envelope.serializer_version)
    ctx.collect(staged)
    _verify(ports.idempotence.verify_staged, ctx.proof())
    restored = ports.idempotence.restore_confirmed(ctx.proof())
    if restored is not None:
        if type(restored) is not CoreMutationResult:
            raise CoreServiceError("RESTAURATION_INVALIDE") from None
        restored.__post_init__()
        if governance_waived is not True and restored.result_ref not in attestation.resource_refs:
            raise CoreServiceError("RESSOURCE_NON_COUVERTE") from None
        if audit_waived is not True:
            event = AuditEvent(request.decision_id, request.subject_id, request.resource_id, request.action_id, request.context, request.correlation_id, Effect.ALLOW, "ALLOWED", decision.policy_version, decision.evaluated_at)
            ctx.collect(ports.audit.stage(event, alias=alias, operation_id=envelope.operation_id, transaction_token=token, context=request.context, decision=decision))
        proof = ctx.proof()
        _verify(ports.idempotence.verify_staged, proof)
        if audit_waived is not True:
            _verify(ports.audit.verify_staged, proof)
        if attestation is not None:
            _verify(ports.governance.verify_staged, proof)
        state["proof"] = proof
        return restored
    consumed_bootstrap = (
        type(ports) is BootstrapServicePorts
        and type(facts) is BootstrapOperatorFacts
        and facts.consumed_operation_id is not None
    )
    if restore_only is True or consumed_bootstrap:
        raise CoreServiceError("ISSUE_INCONNUE") from None
    applied = apply(ctx)
    return _stage_result(ctx, applied, payload_refs, state=state)


def _reconcile(ports, *, envelope, alias, scopes, facts_source, state) -> CoreMutationResult:
    proof = state["proof"]
    if type(proof) is not TransactionProof:
        raise CoreServiceError("ISSUE_INCONNUE") from None
    try:
        outcome = ports.idempotence.reconcile_unknown(proof)
    except (CoreServiceError, CorePortError, CoreInputInvalid, PortError, DatabaseError, InterfaceError) as error:
        if type(error) is CoreServiceError and error.code == "ISSUE_INCONNUE":
            raise
        raise CoreServiceError("ISSUE_INCONNUE") from error
    if type(outcome) is not str or outcome == "":
        raise CoreServiceError("ISSUE_INCONNUE") from None
    newstate = {"token": generate_uuid7().hex, "command_type": state["command_type"], "facts": None, "decision": None, "audit_waived": False, "proof": None}
    try:
        with transaction.atomic(using=alias, durable=True):
            result = _attempt(ports, envelope=envelope, alias=alias, scopes=scopes, apply=None, payload_refs=(), facts_source=facts_source, state=newstate, restore_only=True)
            _, fresh = allow(ports, envelope.request, under_locks=True, alias=alias, operation_id=envelope.operation_id, _facts_source=facts_source)
            if fresh.policy_version != newstate["decision"].policy_version:
                raise CoreServiceError("ISSUE_INCONNUE") from None
    except (CoreServiceError, CorePortError, CoreInputInvalid, PortError, DatabaseError, InterfaceError) as error:
        if type(error) is CoreServiceError and error.code == "ISSUE_INCONNUE":
            raise
        raise CoreServiceError("ISSUE_INCONNUE") from error
    return result


def execute_mutation(*, ports, alias, envelope, resource_id, action_id, correlation_id, command_type, lock_scopes, apply, outbox_payload_refs=(), _facts_source=None) -> CoreMutationResult:
    if type(ports) not in (CoreServicePorts, BootstrapServicePorts):
        raise CoreServiceError("PORTS_INVALIDES") from None
    if type(alias) is not str or alias == "":
        raise CoreServiceError("ALIAS_INVALIDE") from None
    try:
        vendor = connections[alias].vendor
        outer = connections[alias].in_atomic_block
    except ConnectionDoesNotExist as error:
        raise CoreServiceError("ALIAS_INCONNU") from error
    if vendor != "postgresql":
        raise CoreServiceError("MOTEUR_NON_PG_REFUSE") from None
    if outer is True:
        raise CoreServiceError("BLOC_EXTERNE_AMBIGU") from None
    check_request(envelope, resource_id=resource_id, action_id=action_id, correlation_id=correlation_id)
    if type(command_type) is not str or command_type == "":
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    if type(lock_scopes) is not tuple or len(lock_scopes) == 0 or any(type(s) is not str or s == "" for s in lock_scopes):
        raise CoreServiceError("SCOPES_INVALIDES") from None
    if not callable(apply):
        raise CoreServiceError("CALLBACK_INVALIDE") from None
    if type(outbox_payload_refs) is not tuple or any(type(r) is not str or r == "" for r in outbox_payload_refs):
        raise CoreServiceError("PAYLOAD_INVALIDE") from None
    state = {"token": generate_uuid7().hex, "command_type": command_type, "facts_source": _facts_source, "facts": None, "decision": None, "audit_waived": False, "proof": None}
    commit_attempted = False
    try:
        facts, decision = allow(ports, envelope.request, under_locks=False, alias=alias, operation_id=envelope.operation_id, _facts_source=_facts_source)
        state["facts"] = facts
        state["decision"] = decision
        with transaction.atomic(using=alias, durable=True):
            result = _attempt(ports, envelope=envelope, alias=alias, scopes=lock_scopes, apply=apply, payload_refs=outbox_payload_refs, facts_source=_facts_source, state=state, restore_only=False)
            _, fresh = allow(ports, envelope.request, under_locks=True, alias=alias, operation_id=envelope.operation_id, _facts_source=_facts_source)
            if fresh.policy_version != state["decision"].policy_version:
                raise CoreServiceError("VERSION_DIVERGENTE") from None
            if type(state["proof"]) is not TransactionProof:
                raise CoreServiceError("PREUVE_MANQUANTE") from None
            commit_attempted = True
        return result
    except IntegrityError as conflict:
        principal = CoreServiceError("CONFLIT_INTEGRITE")
        principal.__cause__ = conflict
        _refuse(principal, ports, envelope=envelope, alias=alias, state=state)
    except (CoreServiceError, CorePortError, CoreInputInvalid, PortError) as principal:
        _refuse(principal, ports, envelope=envelope, alias=alias, state=state)
    except (DatabaseError, InterfaceError) as unavailable:
        if commit_attempted is True:
            return _reconcile(ports, envelope=envelope, alias=alias, scopes=lock_scopes, facts_source=_facts_source, state=state)
        principal = CoreServiceError("APPLICATION_INDISPONIBLE")
        principal.__cause__ = unavailable
        _refuse(principal, ports, envelope=envelope, alias=alias, state=state)
