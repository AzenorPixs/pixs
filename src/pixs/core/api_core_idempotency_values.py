"""Valeurs pures d'idempotence Core C06 : cle et entree fermees, sans ORM ni commit."""

from __future__ import annotations

import datetime
from dataclasses import dataclass

from pixs.core.api_core_serializer_v1 import API_CORE_COMMAND_TYPES, API_CORE_SERIALIZER_VERSION
from pixs.core.dto import CoreInputInvalid, CoreMutationResult
from pixs.core.scope.context import ScopeContext, ScopeStructureError, ScopeType, validate_structure
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "ApiCoreIdempotencyConflict",
    "ApiCoreIdempotencyUnknown",
    "ApiCoreIdempotencyProofInvalid",
    "ApiCoreIdempotencyConfig",
    "ApiCoreIdempotencyKey",
    "ApiCoreIdempotencyEntry",
    "resolve_idempotency_key",
    "validate_idempotency_entry",
]


class ApiCoreIdempotencyConflict(ValueError):
    code = "IDEMPOTENCE_CONFLIT"

    def __init__(self) -> None:
        super().__init__("Conflit d'idempotence Core.")


class ApiCoreIdempotencyUnknown(ValueError):
    code = "IDEMPOTENCE_ISSUE_INCONNUE"

    def __init__(self) -> None:
        super().__init__("Issue d'idempotence Core inconnue.")


class ApiCoreIdempotencyProofInvalid(ValueError):
    code = "IDEMPOTENCE_PREUVE_INVALIDE"

    def __init__(self) -> None:
        super().__init__("Preuve d'idempotence Core invalide.")


def _fail_proof() -> None:
    raise ApiCoreIdempotencyProofInvalid()


def _opaque(v: object, bound: int) -> str:
    if type(bound) is not int or type(v) is not str or v == "" or len(v) > bound or "\x00" in v:
        _fail_proof()
    try:
        v.encode("utf-8")
    except UnicodeError:
        _fail_proof()
    return v


def _utc(v: object) -> datetime.datetime:
    if type(v) is not datetime.datetime or v.tzinfo is not datetime.timezone.utc:
        _fail_proof()
    return v


@dataclass(frozen=True, slots=True, repr=False)
class ApiCoreIdempotencyConfig:
    replay_window_seconds: int
    max_tenant_chars: int
    max_scope_chars: int
    max_subject_chars: int
    max_command_type_chars: int
    max_key_chars: int

    def __post_init__(self) -> None:
        for name in (
            "replay_window_seconds", "max_tenant_chars", "max_scope_chars",
            "max_subject_chars", "max_command_type_chars", "max_key_chars",
        ):
            value = object.__getattribute__(self, name)
            if type(value) is not int or value < 1:
                _fail_proof()
        try:
            datetime.timedelta(seconds=self.replay_window_seconds)
        except OverflowError:
            _fail_proof()


@dataclass(frozen=True, slots=True, repr=False)
class ApiCoreIdempotencyKey:
    namespace: str
    tenant_id: str | None
    subject_id: str
    command_type: str
    idempotency_key: str

    def __post_init__(self) -> None:
        namespace = object.__getattribute__(self, "namespace")
        tenant = object.__getattribute__(self, "tenant_id")
        if type(namespace) is not str or namespace not in ("PLATFORM", "TENANT"):
            _fail_proof()
        if namespace == "PLATFORM":
            if tenant is not None:
                _fail_proof()
        elif type(tenant) is not str or not tenant:
            _fail_proof()
        for name in ("subject_id", "command_type", "idempotency_key"):
            value = object.__getattribute__(self, name)
            if type(value) is not str or not value or "\x00" in value:
                _fail_proof()
            try:
                value.encode("utf-8")
            except UnicodeError:
                _fail_proof()
        if namespace == "TENANT":
            if "\x00" in tenant:
                _fail_proof()
            try:
                tenant.encode("utf-8")
            except UnicodeError:
                _fail_proof()
        if self.command_type not in API_CORE_COMMAND_TYPES:
            _fail_proof()


@dataclass(frozen=True, slots=True, repr=False)
class ApiCoreIdempotencyEntry:
    """Instantane interne : validation complete avec config explicitement requise."""

    key: ApiCoreIdempotencyKey
    content_sha256: str
    serializer_version: str
    context: ScopeContext
    state: str
    result: CoreMutationResult | None
    created_at: datetime.datetime
    completed_at: datetime.datetime | None
    expires_at: datetime.datetime
    revision: int


def _validate_config(config: object) -> None:
    if type(config) is not ApiCoreIdempotencyConfig:
        _fail_proof()
    try:
        ApiCoreIdempotencyConfig.__post_init__(config)
    except AttributeError:
        _fail_proof()


def resolve_idempotency_key(*, context: ScopeContext, subject_id: object, command_type: object, idempotency_key: object, config: object) -> ApiCoreIdempotencyKey:
    if type(context) is not ScopeContext:
        _fail_proof()
    _validate_config(config)
    try:
        cfg_tenant = object.__getattribute__(config, "max_tenant_chars")
        cfg_scope = object.__getattribute__(config, "max_scope_chars")
        cfg_subject = object.__getattribute__(config, "max_subject_chars")
        cfg_ctype = object.__getattribute__(config, "max_command_type_chars")
        cfg_key = object.__getattribute__(config, "max_key_chars")
        ctx_type = object.__getattribute__(context, "scope_type")
        ctx_tenant = object.__getattribute__(context, "tenant_id")
        ctx_scope = object.__getattribute__(context, "scope_id")
    except AttributeError:
        _fail_proof()
    if type(config) is not ApiCoreIdempotencyConfig:
        _fail_proof()
    if type(context) is not ScopeContext:
        _fail_proof()
    try:
        validate_structure(context)
    except ScopeStructureError:
        _fail_proof()
    if ctx_type is ScopeType.PLATFORM:
        ns: str = "PLATFORM"
        tid: str | None = None
    elif ctx_type is ScopeType.TENANT:
        ns = "TENANT"
        tid = _opaque(ctx_tenant, cfg_tenant)
        if ctx_scope is not None:
            _opaque(ctx_scope, cfg_scope)
    else:
        _fail_proof()
    if type(command_type) is not str or command_type not in API_CORE_COMMAND_TYPES:
        _fail_proof()
    sid = _opaque(subject_id, cfg_subject)
    ctype = _opaque(command_type, cfg_ctype)
    key = _opaque(idempotency_key, cfg_key)
    return ApiCoreIdempotencyKey(namespace=ns, tenant_id=tid, subject_id=sid, command_type=ctype, idempotency_key=key)


def validate_idempotency_entry(entry: object, *, config: object) -> None:
    if type(entry) is not ApiCoreIdempotencyEntry:
        _fail_proof()
    _validate_config(config)
    try:
        key = object.__getattribute__(entry, "key")
        content = object.__getattribute__(entry, "content_sha256")
        sversion = object.__getattribute__(entry, "serializer_version")
        ctx = object.__getattribute__(entry, "context")
        state = object.__getattribute__(entry, "state")
        result = object.__getattribute__(entry, "result")
        created = object.__getattribute__(entry, "created_at")
        completed = object.__getattribute__(entry, "completed_at")
        expires = object.__getattribute__(entry, "expires_at")
        revision = object.__getattribute__(entry, "revision")
        cfg_window = object.__getattribute__(config, "replay_window_seconds")
    except AttributeError:
        _fail_proof()
    if type(config) is not ApiCoreIdempotencyConfig:
        _fail_proof()
    if type(entry) is not ApiCoreIdempotencyEntry:
        _fail_proof()
    if type(key) is not ApiCoreIdempotencyKey:
        _fail_proof()
    try:
        ApiCoreIdempotencyKey.__post_init__(key)
    except AttributeError:
        _fail_proof()
    try:
        expected = resolve_idempotency_key(context=ctx, subject_id=object.__getattribute__(key, "subject_id"), command_type=object.__getattribute__(key, "command_type"), idempotency_key=object.__getattribute__(key, "idempotency_key"), config=config)
    except (ApiCoreIdempotencyConflict, ApiCoreIdempotencyUnknown, ApiCoreIdempotencyProofInvalid, AttributeError):
        _fail_proof()
    try:
        same = (
            object.__getattribute__(expected, "namespace") == object.__getattribute__(key, "namespace")
            and object.__getattribute__(expected, "tenant_id") == object.__getattribute__(key, "tenant_id")
            and object.__getattribute__(expected, "subject_id") == object.__getattribute__(key, "subject_id")
            and object.__getattribute__(expected, "command_type") == object.__getattribute__(key, "command_type")
            and object.__getattribute__(expected, "idempotency_key") == object.__getattribute__(key, "idempotency_key")
        )
    except AttributeError:
        _fail_proof()
    if not same:
        _fail_proof()
    if type(ctx) is not ScopeContext:
        _fail_proof()
    try:
        validate_structure(ctx)
    except ScopeStructureError:
        _fail_proof()
    if type(content) is not str or len(content) != 64:
        _fail_proof()
    for ch in content:
        if not (("0" <= ch <= "9") or ("a" <= ch <= "f")):
            _fail_proof()
    if type(sversion) is not str:
        _fail_proof()
    try:
        parse_version(sversion)
    except ValueError:
        _fail_proof()
    if sversion != API_CORE_SERIALIZER_VERSION:
        _fail_proof()
    if type(state) is not str or (state != "IN_PROGRESS" and state != "SUCCEEDED"):
        _fail_proof()
    created = _utc(created)
    expires = _utc(expires)
    if type(revision) is not int or revision < 1:
        _fail_proof()
    if state == "IN_PROGRESS":
        if completed is not None or result is not None:
            _fail_proof()
        if not expires > created:
            _fail_proof()
        return
    if type(result) is not CoreMutationResult:
        _fail_proof()
    try:
        type(result).__post_init__(result)
    except (CoreInputInvalid, AttributeError):
        _fail_proof()
    if completed is None:
        _fail_proof()
    completed = _utc(completed)
    if not completed >= created:
        _fail_proof()
    try:
        window = datetime.timedelta(seconds=cfg_window)
        minimum_expires = completed + window
    except OverflowError:
        _fail_proof()
    if not expires >= minimum_expires:
        _fail_proof()
