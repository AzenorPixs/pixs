"""Liaison C09 à la demande propriétaire et au décideur courant C04.

Les deux fonctions de composition proviennent du code serveur sélectionné.
Aucune fonction ni preuve d'authentification n'est fournie par le payload.
Une résolution absente, périmée ou non réadmise ferme l'autorisation.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from types import FunctionType
from zoneinfo import ZoneInfo

from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import PortError, Request
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure

__all__ = [
    "C09Refused", "C09AuthorizationRefused", "C09Identity", "C09Resolution",
    "C09Grant", "C09AuthorizationAdapter", "c09_text", "c09_utc", "c09_pg_now",
    "validate_c09_identity",
]


_ERROR_CODES = frozenset((
    "C09_REFUSED", "C09_INPUT_INVALID", "C09_TIME_INVALID",
    "C09_DATABASE_INVALID", "C09_AUTHORIZATION_REFUSED",
    "C09_POLICY_UNRESOLVED", "C09_POLICY_DIVERGENT",
    "C09_LEASE_STALE", "C09_CONTENT_DIVERGENT", "C09_CAPACITY_INVALID",
))


class C09Refused(ValueError):
    def __init__(self, code="C09_REFUSED"):
        if type(code) is not str or code not in _ERROR_CODES:
            raise ValueError("Code de refus C09 invalide.")
        super().__init__("C09 : opération refusée (" + code + ").")
        self.code = code


class C09AuthorizationRefused(C09Refused):
    def __init__(self, request, decision=None):
        super().__init__("C09_AUTHORIZATION_REFUSED")
        self.request = request
        self.decision = decision


def c09_text(value):
    if type(value) is not str or not value or "\x00" in value:
        raise C09Refused("C09_INPUT_INVALID")
    try:
        value.encode("utf-8")
    except UnicodeError:
        raise C09Refused("C09_INPUT_INVALID") from None
    return value


def c09_utc(value, *, database=False):
    if type(value) is not dt.datetime:
        raise C09Refused()
    zone = value.tzinfo
    if zone is dt.timezone.utc:
        return value
    if database and type(zone) is ZoneInfo and zone.key in ("UTC", "Etc/UTC"):
        return value.replace(tzinfo=dt.timezone.utc)
    raise C09Refused()


def c09_pg_now(using):
    from django.db import connections
    from django.utils.connection import ConnectionDoesNotExist
    c09_text(using)
    try:
        connection = connections[using]
    except ConnectionDoesNotExist:
        raise C09Refused() from None
    if connection.vendor != "postgresql" or not connection.in_atomic_block:
        raise C09Refused()
    with connection.cursor() as cursor:
        cursor.execute("SELECT clock_timestamp()")
        row = cursor.fetchone()
    if type(row) is not tuple or len(row) != 1:
        raise C09Refused()
    return c09_utc(row[0], database=True)


@dataclass(frozen=True, slots=True, repr=False)
class C09Identity:
    actor_reference: str
    perimeter_reference: str
    request_reference: str
    request_version: str
    resource_id: str
    action_id: str
    context: ScopeContext
    correlation_id: str


@dataclass(frozen=True, slots=True, repr=False)
class C09Resolution:
    request: Request
    perimeter_reference: str
    content_sha256: str
    readmission_state: str
    readmission_revision: int
    observed_at: dt.datetime
    valid_until: dt.datetime


@dataclass(frozen=True, slots=True, repr=False)
class C09Grant:
    request: Request
    decision: Decision
    decider: object
    content_sha256: str


def validate_c09_identity(value):
    from pixs.kernel.manifest.semver import parse_version
    if type(value) is not C09Identity:
        raise C09Refused()
    for name in ("actor_reference", "perimeter_reference", "request_reference",
                 "request_version", "resource_id", "action_id", "correlation_id"):
        c09_text(getattr(value, name))
    try:
        parse_version(value.request_version)
        if type(value.context) is not ScopeContext:
            raise C09Refused()
        validate_structure(value.context)
    except (ValueError, ScopeStructureError):
        raise C09Refused() from None
    return value


class C09AuthorizationAdapter:
    """Résolution et fabrique C04 explicitement liées par la composition.

    resolver(identity, alias=...) retourne une C09Resolution courante, dont
    la réadmission est produite par son propriétaire. Cette classe ne livre
    ni Auth ni N05. factory(request=..., alias=..., operation_id=...) crée un
    RuntimeAuthorizationDecider réel pour cette invocation exacte.
    """

    def __init__(self, *, resolver, factory):
        if type(resolver) is not FunctionType or type(factory) is not FunctionType:
            raise C09Refused()
        self._resolver = resolver
        self._factory = factory

    def authorize(self, identity, *, using, operation_id, expected_sha=None):
        import uuid
        from pixs.core.services_common import CoreServiceError
        from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
        identity = validate_c09_identity(identity)
        c09_text(operation_id)
        fallback = Request(uuid.uuid4().hex, identity.actor_reference,
                           identity.resource_id, identity.action_id,
                           identity.context, identity.correlation_id)
        c09_pg_now(using)
        try:
            resolution = self._resolver(identity, alias=using)
        except (PortError, CoreServiceError, C09Refused):
            raise C09AuthorizationRefused(fallback) from None
        if type(resolution) is not C09Resolution:
            raise C09AuthorizationRefused(fallback)
        request = resolution.request
        if type(request) is not Request:
            raise C09AuthorizationRefused(fallback)
        try:
            request.__post_init__()
            validate_structure(request.context)
            for name in ("subject_id", "resource_id", "action_id", "decision_id"):
                c09_text(getattr(request, name))
            c09_text(resolution.perimeter_reference)
            digest = c09_text(resolution.content_sha256)
            if re.fullmatch("[0-9a-f]{64}", digest) is None:
                raise C09Refused()
            if (request.subject_id != identity.actor_reference
                    or request.resource_id != identity.resource_id
                    or request.action_id != identity.action_id
                    or request.context != identity.context
                    or request.correlation_id != identity.correlation_id
                    or resolution.perimeter_reference != identity.perimeter_reference):
                raise C09Refused()
            if expected_sha is not None:
                c09_text(expected_sha)
                if digest != expected_sha:
                    raise C09Refused()
            if (type(resolution.readmission_state) is not str
                    or resolution.readmission_state != "CURRENT"
                    or type(resolution.readmission_revision) is not int
                    or not 1 <= resolution.readmission_revision <= 2**63 - 1):
                raise C09Refused()
            now = c09_pg_now(using)
            if not c09_utc(resolution.observed_at) <= now < c09_utc(resolution.valid_until):
                raise C09Refused()
        except (PortError, ScopeStructureError, C09Refused):
            raise C09AuthorizationRefused(fallback) from None
        try:
            decider = self._factory(request=request, alias=using,
                                    operation_id=operation_id)
            if type(decider) is not RuntimeAuthorizationDecider:
                raise C09Refused()
            decision = decider.revalidate_under_locks(
                request, alias=using, operation_id=operation_id)
        except (PortError, CoreServiceError, C09Refused):
            raise C09AuthorizationRefused(request) from None
        if type(decision) is not Decision or decision.effect is not Effect.ALLOW:
            raise C09AuthorizationRefused(
                request, decision if type(decision) is Decision else None)
        try:
            c09_text(decision.decision_id)
            now = c09_pg_now(using)
            if (decision.decision_id != request.decision_id
                    or not c09_utc(decision.evaluated_at) <= now < c09_utc(decision.expires_at)):
                raise C09Refused()
        except C09Refused:
            raise C09AuthorizationRefused(request) from None
        return C09Grant(request, decision, decider, digest)
