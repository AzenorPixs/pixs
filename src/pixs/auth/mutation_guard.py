"""Reçu privé Auth avant effet ; contrôle SQL seulement, jamais autorisation autonome."""
from __future__ import annotations

import copy
from django.db import connections
from pixs.auth.runtime_verifier import _native
from pixs.auth.contracts import AuthServiceError

_KEY = object()
_ACTIONS = {"pixs.auth.session.renew", "pixs.auth.session.logout", "pixs.auth.session.revoke", "pixs.auth.session.revoke_all", "pixs.auth.credential.change", "pixs.auth.credential.recover"}


def _capture(model, alias, lookup, fields):
    if model._meta.app_label != "pixs_auth":
        raise AuthServiceError("AUTH_INPUT_INVALID")
    return list(model.objects.using(alias).filter(**lookup).order_by(model._meta.pk.name).values(*fields))


class _AuthTransitionVerifier:
    def __init__(self, key, *, command, decision, alias, expectations, authority_check):
        if key is not _KEY or command.request.action_id not in _ACTIONS or not callable(authority_check):
            raise AuthServiceError("AUTH_INPUT_INVALID")
        self._command, self._decision, self._alias = command, decision, alias
        self._physical, self._native = _native(alias)
        self._savepoints = tuple(connections[alias].savepoint_ids)
        self._expectations = tuple((model, copy.deepcopy(lookup), tuple(fields), copy.deepcopy(expected)) for model, lookup, fields, expected in expectations)
        self._authority_check = authority_check

    def verify_final_transition(self, request, decision, *, alias, operation_id):
        physical, native = _native(alias)
        if (request != self._command.request or decision is not self._decision or alias != self._alias
                or operation_id != self._command.operation_id or physical is not self._physical or native != self._native
                or tuple(connections[alias].savepoint_ids) != self._savepoints):
            raise AuthServiceError("AUTH_DENIED")
        if self._authority_check() is not None:
            raise AuthServiceError("AUTH_DENIED")
        for model, lookup, fields, expected in self._expectations:
            if _capture(model, alias, lookup, fields) != expected:
                raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
        return None


def _transition(*, command, decision, alias, expectations, authority_check):
    return _AuthTransitionVerifier(_KEY, command=command, decision=decision, alias=alias, expectations=expectations, authority_check=authority_check)
