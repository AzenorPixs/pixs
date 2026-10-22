"""Métadonnées propriétaires Auth, port de composition serveur sans droit implicite.

L'existant est résolu depuis sa ligne ; le contexte de l'appelant n'en est pas
la preuve. Ressource absente/inconnue : None, jamais un contexte fabriqué.
Aucun intent de création n'est accepté par ce resolver de ressources existantes.
"""
from __future__ import annotations

import threading
from django.core.exceptions import ObjectDoesNotExist
from pixs.auth.identifiers import parse_identity_reference, require_uuid7
from pixs.auth.runtime_verifier import AuthVerificationError, _native
from pixs.core.authz.ports import Request
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.core.scope.ownership import ResourceOwnership
import uuid


class AuthResourceMetadataResolver:
    def __init__(self, *, request: Request, alias: str, operation_id: str):
        if type(request) is not Request or type(alias) is not str or not alias or type(operation_id) is not str or not operation_id:
            raise AuthVerificationError()
        request.__post_init__()
        parse_identity_reference(request.subject_id)
        self._request, self._alias, self._operation = request, alias, operation_id
        self._transaction = None
        self._mutex = threading.RLock()

    def ownership(self, resource_id: str, *, context: ScopeContext, alias: str, operation_id: str) -> ResourceOwnership | None:
        from pixs.auth import models as m
        if (type(resource_id) is not str or type(context) is not ScopeContext or context != self._request.context
                or alias != self._alias or operation_id != self._operation):
            raise AuthVerificationError()
        with self._mutex:
            physical, native = _native(alias)
            if self._transaction is None:
                self._transaction = (physical, native)
            elif self._transaction[0] is not physical or self._transaction[1] != native:
                raise AuthVerificationError()
            namespace, separator, tail = resource_id.partition(":")
            mapping = {"pixs.auth.account": (m.AuthAccountGate, False),
                       "pixs.auth.binding": (m.AuthBinding, False),
                       "pixs.auth.credential": (m.AuthPasswordCredential, False),
                       "pixs.auth.session": (m.AuthSession, True),
                       "pixs.auth.policy": (m.AuthPolicyRow, True),
                       "pixs.auth.operation": (m.AuthOperation, True),
                       "pixs.auth.audit-pending": (m.AuthAuditPending, True),
                       "pixs.auth.bootstrap": (m.AuthBootstrapAuthorization, False)}
            if not separator or namespace not in mapping:
                return None
            try:
                key = uuid.UUID(tail)
                require_uuid7(key)
            except (ValueError, AttributeError):
                raise AuthVerificationError() from None
            if str(key) != tail:
                raise AuthVerificationError()
            model, scoped = mapping[namespace]
            try:
                row = model.objects.using(alias).get(pk=key, persistence_state="ACTIVE")
            except ObjectDoesNotExist:
                return None
            actual = ScopeContext(ScopeType(row.scope_type), row.tenant_id, row.scope_id) if scoped else ScopeContext(ScopeType.PLATFORM)
            return ResourceOwnership(resource_id, actual)


__all__ = ["AuthResourceMetadataResolver"]
