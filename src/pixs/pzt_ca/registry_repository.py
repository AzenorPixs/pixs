"""PZT CA registre privé, OperationLink immuable et Résultats distincts.

Utilité privée appelée uniquement par callback FERMÉ autorisé Core.
Le type MutationContext n'est PAS une preuve d'authentification.
Contexte, provenance des faits, permissions lecture/écriture vérifiés
par le propriétaire AVANT appel. Aucune API publique, aucun P.SUBMIT,
aucune activation livrée. Ne prétend pas empêcher restauration PG.
"""
from dataclasses import dataclass

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connections, transaction

from pixs.core.dto import CommandEnvelope
from pixs.core.ports import CoreServicePorts
from pixs.core.services_common import utc_now
from pixs.core.services_transaction_types import MutationContext
from pixs.pzt_ca.ca_result import CaResult
from pixs.pzt_ca.models import CaOperationLink, CaResultRecord, _epoch_int_to_text


class RepositoryError(ValueError):
    def __init__(self, code: str) -> None:
        if type(code) is not str or code not in (
            "CONFLIT",
            "ENTREE_INVALIDE",
            "CONTEXTE_PERSISTANCE_INVALIDE",
        ):
            raise ValueError("CODE_REPOSITORY_INVALIDE")
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True, repr=False)
class CaOperationBinding:
    domain: str
    logical_authority: str
    emission_scope: str
    operation_version: str
    request_id: str
    context_ref: str
    input_fingerprint: str
    policy_ref: str
    epoch: int

    def __post_init__(self) -> None:
        for f in (
            "domain",
            "logical_authority",
            "emission_scope",
            "operation_version",
            "request_id",
            "context_ref",
            "input_fingerprint",
            "policy_ref",
        ):
            v = object.__getattribute__(self, f)
            if type(v) is not str or v == "" or "\x00" in v:
                raise RepositoryError("ENTREE_INVALIDE")
            try:
                v.encode("utf-8", errors="strict")
            except UnicodeEncodeError:
                raise RepositoryError("ENTREE_INVALIDE") from None
        e = object.__getattribute__(self, "epoch")
        if type(e) is not int or e < 0:
            raise RepositoryError("ENTREE_INVALIDE")


def _opaque(v: object) -> str:
    if type(v) is not str or v == "" or "\x00" in v:
        raise RepositoryError("ENTREE_INVALIDE")
    try:
        v.encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        raise RepositoryError("ENTREE_INVALIDE") from None
    return v


def _opaque_opt(v: object) -> str | None:
    if v is None:
        return None
    return _opaque(v)


def _ctx(context: object) -> MutationContext:
    if type(context) is not MutationContext:
        raise RepositoryError("CONTEXTE_PERSISTANCE_INVALIDE")
    if type(context.ports) is not CoreServicePorts:
        raise RepositoryError("CONTEXTE_PERSISTANCE_INVALIDE")
    alias = context.alias
    _opaque(alias)
    if alias not in connections or connections[alias].vendor != "postgresql":
        raise RepositoryError("CONTEXTE_PERSISTANCE_INVALIDE")
    if not transaction.get_connection(alias).in_atomic_block:
        raise RepositoryError("CONTEXTE_PERSISTANCE_INVALIDE")
    if type(context.envelope) is not CommandEnvelope:
        raise RepositoryError("CONTEXTE_PERSISTANCE_INVALIDE")
    return context


def bind_operation(context: MutationContext, binding: CaOperationBinding) -> CaOperationLink:
    ctx = _ctx(context)
    if type(binding) is not CaOperationBinding:
        raise RepositoryError("ENTREE_INVALIDE")
    alias = ctx.alias
    env = ctx.envelope
    operation_id = _opaque(env.operation_id)
    content_sha256 = _opaque(env.content_sha256)
    serializer_version = _opaque(env.serializer_version)
    try:
        epoch_txt = _epoch_int_to_text(binding.epoch)
    except ValidationError:
        raise RepositoryError("ENTREE_INVALIDE") from None
    cls = ctx.classification()
    governance_ref = cls["governance_ref"]
    confidentiality = cls["confidentiality"]
    personal = cls["personal"]
    now = utc_now(ctx.ports.clock)
    cand = CaOperationLink(
        domain=binding.domain, logical_authority=binding.logical_authority,
        emission_scope=binding.emission_scope, operation_id=operation_id,
        operation_version=binding.operation_version, request_id=binding.request_id,
        context_ref=binding.context_ref, input_fingerprint=binding.input_fingerprint,
        epoch=epoch_txt, policy_ref=binding.policy_ref,
        content_sha256=content_sha256, serializer_version=serializer_version,
        governance_ref=governance_ref, confidentiality=confidentiality,
        personal=personal, persistence_state="ACTIVE", retention_state="RETAINED",
        created_at=now, updated_at=now,
    )
    try:
        cand.clean()
    except ValidationError:
        raise RepositoryError("ENTREE_INVALIDE") from None
    row, created = CaOperationLink.objects.using(alias).select_for_update().get_or_create(
        operation_id=operation_id,
        defaults={"domain": cand.domain, "logical_authority": cand.logical_authority,
                  "emission_scope": cand.emission_scope, "operation_version": cand.operation_version,
                  "request_id": cand.request_id, "context_ref": cand.context_ref,
                  "input_fingerprint": cand.input_fingerprint, "epoch": cand.epoch,
                  "policy_ref": cand.policy_ref, "content_sha256": cand.content_sha256,
                  "serializer_version": cand.serializer_version,
                  "governance_ref": cand.governance_ref, "confidentiality": cand.confidentiality,
                  "personal": cand.personal, "persistence_state": "ACTIVE",
                  "retention_state": "RETAINED", "created_at": now, "updated_at": now},
    )
    if created:
        return row
    if (row.domain, row.logical_authority, row.emission_scope, row.operation_version,
        row.request_id, row.context_ref, row.input_fingerprint, row.epoch,
        row.policy_ref, row.content_sha256, row.serializer_version) != (
        cand.domain, cand.logical_authority, cand.emission_scope, cand.operation_version,
        cand.request_id, cand.context_ref, cand.input_fingerprint, cand.epoch,
        cand.policy_ref, cand.content_sha256, cand.serializer_version):
        raise RepositoryError("CONFLIT")
    return row


def record_result(context: MutationContext, result: CaResult) -> CaResultRecord:
    ctx = _ctx(context)
    if type(result) is not CaResult:
        raise RepositoryError("ENTREE_INVALIDE")
    alias = ctx.alias
    env = ctx.envelope
    op_id = _opaque(env.operation_id)
    try:
        link = CaOperationLink.objects.using(alias).select_for_update().get(operation_id=op_id)
    except ObjectDoesNotExist:
        raise RepositoryError("ENTREE_INVALIDE") from None
    for f in ("operation_id", "operation_version", "request_id", "context_ref", "input_fingerprint"):
        if getattr(result, f) != getattr(link, f):
            raise RepositoryError("CONFLIT")
    if env.content_sha256 != link.content_sha256 or env.serializer_version != link.serializer_version:
        raise RepositoryError("CONFLIT")
    cls = ctx.classification()
    governance_ref = cls["governance_ref"]
    confidentiality = cls["confidentiality"]
    personal = cls["personal"]
    now = utc_now(ctx.ports.clock)
    cand = CaResultRecord(
        result_id=_opaque(result.result_id), operation_link=link, recorded_at=result.recorded_at,
        result_kind=_opaque(result.result_kind), validation=_opaque(result.validation_outcome),
        engagement=_opaque(result.engagement_outcome), effect=_opaque(result.effect_outcome),
        error_code=_opaque_opt(result.error_code), engagement_ref=_opaque_opt(result.engagement_ref),
        effect_evidence_ref=_opaque_opt(result.effect_evidence_ref),
        governance_ref=governance_ref, confidentiality=confidentiality,
        personal=personal, persistence_state="ACTIVE", retention_state="RETAINED",
        created_at=now, updated_at=now,
    )
    try:
        cand.clean()
    except ValidationError:
        raise RepositoryError("ENTREE_INVALIDE") from None
    row, created = CaResultRecord.objects.using(alias).select_for_update().get_or_create(
        result_id=cand.result_id,
        defaults={"operation_link": link, "recorded_at": cand.recorded_at,
                  "result_kind": cand.result_kind, "validation": cand.validation,
                  "engagement": cand.engagement, "effect": cand.effect,
                  "error_code": cand.error_code, "engagement_ref": cand.engagement_ref,
                  "effect_evidence_ref": cand.effect_evidence_ref,
                  "governance_ref": cand.governance_ref, "confidentiality": cand.confidentiality,
                  "personal": cand.personal, "persistence_state": "ACTIVE",
                  "retention_state": "RETAINED", "created_at": now, "updated_at": now},
    )
    if created:
        return row
    if (row.operation_link_id, row.recorded_at, row.result_kind, row.validation,
        row.engagement, row.effect, row.error_code, row.engagement_ref,
        row.effect_evidence_ref) != (link.pk, cand.recorded_at, cand.result_kind, cand.validation,
        cand.engagement, cand.effect, cand.error_code, cand.engagement_ref, cand.effect_evidence_ref):
        raise RepositoryError("CONFLIT")
    return row
