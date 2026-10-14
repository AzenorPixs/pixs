"""Primitives PostgreSQL de stockage CommandIdempotencyV1.

Les contextes participant au même alias gardent IN_PROGRESS non engagé.
Aucun owner, provider, horloge, purge, hold ni autorité n'est exécuté ici :
les producteurs serveur fournissent digest, version, contexte et dates.
Les erreurs techniques externes doivent être propagées par l'appelant.
Les modèles ORM internes ne constituent pas une API de workflow.
"""

import re
import threading
from contextlib import contextmanager
from contextvars import ContextVar

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from pixs.backend.bulk_command_idempotency_record import (
    BulkCommandIdempotencyRecord,
    _FIELDS,
)
from pixs.backend.bulk_command_idempotency_values import (
    capture_bulk_command_idempotency_values,
)
from pixs.backend.bulk_execution_values import (
    _is_complete_semver,
    _is_runtime_text,
)
from pixs.backend.bulk_runtime_records import _INT64_MAX

__all__ = [
    "BulkCommandIdempotencyConflict",
    "BulkCommandIdempotencyRefused",
    "BulkCommandIdempotencyRepository",
    "BulkCommandIdempotencyStale",
]

_KEY_FIELDS = ("tenant_id", "subject_id", "command_type", "idempotency_key")
_TERMINAL = frozenset({"SUCCEEDED", "REJECTED"})
_SHA64 = re.compile(r"[0-9a-f]{64}")
_UNIQUE_NAME = "bulkcommandidempotency_key_unique"


class BulkCommandIdempotencyRefused(Exception):
    """Entrée ou contexte de stockage refusé, sans écho de valeur."""


class BulkCommandIdempotencyConflict(Exception):
    """Même clé, identité divergente ou réservation non terminale."""


class BulkCommandIdempotencyStale(Exception):
    """Révision ou identité initiale CAS obsolète."""


def _refused():
    return BulkCommandIdempotencyRefused("commande idempotente refusée")


def _conflict():
    return BulkCommandIdempotencyConflict("conflit d'idempotence commande")


def _stale():
    return BulkCommandIdempotencyStale("révision idempotence commande périmée")


def _values(bound):
    return {field: getattr(bound, field) for field in _FIELDS}


def _capture(candidate):
    bound, diagnostics = capture_bulk_command_idempotency_values(candidate)
    if bound is None or diagnostics:
        raise _refused()
    if bound.revision > _INT64_MAX:
        raise _refused()
    return bound


def _known_unique(exc):
    cause = exc.__cause__
    return (
        cause is not None
        and getattr(cause, "sqlstate", None) == "23505"
        and getattr(getattr(cause, "diag", None), "constraint_name", None)
        == _UNIQUE_NAME
    )


class _IdempotentUnitToken:
    __slots__ = (
        "_owner", "_thread", "_initial", "_values", "_active",
        "_finalized", "_failed", "_replay",
    )

    def __init__(self, owner, initial, replay):
        self._owner = owner
        self._thread = threading.get_ident()
        self._initial = initial
        self._values = initial
        self._active = True
        self._finalized = replay
        self._failed = False
        self._replay = replay

    @property
    def is_replay(self):
        return self._replay

    @property
    def entry(self):
        """Snapshot mémoire owned, sans preuve d'autorité ou d'existence."""
        return _values(self._values)


class BulkCommandIdempotencyRepository:
    """API synchrone interne ; les alias proviennent du serveur déclaré."""

    def __init__(self, using: str = "default") -> None:
        if type(using) is not str or not _is_runtime_text(using):
            raise ValidationError(
                "alias de base invalide",
                code="bulk_command_idempotency_alias_invalid",
            )
        self._using = using
        self._unit_var: ContextVar[_IdempotentUnitToken | None] = ContextVar(
            "bulk_command_idempotency_unit", default=None
        )

    def _mark_failed(self):
        current = self._unit_var.get()
        if (
            type(current) is _IdempotentUnitToken
            and current._owner is self
            and current._active
            and current._thread == threading.get_ident()
        ):
            current._failed = True
            transaction.set_rollback(True, using=self._using)

    @contextmanager
    def _failure_boundary(self):
        # Nettoyage puis propagation inchangée, y compris interruption.
        try:
            yield
        except BaseException:
            self._mark_failed()
            raise

    def _key(self, tenant_id, subject_id, command_type, idempotency_key):
        key = (tenant_id, subject_id, command_type, idempotency_key)
        if any(type(value) is not str or not _is_runtime_text(value) for value in key):
            raise _refused()
        return dict(zip(_KEY_FIELDS, key))

    def _fingerprint(self, content_sha256, serializer_version):
        if type(content_sha256) is not str or _SHA64.fullmatch(content_sha256) is None:
            raise _refused()
        if type(serializer_version) is not str or not _is_runtime_text(serializer_version) or not _is_complete_semver(serializer_version):
            raise _refused()

    def _lookup(self, key, *, lock=False):
        query = BulkCommandIdempotencyRecord.objects.using(
            self._using
        ).filter(**key)
        if lock:
            query = query.select_for_update()
        record = query.first()
        return None if record is None else _capture(record.as_values())

    def get_entry(
        self, *, tenant_id: object, subject_id: object,
        command_type: object, idempotency_key: object,
    ) -> dict | None:
        with self._failure_boundary():
            key = self._key(tenant_id, subject_id, command_type, idempotency_key)
            bound = self._lookup(key)
            return None if bound is None else _values(bound)

    def _match(self, stored, content_sha256, serializer_version):
        if (
            stored.content_sha256 != content_sha256
            or stored.serializer_version != serializer_version
            or stored.state not in _TERMINAL
        ):
            raise _conflict()

    def replay(
        self, *, tenant_id: object, subject_id: object,
        command_type: object, idempotency_key: object,
        content_sha256: object, serializer_version: object,
    ) -> dict | None:
        with self._failure_boundary():
            key = self._key(tenant_id, subject_id, command_type, idempotency_key)
            self._fingerprint(content_sha256, serializer_version)
            stored = self._lookup(key)
            if stored is None:
                return None
            self._match(stored, content_sha256, serializer_version)
            return _values(stored)

    def _token(self, token):
        # Aucun attribut du candidat étranger avant le type et l'identité.
        if type(token) is not _IdempotentUnitToken or self._unit_var.get() is not token:
            raise _refused()
        if (
            token._owner is not self
            or token._thread != threading.get_ident()
            or not token._active
            or token._finalized
            or token._failed
            or token._replay
        ):
            raise _refused()
        return token

    def finalize_terminal(
        self, token: object, *, expected_revision: object, state: object,
        result_reference: object, failure_code: object,
    ) -> int:
        with self._failure_boundary():
            valid = self._token(token)
            if (
                type(expected_revision) is not int
                or expected_revision < 1
                or expected_revision >= _INT64_MAX
            ):
                raise _refused()
            initial = valid._initial
            if expected_revision != initial.revision:
                raise _stale()
            if type(state) is not str or state not in _TERMINAL:
                raise _refused()
            candidate = _values(initial)
            candidate.update(
                state=state, result_reference=result_reference,
                failure_code=failure_code, revision=expected_revision + 1,
            )
            final = _capture(candidate)
            key = {field: getattr(initial, field) for field in _KEY_FIELDS}
            updated = BulkCommandIdempotencyRecord.objects.using(
                self._using
            ).filter(
                **key, revision=expected_revision, state="IN_PROGRESS",
                content_sha256=initial.content_sha256,
                serializer_version=initial.serializer_version,
                created_at=initial.created_at, expires_at=initial.expires_at,
            ).update(
                state=final.state, result_reference=final.result_reference,
                failure_code=final.failure_code, revision=final.revision,
            )
            if updated != 1:
                raise _stale()
            valid._values = final
            valid._finalized = True
            return final.revision

    def _reserve(self, initial):
        key = {field: getattr(initial, field) for field in _KEY_FIELDS}
        stored = self._lookup(key, lock=True)
        if stored is None:
            try:
                # La seule race attendue est isolée dans son savepoint.
                with transaction.atomic(using=self._using):
                    record = BulkCommandIdempotencyRecord.from_values(
                        _values(initial)
                    )
                    record.save(force_insert=True, using=self._using)
            except IntegrityError as exc:
                if not _known_unique(exc):
                    raise
                stored = self._lookup(key, lock=True)
                if stored is None:
                    raise _refused() from exc
            else:
                return initial, False
        self._match(stored, initial.content_sha256, initial.serializer_version)
        return stored, True

    @contextmanager
    def idempotent_unit(self, *, values: object):
        with self._failure_boundary():
            initial = _capture(values)
            if initial.state != "IN_PROGRESS" or initial.revision != 1:
                raise _refused()
            with transaction.atomic(using=self._using, savepoint=False):
                stored, replay = self._reserve(initial)
                token = _IdempotentUnitToken(self, stored, replay)
                previous = self._unit_var.set(token)
                try:
                    try:
                        yield token
                        if (
                            token._failed
                            or not token._finalized
                            or transaction.get_rollback(using=self._using)
                        ):
                            raise _refused()
                    except BaseException:
                        token._failed = True
                        transaction.set_rollback(True, using=self._using)
                        raise
                finally:
                    token._active = False
                    self._unit_var.reset(previous)
