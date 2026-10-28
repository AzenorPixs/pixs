"""Contrats C09 2.1 : valeurs Python pures, structurelles seules.

Aucune persistance, transaction, publication, exécution, boucle, worker,
scheduler, migration, provider, callback ni runtime. Validations
exact-type-first, fermées, sans coercition, sans appel de méthode sur une
valeur étrangère, sans secret ni écho de valeur brute. Diagnostics
statiques, triés et dédupliqués.

Seules bornes techniques de représentation : entier signé PostgreSQL
(INT32). Aucun plafond opérationnel caché : les plafonds d'exploitation
restent des entrées explicites versionnées de la politique. Les cohérences
sont relationnelles entre champs, sans valeur produit par défaut.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass

from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.event_contract import (
    DomainEventContract,
    IntegrationEventContract,
    validate_domain_event_contract,
    validate_integration_event_contract,
)
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "C09PolicyV1",
    "C09EventBindingV1",
    "C09ConsumerDeclarationV1",
    "C09RoleDeclarationV1",
    "validate_c09_policy",
    "validate_c09_event_binding",
    "validate_c09_consumer_declaration",
    "validate_c09_role_declaration",
]

_INT32_MAX = 2**31 - 1


def _refusal(element: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=element,
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_exact_non_empty_str(value: object) -> bool:
    return type(value) is str and bool(value)


def _is_exact_int_in(value: object, low: int, high: int) -> bool:
    if type(value) is not int:
        return False
    return low <= value <= high


def _is_semver(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _is_utc_instant(value: object) -> bool:
    if type(value) is not datetime.datetime:
        return False
    return value.tzinfo is datetime.timezone.utc


@dataclass(frozen=True, slots=True)
class C09PolicyV1:
    """Politique C09 explicite versionnée, sans défaut produit."""

    policy_reference: str
    policy_version: str
    lease_seconds: int
    renewal_seconds: int
    max_attempts: int
    retry_delays_seconds: tuple[int, ...]
    polling_interval_ms: int
    polling_max_batch: int
    max_concurrency: int
    max_units_per_poll: int
    drain_seconds: int
    attempt_timeout_seconds: int
    job_timeout_seconds: int
    process_count: int
    cpu_millicores: int
    max_connections: int
    memory_mb: int
    effective_from: datetime.datetime


@dataclass(frozen=True, slots=True)
class C09EventBindingV1:
    """Liaison structurelle seule vers un contrat existant."""

    owner_reference: str
    entry_reference: str
    contract: DomainEventContract | IntegrationEventContract
    perimeter_reference: str
    tenant_context_reference: str | None


@dataclass(frozen=True, slots=True)
class C09ConsumerDeclarationV1:
    """Déclaration passive de consommateur liée à une liaison existante."""

    consumer_reference: str
    entry_reference: str
    consumer_version: str
    component_reference: str
    event_contract_version: str


@dataclass(frozen=True, slots=True)
class C09RoleDeclarationV1:
    """Rôle déclaratif fermé, référence versionnée sans fonction."""

    role: str
    handler_reference: str
    handler_version: str
    component_reference: str


def validate_c09_policy(candidate: object) -> list[Diagnostic]:
    """Valide une politique C09 explicite, sans écho ni effet."""
    if type(candidate) is not C09PolicyV1:
        return [_refusal("c09_policy", "politique exacte attendue")]
    refusals: list[Diagnostic] = []
    if not _is_exact_non_empty_str(candidate.policy_reference):
        refusals.append(
            _refusal("c09_policy.policy_reference", "référence opaque exacte non vide attendue")
        )
    if not _is_semver(candidate.policy_version):
        refusals.append(
            _refusal("c09_policy.policy_version", "version SemVer complète attendue")
        )
    if not _is_exact_int_in(candidate.lease_seconds, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.lease_seconds", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.renewal_seconds, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.renewal_seconds", "entier exact borné attendu")
        )
    if type(candidate.max_attempts) is not int:
        refusals.append(
            _refusal("c09_policy.max_attempts", "entier exact borné attendu")
        )
    elif not 1 <= candidate.max_attempts <= _INT32_MAX:
        refusals.append(
            _refusal("c09_policy.max_attempts", "entier exact borné attendu")
        )
    delays = candidate.retry_delays_seconds
    if type(candidate.max_attempts) is not int:
        refusals.append(
            _refusal("c09_policy.retry_delays_seconds", "politique invalide sans cohérence vérifiable")
        )
    elif type(delays) is not tuple:
        refusals.append(
            _refusal("c09_policy.retry_delays_seconds", "tuple exact attendu")
        )
    elif len(delays) != candidate.max_attempts - 1:
        refusals.append(
            _refusal(
                "c09_policy.retry_delays_seconds",
                "longueur max_attempts moins un attendue",
            )
        )
    else:
        for _delay in delays:
            if not _is_exact_int_in(_delay, 1, _INT32_MAX):
                refusals.append(
                    _refusal("c09_policy.retry_delays_seconds", "entier exact borné attendu")
                )
                break
    if not _is_exact_int_in(candidate.polling_interval_ms, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.polling_interval_ms", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.polling_max_batch, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.polling_max_batch", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.max_concurrency, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.max_concurrency", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.max_units_per_poll, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.max_units_per_poll", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.drain_seconds, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.drain_seconds", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.attempt_timeout_seconds, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.attempt_timeout_seconds", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.job_timeout_seconds, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.job_timeout_seconds", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.process_count, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.process_count", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.cpu_millicores, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.cpu_millicores", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.max_connections, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.max_connections", "entier exact borné attendu")
        )
    if not _is_exact_int_in(candidate.memory_mb, 1, _INT32_MAX):
        refusals.append(
            _refusal("c09_policy.memory_mb", "entier exact borné attendu")
        )
    if not _is_utc_instant(candidate.effective_from):
        refusals.append(
            _refusal("c09_policy.effective_from", "instant UTC exact attendu")
        )
    if (
        type(candidate.lease_seconds) is int
        and type(candidate.renewal_seconds) is int
        and not 2 * candidate.renewal_seconds < candidate.lease_seconds
    ):
        refusals.append(
            _refusal("c09_policy.renewal_seconds", "marge deux fois renouvellement sous bail attendue")
        )
    if (
        type(candidate.attempt_timeout_seconds) is int
        and type(candidate.job_timeout_seconds) is int
        and not candidate.attempt_timeout_seconds <= candidate.job_timeout_seconds
    ):
        refusals.append(
            _refusal("c09_policy.attempt_timeout_seconds", "cohérence tentative sous travail attendue")
        )
    if (
        type(candidate.polling_max_batch) is int
        and type(candidate.max_units_per_poll) is int
        and not candidate.polling_max_batch <= candidate.max_units_per_poll
    ):
        refusals.append(
            _refusal("c09_policy.polling_max_batch", "cohérence lot sous unités attendue")
        )
    return _pack(refusals)


def validate_c09_event_binding(candidate: object) -> list[Diagnostic]:
    """Valide une liaison structurelle avec contrat porté exact vérifié."""
    if type(candidate) is not C09EventBindingV1:
        return [_refusal("c09_event_binding", "liaison exacte attendue")]
    refusals: list[Diagnostic] = []
    if not _is_exact_non_empty_str(candidate.owner_reference):
        refusals.append(
            _refusal("c09_event_binding.owner_reference", "référence opaque exacte non vide attendue")
        )
    if not _is_exact_non_empty_str(candidate.entry_reference):
        refusals.append(
            _refusal("c09_event_binding.entry_reference", "référence opaque exacte non vide attendue")
        )
    contract = candidate.contract
    if type(contract) is DomainEventContract:
        refusals.extend(validate_domain_event_contract(contract))
    elif type(contract) is IntegrationEventContract:
        refusals.extend(validate_integration_event_contract(contract))
    else:
        refusals.append(
            _refusal("c09_event_binding.contract", "contrat exact existant attendu")
        )
    if not _is_exact_non_empty_str(candidate.perimeter_reference):
        refusals.append(
            _refusal("c09_event_binding.perimeter_reference", "référence opaque exacte non vide attendue")
        )
    tenant = candidate.tenant_context_reference
    if tenant is not None and not _is_exact_non_empty_str(tenant):
        refusals.append(
            _refusal(
                "c09_event_binding.tenant_context_reference",
                "référence opaque exacte ou absence explicite attendue",
            )
        )
    return _pack(refusals)


def validate_c09_consumer_declaration(candidate: object) -> list[Diagnostic]:
    """Valide une déclaration passive de consommateur, sans exécution."""
    if type(candidate) is not C09ConsumerDeclarationV1:
        return [_refusal("c09_consumer", "consommateur exact attendu")]
    refusals: list[Diagnostic] = []
    if not _is_exact_non_empty_str(candidate.consumer_reference):
        refusals.append(
            _refusal("c09_consumer.consumer_reference", "référence opaque exacte non vide attendue")
        )
    if not _is_exact_non_empty_str(candidate.entry_reference):
        refusals.append(
            _refusal("c09_consumer.entry_reference", "référence opaque exacte non vide attendue")
        )
    if not _is_semver(candidate.consumer_version):
        refusals.append(
            _refusal("c09_consumer.consumer_version", "version SemVer complète attendue")
        )
    if not _is_exact_non_empty_str(candidate.component_reference):
        refusals.append(
            _refusal("c09_consumer.component_reference", "référence opaque exacte non vide attendue")
        )
    if not _is_semver(candidate.event_contract_version):
        refusals.append(
            _refusal("c09_consumer.event_contract_version", "version SemVer complète attendue")
        )
    return _pack(refusals)


def validate_c09_role_declaration(candidate: object) -> list[Diagnostic]:
    """Valide un rôle déclaratif fermé, type d'abord, sans appel hostile."""
    if type(candidate) is not C09RoleDeclarationV1:
        return [_refusal("c09_role", "rôle exact attendu")]
    refusals: list[Diagnostic] = []
    role = candidate.role
    if type(role) is not str:
        refusals.append(_refusal("c09_role.role", "rôle fermé attendu"))
    elif role != "web" and role != "worker" and role != "scheduler":
        refusals.append(_refusal("c09_role.role", "rôle fermé attendu"))
    if not _is_exact_non_empty_str(candidate.handler_reference):
        refusals.append(
            _refusal("c09_role.handler_reference", "référence opaque exacte non vide attendue")
        )
    if not _is_semver(candidate.handler_version):
        refusals.append(
            _refusal("c09_role.handler_version", "version SemVer complète attendue")
        )
    if not _is_exact_non_empty_str(candidate.component_reference):
        refusals.append(
            _refusal("c09_role.component_reference", "référence opaque exacte non vide attendue")
        )
    return _pack(refusals)
