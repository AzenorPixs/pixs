"""Source privée d'une invocation serveur, sans session ni effet métier.

Un témoin de vérification locale n'est pas une autorisation de commit. Toute
frontière SQL nouvelle refait les contrôles avec un verifier natif neuf ;
l'instant d'authentification, les empreintes et versions ne sont pas rafraîchis.
La source ne contient ni mot de passe ni jeton brut, et ne doit pas être exposée
par une façade client. Son propriétaire la ferme après le traitement complet.
"""
from __future__ import annotations

import threading
from django.db import connections, transaction
from pixs.auth.runtime_verifier import AuthAuthenticationVerifier, AuthVerificationError, _native
from pixs.auth.resource_metadata import AuthResourceMetadataResolver
from pixs.core.authz.ports import Request, AuthenticationContext, RevocationStatus
from pixs.core.scope.context import ScopeContext
from pixs.core.scope.ownership import ResourceOwnership


class AuthInvocationSource:
    def __init__(self, verifier: AuthAuthenticationVerifier):
        if type(verifier) is not AuthAuthenticationVerifier or verifier._transaction is not None:
            raise AuthVerificationError()
        self._template = verifier
        self._cached = None
        self._mutex = threading.RLock()

    def close(self) -> None:
        with self._mutex:
            self._cached = None
            self._template = None

    def __enter__(self):
        if self._template is None:
            raise AuthVerificationError()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def _pair(self, alias, operation_id):
        physical, native = _native(alias)
        if self._cached is not None and self._cached[0] is physical and self._cached[1] == native:
            return self._cached[2:]
        # Copie du témoin privé seulement. Aucun état de la TX antérieure n'est repris.
        clone = object.__new__(AuthAuthenticationVerifier)
        for name in AuthAuthenticationVerifier.__slots__:
            if name not in ("_transaction", "_mutex"):
                setattr(clone, name, getattr(self._template, name))
        clone._transaction = None
        clone._mutex = threading.RLock()
        metadata = AuthResourceMetadataResolver(request=self._template._request, alias=alias, operation_id=operation_id)
        self._cached = (physical, native, clone, metadata)
        return clone, metadata

    def _operate(self, request, alias, operation_id, callback):
        with self._mutex:
            template = self._template
            if (template is None or type(request) is not Request or request != template._request
                    or alias != template._alias or operation_id != template._operation):
                raise AuthVerificationError()
            conn = connections[alias]
            if conn.vendor != "postgresql":
                raise AuthVerificationError()
            if conn.in_atomic_block:
                return callback(*self._pair(alias, operation_id))
            # Préadmission seulement. Rien de cette TX ne devient un reçu du commit.
            try:
                with transaction.atomic(using=alias):
                    return callback(*self._pair(alias, operation_id))
            finally:
                self._cached = None

    def revalidate(self, request: Request, *, alias: str, operation_id: str) -> tuple[AuthenticationContext, RevocationStatus]:
        return self._operate(request, alias, operation_id,
                             lambda verifier, metadata: verifier.revalidate(request, alias=alias, operation_id=operation_id))

    def ownership(self, resource_id: str, *, context: ScopeContext, alias: str, operation_id: str) -> ResourceOwnership | None:
        with self._mutex:
            if self._template is None or type(context) is not ScopeContext or context != self._template._request.context:
                raise AuthVerificationError()
            request = self._template._request
            def resolve(verifier, metadata):
                verifier.revalidate(request, alias=alias, operation_id=operation_id)
                return metadata.ownership(resource_id, context=context, alias=alias, operation_id=operation_id)
            return self._operate(request, alias, operation_id, resolve)


__all__ = ["AuthInvocationSource"]
