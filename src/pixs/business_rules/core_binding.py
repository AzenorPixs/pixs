"""Raccordement facultatif a une Command Core existante.

La composition trusted choisit le catalogue et le nom de Command hors DSL.
Une proposition minimisee est commise dans une transaction audit distincte
avant la tentative de Command. Son existence ne confirme aucun effet metier.
Les erreurs du proprietaire sont propagees ; la proposition reste consultable
par le seul contrat public filter_audit, avec autorisation courante et politique
C05. Aucun secret ni contexte d entree n est conserve. Une politique qui efface
les champs necessaires de cette explication refuse le raccordement avant effet.
"""

from __future__ import annotations

import urllib.parse as _up
from dataclasses import dataclass

from django.db import transaction

from pixs.backend.api_core_catalog import COMMANDS, command_resource_ref, context_mode, dispatch_command
from pixs.business_rules.evaluator import EvaluatorError, RuleCatalog, evaluate
from pixs.business_rules.json_contract import encode_json_document
from pixs.core.dto import CommandEnvelope, CoreMutationResult
from pixs.core.audit_sink import PostgresAuditParticipant
from pixs.core.ports import CoreServicePorts, StagedRef, TransactionProof
from pixs.core.services_common import allow, check_request, utc_now
from pixs.core.persistence.uuid7 import generate_uuid7
from pixs.kernel.audit_event import AuditEvent


OWNER = "pixs.core"
COMPONENT_ID = "pixs.business-rules"
COMPONENT_VERSION = "1.0.0"
ACTION_PROPOSED = "business-rule.evaluate.proposed"
RESOURCE_TYPE = "business-rule"
RESULT_PROPOSED = "PROPOSED"


def _quote(value: str) -> str:
    if type(value) is not str or not value:
        raise EvaluatorError("invalid_rule_key")
    return _up.quote(value, safe="")


def _proposal_resource_id(owner: str, rule_id: str, rule_version: str) -> str:
    return "business-rule:" + _quote(owner) + "/" + _quote(rule_id) + "/" + _quote(rule_version)


@dataclass(frozen=True, slots=True)
class BusinessRuleCoreBinding:
    """Binding immuable choisi par la composition, sans activation P0."""

    owner: str
    command_name: str
    catalog: RuleCatalog

    def __post_init__(self) -> None:
        if type(self.owner) is not str or self.owner != OWNER:
            raise EvaluatorError("invalid_owner")
        if type(self.command_name) is not str or self.command_name not in COMMANDS:
            raise EvaluatorError("unknown_command")
        if type(self.catalog) is not RuleCatalog:
            raise EvaluatorError("invalid_catalog")

    def invoke(
        self,
        *,
        dto: object,
        envelope: CommandEnvelope,
        ports: object,
        alias: str,
        inputs: bytes,
        rule_id: str,
        rule_version: str,
        correlation_id: str,
    ) -> dict:
        """Evalue puis propose avant une Command existante, sans effet speculatif."""
        self.__post_init__()
        if type(ports) is not CoreServicePorts:
            raise EvaluatorError("invalid_ports")
        if type(ports.audit) is not PostgresAuditParticipant:
            raise EvaluatorError("audit_unavailable")
        if type(envelope) is not CommandEnvelope:
            raise EvaluatorError("invalid_envelope")
        if type(alias) is not str or not alias:
            raise EvaluatorError("invalid_alias")
        if type(correlation_id) is not str or not correlation_id.strip():
            raise EvaluatorError("invalid_correlation_id")
        if type(inputs) is not bytes:
            raise EvaluatorError("invalid_inputs")
        if type(rule_id) is not str or not rule_id:
            raise EvaluatorError("invalid_rule_key")
        if type(rule_version) is not str or not rule_version:
            raise EvaluatorError("invalid_rule_key")

        if transaction.get_connection(alias).in_atomic_block:
            raise EvaluatorError("external_transaction")

        spec = COMMANDS[self.command_name]
        resource_ref = command_resource_ref(self.command_name, dto)
        action = spec["action"]
        dto_correlation = getattr(dto, "correlation_id", None)
        if dto_correlation != correlation_id:
            raise EvaluatorError("correlation_mismatch")
        dto_context = getattr(dto, "context", None)
        request = check_request(
            envelope,
            resource_id=resource_ref,
            action_id=action,
            correlation_id=correlation_id,
        )
        if ((dto_context is not None and dto_context != request.context)
                or context_mode(request.context) not in spec["roots"]):
            raise EvaluatorError("context_mismatch")
        if request.correlation_id != correlation_id:
            raise EvaluatorError("correlation_mismatch")

        allow(
            ports,
            request,
            under_locks=False,
            alias=alias,
            operation_id=envelope.operation_id,
        )

        rule = self.catalog.get(self.owner, rule_id, rule_version)
        if rule.owner != self.owner:
            raise EvaluatorError("invalid_owner")
        evaluation = evaluate(rule, inputs, correlation_id)
        if type(evaluation.get("matched")) is not bool:
            raise EvaluatorError("invalid_result")

        now = utc_now(ports.clock)
        proposal_operation = str(generate_uuid7())
        proposal_token = generate_uuid7().hex
        proposal_event_id = str(generate_uuid7())
        reason_bytes = encode_json_document(evaluation)
        reason_text = reason_bytes.decode("utf-8")
        context = request.context
        event = AuditEvent(
            event_id=proposal_event_id,
            occurred_at=now.isoformat(),
            actor_reference=request.subject_id,
            tenant_reference=context.tenant_id,
            action=ACTION_PROPOSED,
            resource_type=RESOURCE_TYPE,
            resource_id=_proposal_resource_id(self.owner, rule_id, rule_version),
            result=RESULT_PROPOSED,
            reason_or_error=reason_text,
            correlation_ids=(correlation_id,),
            causation_ids=(),
            component_id=COMPONENT_ID,
            component_version=COMPONENT_VERSION,
        )
        with transaction.atomic(using=alias, durable=True):
            row = ports.audit.stage_generic(
                event,
                alias=alias,
                operation_id=proposal_operation,
                transaction_token=proposal_token,
                context=context,
            )
            payload = row.generic_payload
            if (type(payload) is not dict or payload.get("reason_or_error") != reason_text
                    or payload.get("correlation_ids") != [correlation_id]
                    or payload.get("action") != ACTION_PROPOSED
                    or payload.get("resource_type") != RESOURCE_TYPE
                    or payload.get("resource_id") != event.resource_id
                    or payload.get("result") != RESULT_PROPOSED):
                raise EvaluatorError("explanation_redacted")
            audit_reference = "audit:" + str(row.record_id)
            proof = TransactionProof(
                proposal_operation,
                alias,
                proposal_token,
                context,
                (StagedRef(proposal_operation, alias, proposal_token, context, "audit"),),
                now,
            )
            if ports.audit.verify_staged(proof) is not None:
                raise EvaluatorError("audit_unverified")

        if evaluation["matched"] is not True:
            return {
                "evaluation": dict(evaluation),
                "audit_reference": audit_reference,
                "dispatched": False,
                "command_result": None,
            }
        command_result = dispatch_command(
            self.command_name,
            dto=dto,
            envelope=envelope,
            ports=ports,
            alias=alias,
        )
        if type(command_result) is not CoreMutationResult:
            raise EvaluatorError("invalid_owner_result")
        return {
            "evaluation": dict(evaluation),
            "audit_reference": audit_reference,
            "dispatched": True,
            "command_result": command_result,
        }
