"""Façade serveur IMPORT ATOMIC_PER_CHUNK REJECT (B01/B02/B03/B05/B06/B07/B13/B14, B04, B08/B09, B10, B11).

Validation complète préalable puis engagement atomique par chunk sous
participation propriétaire PostgreSQL déclarée même alias, même thread,
même transaction. Aucun worker, Job, provider de production, migration,
dépendance ou configuration créés. Import inerte : stdlib et contrats
purs à l'import, Django/ORM en lazy après gardes.
"""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
from dataclasses import dataclass
from types import MethodType
from datetime import datetime, timedelta, timezone

from asgiref.sync import sync_to_async

from pixs.backend.bulk_execution_values import validate_bulk_policy_values
from pixs.backend.bulk_runtime_contracts import _is_opaque_text, validate_command_execution_values
from pixs.backend.bulk_trusted_ports import (
    _BulkTrustedPorts,
    _OwnerDeclarationSnapshot,
    _capture_python_method,
    validate_owner_command_contract,
)
from pixs.kernel.diagnostics import Diagnostic, VALIDATE

_SCOPE = "bulk_server_apply"

_OPAQUE_RULE = "référence opaque str exacte non vide UTF-8 sans NUL attendue"
_UTC_RULE = "datetime exact aware UTC attendu"
_EVENT_RULE = "asyncio.Event exact attendu"
_REVISION_RULE = "révision int exacte supérieure ou égale à un attendue"
_TRUSTED_RULE = "ports de confiance serveur exacts attendus"
_REPOSITORY_RULE = "dépôt réel exact attendu"
_ALIAS_RULE = "même alias de base déclaré pour les dépôts attendu"
_VENDOR_RULE = "moteur PostgreSQL réel attendu avant tout SQL"
_AUTHORITY_RULE = "autorité EXECUTE actuelle ALLOW attendue"
_GOVERNANCE_RULE = "gouvernance RESOLVED actuelle attendue"
_OBLIGATIONS_RULE = "obligations serveur non implémentées refusées sans prétention"
_MAPPING_RULE = "mapping IMPORT immuable versionné du propriétaire attendu"
_FORMAT_RULE = "format serveur CSV ou NDJSON recroisé au mapping attendu"
_OWNER_RULE = "déclaration propriétaire serveur exacte attendue"
_OWNER_CONTRACT_RULE = "port de commande propriétaire structuralement exact attendu"
_OWNER_CALL_RULE = "méthode propriétaire exacte attendue"
_OWNER_UNAVAILABLE_RULE = "propriétaire indisponible sans détail brut attendu"
_OWNER_VERDICT_RULE = "verdict propriétaire hors contrat refusé sans rapport"
_PARSER_RULE = "parseur IMPORT interne exact attendu avant tout parsing"
_EXAM_RULE = "examen cohérent prouvé avec bilan parser honnête attendu"
_REPORT_RULE = "rapport ValidationReportV1 exact borné attendu"
_LEASE_RULE = "bail pris sous CAS actuel attendu"
_CAS_RULE = "révision connue actuelle attendue sans rebasage concurrent"
_CONSTRAINT_RULE = "invariant de périmètre actuel attendu"
_TRANSITION_RULE = "transition matricielle réelle attendue"
_PERSIST_RULE = "persistance finale atomique sous unité protégée attendue"
_REPLAY_RULE = "rejeu ou second insert refusé sans écrasement"
_RESULT_RULE = "accès au résultat réautorisé sans fuite attendu"
_CANCEL_RULE = "annulation serveur refuse avant résultat"
_EXPIRED_RULE = "échéance effective atteinte refuse avant résultat"
_REJECT_RULE = "rejet propriétaire annule le chunk courant entier attendu"
_RESUME_RULE = "reprise refusée sur source ou mapping divergent attendu"
_KEY_RULE = "clé par commande dérivée exacte attendue"
_RETENTION_RULE = "rétention idempotence exacte attendue"

_PHASE_VALIDATE = "VALIDATE"
_PHASE_APPLY = "APPLY"
_BULK_TYPE = "IMPORT"
_COMMIT_MODE = "ATOMIC_PER_CHUNK"
_CONFLICT = "REJECT"
_REPORT_VERSION = "1.0.0"
_REPORT_MODE = "ATOMIC_PER_CHUNK"
_FORMATS = frozenset({"CSV", "NDJSON"})

_RUNTIME_METHODS = (
    "load_execution",
    "get_binding",
    "get_latest_checkpoint",
    "acquire_lease",
    "protected_unit",
    "commit_checkpoint",
    "apply_transition",
)

_SEAL = object()


class _ApplyRefused(ValueError):
    def __init__(self, diagnostics: list[Diagnostic]):
        super().__init__("apply import refusé")
        self.diagnostics = list(diagnostics)


class _ChunkRejected(Exception):
    pass


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(step=VALIDATE, element=f"{_SCOPE}.{field}", constraint=rule, message=rule)


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for item in refusals:
        unique[(item.element, item.constraint, item.message)] = item
    return [unique[key] for key in sorted(unique)]


def _is_utc_instant(value: object) -> bool:
    return type(value) is datetime and value.tzinfo is timezone.utc


def _is_revision(value: object) -> bool:
    return type(value) is int and value >= 1


@dataclass(frozen=True, slots=True)
class _GuardedTypes:
    lease: type
    cas: type
    constraint: type
    transition: type
    store: type
    conflict: type
    stale: type
    refused: type
    invalid: tuple
    integrity: type


def _load_guarded_types() -> _GuardedTypes:
    from django.core.exceptions import ValidationError as DjangoValidationError
    from django.db import IntegrityError as DjangoIntegrityError

    from pixs.backend.bulk_command_idempotency_repository import (
        BulkCommandIdempotencyConflict,
        BulkCommandIdempotencyRefused,
        BulkCommandIdempotencyStale,
    )
    from pixs.backend.bulk_runtime_repository import (
        CasConflict,
        ConstraintRefused,
        LeaseLost,
        TransitionRefused,
    )
    from pixs.backend.bulk_validation_report_repository import (
        BulkValidationReportRefused,
    )

    return _GuardedTypes(
        lease=LeaseLost,
        cas=CasConflict,
        constraint=ConstraintRefused,
        transition=TransitionRefused,
        store=BulkValidationReportRefused,
        conflict=BulkCommandIdempotencyConflict,
        stale=BulkCommandIdempotencyStale,
        refused=BulkCommandIdempotencyRefused,
        invalid=(DjangoValidationError,),
        integrity=DjangoIntegrityError,
    )


def _load_repository_classes() -> tuple:
    from pixs.backend.bulk_command_idempotency_repository import (
        BulkCommandIdempotencyRepository,
    )
    from pixs.backend.bulk_event_envelope_repository import (
        BulkEventEnvelopeRepository,
    )
    from pixs.backend.bulk_outbox_publication_repository import (
        BulkOutboxPublicationRepository,
    )
    from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository
    from pixs.backend.bulk_validation_report_repository import (
        BulkValidationReportRepository,
    )

    return (
        BulkRuntimeRepository,
        BulkValidationReportRepository,
        BulkCommandIdempotencyRepository,
        BulkEventEnvelopeRepository,
        BulkOutboxPublicationRepository,
    )


def _mapped_refusal(exc: Exception, field: str, guards: _GuardedTypes) -> Diagnostic:
    if isinstance(exc, guards.lease):
        return _refusal(field, _LEASE_RULE)
    if isinstance(exc, guards.cas):
        return _refusal(field, _CAS_RULE)
    if isinstance(exc, guards.constraint):
        return _refusal(field, _CONSTRAINT_RULE)
    if isinstance(exc, guards.transition):
        return _refusal(field, _TRANSITION_RULE)
    if isinstance(exc, guards.store):
        return _refusal(field, _PERSIST_RULE)
    if isinstance(exc, guards.conflict):
        return _refusal(field, _REJECT_RULE)
    if isinstance(exc, guards.stale):
        return _refusal(field, _CAS_RULE)
    if isinstance(exc, guards.refused):
        return _refusal(field, _CONSTRAINT_RULE)
    if isinstance(exc, guards.invalid):
        return _refusal(field, _CONSTRAINT_RULE)
    raise exc


def _check_postgres_vendor(alias: str) -> None:
    try:
        from django.db import connections

        vendor = connections[alias].vendor
    except Exception:
        raise _ApplyRefused([_refusal("vendor", _VENDOR_RULE)]) from None
    if vendor != "postgresql":
        raise _ApplyRefused([_refusal("vendor", _VENDOR_RULE)])


def _capture_sync_method(component: object, name: str) -> object | None:
    captured = _capture_python_method(component, name)
    if captured is None:
        return None
    if inspect.iscoroutinefunction(captured):
        return None
    return captured


@dataclass(frozen=True, slots=True)
class _ServerApplyParticipation:
    _seal: object
    trusted_ports: object
    owner_adapter: object
    validate_fn: object
    execute_fn: object
    canonical_fn: object
    owner_declaration: object
    mapping_descriptor: object
    owner_reference: str
    mapping_reference: str
    mapping_version: str
    contract_version: str
    command_type: str
    serializer_version: str
    order_scope_reference: str
    outbox_failure_catalogue: tuple[str, ...]
    policy_reference: str
    policy_version: str
    runtime_alias: str


def declare_server_apply_participation(
    *,
    trusted_ports: object,
    owner_command_adapter: object,
    owner_reference: object,
    mapping_reference: object,
    mapping_version: object,
    contract_version: object,
    command_type: object,
    serializer_version: object,
    order_scope_reference: object,
    outbox_failure_catalogue: object,
    policy_reference: object,
    policy_version: object,
    runtime_alias: object,
) -> _ServerApplyParticipation:
    from pixs.backend.bulk_execution_values import _is_complete_semver
    from pixs.kernel.manifest.semver import parse_version

    if type(trusted_ports) is not _BulkTrustedPorts:
        raise ValueError("ports de confiance serveur exacts attendus")
    if owner_command_adapter is None or type(owner_command_adapter) is type:
        raise ValueError("adaptateur propriétaire serveur exact attendu")
    if owner_command_adapter is not trusted_ports._owner_command_port:
        raise ValueError("adaptateur distinct du port propriétaire composé refusé")
    if validate_owner_command_contract(owner_command_adapter):
        raise ValueError("port de commande propriétaire structuralement exact attendu")
    for value in (
        owner_reference,
        mapping_reference,
        command_type,
        serializer_version,
        order_scope_reference,
        policy_reference,
        runtime_alias,
    ):
        if not _is_opaque_text(value):
            raise ValueError("référence opaque exacte attendue")
    for value in (mapping_version, contract_version, policy_version, serializer_version):
        if type(value) is not str:
            raise ValueError("version exacte attendue")
        try:
            parse_version(value)
        except ValueError:
            raise ValueError("version SemVer complète exacte attendue") from None
        if not _is_complete_semver(value):
            raise ValueError("version SemVer complète exacte attendue")
    if type(outbox_failure_catalogue) is not tuple:
        raise ValueError("catalogue d'échec serveur exact attendu")
    for item in outbox_failure_catalogue:
        if not _is_opaque_text(item):
            raise ValueError("catalogue d'échec serveur exact attendu")
    declaration = trusted_ports._owner_lookup.get(owner_reference)
    if type(declaration) is not _OwnerDeclarationSnapshot:
        raise ValueError("déclaration propriétaire serveur exacte attendue")
    if declaration.contract_version != contract_version:
        raise ValueError("contract_version distincte de la déclaration propriétaire refusée")
    key = (mapping_reference, mapping_version, owner_reference)
    descriptor = trusted_ports._mapping_lookup.get(key)
    if descriptor is None:
        raise ValueError("mapping non déclaré côté serveur attendu")
    if descriptor.variant != _BULK_TYPE or descriptor.format not in _FORMATS:
        raise ValueError("mapping IMPORT CSV ou NDJSON déclaré attendu")
    validate_fn = _capture_python_method(owner_command_adapter, "validate")
    execute_fn = _capture_python_method(owner_command_adapter, "execute")
    canonical_fn = _capture_python_method(owner_command_adapter, "canonical_bytes")
    for method in (validate_fn, execute_fn, canonical_fn):
        if type(method) is not MethodType or method.__self__ is not owner_command_adapter:
            raise ValueError("méthodes liées au même adaptateur propriétaire attendues")
    if validate_fn is None or not inspect.iscoroutinefunction(validate_fn):
        raise ValueError("validate propriétaire async coopérative exacte attendue")
    if execute_fn is None or inspect.iscoroutinefunction(execute_fn):
        raise ValueError("execute propriétaire synchrone exact attendu")
    if canonical_fn is None or inspect.iscoroutinefunction(canonical_fn):
        raise ValueError("canonical_bytes propriétaire synchrone exact attendu")
    if type(runtime_alias) is not str or not runtime_alias:
        raise ValueError("alias PG serveur explicite attendu")
    return _ServerApplyParticipation(
        _seal=_SEAL,
        trusted_ports=trusted_ports,
        owner_adapter=owner_command_adapter,
        validate_fn=validate_fn,
        execute_fn=execute_fn,
        canonical_fn=canonical_fn,
        owner_declaration=declaration,
        mapping_descriptor=descriptor,
        owner_reference=owner_reference,
        mapping_reference=mapping_reference,
        mapping_version=mapping_version,
        contract_version=contract_version,
        command_type=command_type,
        serializer_version=serializer_version,
        order_scope_reference=order_scope_reference,
        outbox_failure_catalogue=tuple(outbox_failure_catalogue),
        policy_reference=policy_reference,
        policy_version=policy_version,
        runtime_alias=runtime_alias,
    )


def _check_participation(participation: object) -> _ServerApplyParticipation:
    if type(participation) is not _ServerApplyParticipation or participation._seal is not _SEAL:
        raise _ApplyRefused([_refusal("participation", _TRUSTED_RULE)])
    trusted = participation.trusted_ports
    if type(trusted) is not _BulkTrustedPorts:
        raise _ApplyRefused([_refusal("trusted_ports", _TRUSTED_RULE)])
    if participation.owner_adapter is not trusted._owner_command_port:
        raise _ApplyRefused([_refusal("owner", _OWNER_CALL_RULE)])
    for name, must_coro in (("validate_fn", True), ("execute_fn", False), ("canonical_fn", False)):
        fn = getattr(participation, name)
        if type(fn) is not MethodType or fn.__self__ is not participation.owner_adapter:
            raise _ApplyRefused([_refusal("owner", _OWNER_CALL_RULE)])
        if inspect.iscoroutinefunction(fn) is not must_coro:
            raise _ApplyRefused([_refusal("owner", _OWNER_CALL_RULE)])
    if trusted._owner_lookup.get(participation.owner_reference) is not participation.owner_declaration:
        raise _ApplyRefused([_refusal("owner", _OWNER_RULE)])
    if trusted._mapping_lookup.get((participation.mapping_reference, participation.mapping_version, participation.owner_reference)) is not participation.mapping_descriptor:
        raise _ApplyRefused([_refusal("mapping", _MAPPING_RULE)])
    return participation


def _derive_command_key(*, tenant_id: str, subject_id: str, command_type: str, base_key: str, ordinal: int) -> str:
    if not _is_opaque_text(tenant_id) or not _is_opaque_text(subject_id):
        raise _ApplyRefused([_refusal("idempotency_key", _KEY_RULE)])
    if not _is_opaque_text(command_type) or not _is_opaque_text(base_key):
        raise _ApplyRefused([_refusal("idempotency_key", _KEY_RULE)])
    if type(ordinal) is not int or ordinal < 1:
        raise _ApplyRefused([_refusal("idempotency_key", _KEY_RULE)])
    payload = {
        "command_type": command_type,
        "idempotency_key_base": base_key,
        "line_ordinal": ordinal,
        "subject_id": subject_id,
        "tenant_id": tenant_id,
    }
    try:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    except Exception:
        raise _ApplyRefused([_refusal("idempotency_key", _KEY_RULE)]) from None
    return hashlib.sha256(encoded).hexdigest()


def _idempotence_expiry(*, expires_op: datetime, retention_seconds: int) -> datetime:
    if type(retention_seconds) is not int or retention_seconds <= 0:
        raise _ApplyRefused([_refusal("retention", _RETENTION_RULE)])
    if retention_seconds > 2**63 - 1:
        raise _ApplyRefused([_refusal("retention", _RETENTION_RULE)])
    try:
        expiry = expires_op + timedelta(seconds=retention_seconds)
    except OverflowError:
        raise _ApplyRefused([_refusal("retention", _RETENTION_RULE)]) from None
    if expiry.tzinfo is not timezone.utc or expiry <= expires_op:
        raise _ApplyRefused([_refusal("retention", _RETENTION_RULE)])
    return expiry


@dataclass(frozen=True, slots=True)
class _OwnedApplyUnit:
    line_index: int
    serialized_values: str

    def as_values(self) -> dict:
        # Ce JSON interne isole le cache ; il ne remplace pas canonical_bytes propriétaire.
        return json.loads(self.serialized_values)


def _freeze_qualified_units(units: tuple) -> tuple:
    from pixs.backend.bulk_streaming_import import _CsvImportUnit, _NdjsonImportUnit

    frozen = []
    for unit in units:
        if type(unit) is not _CsvImportUnit and type(unit) is not _NdjsonImportUnit:
            raise _ApplyRefused([_refusal("units", _EXAM_RULE)])
        encoded = json.dumps(unit.as_values(), ensure_ascii=True, allow_nan=False, separators=(",", ":"))
        frozen.append(_OwnedApplyUnit(unit.line_index, encoded))
    return tuple(frozen)


def _check_boundary(cancel_event: asyncio.Event, effective: datetime) -> None:
    if cancel_event.is_set():
        raise _ApplyRefused([_refusal("cancel_event", _CANCEL_RULE)])
    if not datetime.now(timezone.utc) < effective:
        raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])


def _exam_qualified(qualified: object, declaration: object, mapping: object) -> dict:
    from pixs.backend.bulk_import_validate import _check_parser_exam, _OrchestrationRefused

    try:
        return _check_parser_exam(qualified, declaration, mapping)
    except _OrchestrationRefused as failure:
        raise _ApplyRefused(list(failure.diagnostics)) from None


def _metadata_snapshot(candidate: object):
    from pixs.backend.bulk_object_staging import _capture_metadata_snapshot

    snapshot, refusals = _capture_metadata_snapshot(candidate)
    if snapshot is None:
        raise _ApplyRefused(list(refusals) or [_refusal("expected_metadata", _RESUME_RULE)])
    return snapshot


@dataclass(frozen=True, slots=True)
class _QualifiedApplyInput:
    _seal: object
    participation_identity: object
    metadata_snapshot: object
    operation_id: str
    sha256: str
    units: tuple
    parser_summary: object
    mapping_version: str
    input_reference: str
    chunk_rows: int
    idempotency_key_base: str
    policy_frozen: tuple
    source_version: object
    owner_reference: str
    mapping_reference: str
    contract_version: str
    policy_reference: str
    policy_version: str

    def owned_policy(self) -> dict:
        owned: dict = {}
        for key, value in self.policy_frozen:
            owned[key] = list(value) if type(value) is tuple else value
        return owned


def _issue_qualified_input(**fields: object) -> _QualifiedApplyInput:
    return _QualifiedApplyInput(_seal=_SEAL, **fields)  # type: ignore[arg-type]


def _check_qualified_input(candidate: object, *, participation: _ServerApplyParticipation, operation_id: str) -> _QualifiedApplyInput:
    if type(candidate) is not _QualifiedApplyInput or candidate._seal is not _SEAL:
        raise _ApplyRefused([_refusal("qualified_input", _EXAM_RULE)])
    from pixs.backend.bulk_object_staging import _ObjectMetadataSnapshot
    from pixs.backend.bulk_streaming_import import _ImportSummary

    if candidate.participation_identity is not participation:
        raise _ApplyRefused([_refusal("qualified_input", _TRUSTED_RULE)])
    if type(candidate.metadata_snapshot) is not _ObjectMetadataSnapshot:
        raise _ApplyRefused([_refusal("qualified_input", _RESUME_RULE)])
    if type(candidate.parser_summary) is not _ImportSummary:
        raise _ApplyRefused([_refusal("qualified_input", _EXAM_RULE)])
    if candidate.parser_summary.complete is not True or candidate.parser_summary.units_refused != 0:
        raise _ApplyRefused([_refusal("qualified_input", _EXAM_RULE)])
    if candidate.operation_id != operation_id:
        raise _ApplyRefused([_refusal("qualified_input", _CONSTRAINT_RULE)])
    if candidate.owner_reference != participation.owner_reference:
        raise _ApplyRefused([_refusal("qualified_input", _MAPPING_RULE)])
    if candidate.mapping_reference != participation.mapping_reference:
        raise _ApplyRefused([_refusal("qualified_input", _MAPPING_RULE)])
    if candidate.mapping_version != participation.mapping_version:
        raise _ApplyRefused([_refusal("qualified_input", _MAPPING_RULE)])
    if candidate.contract_version != participation.contract_version:
        raise _ApplyRefused([_refusal("qualified_input", _OWNER_RULE)])
    if candidate.policy_reference != participation.policy_reference:
        raise _ApplyRefused([_refusal("qualified_input", _GOVERNANCE_RULE)])
    if candidate.policy_version != participation.policy_version:
        raise _ApplyRefused([_refusal("qualified_input", _GOVERNANCE_RULE)])
    if type(candidate.units) is not tuple or candidate.parser_summary.units_emitted != len(candidate.units):
        raise _ApplyRefused([_refusal("qualified_input", _EXAM_RULE)])
    if any(type(unit) is not _OwnedApplyUnit for unit in candidate.units):
        raise _ApplyRefused([_refusal("qualified_input", _EXAM_RULE)])
    if type(candidate.chunk_rows) is not int or candidate.chunk_rows < 1:
        raise _ApplyRefused([_refusal("qualified_input", _GOVERNANCE_RULE)])
    if candidate.sha256 != candidate.metadata_snapshot.sha256:
        raise _ApplyRefused([_refusal("qualified_input", _RESUME_RULE)])
    return candidate


@dataclass(frozen=True, slots=True)
class _ApplyAck:
    operation_id: str
    chunk_index: int
    checkpoint_revision: int
    to_status: str

    def as_values(self) -> dict:
        return {
            "operation_id": self.operation_id,
            "chunk_index": self.chunk_index,
            "checkpoint_revision": self.checkpoint_revision,
            "to_status": self.to_status,
        }


def _resolve_effective_governance(*, trusted_ports: object, server_context: object, assessment: object, mapping_snapshot: object, policy_reference: str, policy_version: str) -> tuple[dict, tuple]:
    resolution, refusals = trusted_ports.resolve_governance(
        server_context=server_context,
        authority_snapshot=assessment,
        governance_contract=mapping_snapshot.as_values(),
        governance_references=(policy_reference, policy_version),
    )
    if resolution is None:
        raise _ApplyRefused(list(refusals) or [_refusal("governance", _GOVERNANCE_RULE)])
    try:
        resolved_values = resolution.as_values()
        resolved_limits = dict(resolved_values["policy"]["limits"])
        obligations = resolved_values["obligations"]
    except Exception:
        raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)]) from None
    if resolved_values.get("decision") != "RESOLVED":
        raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)])
    if type(obligations) is not tuple or obligations != ():
        raise _ApplyRefused([_refusal("obligations", _OBLIGATIONS_RULE)])
    owned: dict = {}
    for key, value in tuple(resolved_limits.items()):
        owned[key] = list(value) if type(value) is list else value
    if validate_bulk_policy_values(dict(owned)):
        raise _ApplyRefused([_refusal("policy", _GOVERNANCE_RULE)])
    return owned, obligations


def _cross_check_metadata(contract: dict, execution: dict) -> None:
    for field, key in (
        ("object_reference", "input_reference"),
        ("version_reference", "input_version"),
        ("sha256", "input_sha256"),
        ("size_bytes", "input_size_bytes"),
    ):
        persisted = execution.get(key)
        if persisted is None or contract.get(field) != persisted:
            raise _ApplyRefused([_refusal("expected_metadata", _VENDOR_RULE)])


async def _bridge_read(callable_object: object, field: str, guards: _GuardedTypes, *args: object, **kwargs: object) -> object:
    from asgiref.sync import sync_to_async as _to_async

    try:
        return await _to_async(callable_object, thread_sensitive=True)(*args, **kwargs)
    except asyncio.CancelledError:
        raise
    except _ApplyRefused:
        raise
    except _ChunkRejected:
        raise
    except Exception as exc:
        if isinstance(
            exc,
            (
                guards.lease,
                guards.cas,
                guards.constraint,
                guards.transition,
                guards.store,
                guards.conflict,
                guards.stale,
                guards.refused,
            ),
        ) or isinstance(exc, guards.invalid):
            raise _ApplyRefused([_mapped_refusal(exc, field, guards)]) from None
        raise


async def _bridge_mutation(
    callable_object: object, field: str, guards: _GuardedTypes,
    *args: object, cancel_event: asyncio.Event, **kwargs: object,
) -> object:
    """Attend une mutation jusqu'à son issue, même après annulations répétées."""
    def run_owned() -> object:
        if cancel_event.is_set():
            raise _ApplyRefused([_refusal("cancel_event", _CANCEL_RULE)])
        return callable_object(*args, **kwargs)

    task = asyncio.create_task(
        sync_to_async(run_owned, thread_sensitive=True)()
    )
    cancelled: asyncio.CancelledError | None = None
    failure: Exception | None = None
    result: object = None
    while True:
        try:
            result = await asyncio.shield(task)
            break
        except asyncio.CancelledError as signal:
            cancelled = cancelled or signal
            cancel_event.set()
            if task.done() and task.cancelled():
                break
        except Exception as error:
            failure = error
            break
    if cancelled is not None:
        if failure is not None:
            raise cancelled from failure
        raise cancelled
    if failure is not None:
        if isinstance(failure, (
            guards.lease, guards.cas, guards.constraint, guards.transition,
            guards.store, guards.conflict, guards.stale, guards.refused,
        )) or isinstance(failure, guards.invalid):
            raise _ApplyRefused(
                [_mapped_refusal(failure, field, guards)]
            ) from None
        raise failure
    return result


async def _validate_all_units_bounded(
    *,
    participation: _ServerApplyParticipation,
    trusted_ports: object,
    server_context: object,
    units: tuple,
    references: tuple,
    policy_owned: dict,
    owner_codes: frozenset,
    owner_fields: frozenset,
    max_diagnostics: int,
    effective: datetime,
    cancel_event: asyncio.Event,
    input_reference: str,
) -> tuple[int, int, list]:
    from pixs.backend.bulk_private_object_reader import _run_with_event as _bounded, _ServerCancelled
    from pixs.backend.bulk_runtime_contracts import validate_command_validation_values as _validate_verdict

    validated_rows = 0
    invalid_rows = 0
    accumulated: list = []
    seen_diagnostics: set = set()
    validate_fn = participation.validate_fn
    for unit in units:
        if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
            raise _ApplyRefused([_refusal("owner.validate", _EXPIRED_RULE)])
        live, live_refusals = trusted_ports.check_authority(
            server_context=server_context, action="EXECUTE",
            operation_reference=references[0], resource_reference=input_reference,
        )
        if live is None:
            raise _ApplyRefused(list(live_refusals) or [_refusal("authority", _AUTHORITY_RULE)])
        live_policy, _ = _resolve_effective_governance(
            trusted_ports=trusted_ports, server_context=server_context, assessment=live,
            mapping_snapshot=participation.mapping_descriptor,
            policy_reference=participation.policy_reference, policy_version=participation.policy_version,
        )
        if live_policy != policy_owned:
            raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)])
        line_index = getattr(unit, "line_index", None)
        if type(line_index) is not int:
            raise _ApplyRefused([_refusal("units", _EXAM_RULE)])
        try:
            mapped = unit.as_values()
        except Exception:
            raise _ApplyRefused([_refusal("units", _EXAM_RULE)]) from None
        if type(mapped) is not dict:
            raise _ApplyRefused([_refusal("units", _EXAM_RULE)])
        entry = {"line_index": line_index, "values": mapped}

        def _remaining() -> float:
            return (effective - datetime.now(timezone.utc)).total_seconds()

        try:
            verdict = await _bounded(
                lambda: validate_fn(server_context, entry, references),
                remaining_fn=_remaining, cancel_event=cancel_event,
            )
        except asyncio.TimeoutError:
            raise _ApplyRefused([_refusal("owner.validate", _EXPIRED_RULE)]) from None
        except _ServerCancelled:
            raise _ApplyRefused([_refusal("owner.validate", _CANCEL_RULE)]) from None
        _check_boundary(cancel_event, effective)
        if type(verdict) is not dict:
            raise _ApplyRefused([_refusal("owner.validate", _OWNER_VERDICT_RULE)])
        if _validate_verdict(
            verdict, policy=dict(policy_owned),
            declared_codes=owner_codes, declared_fields=owner_fields,
        ):
            raise _ApplyRefused([_refusal("owner.validate", _OWNER_VERDICT_RULE)])
        validated_rows += 1
        if verdict["accepted"] is not True:
            invalid_rows += 1
        for item in tuple(verdict["diagnostics"]):
            owned_item = {
                "code": item.get("code"),
                "field_reference": item.get("field_reference"),
                "line_index": item.get("line_index"),
            }
            if owned_item["line_index"] is not None and owned_item["line_index"] != line_index:
                raise _ApplyRefused([_refusal("owner.validate", _OWNER_VERDICT_RULE)])
            key = (owned_item["code"], owned_item["field_reference"], owned_item["line_index"])
            if key not in seen_diagnostics:
                seen_diagnostics.add(key)
                accumulated.append(owned_item)
        if len(accumulated) > max_diagnostics:
            raise _ApplyRefused([_refusal("owner.validate", _REPORT_RULE)])
    return validated_rows, invalid_rows, accumulated


async def prepare_import_apply_readiness(
    *,
    participation: object,
    runtime_repository: object,
    report_repository: object,
    server_context: object,
    operation_id: object,
    validate_job_id: object,
    lease_owner: object,
    expected_metadata: object,
    storage_resolver: object,
    deadline: object,
    now: object,
    cancel_event: object,
    expected_schedule_revision: object,
) -> tuple[_QualifiedApplyInput | None, list[Diagnostic]]:
    try:
        return await _prepare_owned(
            participation=participation, runtime_repository=runtime_repository,
            report_repository=report_repository, server_context=server_context,
            operation_id=operation_id, validate_job_id=validate_job_id, lease_owner=lease_owner,
            expected_metadata=expected_metadata, storage_resolver=storage_resolver,
            deadline=deadline, now=now, cancel_event=cancel_event,
            expected_schedule_revision=expected_schedule_revision,
        )
    except _ApplyRefused as failure:
        return None, _pack(list(failure.diagnostics))
    except asyncio.CancelledError:
        raise
    except Exception:
        raise


async def _prepare_owned(
    *,
    participation: object,
    runtime_repository: object,
    report_repository: object,
    server_context: object,
    operation_id: object,
    validate_job_id: object,
    lease_owner: object,
    expected_metadata: object,
    storage_resolver: object,
    deadline: object,
    now: object,
    cancel_event: object,
    expected_schedule_revision: object,
) -> tuple[_QualifiedApplyInput | None, list[Diagnostic]]:
    from pixs.backend.bulk_object_staging import validate_object_metadata_values
    from pixs.backend.bulk_private_object_reader import _prepare_qualified_import_units
    from pixs.backend.bulk_streaming_import import new_bulk_import_parser
    from pixs.backend.bulk_validation_report_values import validate_bulk_validation_report_values
    from pixs.backend.bulk_import_validate import _check_parser_exam as _exam_generic
    from pixs.kernel.manifest.semver import parse_version

    held = _check_participation(participation)
    trusted_ports = held.trusted_ports
    if server_context is None or type(server_context) is type:
        raise _ApplyRefused([_refusal("server_context", _TRUSTED_RULE)])
    for value in (operation_id, validate_job_id, lease_owner):
        if not _is_opaque_text(value):
            raise _ApplyRefused([_refusal("references", _OPAQUE_RULE)])
    if type(expected_metadata) is not dict:
        raise _ApplyRefused([_refusal("expected_metadata", _VENDOR_RULE)])
    if not _is_utc_instant(deadline) or not _is_utc_instant(now):
        raise _ApplyRefused([_refusal("deadline", _UTC_RULE)])
    if type(cancel_event) is not asyncio.Event:
        raise _ApplyRefused([_refusal("cancel_event", _EVENT_RULE)])
    if not _is_revision(expected_schedule_revision):
        raise _ApplyRefused([_refusal("expected_schedule_revision", _REVISION_RULE)])
    if validate_object_metadata_values(dict(expected_metadata)):
        raise _ApplyRefused([_refusal("expected_metadata", _VENDOR_RULE)])
    metadata_snapshot = _metadata_snapshot(expected_metadata)
    contract = metadata_snapshot.as_values()
    if storage_resolver is None or type(storage_resolver) is type:
        raise _ApplyRefused([_refusal("storage_resolver", _TRUSTED_RULE)])
    meta_expires = contract.get("expires_at")
    if not _is_utc_instant(meta_expires):
        raise _ApplyRefused([_refusal("expected_metadata", _VENDOR_RULE)])
    runtime_class, report_class, _, _, _ = _load_repository_classes()
    if type(runtime_repository) is not runtime_class:
        raise _ApplyRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
    if type(report_repository) is not report_class:
        raise _ApplyRefused([_refusal("report_repository", _REPOSITORY_RULE)])
    try:
        runtime_alias = runtime_repository._using
        report_alias = report_repository._using
    except Exception:
        raise _ApplyRefused([_refusal("alias", _ALIAS_RULE)]) from None
    if type(runtime_alias) is not str or runtime_alias != report_alias:
        raise _ApplyRefused([_refusal("alias", _ALIAS_RULE)])
    if runtime_alias != held.runtime_alias:
        raise _ApplyRefused([_refusal("alias", _ALIAS_RULE)])
    _check_postgres_vendor(runtime_alias)
    methods: dict = {}
    for name in _RUNTIME_METHODS:
        captured = _capture_sync_method(runtime_repository, name)
        if captured is None:
            raise _ApplyRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
        methods[name] = captured
    insert_report = _capture_sync_method(report_repository, "insert_report")
    if insert_report is None:
        raise _ApplyRefused([_refusal("report_repository", _REPOSITORY_RULE)])
    methods["insert_report"] = insert_report
    guards = _load_guarded_types()
    assessment, authority_refusals = trusted_ports.check_authority(
        server_context=server_context, action="EXECUTE",
        operation_reference=operation_id, resource_reference=None,
    )
    if assessment is None:
        raise _ApplyRefused(list(authority_refusals) or [_refusal("authority", _AUTHORITY_RULE)])
    execution = await _bridge_read(methods["load_execution"], "execution", guards, operation_id=operation_id)
    if type(execution) is not dict:
        raise _ApplyRefused([_refusal("execution", _CONSTRAINT_RULE)])
    if execution.get("bulk_type") != _BULK_TYPE or execution.get("commit_mode") != _COMMIT_MODE:
        raise _ApplyRefused([_refusal("mode", _CONSTRAINT_RULE)])
    if execution.get("conflict_strategy") != _CONFLICT:
        raise _ApplyRefused([_refusal("mode", _CONSTRAINT_RULE)])
    if execution.get("status") not in ("STAGED", "VALIDATING"):
        raise _ApplyRefused([_refusal("status", _CONSTRAINT_RULE)])
    if execution.get("cancellation_requested") is not False:
        raise _ApplyRefused([_refusal("cancellation_requested", _CANCEL_RULE)])
    if execution.get("mapping_reference") != held.mapping_reference:
        raise _ApplyRefused([_refusal("mapping", _MAPPING_RULE)])
    if execution.get("mapping_version") != held.mapping_version:
        raise _ApplyRefused([_refusal("mapping", _MAPPING_RULE)])
    if execution.get("policy_reference") != held.policy_reference:
        raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)])
    if execution.get("policy_version") != held.policy_version:
        raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)])
    try:
        parse_version(execution.get("mapping_version"))
    except Exception:
        raise _ApplyRefused([_refusal("references", _OPAQUE_RULE)]) from None
    if execution.get("format") not in _FORMATS:
        raise _ApplyRefused([_refusal("format", _FORMAT_RULE)])
    _cross_check_metadata(contract, execution)
    base_revision = execution.get("revision")
    if not _is_revision(base_revision):
        raise _ApplyRefused([_refusal("revision", _REVISION_RULE)])
    expires_at = execution.get("expires_at")
    if not _is_utc_instant(expires_at):
        raise _ApplyRefused([_refusal("expires_at", _UTC_RULE)])
    binding = await _bridge_read(methods["get_binding"], "binding", guards, operation_id=operation_id, phase=_PHASE_VALIDATE)
    if type(binding) is not dict or binding.get("job_id") != validate_job_id:
        raise _ApplyRefused([_refusal("binding", _CONSTRAINT_RULE)])
    mapping_snapshot = held.mapping_descriptor
    resolved, mapping_refusals = trusted_ports.resolve_mapping(
        held.mapping_reference, held.mapping_version, held.owner_reference
    )
    if resolved is None:
        raise _ApplyRefused(list(mapping_refusals) or [_refusal("mapping", _MAPPING_RULE)])
    if resolved.as_values() != mapping_snapshot.as_values():
        raise _ApplyRefused([_refusal("mapping", _MAPPING_RULE)])
    if mapping_snapshot.variant != _BULK_TYPE or mapping_snapshot.format != execution.get("format"):
        raise _ApplyRefused([_refusal("mapping", _MAPPING_RULE)])
    policy_owned, _ = _resolve_effective_governance(
        trusted_ports=trusted_ports, server_context=server_context, assessment=assessment,
        mapping_snapshot=mapping_snapshot, policy_reference=held.policy_reference,
        policy_version=held.policy_version,
    )
    parser, parser_refusals = new_bulk_import_parser(
        mapping=mapping_snapshot.as_values(), policy=dict(policy_owned),
        declared_owner_fields=tuple(held.owner_declaration.declared_fields),
        declared_codes=tuple(held.owner_declaration.declared_codes),
    )
    if parser is None:
        raise _ApplyRefused(list(parser_refusals) or [_refusal("parser", _PARSER_RULE)])
    try:
        max_runtime = int(policy_owned["max_runtime_seconds"])
        max_diagnostics = int(policy_owned["max_diagnostics"])
        chunk_rows = int(policy_owned["chunk_rows"])
    except Exception:
        raise _ApplyRefused([_refusal("policy", _GOVERNANCE_RULE)]) from None
    if chunk_rows <= 0:
        raise _ApplyRefused([_refusal("policy", _GOVERNANCE_RULE)])
    try:
        resolved_ctx = assessment.resolved_context.as_values()
        tenant_id = resolved_ctx["tenant_id"]
        subject_id = resolved_ctx["subject_id"]
    except Exception:
        raise _ApplyRefused([_refusal("authority", _AUTHORITY_RULE)]) from None
    if not _is_opaque_text(tenant_id) or not _is_opaque_text(subject_id):
        raise _ApplyRefused([_refusal("authority", _AUTHORITY_RULE)])
    base_key = execution.get("idempotency_key")
    if not _is_opaque_text(base_key):
        raise _ApplyRefused([_refusal("references", _OPAQUE_RULE)])
    acquire_now = datetime.now(timezone.utc)
    lease_expires_at = await _bridge_mutation(
        methods["acquire_lease"], "lease", guards,
        operation_id=operation_id, job_id=validate_job_id, phase=_PHASE_VALIDATE,
        owner=lease_owner, policy=dict(policy_owned), now=acquire_now,
        expected_schedule_revision=expected_schedule_revision,
        cancel_event=cancel_event,
    )
    if not _is_utc_instant(lease_expires_at):
        raise _ApplyRefused([_refusal("lease", _LEASE_RULE)])
    schedule_revision = expected_schedule_revision + 1
    effective = min(deadline, meta_expires, expires_at, lease_expires_at, acquire_now + timedelta(seconds=max_runtime))
    if not acquire_now < effective or cancel_event.is_set():
        raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
    if execution.get("status") == "STAGED":
        def _normalize() -> int:
            with methods["protected_unit"](
                operation_id=operation_id, job_id=validate_job_id, phase=_PHASE_VALIDATE,
                owner=lease_owner, policy=dict(policy_owned), now=datetime.now(timezone.utc),
                expected_extension_revision=base_revision, expected_schedule_revision=schedule_revision,
            ):
                inner_now = datetime.now(timezone.utc)
                if cancel_event.is_set() or not inner_now < effective:
                    raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
                revision = methods["apply_transition"](
                    operation_id=operation_id, expected_revision=base_revision,
                    to_status="VALIDATING", now=inner_now,
                )
                _check_boundary(cancel_event, effective)
                return revision

        base_revision = await _bridge_mutation(_normalize, "transition", guards, cancel_event=cancel_event)
    qualified, qualified_refusals = await _prepare_qualified_import_units(
        trusted_ports=trusted_ports, server_context=server_context,
        operation_reference=operation_id, expected_metadata=dict(contract),
        policy_reference=held.policy_reference, policy_version=held.policy_version,
        storage_resolver=storage_resolver, expected_policy=dict(policy_owned),
        parser=parser, deadline=effective, now=datetime.now(timezone.utc), cancel_event=cancel_event,
    )
    if qualified is None:
        raise _ApplyRefused(list(qualified_refusals))
    exam = _exam_qualified(qualified, held.owner_declaration, mapping_snapshot)
    validated_rows, invalid_rows, accumulated = await _validate_all_units_bounded(
        participation=held, trusted_ports=trusted_ports, server_context=server_context,
        units=tuple(qualified.units), references=(operation_id, held.owner_reference, held.mapping_reference, held.mapping_version),
        policy_owned=policy_owned, owner_codes=frozenset(tuple(held.owner_declaration.declared_codes)),
        owner_fields=frozenset(tuple(held.owner_declaration.declared_fields)),
        max_diagnostics=max_diagnostics, effective=effective, cancel_event=cancel_event,
        input_reference=execution.get("input_reference"),
    )
    refused = exam["refused"]
    validated_rows = validated_rows + refused
    invalid_rows = invalid_rows + refused
    complete = bool(exam["full"])
    total_rows = exam["emitted"] if complete else None
    to_status = "READY" if (complete and invalid_rows == 0) else "FAILED"
    from pixs.backend.bulk_import_validate import _build_report_values, _OrchestrationRefused
    try:
        report_values = _build_report_values(
            operation_id=operation_id, mapping_version=held.mapping_version,
            source_version=execution.get("input_version"), total_rows=total_rows,
            validated_rows=validated_rows, invalid_rows=invalid_rows, complete=complete,
            parser_warnings=exam["warnings"], owner_diagnostics=accumulated,
            max_diagnostics=max_diagnostics,
        )
    except _OrchestrationRefused as failure:
        raise _ApplyRefused(list(failure.diagnostics)) from None
    report_values = dict(report_values, mode=_REPORT_MODE)
    if validate_bulk_validation_report_values(
        report_values, policy=dict(policy_owned),
        declared_codes=exam["report_codes"], declared_fields=exam["report_fields"],
    ):
        raise _ApplyRefused([_refusal("report", _REPORT_RULE)])
    fresh = await _bridge_read(methods["load_execution"], "execution", guards, operation_id=operation_id)
    if type(fresh) is not dict or fresh.get("revision") != base_revision:
        raise _ApplyRefused([_refusal("revision", _CAS_RULE)])
    if fresh.get("cancellation_requested") is not False:
        raise _ApplyRefused([_refusal("cancellation_requested", _CANCEL_RULE)])
    if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
        raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])

    sealed_result = None
    if to_status == "READY":
        frozen_policy = tuple(sorted(
            ((k, tuple(v) if type(v) is list else v) for k, v in tuple(policy_owned.items())),
            key=lambda pair: pair[0],
        ))
        sealed_result = _issue_qualified_input(
            participation_identity=held, metadata_snapshot=metadata_snapshot,
            operation_id=operation_id, sha256=qualified.sha256, units=_freeze_qualified_units(qualified.units),
            parser_summary=qualified.parser_summary, mapping_version=held.mapping_version,
            input_reference=execution.get("input_reference"), chunk_rows=chunk_rows,
            idempotency_key_base=base_key, policy_frozen=frozen_policy,
            source_version=execution.get("input_version"), owner_reference=held.owner_reference,
            mapping_reference=held.mapping_reference, contract_version=held.contract_version,
            policy_reference=held.policy_reference, policy_version=held.policy_version,
        )
        _check_qualified_input(sealed_result, participation=held, operation_id=operation_id)

    def _final() -> tuple:
        with methods["protected_unit"](
            operation_id=operation_id, job_id=validate_job_id, phase=_PHASE_VALIDATE,
            owner=lease_owner, policy=dict(policy_owned), now=datetime.now(timezone.utc),
            expected_extension_revision=base_revision, expected_schedule_revision=schedule_revision,
        ) as unit:
            if unit is None:
                raise _ApplyRefused([_refusal("persist", _PERSIST_RULE)])
            inner_now = datetime.now(timezone.utc)
            if cancel_event.is_set() or not inner_now < effective:
                raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
            report_id = methods["insert_report"](
                values=dict(report_values), policy=dict(policy_owned),
                declared_codes=exam["report_codes"], declared_fields=exam["report_fields"],
            )
            checkpoint_revision = methods["commit_checkpoint"](
                unit,
                {
                    "checkpoint_id": f"apply-ready:{operation_id}:{base_revision + 1}:{qualified.sha256}",
                    "operation_id": operation_id, "phase": _PHASE_VALIDATE,
                    "source_fingerprint": qualified.sha256, "mapping_version": held.mapping_version,
                    "committed_unit_index": validated_rows, "progress": dict(report_values["progress"]),
                    "revision": base_revision + 1, "owner_result_reference": None,
                },
            )
            transition_revision = methods["apply_transition"](
                operation_id=operation_id, expected_revision=checkpoint_revision,
                to_status=to_status, now=datetime.now(timezone.utc),
            )
            _check_boundary(cancel_event, effective)
            return (report_id, checkpoint_revision, transition_revision)

    await _bridge_mutation(_final, "persist", guards, cancel_event=cancel_event)
    if to_status != "READY":
        raise _ApplyRefused([_refusal("report", _REJECT_RULE)])
    return sealed_result, []


async def _rebuild_qualified_input(
    *,
    held: _ServerApplyParticipation,
    methods: dict,
    guards: _GuardedTypes,
    policy_owned: dict,
    server_context: object,
    operation_id: str,
    apply_job_id: str,
    expected_metadata: dict,
    storage_resolver: object,
    effective: datetime,
    cancel_event: asyncio.Event,
    execution: dict,
) -> _QualifiedApplyInput:
    from pixs.backend.bulk_private_object_reader import _prepare_qualified_import_units
    from pixs.backend.bulk_streaming_import import new_bulk_import_parser
    from pixs.backend.bulk_import_validate import _check_parser_exam as _exam_generic

    trusted_ports = held.trusted_ports
    parser, parser_refusals = new_bulk_import_parser(
        mapping=held.mapping_descriptor.as_values(), policy=dict(policy_owned),
        declared_owner_fields=tuple(held.owner_declaration.declared_fields),
        declared_codes=tuple(held.owner_declaration.declared_codes),
    )
    if parser is None:
        raise _ApplyRefused(list(parser_refusals) or [_refusal("parser", _PARSER_RULE)])
    qualified, qualified_refusals = await _prepare_qualified_import_units(
        trusted_ports=trusted_ports, server_context=server_context,
        operation_reference=operation_id, expected_metadata=dict(expected_metadata),
        policy_reference=held.policy_reference, policy_version=held.policy_version,
        storage_resolver=storage_resolver, expected_policy=dict(policy_owned),
        parser=parser, deadline=effective, now=datetime.now(timezone.utc), cancel_event=cancel_event,
    )
    if qualified is None:
        raise _ApplyRefused(list(qualified_refusals))
    exam = _exam_qualified(qualified, held.owner_declaration, held.mapping_descriptor)
    try:
        max_diagnostics = int(policy_owned["max_diagnostics"])
        chunk_rows = int(policy_owned["chunk_rows"])
    except Exception:
        raise _ApplyRefused([_refusal("policy", _GOVERNANCE_RULE)]) from None
    validated_rows, invalid_rows, _ = await _validate_all_units_bounded(
        participation=held, trusted_ports=trusted_ports, server_context=server_context,
        units=tuple(qualified.units), references=(operation_id, held.owner_reference, held.mapping_reference, held.mapping_version),
        policy_owned=policy_owned, owner_codes=frozenset(tuple(held.owner_declaration.declared_codes)),
        owner_fields=frozenset(tuple(held.owner_declaration.declared_fields)),
        max_diagnostics=max_diagnostics, effective=effective, cancel_event=cancel_event,
        input_reference=execution.get("input_reference"),
    )
    if not exam["full"]:
        raise _ApplyRefused([_refusal("parser", _EXAM_RULE)])
    if (invalid_rows + exam["refused"]) != 0:
        raise _ApplyRefused([_refusal("report", _REJECT_RULE)])
    frozen_policy = tuple(sorted(
        ((k, tuple(v) if type(v) is list else v) for k, v in tuple(policy_owned.items())),
        key=lambda pair: pair[0],
    ))
    return _issue_qualified_input(
        participation_identity=held, metadata_snapshot=_metadata_snapshot(expected_metadata),
        operation_id=operation_id, sha256=qualified.sha256, units=_freeze_qualified_units(qualified.units),
        parser_summary=qualified.parser_summary, mapping_version=held.mapping_version,
        input_reference=execution.get("input_reference"), chunk_rows=chunk_rows,
        idempotency_key_base=execution.get("idempotency_key"), policy_frozen=frozen_policy,
        source_version=execution.get("input_version"), owner_reference=held.owner_reference,
        mapping_reference=held.mapping_reference, contract_version=held.contract_version,
        policy_reference=held.policy_reference, policy_version=held.policy_version,
    )


async def apply_import_chunks_atomic_per_chunk(
    *,
    participation: object,
    runtime_repository: object,
    idempotency_repository: object,
    envelope_repository: object,
    outbox_repository: object,
    server_context: object,
    operation_id: object,
    apply_job_id: object,
    lease_owner: object,
    qualified_input: object | None,
    expected_metadata: object | None,
    storage_resolver: object | None,
    deadline: object,
    cancel_event: object,
    expected_schedule_revision: object,
) -> tuple[list[dict] | None, list[Diagnostic]]:
    try:
        return await _apply_owned(
            participation=participation, runtime_repository=runtime_repository,
            idempotency_repository=idempotency_repository, envelope_repository=envelope_repository,
            outbox_repository=outbox_repository, server_context=server_context,
            operation_id=operation_id, apply_job_id=apply_job_id, lease_owner=lease_owner,
            qualified_input=qualified_input, expected_metadata=expected_metadata,
            storage_resolver=storage_resolver, deadline=deadline, cancel_event=cancel_event,
            expected_schedule_revision=expected_schedule_revision,
        )
    except _ApplyRefused as failure:
        return None, _pack(list(failure.diagnostics))
    except asyncio.CancelledError:
        raise
    except Exception:
        raise


async def _apply_owned(
    *,
    participation: object,
    runtime_repository: object,
    idempotency_repository: object,
    envelope_repository: object,
    outbox_repository: object,
    server_context: object,
    operation_id: object,
    apply_job_id: object,
    lease_owner: object,
    qualified_input: object | None,
    expected_metadata: object | None,
    storage_resolver: object | None,
    deadline: object,
    cancel_event: object,
    expected_schedule_revision: object,
) -> tuple[list[dict] | None, list[Diagnostic]]:
    from pixs.backend.bulk_object_staging import validate_object_metadata_values

    held = _check_participation(participation)
    trusted_ports = held.trusted_ports
    if server_context is None or type(server_context) is type:
        raise _ApplyRefused([_refusal("server_context", _TRUSTED_RULE)])
    for value in (operation_id, apply_job_id, lease_owner):
        if not _is_opaque_text(value):
            raise _ApplyRefused([_refusal("references", _OPAQUE_RULE)])
    if not _is_utc_instant(deadline):
        raise _ApplyRefused([_refusal("deadline", _UTC_RULE)])
    if type(cancel_event) is not asyncio.Event:
        raise _ApplyRefused([_refusal("cancel_event", _EVENT_RULE)])
    if not _is_revision(expected_schedule_revision):
        raise _ApplyRefused([_refusal("expected_schedule_revision", _REVISION_RULE)])
    checked = None
    if qualified_input is not None:
        checked = _check_qualified_input(qualified_input, participation=held, operation_id=operation_id)
        contract = checked.metadata_snapshot.as_values()
    else:
        if storage_resolver is None or type(storage_resolver) is type:
            raise _ApplyRefused([_refusal("storage_resolver", _TRUSTED_RULE)])
        contract = _metadata_snapshot(expected_metadata).as_values()
    if cancel_event.is_set():
        raise _ApplyRefused([_refusal("cancel_event", _CANCEL_RULE)])
    if not datetime.now(timezone.utc) < min(deadline, contract["expires_at"]):
        raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
    runtime_class, _, idem_class, env_class, outbox_class = _load_repository_classes()
    if type(runtime_repository) is not runtime_class:
        raise _ApplyRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
    if type(idempotency_repository) is not idem_class:
        raise _ApplyRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
    if type(envelope_repository) is not env_class:
        raise _ApplyRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
    if type(outbox_repository) is not outbox_class:
        raise _ApplyRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
    try:
        runtime_alias = runtime_repository._using
    except Exception:
        raise _ApplyRefused([_refusal("alias", _ALIAS_RULE)]) from None
    for repo in (idempotency_repository, envelope_repository, outbox_repository):
        try:
            alias = repo._using
        except Exception:
            raise _ApplyRefused([_refusal("alias", _ALIAS_RULE)]) from None
        if type(alias) is not str or alias != runtime_alias:
            raise _ApplyRefused([_refusal("alias", _ALIAS_RULE)])
    if runtime_alias != held.runtime_alias:
        raise _ApplyRefused([_refusal("alias", _ALIAS_RULE)])
    _check_postgres_vendor(runtime_alias)
    methods: dict = {}
    for name in _RUNTIME_METHODS:
        captured = _capture_sync_method(runtime_repository, name)
        if captured is None:
            raise _ApplyRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
        methods[name] = captured
    guards = _load_guarded_types()
    assessment, authority_refusals = trusted_ports.check_authority(
        server_context=server_context, action="EXECUTE",
        operation_reference=operation_id, resource_reference=None,
    )
    if assessment is None:
        raise _ApplyRefused(list(authority_refusals) or [_refusal("authority", _AUTHORITY_RULE)])
    execution = await _bridge_read(methods["load_execution"], "execution", guards, operation_id=operation_id)
    if type(execution) is not dict:
        raise _ApplyRefused([_refusal("execution", _CONSTRAINT_RULE)])
    if execution.get("bulk_type") != _BULK_TYPE or execution.get("commit_mode") != _COMMIT_MODE:
        raise _ApplyRefused([_refusal("mode", _CONSTRAINT_RULE)])
    if execution.get("conflict_strategy") != _CONFLICT:
        raise _ApplyRefused([_refusal("mode", _CONSTRAINT_RULE)])
    _cross_check_metadata(contract, execution)
    if held.mapping_descriptor.format != execution.get("format"):
        raise _ApplyRefused([_refusal("format", _FORMAT_RULE)])
    if execution.get("status") not in ("READY", "RUNNING"):
        raise _ApplyRefused([_refusal("status", _CONSTRAINT_RULE)])
    if execution.get("cancellation_requested") is not False:
        raise _ApplyRefused([_refusal("cancellation_requested", _CANCEL_RULE)])
    if execution.get("mapping_reference") != held.mapping_reference:
        raise _ApplyRefused([_refusal("mapping", _MAPPING_RULE)])
    if execution.get("mapping_version") != held.mapping_version:
        raise _ApplyRefused([_refusal("mapping", _MAPPING_RULE)])
    if execution.get("policy_reference") != held.policy_reference:
        raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)])
    if execution.get("policy_version") != held.policy_version:
        raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)])
    policy_owned, _ = _resolve_effective_governance(
        trusted_ports=trusted_ports, server_context=server_context, assessment=assessment,
        mapping_snapshot=held.mapping_descriptor, policy_reference=held.policy_reference,
        policy_version=held.policy_version,
    )
    try:
        retention = int(policy_owned["idempotency_retention_seconds"])
        chunk_rows_policy = int(policy_owned["chunk_rows"])
        max_depth = int(policy_owned["max_json_depth"])
        max_members = int(policy_owned["max_json_members"])
        max_runtime = int(policy_owned["max_runtime_seconds"])
    except Exception:
        raise _ApplyRefused([_refusal("policy", _GOVERNANCE_RULE)]) from None
    if chunk_rows_policy <= 0:
        raise _ApplyRefused([_refusal("policy", _GOVERNANCE_RULE)])
    expires_op = execution.get("expires_at")
    if not _is_utc_instant(expires_op):
        raise _ApplyRefused([_refusal("expires_at", _UTC_RULE)])
    expires_idem = _idempotence_expiry(expires_op=expires_op, retention_seconds=retention)
    binding = await _bridge_read(methods["get_binding"], "binding", guards, operation_id=operation_id, phase=_PHASE_APPLY)
    if type(binding) is not dict or binding.get("job_id") != apply_job_id:
        raise _ApplyRefused([_refusal("binding", _CONSTRAINT_RULE)])
    resolved, mapping_refusals = trusted_ports.resolve_mapping(
        held.mapping_reference, held.mapping_version, held.owner_reference
    )
    if resolved is None:
        raise _ApplyRefused(list(mapping_refusals) or [_refusal("mapping", _MAPPING_RULE)])
    if resolved.as_values() != held.mapping_descriptor.as_values():
        raise _ApplyRefused([_refusal("mapping", _MAPPING_RULE)])
    base_revision = execution.get("revision")
    if not _is_revision(base_revision):
        raise _ApplyRefused([_refusal("revision", _REVISION_RULE)])
    acquire_now = datetime.now(timezone.utc)
    lease_expires_at = await _bridge_mutation(
        methods["acquire_lease"], "lease", guards,
        operation_id=operation_id, job_id=apply_job_id, phase=_PHASE_APPLY,
        owner=lease_owner, policy=dict(policy_owned), now=acquire_now,
        expected_schedule_revision=expected_schedule_revision,
        cancel_event=cancel_event,
    )
    if not _is_utc_instant(lease_expires_at):
        raise _ApplyRefused([_refusal("lease", _LEASE_RULE)])
    schedule_revision = expected_schedule_revision + 1
    acquire_deadline = acquire_now + timedelta(seconds=max_runtime)
    effective = min(deadline, contract["expires_at"], expires_op, lease_expires_at, acquire_deadline)
    if not acquire_now < effective or cancel_event.is_set():
        raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
    persisted_progress = execution.get("progress")
    if type(persisted_progress) is not dict:
        raise _ApplyRefused([_refusal("execution", _CONSTRAINT_RULE)])
    persisted_applied = persisted_progress.get("applied_rows")
    if type(persisted_applied) is not int or persisted_applied < 0:
        raise _ApplyRefused([_refusal("execution", _CONSTRAINT_RULE)])
    sealed: _QualifiedApplyInput | None = None
    if qualified_input is not None:
        if (checked.source_version != execution.get("input_version")
                or checked.idempotency_key_base != execution.get("idempotency_key")
                or checked.chunk_rows != chunk_rows_policy):
            raise _ApplyRefused([_refusal("qualified_input", _RESUME_RULE)])
        if dict(checked.owned_policy()) != dict(policy_owned):
            raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)])
        if checked.sha256 != execution.get("input_sha256"):
            raise _ApplyRefused([_refusal("qualified_input", _RESUME_RULE)])
        if checked.input_reference != execution.get("input_reference"):
            raise _ApplyRefused([_refusal("qualified_input", _RESUME_RULE)])
        sealed = checked
    else:
        sealed = await _rebuild_qualified_input(
            held=held, methods=methods, guards=guards, policy_owned=policy_owned,
            server_context=server_context, operation_id=operation_id, apply_job_id=apply_job_id,
            expected_metadata=dict(contract), storage_resolver=storage_resolver,
            effective=effective, cancel_event=cancel_event, execution=execution,
        )
    sealed = _check_qualified_input(sealed, participation=held, operation_id=operation_id)
    persisted = await _bridge_read(
        methods["get_latest_checkpoint"], "checkpoint", guards,
        operation_id=operation_id, phase=_PHASE_APPLY,
    )
    start_ordinal = 0
    if persisted is not None:
        if type(persisted) is not dict:
            raise _ApplyRefused([_refusal("checkpoint", _RESUME_RULE)])
        if persisted.get("source_fingerprint") != sealed.sha256:
            raise _ApplyRefused([_refusal("checkpoint", _RESUME_RULE)])
        if persisted.get("mapping_version") != sealed.mapping_version:
            raise _ApplyRefused([_refusal("checkpoint", _RESUME_RULE)])
        start_ordinal = persisted.get("committed_unit_index")
        if type(start_ordinal) is not int or start_ordinal < 0:
            raise _ApplyRefused([_refusal("checkpoint", _RESUME_RULE)])
    total_units = tuple(sealed.units)
    if (start_ordinal > len(total_units)
            or (start_ordinal != len(total_units) and start_ordinal % sealed.chunk_rows != 0)):
        raise _ApplyRefused([_refusal("checkpoint", _RESUME_RULE)])
    if (persisted_progress.get("total_rows") != len(total_units)
            or persisted_progress.get("validated_rows") != len(total_units)
            or persisted_progress.get("invalid_rows") != 0
            or persisted_progress.get("execution_rejected_rows") != 0
            or persisted_progress.get("exported_rows") != 0
            or persisted_applied > start_ordinal):
        raise _ApplyRefused([_refusal("progress", _RESUME_RULE)])
    if persisted is None:
        if persisted_applied != 0:
            raise _ApplyRefused([_refusal("progress", _RESUME_RULE)])
    elif persisted.get("progress") != persisted_progress:
        raise _ApplyRefused([_refusal("checkpoint", _RESUME_RULE)])
    remaining = total_units[start_ordinal:]
    try:
        owner_codes = frozenset(tuple(held.owner_declaration.declared_codes))
        owner_fields = frozenset(tuple(held.owner_declaration.declared_fields))
    except Exception:
        raise _ApplyRefused([_refusal("owner", _OWNER_RULE)]) from None
    references = (operation_id, held.owner_reference, held.mapping_reference, held.mapping_version)
    if execution.get("status") == "READY":
        def _to_running() -> int:
            with methods["protected_unit"](
                operation_id=operation_id, job_id=apply_job_id, phase=_PHASE_APPLY,
                owner=lease_owner, policy=dict(policy_owned), now=datetime.now(timezone.utc),
                expected_extension_revision=base_revision,
                expected_schedule_revision=schedule_revision,
            ):
                if cancel_event.is_set():
                    raise _ApplyRefused([_refusal("cancel_event", _CANCEL_RULE)])
                if not datetime.now(timezone.utc) < effective:
                    raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
                revision = methods["apply_transition"](
                    operation_id=operation_id, expected_revision=base_revision,
                    to_status="RUNNING", now=datetime.now(timezone.utc),
                )
                _check_boundary(cancel_event, effective)
                return revision

        base_revision = await _bridge_mutation(_to_running, "transition", guards, cancel_event=cancel_event)
    chunk_index = start_ordinal // sealed.chunk_rows if sealed.chunk_rows else 0
    ordinal = start_ordinal
    acks: list[dict] = []
    for offset in range(0, len(remaining), sealed.chunk_rows):
        chunk = remaining[offset:offset + sealed.chunk_rows]
        chunk_index += 1
        if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
            raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])

        def _chunk_tx(chunk_units: tuple = tuple(chunk), chunk_ordinal_base: int = ordinal, chunk_number: int = chunk_index) -> tuple[int, int]:
            import threading as _threading

            with methods["protected_unit"](
                operation_id=operation_id, job_id=apply_job_id, phase=_PHASE_APPLY,
                owner=lease_owner, policy=dict(policy_owned), now=datetime.now(timezone.utc),
                expected_extension_revision=base_revision,
                expected_schedule_revision=schedule_revision,
            ) as unit:
                if unit is None:
                    raise _ApplyRefused([_refusal("persist", _PERSIST_RULE)])
                current = runtime_repository._unit_var.get()
                if current is not unit or not unit.active or _threading.get_ident() != unit.thread_ident:
                    raise _ApplyRefused([_refusal("persist", _PERSIST_RULE)])
                if runtime_repository._using != runtime_alias:
                    raise _ApplyRefused([_refusal("alias", _ALIAS_RULE)])
                if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
                    raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
                unit.now = datetime.now(timezone.utc)
                local_ordinal = chunk_ordinal_base
                local_fresh = 0
                for item in chunk_units:
                    live, live_refusals = trusted_ports.check_authority(
                        server_context=server_context, action="EXECUTE",
                        operation_reference=operation_id, resource_reference=execution.get("input_reference"),
                    )
                    if live is None:
                        raise _ApplyRefused(list(live_refusals) or [_refusal("authority", _AUTHORITY_RULE)])
                    live_policy, _ = _resolve_effective_governance(
                        trusted_ports=trusted_ports, server_context=server_context, assessment=live,
                        mapping_snapshot=held.mapping_descriptor, policy_reference=held.policy_reference,
                        policy_version=held.policy_version,
                    )
                    if live_policy != policy_owned:
                        raise _ApplyRefused([_refusal("governance", _GOVERNANCE_RULE)])
                    try:
                        live_ctx = live.resolved_context.as_values()
                        cur_tenant = live_ctx["tenant_id"]
                        cur_subject = live_ctx["subject_id"]
                    except Exception:
                        raise _ApplyRefused([_refusal("authority", _AUTHORITY_RULE)]) from None
                    local_ordinal += 1
                    line_index = getattr(item, "line_index", None)
                    if type(line_index) is not int:
                        raise _ApplyRefused([_refusal("units", _EXAM_RULE)])
                    try:
                        mapped = item.as_values()
                    except Exception:
                        raise _ApplyRefused([_refusal("units", _EXAM_RULE)]) from None
                    if type(mapped) is not dict:
                        raise _ApplyRefused([_refusal("units", _EXAM_RULE)])
                    if not _is_opaque_text(cur_tenant) or not _is_opaque_text(cur_subject):
                        raise _ApplyRefused([_refusal("authority", _AUTHORITY_RULE)])
                    if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
                        raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
                    unit.now = datetime.now(timezone.utc)
                    canonical = held.canonical_fn(item.as_values())
                    _check_boundary(cancel_event, effective)
                    if type(canonical) is not bytes:
                        raise _ApplyRefused([_refusal("owner.canonical_bytes", _OWNER_VERDICT_RULE)])
                    content_sha = hashlib.sha256(canonical).hexdigest()
                    derived = _derive_command_key(
                        tenant_id=cur_tenant, subject_id=cur_subject,
                        command_type=held.command_type,
                        base_key=sealed.idempotency_key_base, ordinal=local_ordinal,
                    )
                    idem_values = {
                        "tenant_id": cur_tenant, "subject_id": cur_subject,
                        "command_type": held.command_type, "idempotency_key": derived,
                        "content_sha256": content_sha, "serializer_version": held.serializer_version,
                        "state": "IN_PROGRESS", "result_reference": None, "failure_code": None,
                        "created_at": datetime.now(timezone.utc), "expires_at": expires_idem, "revision": 1,
                    }
                    with idempotency_repository.idempotent_unit(values=dict(idem_values)) as token:
                        if runtime_repository._unit_var.get() is not unit:
                            raise _ApplyRefused([_refusal("persist", _PERSIST_RULE)])
                        if idempotency_repository._unit_var.get() is not token:
                            raise _ApplyRefused([_refusal("persist", _PERSIST_RULE)])
                        if token.is_replay:
                            try:
                                replayed = token.entry
                            except Exception:
                                raise _ApplyRefused([_refusal("idempotency", _CONSTRAINT_RULE)]) from None
                            if not _is_utc_instant(replayed.get("expires_at")) or replayed["expires_at"] < expires_idem:
                                raise _ApplyRefused([_refusal("idempotency", _RETENTION_RULE)])
                            if replayed.get("state") == "REJECTED":
                                raise _ChunkRejected()
                            if replayed.get("state") != "SUCCEEDED" or replayed.get("content_sha256") != content_sha:
                                raise _ApplyRefused([_refusal("idempotency", _REPLAY_RULE)])
                            _check_boundary(cancel_event, effective)
                            continue
                        entry = {"line_index": line_index, "values": item.as_values()}
                        verdict = held.execute_fn(server_context, entry, references)
                        if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
                            raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
                        unit.now = datetime.now(timezone.utc)
                        from pixs.backend.bulk_runtime_contracts import validate_command_execution_values as _validate_exec

                        if _validate_exec(
                            verdict, policy=dict(policy_owned),
                            declared_codes=owner_codes, declared_fields=owner_fields,
                        ):
                            raise _ApplyRefused([_refusal("owner.execute", _OWNER_VERDICT_RULE)])
                        if verdict["outcome"] == "REJECTED":
                            raise _ChunkRejected()
                        if verdict["outcome"] not in ("APPLIED", "REPLAYED"):
                            raise _ApplyRefused([_refusal("owner.execute", _OWNER_VERDICT_RULE)])
                        if verdict["outcome"] == "REPLAYED":
                            idempotency_repository.finalize_terminal(
                                token, expected_revision=1, state="SUCCEEDED",
                                result_reference=verdict["result_reference"], failure_code=None,
                            )
                            _check_boundary(cancel_event, effective)
                            continue
                        refs = tuple(verdict["event_references"])
                        for event_id in refs:
                            if not _is_opaque_text(event_id):
                                raise _ApplyRefused([_refusal("envelope", _CONSTRAINT_RULE)])
                            found = envelope_repository.get_envelope(
                                event_id=event_id, max_depth=max_depth,
                                max_members=max_members, non_tenant_authorized=False,
                            )
                            if found is None:
                                raise _ApplyRefused([_refusal("envelope", _CONSTRAINT_RULE)])
                            try:
                                snapshot = found.as_values()
                            except Exception:
                                raise _ApplyRefused([_refusal("envelope", _CONSTRAINT_RULE)]) from None
                            if snapshot.get("event_id") != event_id:
                                raise _ApplyRefused([_refusal("envelope", _CONSTRAINT_RULE)])
                            if snapshot.get("order_scope_reference") != held.order_scope_reference:
                                raise _ApplyRefused([_refusal("envelope", _CONSTRAINT_RULE)])
                            # Référence de contexte opaque : le contrat enveloppe la valide,
                            # sans la confondre avec tenant_id de la clé idempotente.
                        for event_id in refs:
                            outbox_repository.insert_initial(
                                event_id=event_id, state="PENDING", attempt_count=0,
                                lease_owner=None, lease_expires_at=None, next_attempt_at=None,
                                published_at=None, failure_code=None,
                                policy_reference=held.policy_reference,
                                policy_version=held.policy_version, revision=1,
                                failure_catalogue=tuple(held.outbox_failure_catalogue),
                            )
                        idempotency_repository.finalize_terminal(
                            token, expected_revision=1, state="SUCCEEDED",
                            result_reference=verdict["result_reference"], failure_code=None,
                        )
                        local_fresh += 1
                    if cancel_event.is_set():
                        raise _ApplyRefused([_refusal("cancel_event", _CANCEL_RULE)])
                if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
                    raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])
                unit.now = datetime.now(timezone.utc)
                applied_here = persisted_applied + local_fresh
                progress = {
                    "total_rows": len(total_units), "validated_rows": len(total_units),
                    "invalid_rows": 0, "applied_rows": applied_here,
                    "execution_rejected_rows": 0, "exported_rows": 0,
                }
                checkpoint_revision = methods["commit_checkpoint"](
                    unit,
                    {
                        "checkpoint_id": f"apply:{operation_id}:{base_revision + 1}:{sealed.sha256}:{chunk_number}",
                        "operation_id": operation_id, "phase": _PHASE_APPLY,
                        "source_fingerprint": sealed.sha256,
                        "mapping_version": sealed.mapping_version,
                        "committed_unit_index": local_ordinal, "progress": dict(progress),
                        "revision": base_revision + 1, "owner_result_reference": None,
                    },
                )
                _check_boundary(cancel_event, effective)
                return checkpoint_revision, applied_here

        try:
            checkpoint_revision, applied_here = await _bridge_mutation(_chunk_tx, "chunk", guards, cancel_event=cancel_event)
        except _ChunkRejected:
            raise _ApplyRefused([_refusal("chunk", _REJECT_RULE)])
        ordinal += len(chunk)
        persisted_applied = applied_here
        base_revision = checkpoint_revision
        acks.append(
            _ApplyAck(
                operation_id=operation_id, chunk_index=chunk_index,
                checkpoint_revision=checkpoint_revision, to_status="RUNNING",
            ).as_values()
        )
    fresh = await _bridge_read(methods["load_execution"], "execution", guards, operation_id=operation_id)
    if type(fresh) is not dict or fresh.get("revision") != base_revision:
        raise _ApplyRefused([_refusal("revision", _CAS_RULE)])
    if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
        raise _ApplyRefused([_refusal("now", _EXPIRED_RULE)])

    def _finish() -> int:
        with methods["protected_unit"](
            operation_id=operation_id, job_id=apply_job_id, phase=_PHASE_APPLY,
            owner=lease_owner, policy=dict(policy_owned), now=datetime.now(timezone.utc),
            expected_extension_revision=base_revision,
            expected_schedule_revision=schedule_revision,
        ):
            if cancel_event.is_set():
                raise _ApplyRefused([_refusal("cancel_event", _CANCEL_RULE)])
            _check_boundary(cancel_event, effective)
            revision = methods["apply_transition"](
                operation_id=operation_id, expected_revision=base_revision,
                to_status="COMPLETED", now=datetime.now(timezone.utc),
            )
            _check_boundary(cancel_event, effective)
            return revision

    transition_revision = await _bridge_mutation(_finish, "transition", guards, cancel_event=cancel_event)
    return acks + [
        _ApplyAck(
            operation_id=operation_id, chunk_index=chunk_index,
            checkpoint_revision=base_revision, to_status="COMPLETED",
        ).as_values()
    ], []
