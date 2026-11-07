"""Commandes DNS PostgreSQL : C04, résultat d'idempotence et audit C05 locaux."""
from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import dataclass, fields

from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.core.audit_contracts import AuditError
from pixs.core.audit_sink import PostgresAuditParticipant
from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuthenticationContext, PortError, RevocationStatus
from pixs.core.idempotency_dimensions import collect_command_idempotency_dimensions
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_common import CoreServiceError, lock_scopes
from pixs.core.services_runtime_store import CoreAuthorizationStore
from pixs.kernel.audit_event import AuditEvent
from pixs.kernel.data_governance_profile import DataGovernanceProfile, validate_data_governance_profile
MODULE_VERSION = "0.1.0"
from pixs.dns.adapters import build_dns_authorization
from pixs.dns.contracts import (
    DeclareDesiredDns, RetireDesiredDns, GetDesiredDns, GetAppliedDns,
    DeclareName, RetireName, ResolveViewPolicy,
    validate_declare_name, validate_retire_name, validate_resolve_view_policy,
    validate_declare_desired_dns, validate_retire_desired_dns,
    validate_get_desired_dns, validate_get_applied_dns,
)
from pixs.dns.identifiers import new_uuid7
from pixs.dns.models import DesiredDnsRecord, DnsIdempotenceRecord, DnsNameRecord
from pixs.dns.naming import dns_name_key

__all__ = ["DnsServiceError", "DnsCommandResult", "DnsManagementPolicy", "PostgresDnsService"]
_SERIALIZER = "1.0.0"
_OWNER = "pixs.dns"


class DnsServiceError(ValueError):
    def __init__(self, code):
        super().__init__("Commande de gestion DNS refusée.")
        self.code = code


@dataclass(frozen=True, slots=True)
class DnsManagementPolicy:
    """Valeurs administrées du serveur ; aucune durée ou classification par défaut."""
    idempotence_lifetime: datetime.timedelta
    governance: DataGovernanceProfile | None

    def __post_init__(self):
        if type(self.idempotence_lifetime) is not datetime.timedelta or self.idempotence_lifetime <= datetime.timedelta():
            raise DnsServiceError("DNS_POLICY_INVALID")
        if self.governance is not None:
            if (type(self.governance) is not DataGovernanceProfile
                    or validate_data_governance_profile(self.governance)
                    or self.governance.owner_component != _OWNER):
                raise DnsServiceError("DNS_POLICY_INVALID")


@dataclass(frozen=True, slots=True, repr=False)
class DnsCommandResult:
    operation_id: str
    resource_id: str
    config_revision: int | None
    outcome: str
    audit_disposition: str
    replayed: bool = False

    def record(self):
        return {
            "operation_id": self.operation_id, "resource_id": self.resource_id,
            "config_revision": self.config_revision, "outcome": self.outcome,
            "audit_disposition": self.audit_disposition,
        }


def _utc(value):
    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
        raise DnsServiceError("DNS_CLOCK_INVALID")
    return value


def _context(row):
    return ScopeContext(ScopeType(row.scope_type), row.tenant_id, row.scope_id)


def _governance(profile):
    if type(profile) is not DataGovernanceProfile or validate_data_governance_profile(profile):
        raise DnsServiceError("DNS_GOVERNANCE_INVALID")
    result = {}
    for field in fields(DataGovernanceProfile):
        value = getattr(profile, field.name)
        if type(value) is frozenset:
            value = sorted(value)
        elif field.name in ("confidentiality", "personal_data"):
            value = value.value
        result[field.name] = value
    return result


def _configuration(value):
    return {
        "schema_version": value.schema_version, "owner_id": value.owner_id,
        "config_revision": value.config_revision, "suffix": value.suffix,
        "ttl_positive": value.ttl_positive, "ttl_negative": value.ttl_negative,
        "views": list(value.views), "governance": _governance(value.governance),
        "secret_refs": [
            {"owner_id": ref.owner_id, "entry_id": ref.entry_id, "source": ref.source}
            for ref in value.secret_refs
        ],
    }


def _canonical(document):
    try:
        return json.dumps(
            document, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        raise DnsServiceError("DNS_INPUT_INVALID") from None


def _dimensions(command):
    dims, diagnostics = collect_command_idempotency_dimensions(command.metadata)
    if diagnostics or dims is None:
        raise DnsServiceError("DNS_INPUT_INVALID")
    return {
        "tenant_id": dims.tenant_id, "subject_id": dims.subject_id,
        "command_type": dims.command_type, "idempotency_key": dims.idempotency_key,
    }


def _payload(command, dimensions):
    context = command.request.context
    result = {
        "serializer_version": _SERIALIZER, "schema_version": command.schema_version,
        "owner_id": _OWNER, "resource_id": command.resource_id,
        "expected_revision": command.expected_revision, "dimensions": dimensions,
        "scope": {"scope_type": context.scope_type.value,
                  "tenant_id": context.tenant_id, "scope_id": context.scope_id},
    }
    if type(command) is DeclareDesiredDns:
        result["configuration"] = _configuration(command.configuration)
    elif type(command) in (DeclareName, RetireName):
        result["name_key"] = _name_key(command.name)
        result["view"] = command.view
        if type(command) is DeclareName:
            result["target_ref"] = command.target_ref
    else:
        # La raison participe au rejet d'un contenu divergent, sans être journalisée.
        result["reason"] = command.reason
    return hashlib.sha256(_canonical(result)).hexdigest()


def _name_key(value):
    try:
        return dns_name_key(value)
    except ValueError:
        raise DnsServiceError("DNS_NAME_INVALID") from None


def _get(model, alias, **lookup):
    try:
        return model.objects.using(alias).get(**lookup)
    except model.DoesNotExist:
        return None
    except model.MultipleObjectsReturned:
        raise DnsServiceError("DNS_STATE_UNAVAILABLE") from None


def _metadata(policy, waived):
    if waived:
        return {"governance_ref": None, "confidentiality": None, "personal": None}
    profile = policy.governance
    if profile is None:
        raise DnsServiceError("DNS_GOVERNANCE_UNAVAILABLE")
    return {
        "governance_ref": profile.data_asset_id,
        "confidentiality": profile.confidentiality.value,
        "personal": profile.personal_data.value,
    }


def _stored(row, dimensions, digest, context, now):
    row.clean()
    if (row.serializer_version != _SERIALIZER or row.result_version != 1
            or row.payload_sha256 != digest or _context(row) != context
            or any(getattr(row, key) != value for key, value in dimensions.items())):
        raise DnsServiceError("DNS_IDEMPOTENCE_CONFLICT")
    if row.persistence_state != "ACTIVE" or row.expires_at <= now:
        raise DnsServiceError("DNS_IDEMPOTENCE_EXPIRED")
    if row.state != "SUCCEEDED" or row.result["audit_disposition"] == "UNKNOWN":
        raise DnsServiceError("DNS_OUTCOME_UNKNOWN")
    result = row.result
    return DnsCommandResult(
        result["operation_id"], result["resource_id"], result["config_revision"],
        result["outcome"], result["audit_disposition"], True,
    )


class PostgresDnsService:
    """Ports internes sélectionnés par la composition serveur, jamais par un DTO."""

    def __init__(self, *, alias, peer_alias, store, clock, audit, auth_factory, policy_source):
        if (type(alias) is not str or not alias or type(peer_alias) is not str
                or not peer_alias or peer_alias == alias
                or type(store) is not CoreAuthorizationStore or store.alias != alias
                or type(audit) is not PostgresAuditParticipant or audit.peer_alias != peer_alias
                or not callable(auth_factory) or not callable(getattr(clock, "now", None))
                or not callable(getattr(policy_source, "resolve", None))):
            raise DnsServiceError("DNS_COMPOSITION_INVALID")
        self._alias, self._peer, self._store = alias, peer_alias, store
        self._clock, self._audit = clock, audit
        self._auth, self._policy = auth_factory, policy_source

    def _now(self):
        return _utc(self._clock.now())

    def _source(self, command):
        return self._source_request(command.request, command.metadata.command_id)

    def _source_request(self, request, operation):
        source = self._auth(request=request, alias=self._alias, operation_id=operation)
        if not callable(getattr(source, "revalidate", None)):
            raise DnsServiceError("DNS_AUTH_UNAVAILABLE")
        return source

    def _owner(self):
        try:
            connection = connections[self._alias]
        except ConnectionDoesNotExist:
            raise DnsServiceError("DNS_COMPOSITION_INVALID") from None
        if (connection.vendor != "postgresql" or connection.in_atomic_block
                or not connection.get_autocommit()):
            raise DnsServiceError("DNS_TRANSACTION_INVALID")

    def _event(self, *, actor, context, action, target, result, reason, correlations, causations):
        return AuditEvent(
            str(new_uuid7()), self._now().isoformat(), actor, context.tenant_id,
            action, "dns.management", target, result, reason,
            correlations, causations, _OWNER, MODULE_VERSION,
        )

    def _stage(self, event, operation, token, context):
        # La référence ci-dessous devient une preuve seulement après C05.verify_staged.
        self._audit.stage_generic(
            event, alias=self._alias, operation_id=operation,
            transaction_token=token, context=context,
        )
        proof = TransactionProof(
            operation, self._alias, token, context,
            (StagedRef(operation, self._alias, token, context, "audit"),), self._now(),
        )
        if self._audit.verify_staged(proof) is not None:
            raise DnsServiceError("DNS_AUDIT_UNAVAILABLE")
        return proof

    def _refusal(self, command, code, waived):
        return self._request_refusal(command.request, command.metadata.command_id, code, waived)

    def _request_refusal(self, request, bound_operation, code, waived):
        """Après rollback : refus courant attesté ou diagnostic anonyme de plateforme."""
        if waived:
            return
        operation, token = str(new_uuid7()), str(new_uuid7())
        try:
            with transaction.atomic(using=self._alias, durable=True):
                actor, context, target = "UNVERIFIED", ScopeContext(ScopeType.PLATFORM), _OWNER
                try:
                    # Le savepoint de lecture est clos avant le stage C05 externe.
                    with transaction.atomic(using=self._alias):
                        self._store.pinned_snapshot(
                            context=request.context, actor_ref=request.subject_id,
                        )
                        authentication, revocation = self._source_request(request, bound_operation).revalidate(
                            request, alias=self._alias,
                            operation_id=bound_operation,
                        )
                        if (type(authentication) is not AuthenticationContext
                                or revocation is not RevocationStatus.ACTIVE
                                or authentication.digital_identity_id != request.subject_id
                                or authentication.context != request.context):
                            raise DnsServiceError("DNS_AUTH_UNAVAILABLE")
                        actor, context, target = (
                            authentication.digital_identity_id, authentication.context,
                            request.resource_id,
                        )
                except (PortError, CorePortError, CoreServiceError, DnsServiceError, DatabaseError):
                    actor, context, target = "UNVERIFIED", ScopeContext(ScopeType.PLATFORM), _OWNER
                event = self._event(
                    actor=actor, context=context, action=request.action_id,
                    target=target, result="DENIED", reason=code,
                    correlations=(operation,), causations=(),
                )
                self._stage(event, operation, token, context)
        except (AuditError, CorePortError, PortError, DatabaseError, ValidationError, DnsServiceError):
            raise DnsServiceError("DNS_AUDIT_UNAVAILABLE") from None

    def _peer_row(self, dimensions, namespace, original_connection):
        owner, peer = connections[self._alias], connections[self._peer]
        if owner.in_atomic_block or peer.in_atomic_block or not peer.get_autocommit():
            raise DnsServiceError("DNS_OUTCOME_UNKNOWN")
        keys = ("ENGINE", "HOST", "PORT", "NAME", "OPTIONS")
        if any(owner.settings_dict.get(key) != peer.settings_dict.get(key) for key in keys):
            raise DnsServiceError("DNS_OUTCOME_UNKNOWN")
        with transaction.atomic(using=self._peer, durable=True):
            identity = transaction_identity(self._peer)
            if identity[2:] != namespace or peer.connection is original_connection:
                raise DnsServiceError("DNS_OUTCOME_UNKNOWN")
            row = _get(DnsIdempotenceRecord, self._peer, **dimensions)
            if row is not None:
                row.clean()
            return row

    def _confirm(self, proof, disposition):
        if disposition == "WAIVED":
            return True
        return disposition == "AUDITED" and self._audit.reconcile_unknown(proof) == "CONFIRMED"

    def _unknown(self, command, dimensions, digest, namespace, original_connection):
        """Aucun nouvel effet : rapprochement indépendant, résultat restant UNKNOWN."""
        disposition = "UNKNOWN"
        try:
            row = self._peer_row(dimensions, namespace, original_connection)
            if row is not None:
                stored = _stored(row, dimensions, digest, command.request.context, self._now())
                proof = TransactionProof(
                    row.operation_id, self._alias, row.transaction_token, _context(row),
                    (StagedRef(row.operation_id, self._alias, row.transaction_token,
                               _context(row), "audit"),), row.created_at,
                )
                if self._confirm(proof, stored.audit_disposition):
                    disposition = stored.audit_disposition
        except (DatabaseError, ConnectionDoesNotExist, ValidationError,
                CoreServiceError, CorePortError, PortError, AuditError, DnsServiceError):
            disposition = "UNKNOWN"
        return DnsCommandResult(
            command.metadata.command_id, command.resource_id, None,
            "UNKNOWN", disposition,
        )

    def declare_desired(self, command, *, waiver_request=None):
        if type(command) is not DeclareDesiredDns or validate_declare_desired_dns(command):
            raise DnsServiceError("DNS_INPUT_INVALID")
        return self._execute(command, waiver_request)

    def retire_desired(self, command, *, waiver_request=None):
        if type(command) is not RetireDesiredDns or validate_retire_desired_dns(command):
            raise DnsServiceError("DNS_INPUT_INVALID")
        return self._execute(command, waiver_request)


    def declare_name(self, command, *, waiver_request=None):
        if type(command) is not DeclareName or validate_declare_name(command):
            raise DnsServiceError("DNS_INPUT_INVALID")
        _name_key(command.name)
        return self._execute(command, waiver_request)

    def retire_name(self, command, *, waiver_request=None):
        if type(command) is not RetireName or validate_retire_name(command):
            raise DnsServiceError("DNS_INPUT_INVALID")
        _name_key(command.name)
        return self._execute(command, waiver_request)

    def _prepare_name(self, command, desired, context, metadata, moment):
        if desired is None or desired.business_state != "DECLARED":
            raise DnsServiceError("DNS_RESOURCE_UNAVAILABLE")
        key, suffix = _name_key(command.name), _name_key(desired.suffix)
        if key == suffix or not key.endswith("." + suffix):
            raise DnsServiceError("DNS_NAME_OUTSIDE_ZONE")
        if command.view not in desired.views:
            raise DnsServiceError("DNS_VIEW_UNAVAILABLE")
        row = _get(DnsNameRecord, self._alias, zone=desired, name_key=key,
                   view=command.view, is_current=True)
        if row is not None:
            row.clean()
            if (_context(row.zone) != context or row.persistence_state != "ACTIVE"
                    or row.business_state != "DECLARED"):
                raise DnsServiceError("DNS_RESOURCE_UNAVAILABLE")
        if type(command) is RetireName and row is None:
            raise DnsServiceError("DNS_NAME_UNAVAILABLE")
        if (type(command) is DeclareName and row is not None
                and row.target_ref != command.target_ref):
            raise DnsServiceError("DNS_NAME_RETIREMENT_REQUIRED")
        new_row, prior_version = row is None, None if row is None else row.version
        if new_row:
            row = DnsNameRecord(
                zone=desired, name=command.name, name_key=key, view=command.view,
                target_ref=command.target_ref, created_at=moment,
            )
        row.updated_at, row.version = moment, 1 if new_row else prior_version + 1
        row.config_revision = desired.config_revision + 1
        row.business_state = "RETIRED" if type(command) is RetireName else "DECLARED"
        row.is_current = type(command) is DeclareName
        for name, value in metadata.items():
            setattr(row, name, value)
        row.full_clean()
        return row, new_row, prior_version

    def _persist_name(self, pending):
        row, new_row, prior_version = pending
        if new_row:
            row.save(using=self._alias, force_insert=True)
        else:
            names = ("version", "updated_at", "governance_ref", "confidentiality",
                     "personal", "config_revision", "business_state", "is_current")
            changed = DnsNameRecord.objects.using(self._alias).filter(
                pk=row.pk, version=prior_version, is_current=True,
                persistence_state="ACTIVE",
            ).update(**{name: getattr(row, name) for name in names})
            if changed != 1:
                raise DnsServiceError("DNS_REVISION_CONFLICT")
        actual = _get(DnsNameRecord, self._alias, pk=row.pk)
        actual.clean()
        if any(getattr(actual, field.attname) != getattr(row, field.attname)
               for field in row._meta.concrete_fields):
            raise DnsServiceError("DNS_STATE_UNAVAILABLE")

    def _decision(self, decider, request, operation):
        decision = decider.revalidate_under_locks(
            request, alias=self._alias, operation_id=operation,
        )
        now = self._now()
        if (type(decision) is not Decision or decision.effect is not Effect.ALLOW
                or decision.decision_id != request.decision_id
                or type(decision.evaluated_at) is not datetime.datetime
                or type(decision.expires_at) is not datetime.datetime
                or decision.evaluated_at.tzinfo is not datetime.timezone.utc
                or decision.expires_at.tzinfo is not datetime.timezone.utc
                or not decision.evaluated_at <= now < decision.expires_at):
            raise DnsServiceError("DNS_DENIED")
        flags = (
            decider.audit_waived(request, decision, alias=self._alias, operation_id=operation),
            decider.governance_waived(request, decision, alias=self._alias, operation_id=operation),
        )
        if any(type(flag) is not bool for flag in flags):
            raise DnsServiceError("DNS_DENIED")
        return decision, flags

    def _execute(self, command, waiver_request):
        self._owner()
        dimensions = _dimensions(command)
        digest = _payload(command, dimensions)
        request, operation = command.request, command.metadata.command_id
        token = str(new_uuid7())
        commit_requested, audit_waived = False, False
        replay_proof = None
        namespace, original_connection = None, None
        try:
            with transaction.atomic(using=self._alias, durable=True):
                provider, decider, _ = build_dns_authorization(
                    store=self._store, auth_source=self._source(command), clock=self._clock,
                    cmd=command, alias=self._alias, operation_id=operation,
                    waiver_request=waiver_request,
                )
                lock_scopes(self._alias, (
                    "dns-idempotence:" + hashlib.sha256(_canonical(dimensions)).hexdigest(),
                ))
                decision, flags = self._decision(decider, request, operation)
                audit_waived, governance_waived = flags
                facts = provider.resolve(request)
                trusted_context = facts.ownership.context
                if trusted_context != request.context:
                    raise DnsServiceError("DNS_DENIED")
                identity = transaction_identity(self._alias)
                namespace, original_connection = identity[2:], connections[self._alias].connection
                policy = self._policy.resolve(
                    context=trusted_context, alias=self._alias, operation_id=operation,
                )
                if type(policy) is not DnsManagementPolicy:
                    raise DnsServiceError("DNS_POLICY_INVALID")
                policy.__post_init__()
                metadata = _metadata(policy, governance_waived)
                moment = self._now()
                desired = _get(
                    DesiredDnsRecord, self._alias,
                    resource_id=command.resource_id, tenant_id=trusted_context.tenant_id,
                )
                if desired is not None:
                    desired.clean()
                    if _context(desired) != trusted_context or desired.persistence_state != "ACTIVE":
                        raise DnsServiceError("DNS_RESOURCE_UNAVAILABLE")
                previous = _get(DnsIdempotenceRecord, self._alias, **dimensions)
                if previous is not None:
                    result = _stored(previous, dimensions, digest, trusted_context, moment)
                    if result.resource_id != command.resource_id:
                        raise DnsServiceError("DNS_IDEMPOTENCE_CONFLICT")
                    replay_proof = TransactionProof(
                        previous.operation_id, self._alias, previous.transaction_token,
                        trusted_context, (StagedRef(previous.operation_id, self._alias,
                        previous.transaction_token, trusted_context, "audit"),), previous.created_at,
                    )
                else:
                    current = 0 if desired is None else desired.config_revision
                    if current != command.expected_revision:
                        raise DnsServiceError("DNS_REVISION_CONFLICT")
                    if type(command) is RetireDesiredDns and desired is None:
                        raise DnsServiceError("DNS_RESOURCE_UNAVAILABLE")
                    pending_name = None
                    if type(command) in (DeclareName, RetireName):
                        pending_name = self._prepare_name(
                            command, desired, trusted_context, metadata, moment)
                    elif type(command) is DeclareDesiredDns:
                        _name_key(command.configuration.suffix)
                        if desired is not None:
                            if _name_key(command.configuration.suffix) != _name_key(desired.suffix):
                                raise DnsServiceError("DNS_NAMESPACE_MIGRATION_REQUIRED")
                            if DnsNameRecord.objects.using(self._alias).filter(
                                    zone=desired, is_current=True).exclude(
                                    view__in=command.configuration.views).exists():
                                raise DnsServiceError("DNS_VIEW_IN_USE")
                    elif DnsNameRecord.objects.using(self._alias).filter(
                            zone=desired, is_current=True).exists():
                        raise DnsServiceError("DNS_NAMES_IN_USE")
                    if (type(command) is DeclareDesiredDns and not governance_waived
                            and command.configuration.governance != policy.governance):
                        raise DnsServiceError("DNS_GOVERNANCE_INVALID")
                    try:
                        expires = moment + policy.idempotence_lifetime
                    except OverflowError:
                        raise DnsServiceError("DNS_POLICY_INVALID") from None
                    new_record = desired is None
                    previous_version = None if new_record else desired.version
                    if new_record:
                        desired = DesiredDnsRecord(
                            resource_id=command.resource_id, created_at=moment,
                            scope_type=trusted_context.scope_type.value,
                            tenant_id=trusted_context.tenant_id, scope_id=trusted_context.scope_id,
                        )
                    desired.config_revision = current + 1
                    desired.version = 1 if new_record else previous_version + 1
                    desired.updated_at = moment
                    desired.payload_sha256, desired.serializer_version = digest, _SERIALIZER
                    for name, value in metadata.items():
                        setattr(desired, name, value)
                    if type(command) is DeclareDesiredDns:
                        cfg = command.configuration
                        if cfg.config_revision != current + 1:
                            raise DnsServiceError("DNS_REVISION_CONFLICT")
                        desired.business_state = "DECLARED"
                        desired.suffix = cfg.suffix
                        desired.ttl_positive, desired.ttl_negative = cfg.ttl_positive, cfg.ttl_negative
                        desired.views = list(cfg.views)
                        document = _configuration(cfg)
                        desired.config = {
                            name: document[name] for name in (
                                "schema_version", "suffix", "ttl_positive", "ttl_negative", "views")
                        }
                        desired.secret_refs = document["secret_refs"]
                        desired.governance = document["governance"]
                    elif type(command) is RetireDesiredDns:
                        desired.business_state = "RETIRED"
                    if not governance_waived:
                        desired.governance = _governance(policy.governance)
                    disposition = "WAIVED" if audit_waived else "AUDITED"
                    result = DnsCommandResult(
                        operation, command.resource_id, current + 1, "SUCCEEDED", disposition,
                    )
                    idempotence = DnsIdempotenceRecord(
                        **dimensions, **metadata, created_at=moment, updated_at=moment,
                        payload_sha256=digest, serializer_version=_SERIALIZER,
                        operation_id=operation, transaction_token=token, staged_xid=identity[1],
                        scope_type=trusted_context.scope_type.value, scope_id=trusted_context.scope_id,
                        expires_at=expires, state="IN_PROGRESS", result={}, result_version=1,
                    )
                    # Toutes les validations attendues précèdent les premières écritures.
                    desired.full_clean()
                    idempotence.full_clean()
                    idempotence.save(using=self._alias, force_insert=True)
                    if new_record:
                        desired.save(using=self._alias, force_insert=True)
                    else:
                        names = (
                            "version", "updated_at", "governance_ref", "confidentiality", "personal",
                            "config_revision", "business_state", "suffix", "ttl_positive",
                            "ttl_negative", "views", "config", "secret_refs", "governance",
                            "payload_sha256", "serializer_version",
                        )
                        changed = DesiredDnsRecord.objects.using(self._alias).filter(
                            pk=desired.pk, version=previous_version, config_revision=current,
                            persistence_state="ACTIVE",
                        ).update(**{name: getattr(desired, name) for name in names})
                        if changed != 1:
                            raise DnsServiceError("DNS_REVISION_CONFLICT")
                    if pending_name is not None:
                        self._persist_name(pending_name)
                    if not audit_waived:
                        event = self._event(
                            actor=facts.auth.digital_identity_id, context=trusted_context,
                            action=command.metadata.command_type, target=command.resource_id,
                            result="SUCCEEDED",
                            reason=command.metadata.command_type.upper(),
                            correlations=command.metadata.correlation_ids,
                            causations=command.metadata.causation_ids,
                        )
                        self._stage(event, operation, token, trusted_context)
                    idempotence.state, idempotence.result = "SUCCEEDED", result.record()
                    idempotence.version += 1
                    idempotence.updated_at = self._now()
                    idempotence.full_clean()
                    idempotence.save(
                        using=self._alias,
                        update_fields=("state", "result", "version", "updated_at"),
                    )
                    actual = _get(DnsIdempotenceRecord, self._alias, pk=idempotence.pk)
                    actual.clean()
                    if (actual.operation_id != operation or actual.transaction_token != token
                            or actual.staged_xid != transaction_identity(self._alias)[1]
                            or actual.result != result.record() or actual.payload_sha256 != digest
                            or _context(actual) != trusted_context
                            or any(getattr(actual, key) != value for key, value in dimensions.items())):
                        raise DnsServiceError("DNS_STATE_UNAVAILABLE")
                    persisted = _get(DesiredDnsRecord, self._alias, pk=desired.pk)
                    persisted.clean()
                    if (persisted.config_revision != desired.config_revision
                            or persisted.payload_sha256 != digest
                            or persisted.business_state != desired.business_state
                            or persisted.created_at != desired.created_at
                            or _context(persisted) != trusted_context):
                        raise DnsServiceError("DNS_STATE_UNAVAILABLE")
                final, final_flags = self._decision(decider, request, operation)
                if final.policy_version != decision.policy_version or final_flags != flags:
                    audit_waived = final_flags[0]
                    raise DnsServiceError("DNS_DENIED")
                commit_requested = True
        except DnsServiceError as error:
            if error.code == "DNS_DENIED":
                audit_waived = False
            self._refusal(command, error.code, audit_waived)
            raise
        except (CoreServiceError, CorePortError, PortError, AuditError, ValidationError) as error:
            if isinstance(error, (CoreServiceError, CorePortError, PortError)):
                audit_waived = False
            mapped = DnsServiceError(
                "DNS_AUDIT_UNAVAILABLE" if type(error) is AuditError else "DNS_STATE_UNAVAILABLE")
            self._refusal(command, mapped.code, audit_waived)
            raise mapped from None
        except DatabaseError as error:
            if commit_requested:
                return self._unknown(
                    command, dimensions, digest, namespace, original_connection,
                )
            mapped = DnsServiceError(
                "DNS_REVISION_CONFLICT" if isinstance(error, IntegrityError)
                else "DNS_STATE_UNAVAILABLE")
            self._refusal(command, mapped.code, audit_waived)
            raise mapped from None
        if replay_proof is not None:
            try:
                if not self._confirm(replay_proof, result.audit_disposition):
                    raise DnsServiceError("DNS_OUTCOME_UNKNOWN")
            except (CorePortError, AuditError, DatabaseError):
                raise DnsServiceError("DNS_OUTCOME_UNKNOWN") from None
        return result


    def get_desired(self, query, *, operation_id, waiver_request=None):
        if type(query) is not GetDesiredDns or validate_get_desired_dns(query):
            raise DnsServiceError("DNS_INPUT_INVALID")
        return self._query(query, operation_id, waiver_request, applied=False)

    def get_applied(self, query, *, operation_id, waiver_request=None):
        if type(query) is not GetAppliedDns or validate_get_applied_dns(query):
            raise DnsServiceError("DNS_INPUT_INVALID")
        return self._query(query, operation_id, waiver_request, applied=True)

    def resolve_view_policy(self, query, *, operation_id, waiver_request=None):
        if type(query) is not ResolveViewPolicy or validate_resolve_view_policy(query):
            raise DnsServiceError("DNS_INPUT_INVALID")
        _name_key(query.name)
        return self._query(query, operation_id, waiver_request, applied=False)

    def _query(self, query, operation, waiver_request, *, applied):
        self._owner()
        if type(operation) is not str or not operation:
            raise DnsServiceError("DNS_INPUT_INVALID")
        request, waived = query.request, False
        try:
            with transaction.atomic(using=self._alias, durable=True):
                provider, decider, _ = build_dns_authorization(
                    store=self._store, auth_source=self._source_request(request, operation),
                    clock=self._clock, cmd=query, alias=self._alias, operation_id=operation,
                    waiver_request=waiver_request,
                )
                decision, flags = self._decision(decider, request, operation)
                waived, governance_waived = flags
                facts = provider.resolve(request)
                policy = self._policy.resolve(
                    context=facts.ownership.context, alias=self._alias, operation_id=operation,
                )
                if type(policy) is not DnsManagementPolicy:
                    raise DnsServiceError("DNS_POLICY_INVALID")
                policy.__post_init__()
                _metadata(policy, governance_waived)
                row = _get(
                    DesiredDnsRecord, self._alias,
                    tenant_id=request.context.tenant_id, resource_id=query.resource_id,
                )
                if row is None:
                    raise DnsServiceError("DNS_RESOURCE_UNAVAILABLE")
                row.clean()
                if _context(row) != facts.ownership.context or row.persistence_state != "ACTIVE":
                    raise DnsServiceError("DNS_RESOURCE_UNAVAILABLE")
                if applied:
                    data = {
                        "resource_id": row.resource_id, "desired_revision": row.config_revision,
                        "applied_revision": None, "applied_present": None,
                        "generation": None, "observed_at": None, "valid_until": None,
                        "measurements": None, "application_status": "UNKNOWN",
                        "measurement_status": "UNMEASURED",
                    }
                else:
                    data = {
                        "schema_version": _SERIALIZER, "resource_id": row.resource_id,
                        "config_revision": row.config_revision, "business_state": row.business_state,
                        "persistence_state": row.persistence_state, "retention_state": row.retention_state,
                        "configuration": {
                            **row.config, "owner_id": _OWNER, "config_revision": row.config_revision,
                            "governance": row.governance, "secret_refs": row.secret_refs,
                        },
                    }
                if type(query) is ResolveViewPolicy:
                    if row.business_state != "DECLARED":
                        raise DnsServiceError("DNS_RESOURCE_UNAVAILABLE")
                    key, suffix = _name_key(query.name), _name_key(row.suffix)
                    if key == suffix or not key.endswith("." + suffix):
                        raise DnsServiceError("DNS_NAME_OUTSIDE_ZONE")
                    if query.view not in row.views:
                        raise DnsServiceError("DNS_VIEW_UNAVAILABLE")
                    name = _get(DnsNameRecord, self._alias, zone=row,
                                name_key=key, view=query.view, is_current=True)
                    if name is not None:
                        name.clean()
                        if (_context(name.zone) != facts.ownership.context
                                or name.persistence_state != "ACTIVE"
                                or name.business_state != "DECLARED"):
                            raise DnsServiceError("DNS_RESOURCE_UNAVAILABLE")
                    data = {
                        "resource_id": row.resource_id, "desired_revision": row.config_revision,
                        "view": query.view, "name_key": key,
                        "desired_name_present": name is not None,
                        "desired_target_ref": None if name is None else name.target_ref,
                        "target_verification": "UNVERIFIED",
                        "ttl_positive_ceiling": row.ttl_positive,
                        "ttl_negative_ceiling": row.ttl_negative,
                        "applied_revision": None, "applied_present": None,
                        "application_status": "UNKNOWN", "measurement_status": "UNMEASURED",
                    }
                if not waived:
                    event = self._event(
                        actor=facts.auth.digital_identity_id, context=facts.ownership.context,
                        action=request.action_id, target=query.resource_id, result="SUCCEEDED",
                        reason="DESIRED_READ" if not applied else "OBSERVATION_READ",
                        correlations=(request.correlation_id,), causations=(),
                    )
                    self._stage(event, operation, str(new_uuid7()), facts.ownership.context)
                final, final_flags = self._decision(decider, request, operation)
                if final.policy_version != decision.policy_version or final_flags != flags:
                    raise DnsServiceError("DNS_DENIED")
            return data
        except DnsServiceError as error:
            if error.code == "DNS_DENIED":
                waived = False
            self._request_refusal(request, operation, error.code, waived)
            raise
        except (CoreServiceError, CorePortError, PortError, AuditError, ValidationError):
            self._request_refusal(request, operation, "DNS_STATE_UNAVAILABLE", False)
            raise DnsServiceError("DNS_STATE_UNAVAILABLE") from None
        except DatabaseError:
            # Aucune donnée n'est exposée si le commit de l'audit n'est pas confirmé.
            raise DnsServiceError("DNS_OUTCOME_UNKNOWN") from None
