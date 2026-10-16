"""Orchestration VALIDATE IMPORT VALIDATE_ONLY en parcours qualifié unique.

Module purement mémoire à l'import : sans ORM, Django, psycopg, fichier,
réseau, processus, environnement, route, worker, upload, sérialisation
globale, import dynamique, secret, aléa, configuration automatique ni
état global mutable. Les accès Django et PostgreSQL sont importés en
lazy dans les fonctions, après les gardes pures. Les diagnostics sont
VALIDATE statiques, triés et dédupliqués, sans valeur fournie ni
exception brute.

Convention serveur du port de commande du propriétaire, documentée ici
sans jamais invoquer ``execute`` ni ``canonical_bytes`` :
``validate(server_context, entry, references)`` en positionnels, une
fois par unité réelle, où ``entry`` est un dict exact ``line_index`` int
et ``values`` dict, et ``references`` le tuple exact ``(operation_id,
owner_reference, mapping_reference, mapping_version)``. Avant chaque
transfert, l'autorité EXECUTE et la gouvernance effective sont
revalidées par callback serveur pure ; un seul contrôle avant la boucle
ne suffit pas pour N await. La réponse est un dict exact ``accepted``
bool et ``diagnostics`` tuple de dicts RowDiagnosticV1, contrôlée par
CommandValidationV1 sous les catalogues déclarés du propriétaire. Chaque
verdict valide incrémente ``validated_rows``, y compris rejeté ; un
verdict ``accepted`` faux incrémente aussi ``invalid_rows`` de cette
unité une fois ; un diagnostic portant une ligne étrangère à l'unité
refuse sans normalisation.

Séquence : paramètres primitifs exacts puis ObjectMetadataV1 profond
copié en snapshot avant tout await, dépôts réels PostgreSQL même alias
et vendeur réel, autorité EXECUTE avant toute lecture observable,
exécution et liaison VALIDATE relues au persistant, mapping résolu
recroisé au format et à la variante, gouvernance effective avant
données, parser interne, bail pris par ``acquire_lease``, normalisation
STAGED vers VALIDATING sous bail et unité protégée avant tout travail
asynchrone, parcours storage qualifié unique avec intégrité positive et
fermeture réussie avant tout ``owner.validate``, boucle bornée de
verdicts par unité, puis persistance finale unique (rapport, checkpoint
Nfinal+1, transition Nfinal+2) dans un seul bloc synchrone sous
``protected_unit`` réel, même thread et même transaction, avec horloge
et Event relus dans le bloc.

Bornes effectives : min(deadline, expires objet, expires opération,
bail, acquire+max_runtime) sans étendre aucune limite. Aucune
transaction ne reste ouverte à travers un ``await``. La révision lue à
l'entrée est conservée telle quelle ; aucun rebasage sur mise à jour
concurrente après I/O. Toute annulation, expiration ou perte de bail
refuse sans persistance forcée, sans fausse terminalité et sans faux
succès. Les unités refusées parser sont examinées invalides ; un total
inconnu après parsing interrompu reste None avec committed_unit_index
entier réel séparé, rapport incomplet FAILED sous gardes, jamais de
faux total ni diagnostic fabriqué. Aucune capacité d'obligation n'est
implémentée : des obligations non vides refusent au lieu d'être
prétendues appliquées.
"""

from __future__ import annotations

import asyncio
import inspect
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from asgiref.sync import sync_to_async

from pixs.backend.bulk_execution_values import (
    validate_bulk_policy_values,
    validate_bulk_progress_values,
)
from pixs.backend.bulk_object_staging import validate_object_metadata_values
from pixs.backend.bulk_private_object_reader import (
    _ServerCancelled,
    _prepare_qualified_import_units,
    _run_with_event,
)
from pixs.backend.bulk_runtime_contracts import (
    _catalog_state,
    validate_command_validation_values,
    validate_row_diagnostic_values,
)
from pixs.backend.bulk_streaming_import import _CONTENT_CODES, new_bulk_import_parser
from pixs.backend.bulk_trusted_ports import (
    _BulkTrustedPorts,
    _OwnerDeclarationSnapshot,
    _capture_python_method,
    validate_owner_command_contract,
)
from pixs.backend.bulk_validation_report_values import (
    validate_bulk_validation_report_values,
)
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from pixs.kernel.manifest.semver import parse_version

_SCOPE = "bulk_import_validate"

_OPAQUE_RULE = "référence opaque str exacte non vide UTF-8 sans NUL attendue"
_UTC_RULE = "datetime exact aware UTC attendu"
_EVENT_RULE = "asyncio.Event exact attendu"
_REVISION_RULE = "révision int exacte supérieure ou égale à un attendue"
_TRUSTED_RULE = "ports de confiance serveur exacts attendus"
_REPOSITORY_RULE = "BulkRuntimeRepository réel exact attendu"
_REPORT_STORE_RULE = "BulkValidationReportRepository réel exact attendu"
_ALIAS_RULE = "même alias de base déclaré pour les deux dépôts attendu"
_VENDOR_RULE = "moteur PostgreSQL réel attendu avant tout SQL"
_METADATA_RULE = "ObjectMetadataV1 exact valide attendu"
_RESOLVER_RULE = "résolveur de qualification serveur exact attendu"
_MODE_RULE = "opération IMPORT VALIDATE_ONLY exacte attendue"
_STATUS_RULE = "opération STAGED ou VALIDATING non terminale attendue"
_CANCELLED_OP_RULE = "opération annulée côté serveur refuse avant persistance"
_BINDING_RULE = "liaison VALIDATE au Job serveur déclaré attendue"
_AUTHORITY_RULE = "autorité EXECUTE actuelle ALLOW attendue"
_GOVERNANCE_RULE = "gouvernance RESOLVED actuelle attendue"
_OBLIGATIONS_RULE = "obligations serveur non implémentées refusées sans prétention"
_MAPPING_RULE = "mapping IMPORT immuable versionné du propriétaire attendu"
_FORMAT_RULE = "format serveur CSV ou NDJSON recroisé au mapping attendu"
_OWNER_RULE = "déclaration propriétaire serveur exacte attendue"
_OWNER_CONTRACT_RULE = "port de commande propriétaire structuralement exact attendu"
_OWNER_CALL_RULE = "validate propriétaire async coopérative exacte attendue"
_OWNER_UNAVAILABLE_RULE = "propriétaire indisponible sans détail brut attendu"
_OWNER_VERDICT_RULE = "verdict propriétaire hors CommandValidationV1 refusé sans rapport"
_COOP_RULE = "capacité async coopérative exacte attendue"
_PARSER_RULE = "parseur IMPORT interne exact attendu avant tout parsing"
_EXAM_RULE = "examen cohérent prouvé avec bilan parser honnête attendu"
_COUNTER_RULE = "compteurs validés et rejetés exacts sans double compte attendus"
_REPORT_RULE = "rapport ValidationReportV1 exact borné attendu"
_LEASE_RULE = "bail pris sous CAS actuel attendu"
_CAS_RULE = "révision connue actuelle attendue sans rebasage concurrent"
_CONSTRAINT_RULE = "invariant de périmètre actuel attendu"
_TRANSITION_RULE = "transition matricielle réelle attendue"
_PERSIST_RULE = "persistance finale atomique sous unité protégée attendue"
_REPLAY_RULE = "rejeu ou second insert refusé sans écrasement"
_RESULT_RULE = "accès au résultat réautorisé sans fuite attendu"
_PROVIDER_RULE = "fournisseur indisponible sans détail brut attendu"
_CANCEL_RULE = "annulation serveur refuse avant résultat"
_EXPIRED_RULE = "échéance effective atteinte refuse avant résultat"

_PHASE = "VALIDATE"
_MODE = "VALIDATE_ONLY"
_BULK_TYPE = "IMPORT"
_ENTRY_STATUSES = frozenset({"STAGED", "VALIDATING"})
_TERMINAL_STATUSES = frozenset({"COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED", "CANCELLED", "EXPIRED"})
_REPORT_VERSION = "1.0.0"
_FORMATS = frozenset({"CSV", "NDJSON"})

_RUNTIME_METHODS = (
    "load_execution",
    "get_binding",
    "acquire_lease",
    "protected_unit",
    "commit_checkpoint",
    "apply_transition",
)


class _OrchestrationRefused(ValueError):
    """Refus interne portant seulement des diagnostics déjà construits."""

    def __init__(self, diagnostics: list[Diagnostic]):
        super().__init__("validation d'import refusée")
        self.diagnostics = list(diagnostics)


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(step=VALIDATE, element=f"{_SCOPE}.{field}", constraint=rule, message=rule)


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for item in refusals:
        unique[(item.element, item.constraint, item.message)] = item
    return [unique[key] for key in sorted(unique)]


def _is_opaque_text(value: object) -> bool:
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_utc_instant(value: object) -> bool:
    return type(value) is datetime and value.tzinfo is timezone.utc


def _is_revision(value: object) -> bool:
    return type(value) is int and value >= 1


@dataclass(frozen=True, slots=True)
class _GuardedTypes:
    """Classes d'exceptions réelles, chargées en lazy sans état global."""

    lease: type
    cas: type
    constraint: type
    transition: type
    store: type
    invalid: tuple
    integrity: type


def _load_guarded_types() -> _GuardedTypes:
    """Importe en lazy les exceptions réelles des dépôts."""
    from django.core.exceptions import ValidationError as DjangoValidationError
    from django.db import IntegrityError as DjangoIntegrityError

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
        invalid=(DjangoValidationError,),
        integrity=DjangoIntegrityError,
    )


def _load_repository_classes() -> tuple:
    """Importe en lazy les classes exactes des dépôts réels."""
    from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository
    from pixs.backend.bulk_validation_report_repository import (
        BulkValidationReportRepository,
    )

    return (BulkRuntimeRepository, BulkValidationReportRepository)


def _mapped_refusal(exc: Exception, field: str, guards: _GuardedTypes) -> Diagnostic:
    """Convertit une exception réelle en refus statique, sans écho."""
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
    if isinstance(exc, guards.invalid):
        return _refusal(field, _CONSTRAINT_RULE)
    if isinstance(exc, guards.integrity):
        return _refusal(field, _REPLAY_RULE)
    return _refusal(field, _PROVIDER_RULE)


async def _bridge(callable_object: object, field: str, guards: _GuardedTypes, *args: object, **kwargs: object) -> object:
    """Exécute un appel synchrone autonome, annulation externe propagée."""
    try:
        return await sync_to_async(callable_object, thread_sensitive=True)(*args, **kwargs)
    except asyncio.CancelledError:
        raise
    except _OrchestrationRefused:
        raise
    except Exception as exc:
        raise _OrchestrationRefused([_mapped_refusal(exc, field, guards)]) from None


def _capture_sync_method(component: object, name: str) -> object | None:
    """Capture une méthode synchrone exacte, sans I/O ni invocation."""
    captured = _capture_python_method(component, name)
    if captured is None:
        return None
    if inspect.iscoroutinefunction(captured):
        return None
    return captured


def _owned_limits(policy: object) -> dict:
    """Copie possédée des limites PolicyV1 déjà résolues côté serveur."""
    owned: dict = {}
    for key, value in tuple(dict(policy).items()):
        if type(value) is list:
            owned[key] = list(value)
        else:
            owned[key] = value
    return owned


def _check_postgres_vendor(alias: str) -> None:
    """Vérifie le vendeur PostgreSQL réel avant tout SQL, sans I/O."""
    try:
        from django.db import connections

        vendor = connections[alias].vendor
    except Exception:
        raise _OrchestrationRefused([_refusal("vendor", _VENDOR_RULE)]) from None
    if vendor != "postgresql":
        raise _OrchestrationRefused([_refusal("vendor", _VENDOR_RULE)])


@dataclass(frozen=True, slots=True)
class _ValidateOnlyOutcome:
    """Bilan terminal honnête, sans octets ni secret."""

    operation_id: str
    mode: str
    phase: str
    to_status: str
    report_id: int
    checkpoint_revision: int
    transition_revision: int
    total_rows: int | None
    validated_rows: int
    invalid_rows: int
    complete: bool
    source_fingerprint: str
    mapping_version: str
    obligations: tuple[str, ...]

    def as_values(self) -> dict:
        return {
            "operation_id": self.operation_id,
            "mode": self.mode,
            "phase": self.phase,
            "to_status": self.to_status,
            "report_id": self.report_id,
            "checkpoint_revision": self.checkpoint_revision,
            "transition_revision": self.transition_revision,
            "total_rows": self.total_rows,
            "validated_rows": self.validated_rows,
            "invalid_rows": self.invalid_rows,
            "complete": self.complete,
            "source_fingerprint": self.source_fingerprint,
            "mapping_version": self.mapping_version,
            "obligations": tuple(self.obligations),
        }


async def validate_import_only(
    *,
    trusted_ports: object,
    runtime_repository: object,
    report_repository: object,
    server_context: object,
    operation_id: object,
    job_id: object,
    owner_reference: object,
    lease_owner: object,
    expected_metadata: object,
    storage_resolver: object,
    deadline: object,
    now: object,
    cancel_event: object,
    expected_schedule_revision: object,
) -> tuple[_ValidateOnlyOutcome | None, list[Diagnostic]]:
    """Valide un import sans mutation sur parcours qualifié unique."""
    scratch: list = []
    try:
        return await _validate_import_only_owned(
            trusted_ports=trusted_ports,
            runtime_repository=runtime_repository,
            report_repository=report_repository,
            server_context=server_context,
            operation_id=operation_id,
            job_id=job_id,
            owner_reference=owner_reference,
            lease_owner=lease_owner,
            expected_metadata=expected_metadata,
            storage_resolver=storage_resolver,
            deadline=deadline,
            now=now,
            cancel_event=cancel_event,
            expected_schedule_revision=expected_schedule_revision,
            scratch=scratch,
        )
    except _OrchestrationRefused as failure:
        return None, _pack(list(failure.diagnostics))
    except asyncio.CancelledError:
        raise
    except Exception:
        return None, _pack([_refusal("provider", _PROVIDER_RULE)])
    finally:
        scratch.clear()


async def _validate_import_only_owned(
    *,
    trusted_ports: object,
    runtime_repository: object,
    report_repository: object,
    server_context: object,
    operation_id: object,
    job_id: object,
    owner_reference: object,
    lease_owner: object,
    expected_metadata: object,
    storage_resolver: object,
    deadline: object,
    now: object,
    cancel_event: object,
    expected_schedule_revision: object,
    scratch: list,
) -> tuple[_ValidateOnlyOutcome | None, list[Diagnostic]]:
    """Corps : gardes pures, lectures, examen, verdicts, persistance unique."""
    if type(trusted_ports) is not _BulkTrustedPorts:
        raise _OrchestrationRefused([_refusal("trusted_ports", _TRUSTED_RULE)])
    if server_context is None or type(server_context) is type:
        raise _OrchestrationRefused([_refusal("server_context", _TRUSTED_RULE)])
    for value in (operation_id, job_id, owner_reference, lease_owner):
        if not _is_opaque_text(value):
            raise _OrchestrationRefused([_refusal("references", _OPAQUE_RULE)])
    if type(expected_metadata) is not dict:
        raise _OrchestrationRefused([_refusal("expected_metadata", _METADATA_RULE)])
    if storage_resolver is None or type(storage_resolver) is type:
        raise _OrchestrationRefused([_refusal("storage_resolver", _RESOLVER_RULE)])
    if not _is_utc_instant(deadline) or not _is_utc_instant(now):
        raise _OrchestrationRefused([_refusal("deadline", _UTC_RULE)])
    if type(cancel_event) is not asyncio.Event:
        raise _OrchestrationRefused([_refusal("cancel_event", _EVENT_RULE)])
    if not _is_revision(expected_schedule_revision):
        raise _OrchestrationRefused([_refusal("expected_schedule_revision", _REVISION_RULE)])
    metadata_refusals = validate_object_metadata_values(dict(expected_metadata))
    if metadata_refusals:
        raise _OrchestrationRefused(list(metadata_refusals))
    contract = dict(expected_metadata)
    meta_expires = contract.get("expires_at")
    if not _is_utc_instant(meta_expires):
        raise _OrchestrationRefused([_refusal("expected_metadata", _METADATA_RULE)])

    runtime_class, report_class = _load_repository_classes()
    if type(runtime_repository) is not runtime_class:
        raise _OrchestrationRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
    if type(report_repository) is not report_class:
        raise _OrchestrationRefused([_refusal("report_repository", _REPORT_STORE_RULE)])
    try:
        runtime_alias = runtime_repository._using
        report_alias = report_repository._using
    except Exception:
        raise _OrchestrationRefused([_refusal("alias", _ALIAS_RULE)]) from None
    if type(runtime_alias) is not str or runtime_alias != report_alias:
        raise _OrchestrationRefused([_refusal("alias", _ALIAS_RULE)])
    _check_postgres_vendor(runtime_alias)
    methods: dict = {}
    for name in _RUNTIME_METHODS:
        captured = _capture_sync_method(runtime_repository, name)
        if captured is None:
            raise _OrchestrationRefused([_refusal("runtime_repository", _REPOSITORY_RULE)])
        methods[name] = captured
    insert_report = _capture_sync_method(report_repository, "insert_report")
    if insert_report is None:
        raise _OrchestrationRefused([_refusal("report_repository", _REPORT_STORE_RULE)])
    methods["insert_report"] = insert_report
    guards = _load_guarded_types()

    assessment, authority_refusals = trusted_ports.check_authority(
        server_context=server_context,
        action="EXECUTE",
        operation_reference=operation_id,
        resource_reference=None,
    )
    if assessment is None:
        raise _OrchestrationRefused(
            list(authority_refusals) or [_refusal("authority", _AUTHORITY_RULE)]
        )

    execution = await _bridge(methods["load_execution"], "execution", guards, operation_id=operation_id)
    if type(execution) is not dict:
        raise _OrchestrationRefused([_refusal("execution", _STATUS_RULE)])
    if execution.get("bulk_type") != _BULK_TYPE or execution.get("commit_mode") != _MODE:
        raise _OrchestrationRefused([_refusal("mode", _MODE_RULE)])
    entry_status = execution.get("status")
    if entry_status not in _ENTRY_STATUSES:
        raise _OrchestrationRefused([_refusal("status", _STATUS_RULE)])
    if execution.get("cancellation_requested") is not False:
        raise _OrchestrationRefused([_refusal("cancellation_requested", _CANCELLED_OP_RULE)])
    if validate_bulk_progress_values(execution.get("progress")):
        raise _OrchestrationRefused([_refusal("progress", _STATUS_RULE)])
    mapping_reference = execution.get("mapping_reference")
    mapping_version = execution.get("mapping_version")
    policy_reference = execution.get("policy_reference")
    policy_version = execution.get("policy_version")
    execution_format = execution.get("format")
    input_reference = execution.get("input_reference")
    if not _is_opaque_text(mapping_reference) or not _is_opaque_text(policy_reference):
        raise _OrchestrationRefused([_refusal("references", _OPAQUE_RULE)])
    try:
        parse_version(mapping_version)
        parse_version(policy_version)
    except Exception:
        raise _OrchestrationRefused([_refusal("references", _OPAQUE_RULE)]) from None
    if type(execution_format) is not str or execution_format not in _FORMATS:
        raise _OrchestrationRefused([_refusal("format", _FORMAT_RULE)])
    base_revision = execution.get("revision")
    if not _is_revision(base_revision):
        raise _OrchestrationRefused([_refusal("revision", _REVISION_RULE)])
    expires_at = execution.get("expires_at")
    if not _is_utc_instant(expires_at):
        raise _OrchestrationRefused([_refusal("expires_at", _UTC_RULE)])
    source_version = execution.get("input_version")
    if type(source_version) is not str and source_version is not None:
        raise _OrchestrationRefused([_refusal("input_version", _METADATA_RULE)])
    _cross_check_metadata(contract, execution)
    if cancel_event.is_set():
        raise _OrchestrationRefused([_refusal("cancel_event", _CANCEL_RULE)])
    if not datetime.now(timezone.utc) < min(deadline, meta_expires, expires_at):
        raise _OrchestrationRefused([_refusal("now", _EXPIRED_RULE)])

    binding = await _bridge(
        methods["get_binding"], "binding", guards, operation_id=operation_id, phase=_PHASE
    )
    if type(binding) is not dict or binding.get("job_id") != job_id:
        raise _OrchestrationRefused([_refusal("binding", _BINDING_RULE)])

    mapping_snapshot, mapping_refusals = trusted_ports.resolve_mapping(
        mapping_reference, mapping_version, owner_reference
    )
    if mapping_snapshot is None:
        raise _OrchestrationRefused(list(mapping_refusals) or [_refusal("mapping", _MAPPING_RULE)])
    if mapping_snapshot.variant != _BULK_TYPE or mapping_snapshot.owner_reference != owner_reference:
        raise _OrchestrationRefused([_refusal("mapping", _MAPPING_RULE)])
    if mapping_snapshot.format != execution_format:
        raise _OrchestrationRefused([_refusal("format", _FORMAT_RULE)])
    declaration = trusted_ports._owner_lookup.get(owner_reference)
    if type(declaration) is not _OwnerDeclarationSnapshot:
        raise _OrchestrationRefused([_refusal("owner", _OWNER_RULE)])

    policy_owned, _ = _resolve_effective_governance(
        trusted_ports=trusted_ports,
        server_context=server_context,
        assessment=assessment,
        mapping_snapshot=mapping_snapshot,
        policy_reference=policy_reference,
        policy_version=policy_version,
    )

    owner_adapter = trusted_ports._owner_command_port
    if owner_adapter is None:
        raise _OrchestrationRefused([_refusal("owner", _OWNER_UNAVAILABLE_RULE)])
    if validate_owner_command_contract(owner_adapter):
        raise _OrchestrationRefused([_refusal("owner", _OWNER_CONTRACT_RULE)])
    validate_fn = _capture_python_method(owner_adapter, "validate")
    if validate_fn is None or not inspect.iscoroutinefunction(validate_fn):
        raise _OrchestrationRefused([_refusal("owner.validate", _OWNER_CALL_RULE)])

    parser, parser_refusals = new_bulk_import_parser(
        mapping=mapping_snapshot.as_values(),
        policy=dict(policy_owned),
        declared_owner_fields=tuple(declaration.declared_fields),
        declared_codes=tuple(declaration.declared_codes),
    )
    if parser is None:
        raise _OrchestrationRefused(list(parser_refusals) or [_refusal("parser", _PARSER_RULE)])
    try:
        max_runtime = int(policy_owned["max_runtime_seconds"])
        max_diagnostics = int(policy_owned["max_diagnostics"])
    except Exception:
        raise _OrchestrationRefused([_refusal("policy", _GOVERNANCE_RULE)]) from None

    acquire_now = datetime.now(timezone.utc)
    lease_expires_at = await _bridge(
        methods["acquire_lease"],
        "lease",
        guards,
        operation_id=operation_id,
        job_id=job_id,
        phase=_PHASE,
        owner=lease_owner,
        policy=dict(policy_owned),
        now=acquire_now,
        expected_schedule_revision=expected_schedule_revision,
    )
    if not _is_utc_instant(lease_expires_at):
        raise _OrchestrationRefused([_refusal("lease", _LEASE_RULE)])
    acquire_mono = time.monotonic()
    acquire_deadline = acquire_now + timedelta(seconds=max_runtime)
    schedule_revision = expected_schedule_revision + 1
    effective = min(deadline, meta_expires, expires_at, lease_expires_at, acquire_deadline)
    if not acquire_now < effective or cancel_event.is_set():
        raise _OrchestrationRefused([_refusal("now", _EXPIRED_RULE)])

    base_revision = await _normalize_staged_under_lease(
        methods=methods,
        guards=guards,
        operation_id=operation_id,
        job_id=job_id,
        lease_owner=lease_owner,
        policy_owned=policy_owned,
        entry_status=entry_status,
        entry_revision=base_revision,
        schedule_revision=schedule_revision,
        deadline=deadline,
        meta_expires=meta_expires,
        expires_at=expires_at,
        lease_expires_at=lease_expires_at,
        acquire_deadline=acquire_deadline,
        cancel_event=cancel_event,
    )

    qualified, qualified_refusals = await _prepare_qualified_import_units(
        trusted_ports=trusted_ports,
        server_context=server_context,
        operation_reference=operation_id,
        expected_metadata=dict(contract),
        policy_reference=policy_reference,
        policy_version=policy_version,
        storage_resolver=storage_resolver,
        expected_policy=dict(policy_owned),
        parser=parser,
        deadline=effective,
        now=datetime.now(timezone.utc),
        cancel_event=cancel_event,
    )
    if qualified is None:
        raise _OrchestrationRefused(list(qualified_refusals))
    exam = _check_parser_exam(qualified, declaration, mapping_snapshot)

    def _ensure_current_transfer() -> None:
        live_assessment, live_refusals = trusted_ports.check_authority(
            server_context=server_context,
            action="EXECUTE",
            operation_reference=operation_id,
            resource_reference=input_reference,
        )
        if live_assessment is None:
            raise _OrchestrationRefused(
                list(live_refusals) or [_refusal("authority", _AUTHORITY_RULE)]
            )
        live_policy, _ = _resolve_effective_governance(
            trusted_ports=trusted_ports,
            server_context=server_context,
            assessment=live_assessment,
            mapping_snapshot=mapping_snapshot,
            policy_reference=policy_reference,
            policy_version=policy_version,
        )
        if live_policy != policy_owned:
            raise _OrchestrationRefused([_refusal("governance", _GOVERNANCE_RULE)])

    def _owner_remaining() -> float:
        current = datetime.now(timezone.utc)
        remaining_utc = (effective - current).total_seconds()
        remaining_mono = max_runtime - (time.monotonic() - acquire_mono)
        return remaining_utc if remaining_utc < remaining_mono else remaining_mono

    references = (operation_id, owner_reference, mapping_reference, mapping_version)
    owner_validated, owner_invalid, owner_diagnostics = await _validate_units_one_by_one(
        validate_fn=validate_fn,
        server_context=server_context,
        units=qualified.units,
        references=references,
        policy_owned=policy_owned,
        owner_codes=frozenset(tuple(declaration.declared_codes)),
        owner_fields=frozenset(tuple(declaration.declared_fields)),
        max_diagnostics=max_diagnostics,
        remaining_fn=_owner_remaining,
        cancel_event=cancel_event,
        effective=effective,
        transfer_guard=_ensure_current_transfer,
        scratch=scratch,
    )
    refused = exam["refused"]
    validated_rows = owner_validated + refused
    invalid_rows = owner_invalid + refused
    report_warnings = list(exam["warnings"])
    scratch.clear()

    complete = bool(exam["full"])
    total_rows = exam["emitted"] if complete else None
    to_status = "FAILED" if not complete else ("COMPLETED" if invalid_rows == 0 else "COMPLETED_WITH_ERRORS")
    report_values = _build_report_values(
        operation_id=operation_id,
        mapping_version=mapping_version,
        source_version=source_version,
        total_rows=total_rows,
        validated_rows=validated_rows,
        invalid_rows=invalid_rows,
        complete=complete,
        parser_warnings=report_warnings,
        owner_diagnostics=owner_diagnostics,
        max_diagnostics=max_diagnostics,
    )
    report_refusals = validate_bulk_validation_report_values(
        report_values,
        policy=dict(policy_owned),
        declared_codes=exam["report_codes"],
        declared_fields=exam["report_fields"],
    )
    if report_refusals:
        raise _OrchestrationRefused(list(report_refusals))

    fresh = await _bridge(methods["load_execution"], "execution", guards, operation_id=operation_id)
    if type(fresh) is not dict:
        raise _OrchestrationRefused([_refusal("execution", _REPLAY_RULE)])
    fresh_status = fresh.get("status")
    if fresh_status in _TERMINAL_STATUSES:
        raise _OrchestrationRefused([_refusal("status", _REPLAY_RULE)])
    if fresh_status not in _ENTRY_STATUSES:
        raise _OrchestrationRefused([_refusal("status", _STATUS_RULE)])
    if fresh.get("cancellation_requested") is not False:
        raise _OrchestrationRefused([_refusal("cancellation_requested", _CANCELLED_OP_RULE)])
    if fresh.get("revision") != base_revision:
        raise _OrchestrationRefused([_refusal("revision", _CAS_RULE)])
    if cancel_event.is_set() or not datetime.now(timezone.utc) < effective:
        raise _OrchestrationRefused([_refusal("now", _EXPIRED_RULE)])

    persisted = await _persist_final_block(
        methods=methods,
        guards=guards,
        operation_id=operation_id,
        job_id=job_id,
        lease_owner=lease_owner,
        policy_owned=policy_owned,
        base_revision=base_revision,
        schedule_revision=schedule_revision,
        report_values=report_values,
        report_codes=exam["report_codes"],
        report_fields=exam["report_fields"],
        source_fingerprint=qualified.sha256,
        mapping_version=mapping_version,
        committed_unit_index=validated_rows,
        progress=dict(report_values["progress"]),
        to_status=to_status,
        deadline=deadline,
        meta_expires=meta_expires,
        expires_at=expires_at,
        lease_expires_at=lease_expires_at,
        acquire_deadline=acquire_deadline,
        cancel_event=cancel_event,
    )
    report_id, checkpoint_revision, transition_revision = persisted

    read_assessment, read_refusals = trusted_ports.check_authority(
        server_context=server_context,
        action="READ_RESULT",
        operation_reference=operation_id,
        resource_reference=None,
    )
    if read_assessment is None:
        raise _OrchestrationRefused(
            list(read_refusals) or [_refusal("result", _RESULT_RULE)]
        )
    _resolve_effective_governance(
        trusted_ports=trusted_ports,
        server_context=server_context,
        assessment=read_assessment,
        mapping_snapshot=mapping_snapshot,
        policy_reference=policy_reference,
        policy_version=policy_version,
    )
    return _ValidateOnlyOutcome(
        operation_id=operation_id,
        mode=_MODE,
        phase=_PHASE,
        to_status=to_status,
        report_id=report_id,
        checkpoint_revision=checkpoint_revision,
        transition_revision=transition_revision,
        total_rows=total_rows,
        validated_rows=validated_rows,
        invalid_rows=invalid_rows,
        complete=complete,
        source_fingerprint=qualified.sha256,
        mapping_version=mapping_version,
        obligations=(),
    ), []


def _cross_check_metadata(contract: dict, execution: dict) -> None:
    """Recroise le snapshot aux entrées persistantes ; échéances bornées par min."""
    for field, key in (
        ("object_reference", "input_reference"),
        ("version_reference", "input_version"),
        ("sha256", "input_sha256"),
        ("size_bytes", "input_size_bytes"),
    ):
        persisted = execution.get(key)
        if persisted is None or contract.get(field) != persisted:
            raise _OrchestrationRefused([_refusal("expected_metadata", _METADATA_RULE)])


def _resolve_effective_governance(
    *,
    trusted_ports: object,
    server_context: object,
    assessment: object,
    mapping_snapshot: object,
    policy_reference: str,
    policy_version: str,
) -> tuple[dict, tuple]:
    """Résout la gouvernance effective ; obligations non vides refusées."""
    resolution, governance_refusals = trusted_ports.resolve_governance(
        server_context=server_context,
        authority_snapshot=assessment,
        governance_contract=mapping_snapshot.as_values(),
        governance_references=(policy_reference, policy_version),
    )
    if resolution is None:
        raise _OrchestrationRefused(
            list(governance_refusals) or [_refusal("governance", _GOVERNANCE_RULE)]
        )
    try:
        resolved_values = resolution.as_values()
        resolved_limits = dict(resolved_values["policy"]["limits"])
        obligations = resolved_values["obligations"]
    except Exception:
        raise _OrchestrationRefused([_refusal("governance", _GOVERNANCE_RULE)]) from None
    if resolved_values.get("decision") != "RESOLVED":
        raise _OrchestrationRefused([_refusal("governance", _GOVERNANCE_RULE)])
    if type(obligations) is not tuple or obligations != ():
        raise _OrchestrationRefused([_refusal("obligations", _OBLIGATIONS_RULE)])
    policy_owned = _owned_limits(resolved_limits)
    if validate_bulk_policy_values(dict(policy_owned)):
        raise _OrchestrationRefused([_refusal("policy", _GOVERNANCE_RULE)])
    return policy_owned, obligations


async def _normalize_staged_under_lease(
    *,
    methods: dict,
    guards: _GuardedTypes,
    operation_id: str,
    job_id: str,
    lease_owner: str,
    policy_owned: dict,
    entry_status: str,
    entry_revision: int,
    schedule_revision: int,
    deadline: datetime,
    meta_expires: datetime,
    expires_at: datetime,
    lease_expires_at: datetime,
    acquire_deadline: datetime,
    cancel_event: asyncio.Event,
) -> int:
    """Entre VALIDATING sous bail et unité protégée avant tout travail async."""
    if entry_status != "STAGED":
        return entry_revision

    def _normalize() -> int:
        with methods["protected_unit"](
            operation_id=operation_id,
            job_id=job_id,
            phase=_PHASE,
            owner=lease_owner,
            policy=dict(policy_owned),
            now=datetime.now(timezone.utc),
            expected_extension_revision=entry_revision,
            expected_schedule_revision=schedule_revision,
        ):
            inner_now = datetime.now(timezone.utc)
            if cancel_event.is_set():
                raise _OrchestrationRefused([_refusal("cancel_event", _CANCEL_RULE)])
            if not inner_now < min(deadline, meta_expires, expires_at, lease_expires_at, acquire_deadline):
                raise _OrchestrationRefused([_refusal("now", _EXPIRED_RULE)])
            return methods["apply_transition"](
                operation_id=operation_id,
                expected_revision=entry_revision,
                to_status="VALIDATING",
                now=inner_now,
            )

    normalized = await _bridge(_normalize, "transition", guards)
    if type(normalized) is not int:
        raise _OrchestrationRefused([_refusal("transition", _TRANSITION_RULE)])
    return normalized


def _check_parser_exam(
    qualified: object, declaration: object, mapping_snapshot: object
) -> dict:
    """Contrôle la cohérence du bilan parser ; diagnostics déjà dicts."""
    try:
        summary_values = qualified.parser_summary.as_values()
        units = tuple(qualified.units)
    except Exception:
        raise _OrchestrationRefused([_refusal("parser", _EXAM_RULE)]) from None
    if type(summary_values.get("complete")) is not bool:
        raise _OrchestrationRefused([_refusal("parser", _EXAM_RULE)])
    emitted = summary_values.get("units_emitted")
    refused = summary_values.get("units_refused")
    if type(emitted) is not int or type(refused) is not int or emitted < 0 or refused < 0:
        raise _OrchestrationRefused([_refusal("parser", _EXAM_RULE)])
    if emitted != len(units):
        raise _OrchestrationRefused([_refusal("parser", _EXAM_RULE)])
    raw_warnings = summary_values.get("diagnostics")
    if type(raw_warnings) is not tuple:
        raise _OrchestrationRefused([_refusal("parser", _EXAM_RULE)])
    report_codes, report_fields = _report_catalogues(declaration, mapping_snapshot)
    warnings: list = []
    for warning in raw_warnings:
        if type(warning) is not dict:
            raise _OrchestrationRefused([_refusal("parser", _EXAM_RULE)])
        owned_warning = {
            "code": warning.get("code"),
            "field_reference": warning.get("field_reference"),
            "line_index": warning.get("line_index"),
        }
        if validate_row_diagnostic_values(
            owned_warning, declared_codes=report_codes, declared_fields=report_fields
        ):
            raise _OrchestrationRefused([_refusal("parser", _EXAM_RULE)])
        warnings.append(owned_warning)
    full = bool(summary_values.get("complete")) and refused == 0
    try:
        owner_codes = frozenset(tuple(declaration.declared_codes))
        owner_fields = frozenset(tuple(declaration.declared_fields))
    except Exception:
        raise _OrchestrationRefused([_refusal("parser", _EXAM_RULE)]) from None
    return {
        "full": full,
        "emitted": emitted,
        "refused": refused,
        "warnings": warnings,
        "owner_codes": owner_codes,
        "owner_fields": owner_fields,
        "report_codes": report_codes,
        "report_fields": report_fields,
    }


def _report_catalogues(declaration: object, mapping_snapshot: object) -> tuple[frozenset, frozenset]:
    """Catalogues immuables déclarés : propriétaire, contenu et mapping."""
    try:
        owner_codes = frozenset(tuple(declaration.declared_codes))
        owner_fields = frozenset(tuple(declaration.declared_fields))
        mapping_values = mapping_snapshot.as_values()
        source_fields = frozenset(tuple(mapping_values["source_fields"]))
        target_fields = frozenset(tuple(mapping_values["target_fields"]))
    except Exception:
        raise _OrchestrationRefused([_refusal("catalogues", _REPORT_RULE)]) from None
    codes = owner_codes | _CONTENT_CODES
    fields = owner_fields | source_fields | target_fields
    checked_codes, code_refusals = _catalog_state(codes, _SCOPE, "declared_codes")
    checked_fields, field_refusals = _catalog_state(fields, _SCOPE, "declared_fields")
    if checked_codes is None or checked_fields is None:
        raise _OrchestrationRefused(
            _pack([*code_refusals, *field_refusals]) or [_refusal("catalogues", _REPORT_RULE)]
        )
    return checked_codes, checked_fields


async def _validate_units_one_by_one(
    *,
    validate_fn: object,
    server_context: object,
    units: tuple,
    references: tuple,
    policy_owned: dict,
    owner_codes: frozenset,
    owner_fields: frozenset,
    max_diagnostics: int,
    remaining_fn: object,
    cancel_event: asyncio.Event,
    effective: datetime,
    transfer_guard: object,
    scratch: list,
) -> tuple[int, int, list]:
    """Boucle bornée : un verdict CommandValidationV1 gardé par unité réelle."""
    validated_rows = 0
    invalid_rows = 0
    accumulated: list = []
    try:
        for unit in units:
            if len(accumulated) >= max_diagnostics:
                raise _OrchestrationRefused(
                    [
                        Diagnostic(
                            step=VALIDATE,
                            element=f"{_SCOPE}.owner.validate",
                            constraint="limite de diagnostics atteinte ; examen incomplet",
                            message="limite de diagnostics atteinte ; examen incomplet",
                        )
                    ]
                )
            if cancel_event.is_set():
                raise _OrchestrationRefused([_refusal("cancel_event", _CANCEL_RULE)])
            if not datetime.now(timezone.utc) < effective:
                raise _OrchestrationRefused([_refusal("owner.validate", _EXPIRED_RULE)])
            transfer_guard()
            line_index = getattr(unit, "line_index", None)
            if type(line_index) is not int:
                raise _OrchestrationRefused([_refusal("units", _EXAM_RULE)])
            try:
                mapped = unit.as_values()
            except Exception:
                raise _OrchestrationRefused([_refusal("units", _EXAM_RULE)]) from None
            if type(mapped) is not dict:
                raise _OrchestrationRefused([_refusal("units", _EXAM_RULE)])
            entry = {"line_index": line_index, "values": mapped}
            try:
                verdict = await _run_with_event(
                    lambda: validate_fn(server_context, entry, references),
                    remaining_fn=remaining_fn,
                    cancel_event=cancel_event,
                )
            except _ServerCancelled:
                raise _OrchestrationRefused([_refusal("cancel_event", _CANCEL_RULE)]) from None
            except asyncio.TimeoutError:
                raise _OrchestrationRefused([_refusal("owner.validate", _EXPIRED_RULE)]) from None
            except asyncio.CancelledError:
                raise
            except Exception:
                raise _OrchestrationRefused(
                    [_refusal("owner.validate", _OWNER_UNAVAILABLE_RULE)]
                ) from None
            if type(verdict) is not dict:
                raise _OrchestrationRefused([_refusal("owner.validate", _OWNER_VERDICT_RULE)])
            command_refusals = validate_command_validation_values(
                verdict,
                policy=dict(policy_owned),
                declared_codes=owner_codes,
                declared_fields=owner_fields,
            )
            if command_refusals:
                raise _OrchestrationRefused([_refusal("owner.validate", _OWNER_VERDICT_RULE)])
            validated_rows += 1
            if verdict["accepted"] is not True:
                invalid_rows += 1
            for item in tuple(verdict["diagnostics"]):
                owned_item = {
                    "code": item.get("code"),
                    "field_reference": item.get("field_reference"),
                    "line_index": item.get("line_index"),
                }
                foreign = owned_item["line_index"]
                if foreign is not None and foreign != line_index:
                    raise _OrchestrationRefused([_refusal("owner.validate", _OWNER_VERDICT_RULE)])
                accumulated.append(owned_item)
                scratch.append(owned_item)
            if len(accumulated) > max_diagnostics:
                raise _OrchestrationRefused([_refusal("owner.validate", _REPORT_RULE)])
        return validated_rows, invalid_rows, accumulated
    finally:
        scratch.clear()


def _build_report_values(
    *,
    operation_id: str,
    mapping_version: str,
    source_version: object,
    total_rows: int | None,
    validated_rows: int,
    invalid_rows: int,
    complete: bool,
    parser_warnings: list,
    owner_diagnostics: list,
    max_diagnostics: int,
) -> dict:
    """Construit le rapport exact, diagnostics réels dédupliqués et bornés."""
    seen: set = set()
    ordered: list = []
    for item in (*parser_warnings, *owner_diagnostics):
        key = (item.get("code"), item.get("field_reference"), item.get("line_index"))
        if key in seen:
            continue
        seen.add(key)
        ordered.append(
            {
                "code": item.get("code"),
                "field_reference": item.get("field_reference"),
                "line_index": item.get("line_index"),
            }
        )
    if len(ordered) > max_diagnostics:
        raise _OrchestrationRefused([_refusal("report", _REPORT_RULE)])
    if type(source_version) is not str and source_version is not None:
        raise _OrchestrationRefused([_refusal("report", _REPORT_RULE)])
    return {
        "report_version": _REPORT_VERSION,
        "operation_id": operation_id,
        "mode": _MODE,
        "progress": {
            "total_rows": total_rows,
            "validated_rows": validated_rows,
            "invalid_rows": invalid_rows,
            "applied_rows": 0,
            "execution_rejected_rows": 0,
            "exported_rows": 0,
        },
        "diagnostics": tuple(ordered),
        "complete": complete,
        "source_version": source_version,
        "mapping_version": mapping_version,
    }


async def _persist_final_block(
    *,
    methods: dict,
    guards: _GuardedTypes,
    operation_id: str,
    job_id: str,
    lease_owner: str,
    policy_owned: dict,
    base_revision: int,
    schedule_revision: int,
    report_values: dict,
    report_codes: frozenset,
    report_fields: frozenset,
    source_fingerprint: str,
    mapping_version: str,
    committed_unit_index: int,
    progress: dict,
    to_status: str,
    deadline: datetime,
    meta_expires: datetime,
    expires_at: datetime,
    lease_expires_at: datetime,
    acquire_deadline: datetime,
    cancel_event: asyncio.Event,
) -> tuple:
    """Bloc synchrone unique : rapport, checkpoint Nfinal+1, transition Nfinal+2."""

    def _final() -> tuple:
        with methods["protected_unit"](
            operation_id=operation_id,
            job_id=job_id,
            phase=_PHASE,
            owner=lease_owner,
            policy=dict(policy_owned),
            now=datetime.now(timezone.utc),
            expected_extension_revision=base_revision,
            expected_schedule_revision=schedule_revision,
        ) as unit:
            if unit is None:
                raise _OrchestrationRefused([_refusal("persist", _PERSIST_RULE)])
            inner_now = datetime.now(timezone.utc)
            inner_effective = min(deadline, meta_expires, expires_at, lease_expires_at, acquire_deadline)
            if cancel_event.is_set():
                raise _OrchestrationRefused([_refusal("cancel_event", _CANCEL_RULE)])
            if not inner_now < inner_effective:
                raise _OrchestrationRefused([_refusal("now", _EXPIRED_RULE)])
            unit.now = inner_now
            report_id = methods["insert_report"](
                values=dict(report_values),
                policy=dict(policy_owned),
                declared_codes=report_codes,
                declared_fields=report_fields,
            )
            checkpoint_revision = methods["commit_checkpoint"](
                unit,
                {
                    "checkpoint_id": f"validate-only:{operation_id}:{base_revision + 1}:{source_fingerprint}",
                    "operation_id": operation_id,
                    "phase": _PHASE,
                    "source_fingerprint": source_fingerprint,
                    "mapping_version": mapping_version,
                    "committed_unit_index": committed_unit_index,
                    "progress": dict(progress),
                    "revision": base_revision + 1,
                    "owner_result_reference": None,
                },
            )
            transition_now = datetime.now(timezone.utc)
            if cancel_event.is_set() or not transition_now < inner_effective:
                raise _OrchestrationRefused([_refusal("now", _EXPIRED_RULE)])
            if not unit.now < inner_effective:
                raise _OrchestrationRefused([_refusal("now", _EXPIRED_RULE)])
            transition_revision = methods["apply_transition"](
                operation_id=operation_id,
                expected_revision=checkpoint_revision,
                to_status=to_status,
                now=transition_now,
            )
            if type(report_id) is not int or type(checkpoint_revision) is not int:
                raise _OrchestrationRefused([_refusal("persist", _PERSIST_RULE)])
            if type(transition_revision) is not int:
                raise _OrchestrationRefused([_refusal("persist", _PERSIST_RULE)])
            return (report_id, checkpoint_revision, transition_revision)

    try:
        return await sync_to_async(_final, thread_sensitive=True)()
    except asyncio.CancelledError:
        raise
    except _OrchestrationRefused:
        raise
    except Exception as exc:
        raise _OrchestrationRefused([_mapped_refusal(exc, "persist", guards)]) from None
