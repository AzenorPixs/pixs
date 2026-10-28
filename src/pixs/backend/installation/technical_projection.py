"""Projection technique C08 1.0.0 : codec pur, sans autorité ni publication.

Les références et les observations restent à résoudre chez leurs propriétaires.
Aucune absence réelle, signature, confirmation ou disponibilité ne découle
de ces structures. Le profil PA courant refuse Docker et RECREATE.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, fields

__all__ = ["TechnicalProjectionError", "ProjectionLimits", "ProjectionService",
           "ProjectionRole", "ProjectionDatabase", "ProjectionObservation",
           "TechnicalProjection", "parse_projection_bytes",
           "dump_projection_canonical", "projection_sha256",
           "validate_effects_for_actions"]

_SCHEMA = {"schema_version": "1.0.0", "catalog_operation": "prepare_postgresql",
           "catalog_version": "1.0.0"}
_EFFECTS = ("SERVICE_INSTALL", "SERVICE_CONFIGURE", "CLUSTER_INITIALIZE",
            "SERVICE_START", "ROLE_CREATE", "DATABASE_DROP", "DATABASE_CREATE")


class TechnicalProjectionError(ValueError):
    def __init__(self):
        super().__init__("Projection technique C08 non vérifiable.")
        self.code = "C08_TECHNICAL_PROJECTION_INVALID"
        self.element = "technical_projection"
        self.step = "validate_technical_projection"


@dataclass(frozen=True, slots=True)
class ProjectionLimits:
    max_bytes: int
    max_ref_bytes: int
    max_correlation_refs: int
    max_causation_refs: int


@dataclass(frozen=True, slots=True, repr=False)
class ProjectionService:
    ref: str
    action: str
    profile_ref: str
    profile_version: str


@dataclass(frozen=True, slots=True, repr=False)
class ProjectionRole:
    ref: str
    action: str
    profile_ref: str
    profile_version: str
    credential_binding_ref: str
    credential_binding_version: str


@dataclass(frozen=True, slots=True, repr=False)
class ProjectionDatabase:
    ref: str
    action: str
    profile_ref: str
    profile_version: str


@dataclass(frozen=True, slots=True, repr=False)
class ProjectionObservation:
    ref: str
    version: str
    sha256: str


@dataclass(frozen=True, slots=True, repr=False)
class TechnicalProjection:
    projection_ref: str
    operation_id: str
    installation_ref: str
    target_ref: str
    runtime_profile_ref: str
    runtime_profile_version: str
    service: ProjectionService
    role: ProjectionRole
    database: ProjectionDatabase
    observation: ProjectionObservation
    allowed_effects: tuple[str, ...]
    correlation_id: str
    idempotency_key: str
    causation_id: str | None
    correlation_ids: tuple[str, ...]
    causation_ids: tuple[str, ...]


def _fail():
    raise TechnicalProjectionError()


def _limits(value):
    if type(value) is not ProjectionLimits:
        _fail()
    if any(type(getattr(value, f.name)) is not int or getattr(value, f.name) < 1
           for f in fields(ProjectionLimits)):
        _fail()


def _ref(value, limits):
    if type(value) is not str or not value or not value.isprintable():
        _fail()
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        raise TechnicalProjectionError() from None
    if size > limits.max_ref_bytes:
        _fail()


def _digest(value):
    if (type(value) is not str or len(value) != 64
            or any(c not in "0123456789abcdef" for c in value)):
        _fail()


def validate_effects_for_actions(service_action: str, role_action: str,
                                 database_action: str,
                                 allowed: tuple[str, ...]) -> None:
    if (any(type(v) is not str for v in (service_action, role_action, database_action))
            or service_action not in ("INSTALL_CONFIGURE_START", "START_EXISTING", "REUSE_RUNNING")
            or role_action not in ("CREATE", "REUSE")
            or database_action not in ("CREATE", "REUSE")
            or type(allowed) is not tuple
            or any(type(v) is not str for v in allowed)
            or len(allowed) > len(_EFFECTS)):
        _fail()
    selected = set(allowed)
    if (len(selected) != len(allowed) or "DATABASE_DROP" in selected
            or tuple(v for v in _EFFECTS if v in selected) != allowed):
        _fail()
    expected = set()
    if service_action == "INSTALL_CONFIGURE_START":
        expected.update(("SERVICE_INSTALL", "SERVICE_CONFIGURE", "SERVICE_START"))
        if "CLUSTER_INITIALIZE" in selected:
            expected.add("CLUSTER_INITIALIZE")
    elif service_action == "START_EXISTING":
        expected.add("SERVICE_START")
    if role_action == "CREATE":
        expected.add("ROLE_CREATE")
    if database_action == "CREATE":
        expected.add("DATABASE_CREATE")
    if selected != expected:
        _fail()
    return None


def _validate(projection, limits):
    _limits(limits)
    if type(projection) is not TechnicalProjection:
        _fail()
    nested = {"service": ProjectionService, "role": ProjectionRole,
              "database": ProjectionDatabase, "observation": ProjectionObservation}
    for name, kind in nested.items():
        item = getattr(projection, name)
        if type(item) is not kind:
            _fail()
        for field in fields(kind):
            if field.name not in ("action", "sha256"):
                _ref(getattr(item, field.name), limits)
    for field in fields(TechnicalProjection):
        name = field.name
        if name not in (*nested, "allowed_effects", "causation_id",
                        "correlation_ids", "causation_ids"):
            _ref(getattr(projection, name), limits)
    if projection.causation_id is not None:
        _ref(projection.causation_id, limits)
    _digest(projection.observation.sha256)
    for name, maximum in (("correlation_ids", limits.max_correlation_refs),
                          ("causation_ids", limits.max_causation_refs)):
        values = getattr(projection, name)
        if type(values) is not tuple or len(values) > maximum:
            _fail()
        for value in values:
            _ref(value, limits)
    validate_effects_for_actions(projection.service.action, projection.role.action,
                                 projection.database.action, projection.allowed_effects)


def dump_projection_canonical(projection: TechnicalProjection,
                              limits: ProjectionLimits) -> bytes:
    _validate(projection, limits)
    document = asdict(projection)
    document.update(_SCHEMA)
    for name in ("allowed_effects", "correlation_ids", "causation_ids"):
        document[name] = list(document[name])
    try:
        encoded = json.dumps(document, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError):
        raise TechnicalProjectionError() from None
    if len(encoded) > limits.max_bytes:
        _fail()
    return encoded


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail()
        result[key] = value
    return result


def _number(_):
    _fail()


def _object(value, names):
    if type(value) is not dict or set(value) != set(names):
        _fail()
    return value


def parse_projection_bytes(raw: bytes, limits: ProjectionLimits) -> TechnicalProjection:
    _limits(limits)
    if type(raw) is not bytes or not raw or len(raw) > limits.max_bytes:
        _fail()
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                              parse_int=_number, parse_float=_number, parse_constant=_number)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError):
        raise TechnicalProjectionError() from None
    _object(document, tuple(_SCHEMA) + tuple(f.name for f in fields(TechnicalProjection)))
    for key, expected in _SCHEMA.items():
        if type(document[key]) is not str or document[key] != expected:
            _fail()
    values = {f.name: document[f.name] for f in fields(TechnicalProjection)}
    for name, kind in (("service", ProjectionService), ("role", ProjectionRole),
                       ("database", ProjectionDatabase), ("observation", ProjectionObservation)):
        nested = _object(values[name], tuple(f.name for f in fields(kind)))
        values[name] = kind(**nested)
    for name in ("allowed_effects", "correlation_ids", "causation_ids"):
        if type(values[name]) is not list:
            _fail()
        values[name] = tuple(values[name])
    projection = TechnicalProjection(**values)
    # La publication confirmée et son digest portent sur ces mêmes octets ;
    # une représentation JSON équivalente n'est pas une seconde forme admise.
    if dump_projection_canonical(projection, limits) != raw:
        _fail()
    return projection


def projection_sha256(projection: TechnicalProjection, limits: ProjectionLimits) -> str:
    return hashlib.sha256(dump_projection_canonical(projection, limits)).hexdigest()
