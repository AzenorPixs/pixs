"""Faits runtime C04 : preuve Auth propriétaire et propriété des ressources réelle.

Les objets de source sont injectés par la composition serveur. Aucun DTO
d'authentification, header de propriété ou booléen client ne crée d'autorité.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass

from django.db import connections, transaction, DatabaseError, InterfaceError

from pixs.core.authz.ports import (
    AuthenticationContext, PortError, Request, RevocationStatus, TrustedFacts,
)
from pixs.core.query_source import _KINDS, _parse_ref, collection_ref
from pixs.core.scope.context import ScopeContext, ScopeType, validate_structure
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_runtime_filter import _core_ownership, _CORE_PREFIXES
from pixs.core.services_runtime_store import CoreAuthorizationStore


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeResourceOwner:
    resource_prefix: str
    ownership: object

    def __post_init__(self):
        if (type(self.resource_prefix) is not str or not self.resource_prefix
                or any(ch in self.resource_prefix for ch in "*?[]")
                or not callable(self.ownership)):
            raise PortError()


_CREATE = {
    "USER": "pixs.core.identity.user.create",
    "IDENTITY": "pixs.core.identity.identity.create",
    "LINK": "pixs.core.identity.link.create",
    "GROUP": "pixs.core.groups.group.create",
    "USER_GROUP": "pixs.core.groups.user-group.add",
    "TENANT_MEMBERSHIP": "pixs.core.groups.tenant-membership.activate",
    "TENANT": "pixs.core.scope.tenant.create",
    "SCOPE": "pixs.core.scope.node.create",
    "PERMISSION": "pixs.core.authz.permission.declare",
    "ROLE": "pixs.core.authz.role.create",
    "ROLE_ASSIGNMENT": "pixs.core.authz.role.assign",
    "POLICY": "pixs.core.authz.policy.persist",
    "GRANT": "pixs.core.authz.super-admin.tenant.grant",
}
_GLOBAL = ("USER", "IDENTITY", "LINK", "TENANT", "PERMISSION", "POLICY", "BINDING", "GRANT")


class RuntimeTrustedFactsProvider:
    """Une instance par invocation, sans cache d'AuthenticationContext admis."""

    def __init__(self, *, store: CoreAuthorizationStore, authentication_source,
                 request: Request, operation_id: str, additional_owners=(), fact_source=None):
        if type(store) is not CoreAuthorizationStore or type(request) is not Request:
            raise PortError()
        request.__post_init__()
        validate_structure(request.context)
        if type(operation_id) is not str or not operation_id:
            raise PortError()
        if not callable(getattr(authentication_source, "revalidate", None)):
            raise PortError()
        if type(additional_owners) is not tuple or len(additional_owners) > store.limits.max_selector_values:
            raise PortError()
        prefixes = list(_CORE_PREFIXES.values()) + ["pixs.core.query-collection:"]
        for owner in additional_owners:
            if type(owner) is not RuntimeResourceOwner:
                raise PortError()
            if any(owner.resource_prefix.startswith(p) or p.startswith(owner.resource_prefix) for p in prefixes):
                raise PortError()
            prefixes.append(owner.resource_prefix)
        if fact_source is not None and not callable(getattr(fact_source, "resolve", None)):
            raise PortError()
        self._store, self._auth, self._origin, self._op = store, authentication_source, request, operation_id
        self._owners, self._extra = additional_owners, fact_source
        self._mutex = threading.RLock()
        self._native = None
        self._ownership = {}

    def _bound(self, request):
        if type(request) is not Request:
            raise PortError()
        request.__post_init__()
        if ((request.subject_id, request.action_id, request.context, request.correlation_id)
                != (self._origin.subject_id, self._origin.action_id,
                    self._origin.context, self._origin.correlation_id)):
            raise PortError()
        if (request.resource_id not in self._store.catalog.resource_ids
                or request.action_id not in self._store.catalog.action_ids):
            raise PortError()

    def _core_kind(self, reference):
        kinds = [kind for kind, prefix in _CORE_PREFIXES.items() if reference.startswith(prefix)]
        if len(kinds) > 1:
            raise PortError()
        return kinds[0] if kinds else None

    def _exists(self, kind, values):
        model, _prefix, fields, *_ = _KINDS[kind]
        return model.objects.using(self._store.alias).filter(
            **dict(zip(fields, values)), persistence_state="ACTIVE").exists()

    def _creation(self, kind, request):
        if _CREATE.get(kind) != request.action_id:
            return None
        keys = _parse_ref(kind, request.resource_id)
        platform = ScopeContext(ScopeType.PLATFORM)
        if kind == "LINK":
            if not self._exists("USER", (keys[0],)) or not self._exists("IDENTITY", (keys[1],)):
                return None
        if kind == "GRANT":
            if not self._exists("BINDING", (keys[0],)) or not self._exists("TENANT", (keys[1],)):
                return None
        if kind in _GLOBAL:
            return ResourceOwnership(request.resource_id, platform)
        if kind in ("GROUP", "ROLE"):
            return ResourceOwnership(request.resource_id, request.context)
        if kind == "SCOPE":
            if request.context.scope_type is not ScopeType.TENANT or request.context.scope_id is not None:
                return None
            return ResourceOwnership(request.resource_id, request.context)
        if kind == "TENANT_MEMBERSHIP":
            if not self._exists("IDENTITY", (keys[0],)) or not self._exists("TENANT", (keys[1],)):
                return None
            return ResourceOwnership(request.resource_id, ScopeContext(ScopeType.TENANT, keys[1]))
        if kind == "USER_GROUP":
            if not self._exists("USER", (keys[0],)):
                return None
            parent = _core_ownership(resource_id=_CORE_PREFIXES["GROUP"] + keys[1],
                context=request.context, alias=self._store.alias)
            return None if parent is None else ResourceOwnership(request.resource_id, parent.context)
        if kind == "ROLE_ASSIGNMENT":
            role, subject_type, subject = keys
            subject_kind = {"USER": "USER", "IDENTITY": "IDENTITY", "GROUP": "GROUP"}[subject_type]
            if not self._exists(subject_kind, (subject,)):
                return None
            parent = _core_ownership(resource_id=_CORE_PREFIXES["ROLE"] + role,
                context=request.context, alias=self._store.alias)
            return None if parent is None else ResourceOwnership(request.resource_id, parent.context)
        return None

    def _resolve_ownership(self, request):
        key = request.resource_id
        if key in self._ownership:
            return self._ownership[key]
        alias = self._store.alias
        kind = self._core_kind(key)
        if kind is not None:
            # Métadonnées internes de lignes retenues : la permission et l'état
            # applicatif restent contrôlés par le PDP et le service propriétaire.
            owner = _core_ownership(resource_id=key, context=request.context,
                                    alias=alias, include_inactive=True)
            if owner is None:
                owner = self._creation(kind, request)
        elif key.startswith("pixs.core.query-collection:"):
            if not any(key == collection_ref(k, request.context) for k in _KINDS):
                raise PortError()
            owner = ResourceOwnership(key, request.context)
        else:
            matches = [s for s in self._owners if key.startswith(s.resource_prefix)]
            if len(matches) != 1:
                raise PortError()
            owner = matches[0].ownership(key, context=request.context, alias=alias, operation_id=self._op)
        if type(owner) is not ResourceOwnership or owner.resource_id != key:
            raise PortError()
        owner.__post_init__()
        if owner.context != request.context:
            raise PortError()
        self._ownership[key] = owner
        return owner

    def _resolve_locked(self, request):
        self._bound(request)
        alias = self._store.alias
        # Core précède tout appel Auth, même pendant la préadmission en lecture.
        self._store.pinned_snapshot(context=request.context, actor_ref=request.subject_id)
        connection = connections[alias]
        native = (connection.connection, transaction_identity(alias), tuple(connection.savepoint_ids))
        with self._mutex:
            if self._native != native:
                self._ownership.clear()
                self._native = native
            ownership = self._resolve_ownership(request)
            answer = self._auth.revalidate(self._origin, alias=alias, operation_id=self._op)
            if (type(answer) is not tuple or len(answer) != 2
                    or type(answer[0]) is not AuthenticationContext
                    or type(answer[1]) is not RevocationStatus):
                raise PortError()
            auth, revocation = answer
            auth.__post_init__()
            if auth.digital_identity_id != request.subject_id or auth.context != request.context:
                raise PortError()
            memberships, attributes = (), ()
            if self._extra is not None:
                extension = self._extra.resolve(request, alias=alias, operation_id=self._op)
                if (type(extension) is not tuple or len(extension) != 2
                        or type(extension[0]) is not tuple or type(extension[1]) is not tuple):
                    raise PortError()
                memberships, attributes = extension
            return TrustedFacts(request.subject_id, request.resource_id, request.action_id,
                auth, ownership, request.context, revocation, memberships, attributes)

    def resolve(self, request: Request) -> TrustedFacts:
        try:
            if connections[self._store.alias].in_atomic_block:
                return self._resolve_locked(request)
            with transaction.atomic(using=self._store.alias):
                return self._resolve_locked(request)
        except (ValueError, DatabaseError, InterfaceError) as error:
            raise PortError() from error
