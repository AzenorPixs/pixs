"""Façade serveur de demande d'annulation Bulk v1.

Compose l'autorité CANCEL courante vers la primitive CAS existante,
sans terminaliser ni reprendre le worker. Import inerte : sans Django,
ORM, environnement, réseau ou processus ; les dépendances ORM sont
chargées seulement après les gardes élémentaires.
"""

from __future__ import annotations

from pixs.kernel.diagnostics import VALIDATE, Diagnostic

__all__ = ["request_bulk_cancellation"]

_INT64_MAX = 2**63 - 1
_SCOPE = "bulk_server_cancellation"


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"{_SCOPE}.{field}",
        constraint=rule,
        message=rule,
    )


def _is_opaque_text(value: str) -> bool:
    if not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def request_bulk_cancellation(
    *,
    trusted_ports: object,
    runtime_repository: object,
    server_context: object,
    operation_id: object,
    expected_revision: object,
) -> tuple[int | None, list[Diagnostic]]:
    """Pose une demande d'annulation autorisée, sans annulation achevée."""
    if type(operation_id) is not str or not _is_opaque_text(operation_id):
        return None, [_refusal("operation_id", "référence opaque str exacte non vide UTF-8 sans NUL attendue")]
    if type(expected_revision) is not int:
        return None, [_refusal("expected_revision", "int exact attendu")]
    if expected_revision < 1 or expected_revision >= _INT64_MAX:
        return None, [_refusal("expected_revision", "révision exacte compatible N+1 attendue")]
    try:
        from pixs.backend.bulk_runtime_contracts import _AuthorityAssessmentSnapshot
        from pixs.backend.bulk_trusted_ports import _BulkTrustedPorts
    except ImportError:
        return None, [_refusal("capability", "capacité serveur indisponible")]
    if type(trusted_ports) is not _BulkTrustedPorts:
        return None, [_refusal("trusted_ports", "ports serveur exacts attendus")]
    try:
        from django.core.exceptions import (
            AppRegistryNotReady,
            ImproperlyConfigured,
            ValidationError,
        )
        from django.db import DatabaseError
        from django.utils.connection import ConnectionDoesNotExist
    except ImportError:
        return None, [_refusal("capability", "capacité serveur indisponible")]
    try:
        from pixs.backend.bulk_runtime_repository import (
            BulkRuntimeRepository,
            CasConflict,
            ConstraintRefused,
            TransitionRefused,
        )
    except (ImportError, ImproperlyConfigured, AppRegistryNotReady):
        return None, [_refusal("capability", "capacité serveur indisponible")]
    if type(runtime_repository) is not BulkRuntimeRepository:
        return None, [_refusal("runtime_repository", "repository exact attendu")]
    try:
        using = object.__getattribute__(runtime_repository, "_using")
    except AttributeError:
        return None, [_refusal("capability", "alias PostgreSQL déclaré attendu")]
    if type(using) is not str or not _is_opaque_text(using):
        return None, [_refusal("capability", "alias PostgreSQL déclaré attendu")]
    try:
        from django.db import connections

        vendor = connections[using].vendor
    except (ConnectionDoesNotExist, ImproperlyConfigured, ImportError, DatabaseError, AttributeError):
        return None, [_refusal("capability", "alias PostgreSQL déclaré attendu")]
    if type(vendor) is not str:
        return None, [_refusal("capability", "alias PostgreSQL déclaré attendu")]
    if vendor != "postgresql":
        return None, [_refusal("capability", "alias PostgreSQL déclaré attendu")]
    assessment = _BulkTrustedPorts.check_authority(
        trusted_ports,
        server_context=server_context,
        action="CANCEL",
        operation_reference=operation_id,
        resource_reference=None,
    )
    if type(assessment) is not tuple or len(assessment) != 2:
        return None, [_refusal("authority", "autorité refusée sans contexte exploitable")]
    snapshot, authority_diagnostics = assessment
    if type(authority_diagnostics) is not list:
        return None, [_refusal("authority", "autorité refusée sans contexte exploitable")]
    if authority_diagnostics:
        return None, [_refusal("authority", "autorité refusée sans contexte exploitable")]
    if snapshot is None:
        return None, [_refusal("authority", "autorité refusée sans contexte exploitable")]
    if type(snapshot) is not _AuthorityAssessmentSnapshot:
        return None, [_refusal("authority", "autorité refusée sans contexte exploitable")]
    decision = snapshot.decision
    if type(decision) is not str or decision != "ALLOW":
        return None, [_refusal("authority", "autorité refusée sans contexte exploitable")]
    try:
        new_revision = BulkRuntimeRepository.request_cancellation(
            runtime_repository,
            operation_id=operation_id,
            expected_revision=expected_revision,
        )
    except (CasConflict, TransitionRefused):
        return None, [_refusal("revision", "révision concurrente ou opération terminale refusée")]
    except (ValidationError, ConstraintRefused):
        return None, [_refusal("values", "valeurs refusées sans écho")]
    except DatabaseError:
        return None, [_refusal("capability", "capacité PostgreSQL indisponible")]
    if type(new_revision) is not int or new_revision != expected_revision + 1:
        return None, [_refusal("revision", "révision concurrente ou opération terminale refusée")]
    return new_revision, []
