"""Socle Core : gardes et verrous seuls, sans mutation ni lecture metier."""

from __future__ import annotations

import datetime
import hashlib

from django.db import DatabaseError, InterfaceError, connections
from django.utils.connection import ConnectionDoesNotExist

from pixs.core.authz.decision import Decision
from pixs.core.bootstrap_operator import BootstrapOperatorFacts
from pixs.core.services_bootstrap_facts import (
    BootstrapBindingError,
    check_request_binding,
    require_current_window,
)
from pixs.core.authz.policy import Effect, Obligation
from pixs.core.authz.ports import (
    AuthenticationContext,
    Clock,
    PortError,
    Request,
    RevocationStatus,
    TrustedFacts,
)
from pixs.core.dto import (
    CommandEnvelope,
    CoreInputInvalid,
    GovernanceAttestation,
)
from pixs.core.ports import (
    CorePortError,
    CoreServicePorts,
    BootstrapServicePorts,
    StagedRef,
    TransactionProof,
)
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure
from pixs.core.scope.ownership import OwnershipError, ResourceOwnership

__all__ = [
    "CoreServiceError",
    "utc_now",
    "check_request",
    "allow",
    "lock_scopes",
    "published_profile",
    "check_stage",
    "make_proof",
]

_FIXED_MESSAGE = "Garde Core refusee."
_MODULE_SEED = b"pixs-core-services-common-v1:"
_OWNER = "pixs.core"


class CoreServiceError(ValueError):
    def __init__(self, code: str = "CORE_GARDE_REFUSEE", *, facts=None, decision=None) -> None:
        super().__init__(_FIXED_MESSAGE)
        self.code = code
        self.element = "core_service"
        self.step = "garde"
        self.facts = facts
        self.decision = decision


def _is_id(v: object) -> bool:
    return type(v) is str and v != ""


def utc_now(clock: Clock) -> datetime.datetime:
    try:
        now = clock.now()
    except (PortError, CorePortError, CoreInputInvalid, DatabaseError, InterfaceError) as error:
        raise CoreServiceError("HORLOGE_ILLISIBLE") from error
    if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
        raise CoreServiceError("HORLOGE_NON_UTC") from None
    return now


def check_request(envelope: object, *, resource_id: str, action_id: str, correlation_id: str) -> Request:
    if type(envelope) is not CommandEnvelope:
        raise CoreServiceError("ENVELOPPE_INVALIDE") from None
    try:
        envelope.__post_init__()
    except CoreInputInvalid as error:
        raise CoreServiceError("ENVELOPPE_INVALIDE") from error
    request = object.__getattribute__(envelope, "request")
    if type(request) is not Request:
        raise CoreServiceError("REQUETE_INVALIDE") from None
    try:
        request.__post_init__()
    except PortError as error:
        raise CoreServiceError("REQUETE_INVALIDE") from error
    if not _is_id(resource_id) or not _is_id(action_id) or not _is_id(correlation_id):
        raise CoreServiceError("IDENTIFIANTS_INVALIDES") from None
    if object.__getattribute__(request, "resource_id") != resource_id:
        raise CoreServiceError("RESSOURCE_DIVERGENTE") from None
    if object.__getattribute__(request, "action_id") != action_id:
        raise CoreServiceError("ACTION_DIVERGENTE") from None
    if object.__getattribute__(request, "correlation_id") != correlation_id:
        raise CoreServiceError("CORRELATION_DIVERGENTE") from None
    return request


def allow(ports: object, request: object, *, under_locks: bool, alias: str, operation_id: str, _facts_source=None) -> tuple[TrustedFacts | BootstrapOperatorFacts, Decision]:
    if type(ports) not in (CoreServicePorts, BootstrapServicePorts) or type(under_locks) is not bool:
        raise CoreServiceError("PORTS_INVALIDES") from None
    if type(ports) is CoreServicePorts and _facts_source is not None:
        raise CoreServiceError("SOURCE_INTERDITE") from None
    if type(ports) is BootstrapServicePorts and not callable(_facts_source):
        raise CoreServiceError("SOURCE_MANQUANTE") from None
    try:
        type(ports).__post_init__(ports)
    except CorePortError as error:
        raise CoreServiceError("PORTS_INVALIDES") from error
    if type(request) is not Request:
        raise CoreServiceError("REQUETE_INVALIDE") from None
    try:
        Request.__post_init__(request)
        validate_structure(request.context)
    except (PortError, ScopeStructureError) as error:
        raise CoreServiceError("REQUETE_INVALIDE") from error
    if type(alias) is not str or alias == "":
        raise CoreServiceError("ALIAS_INVALIDE") from None
    if not _is_id(operation_id):
        raise CoreServiceError("OPERATION_INVALIDE") from None
    if under_locks is True and type(ports) is CoreServicePorts:
        prepare = getattr(ports.decider, "prepare_core_under_locks", None)
        if callable(prepare):
            try:
                prepare(request, alias=alias, operation_id=operation_id)
            except (PortError, CorePortError, CoreInputInvalid, DatabaseError, InterfaceError) as error:
                raise CoreServiceError("DECISION_ILLISIBLE") from error
    try:
        facts = ports.facts_provider.resolve(request) if type(ports) is CoreServicePorts else _facts_source(request)
    except (PortError, CorePortError, CoreInputInvalid, DatabaseError, InterfaceError) as error:
        raise CoreServiceError("FAITS_ILLISIBLES") from error
    if type(facts) is BootstrapOperatorFacts:
        if type(ports) is not BootstrapServicePorts:
            raise CoreServiceError("FAITS_INVALIDES") from None
        try:
            check_request_binding(facts, request, operation_id=operation_id)
            require_current_window(facts, utc_now(ports.clock))
        except BootstrapBindingError as error:
            raise CoreServiceError("FAITS_INVALIDES") from error
    else:
        if type(facts) is not TrustedFacts:
            raise CoreServiceError("FAITS_INVALIDES") from None
        try:
            facts.__post_init__()
            object.__getattribute__(facts, "auth").__post_init__()
            object.__getattribute__(facts, "ownership").__post_init__()
        except (PortError, OwnershipError) as error:
            raise CoreServiceError("FAITS_INVALIDES") from error
        auth = object.__getattribute__(facts, "auth")
        own = object.__getattribute__(facts, "ownership")
        if type(auth) is not AuthenticationContext or type(own) is not ResourceOwnership:
            raise CoreServiceError("FAITS_INVALIDES") from None
        for context in (facts.context, auth.context, own.context):
            try:
                validate_structure(context)
            except ScopeStructureError as error:
                raise CoreServiceError("CONTEXTE_INVALIDE") from error
        if object.__getattribute__(facts, "subject_id") != object.__getattribute__(request, "subject_id"):
            raise CoreServiceError("SUJET_DIVERGENT") from None
        if object.__getattribute__(auth, "digital_identity_id") != object.__getattribute__(request, "subject_id"):
            raise CoreServiceError("SUJET_DIVERGENT") from None
        if object.__getattribute__(facts, "resource_id") != object.__getattribute__(request, "resource_id"):
            raise CoreServiceError("RESSOURCE_DIVERGENTE") from None
        if object.__getattribute__(own, "resource_id") != object.__getattribute__(request, "resource_id"):
            raise CoreServiceError("RESSOURCE_DIVERGENTE") from None
        if object.__getattribute__(facts, "action_id") != object.__getattribute__(request, "action_id"):
            raise CoreServiceError("ACTION_DIVERGENTE") from None
        if object.__getattribute__(facts, "context") != object.__getattribute__(request, "context"):
            raise CoreServiceError("CONTEXTE_DIVERGENT") from None
        if object.__getattribute__(auth, "context") != object.__getattribute__(request, "context"):
            raise CoreServiceError("CONTEXTE_DIVERGENT") from None
        if object.__getattribute__(own, "context") != object.__getattribute__(request, "context"):
            raise CoreServiceError("CONTEXTE_DIVERGENT") from None
        if object.__getattribute__(facts, "revocation_status") is not RevocationStatus.ACTIVE:
            raise CoreServiceError("REVOCATION_NON_ACTIVE") from None
        now = utc_now(ports.clock)
        auth_time = object.__getattribute__(auth, "authentication_time")
        auth_exp = object.__getattribute__(auth, "expires_at")
        if not (type(auth_time) is datetime.datetime and auth_time.tzinfo is datetime.timezone.utc):
            raise CoreServiceError("FRAICHEUR_INVALIDE") from None
        if not (type(auth_exp) is datetime.datetime and auth_exp.tzinfo is datetime.timezone.utc):
            raise CoreServiceError("FRAICHEUR_INVALIDE") from None
        if not (auth_time <= now < auth_exp):
            raise CoreServiceError("FRAICHEUR_EXPIREE") from None
    try:
        if under_locks is True:
            decision = ports.decider.revalidate_under_locks(request, alias=alias, operation_id=operation_id)
        else:
            decision = ports.decider.decide(request)
    except (PortError, CorePortError, CoreInputInvalid, DatabaseError, InterfaceError) as error:
        raise CoreServiceError("DECISION_ILLISIBLE") from error
    if type(decision) is not Decision:
        raise CoreServiceError("DECISION_INVALIDE") from None
    now = utc_now(ports.clock)
    if object.__getattribute__(decision, "effect") is Effect.DENY:
        raise CoreServiceError("DECISION_REFUSEE", facts=facts, decision=decision) from None
    if object.__getattribute__(decision, "effect") is not Effect.ALLOW:
        raise CoreServiceError("DECISION_INVALIDE") from None
    if type(decision.reason_code) is not str or decision.reason_code != "ALLOWED":
        raise CoreServiceError("DECISION_INVALIDE") from None
    if not _is_id(decision.decision_id) or decision.decision_id != request.decision_id:
        raise CoreServiceError("DECISION_DIVERGENTE") from None
    version = object.__getattribute__(decision, "policy_version")
    if type(version) is not tuple or len(version) != 2:
        raise CoreServiceError("VERSION_INVALIDE") from None
    if type(version[0]) is not str or version[0] == "":
        raise CoreServiceError("VERSION_INVALIDE") from None
    if type(version[1]) is not tuple or any(type(p) is not tuple or len(p) != 2 or type(p[0]) is not str or type(p[1]) is not str or p[0] == "" or p[1] == "" for p in version[1]):
        raise CoreServiceError("VERSION_INVALIDE") from None
    evaluated = object.__getattribute__(decision, "evaluated_at")
    expires = object.__getattribute__(decision, "expires_at")
    if type(evaluated) is not datetime.datetime or evaluated.tzinfo is not datetime.timezone.utc:
        raise CoreServiceError("DECISION_EXPIREE") from None
    if type(expires) is not datetime.datetime or expires.tzinfo is not datetime.timezone.utc:
        raise CoreServiceError("DECISION_EXPIREE") from None
    if not (evaluated <= now < expires):
        raise CoreServiceError("DECISION_EXPIREE") from None
    obligations = object.__getattribute__(decision, "obligations")
    if type(obligations) is not tuple:
        raise CoreServiceError("OBLIGATION_INVALIDE") from None
    for obligation in obligations:
        if type(obligation) is not Obligation or type(obligation.kind) is not str or obligation.kind != "AUDIT":
            raise CoreServiceError("OBLIGATION_INVALIDE") from None
    return (facts, decision)


def _connection(alias: object):
    if type(alias) is not str or alias == "":
        raise CoreServiceError("ALIAS_INVALIDE") from None
    try:
        conn = connections[alias]
    except ConnectionDoesNotExist as error:
        raise CoreServiceError("ALIAS_INCONNU") from error
    if conn.vendor != "postgresql":
        raise CoreServiceError("MOTEUR_NON_PG_REFUSE") from None
    if conn.in_atomic_block is not True:
        raise CoreServiceError("HORS_TRANSACTION") from None
    return conn


def _validate_scope_token(token: object) -> None:
    if type(token) is not str or token == "" or ":" not in token:
        raise CoreServiceError("SCOPE_INVALIDE") from None
    head, _, tail = token.partition(":")
    if head == "" or tail == "":
        raise CoreServiceError("SCOPE_INVALIDE") from None
    if head == "uuid":
        if len(tail) != 32 or any(c not in "0123456789abcdef" for c in tail):
            raise CoreServiceError("SCOPE_INVALIDE") from None


def lock_scopes(alias: str, scopes: tuple[str, ...], *, shared: bool = False) -> None:
    if type(scopes) is not tuple or len(scopes) == 0:
        raise CoreServiceError("SCOPES_INVALIDES") from None
    if type(shared) is not bool:
        raise CoreServiceError("SCOPES_INVALIDES") from None
    for scope in scopes:
        _validate_scope_token(scope)
    conn = _connection(alias)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_schema();")
            row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_schemas(false);")
            paths = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT oid FROM pg_database WHERE datname = current_database();")
            db_row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT oid FROM pg_namespace WHERE nspname = current_schema();")
            nsp_row = cursor.fetchone()
    except (DatabaseError, InterfaceError) as error:
        raise CoreServiceError("VERROU_INACQUIS") from error
    if row is None or type(row[0]) is not str or row[0] == "":
        raise CoreServiceError("NAMESPACE_INDETERMINE") from None
    if paths is None or type(paths[0]) is not list or len(paths[0]) != 1 or type(paths[0][0]) is not str or paths[0][0] != row[0]:
        raise CoreServiceError("NAMESPACE_AMBIGU") from None
    if db_row is None or type(db_row[0]) is not int:
        raise CoreServiceError("BASE_INDETERMINEE") from None
    if nsp_row is None or type(nsp_row[0]) is not int:
        raise CoreServiceError("NAMESPACE_INDETERMINE") from None
    prefix = _MODULE_SEED + str(db_row[0]).encode("ascii") + b":" + str(nsp_row[0]).encode("ascii") + b":"
    for scope in sorted(set(scopes)):
        key = int.from_bytes(hashlib.sha256(prefix + scope.encode("utf-8")).digest()[:8], "big", signed=True)
        try:
            with conn.cursor() as cursor:
                if shared is True:
                    cursor.execute("SELECT pg_try_advisory_xact_lock_shared(%s);", [key])
                else:
                    cursor.execute("SELECT pg_try_advisory_xact_lock(%s);", [key])
                locked = cursor.fetchone()
        except (DatabaseError, InterfaceError) as error:
            raise CoreServiceError("VERROU_INACQUIS") from error
        if locked is None or locked[0] is not True:
            raise CoreServiceError("VERROU_CONCURRENT") from None


def published_profile(ports: object, request: Request, decision: Decision, *, alias: str, operation_id: str, token: str) -> tuple[GovernanceAttestation | None, bool, bool]:
    if type(ports) not in (CoreServicePorts, BootstrapServicePorts):
        raise CoreServiceError("PORTS_INVALIDES") from None
    if type(request) is not Request or type(decision) is not Decision:
        raise CoreServiceError("ENTREES_INVALIDES") from None
    if not _is_id(alias) or not _is_id(operation_id) or not _is_id(token):
        raise CoreServiceError("IDENTIFIANTS_INVALIDES") from None
    try:
        audit_waived = ports.decider.audit_waived(request, decision, alias=alias, operation_id=operation_id)
        governance_waived = ports.decider.governance_waived(request, decision, alias=alias, operation_id=operation_id)
    except (PortError, CorePortError, CoreInputInvalid, DatabaseError, InterfaceError) as error:
        raise CoreServiceError("DEROGATION_ILLISIBLE") from error
    if type(audit_waived) is not bool or type(governance_waived) is not bool:
        raise CoreServiceError("DEROGATION_INVALIDE") from None
    if object.__getattribute__(ports, "audit") is None and audit_waived is not True:
        raise CoreServiceError("AUDIT_ABSENT") from None
    if governance_waived is True:
        return (None, audit_waived, True)
    provider = object.__getattribute__(ports, "governance")
    if provider is None:
        raise CoreServiceError("GOUVERNANCE_ABSENTE") from None
    try:
        attestation = provider.attest(request, alias=alias, operation_id=operation_id, transaction_token=token)
    except (PortError, CorePortError, CoreInputInvalid, DatabaseError, InterfaceError) as error:
        raise CoreServiceError("ATTESTATION_ILLISIBLE") from error
    if type(attestation) is not GovernanceAttestation:
        raise CoreServiceError("ATTESTATION_INVALIDE") from None
    try:
        attestation.__post_init__()
    except CoreInputInvalid as error:
        raise CoreServiceError("ATTESTATION_INVALIDE") from error
    if object.__getattribute__(object.__getattribute__(attestation, "profile"), "owner_component") != _OWNER:
        raise CoreServiceError("ATTESTATION_INVALIDE") from None
    if object.__getattribute__(attestation, "context") != object.__getattribute__(request, "context"):
        raise CoreServiceError("ATTESTATION_DIVERGENTE") from None
    if object.__getattribute__(request, "resource_id") not in object.__getattribute__(attestation, "resource_refs"):
        raise CoreServiceError("ATTESTATION_DIVERGENTE") from None
    now = utc_now(ports.clock)
    if object.__getattribute__(attestation, "attested_at") > now:
        raise CoreServiceError("ATTESTATION_FUTURE") from None
    return (attestation, audit_waived, False)


def check_stage(ref: object, envelope: CommandEnvelope, *, alias: str, token: str) -> StagedRef:
    if type(ref) is not StagedRef:
        raise CoreServiceError("STAGE_INVALIDE") from None
    if type(envelope) is not CommandEnvelope:
        raise CoreServiceError("ENVELOPPE_INVALIDE") from None
    if not _is_id(alias) or not _is_id(token):
        raise CoreServiceError("IDENTIFIANTS_INVALIDES") from None
    try:
        ref.__post_init__()
    except CorePortError as error:
        raise CoreServiceError("STAGE_INVALIDE") from error
    if object.__getattribute__(ref, "operation_id") != object.__getattribute__(envelope, "operation_id"):
        raise CoreServiceError("STAGE_DIVERGENT") from None
    if object.__getattribute__(ref, "alias") != alias:
        raise CoreServiceError("STAGE_DIVERGENT") from None
    if object.__getattribute__(ref, "transaction_token") != token:
        raise CoreServiceError("STAGE_DIVERGENT") from None
    if object.__getattribute__(ref, "context") != object.__getattribute__(envelope.request, "context"):
        raise CoreServiceError("STAGE_DIVERGENT") from None
    return ref


def make_proof(envelope: CommandEnvelope, *, alias: str, token: str, stages: tuple[StagedRef, ...], now: datetime.datetime) -> TransactionProof:
    if type(envelope) is not CommandEnvelope:
        raise CoreServiceError("ENVELOPPE_INVALIDE") from None
    if not _is_id(alias) or not _is_id(token):
        raise CoreServiceError("IDENTIFIANTS_INVALIDES") from None
    if type(stages) is not tuple or len(stages) == 0 or any(type(s) is not StagedRef for s in stages):
        raise CoreServiceError("STAGES_INVALIDES") from None
    if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
        raise CoreServiceError("INSTANT_INVALIDE") from None
    return TransactionProof(object.__getattribute__(envelope, "operation_id"), alias, token, object.__getattribute__(envelope.request, "context"), stages, now)
