"""Plans C09 explicites : ressources accordées, demandées et observées distinctes.

Cette validation pure ne lance aucun processus, n'applique aucune limite OS et
n'atteste ni disponibilité ni performance d'un environnement. Les observations
effectives doivent venir du propriétaire serveur authentifié à l'entrée.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import json
from dataclasses import dataclass

from pixs.backend.c09_authorization_adapter import C09Refused, c09_text, c09_utc
from pixs.backend.c09_contracts import C09PolicyV1, validate_c09_policy
from pixs.kernel.manifest.semver import parse_version

__all__ = ["C09QueueBudgetV1", "C09RolePlanV1", "C09RuntimePlanV1",
           "C09BudgetObservationV1", "C09AppliedObservationV1",
           "validate_c09_runtime_plan", "c09_runtime_plan_sha256",
           "validate_c09_applied_observation", "c09_role_plan"]
_I32 = 2**31-1
_I64 = 2**63-1
_ROLES = ("SCHEDULER", "WEB", "WORKER")


@dataclass(frozen=True, slots=True)
class C09QueueBudgetV1:
    max_pending_jobs: int
    max_pending_schedules: int
    max_pending_events: int
    max_pending_deliveries: int
    max_event_bytes: int
    max_payload_refs: int
    buffer_bytes: int


@dataclass(frozen=True, slots=True)
class C09RolePlanV1:
    role: str
    policy: C09PolicyV1


@dataclass(frozen=True, slots=True)
class C09RuntimePlanV1:
    plan_reference: str
    plan_version: str
    owner_reference: str
    environment_reference: str
    roles: tuple[C09RolePlanV1, ...]
    queues: C09QueueBudgetV1


@dataclass(frozen=True, slots=True)
class C09BudgetObservationV1:
    source_reference: str
    source_version: str
    environment_reference: str
    revision: int
    observed_at: dt.datetime
    valid_until: dt.datetime
    detected_cpu_millicores: int | None
    detected_memory_mb: int | None
    granted_cpu_millicores: int
    granted_memory_mb: int
    granted_pg_connections: int
    granted_processes: int
    granted_concurrency: int
    reserved_cpu_millicores: int
    reserved_memory_mb: int
    reserved_pg_connections: int


@dataclass(frozen=True, slots=True)
class C09AppliedObservationV1:
    source_reference: str
    source_version: str
    environment_reference: str
    plan_sha256: str
    role: str
    process_index: int
    process_reference: str
    revision: int
    observed_at: dt.datetime
    valid_until: dt.datetime
    state: str
    cpu_millicores: int
    memory_mb: int
    pg_connections: int
    concurrency: int
    buffer_bytes: int
    process_counts: tuple[tuple[str, int], ...]


def _integer(value, *, zero=False, maximum=_I32):
    if type(value) is not int or not (0 if zero else 1) <= value <= maximum:
        raise C09Refused("C09_CAPACITY_INVALID")
    return value


def _version(value):
    c09_text(value)
    try:
        parse_version(value)
    except ValueError:
        raise C09Refused("C09_POLICY_UNRESOLVED") from None
    return value


def _fresh(observation, now):
    c09_utc(now)
    c09_text(observation.source_reference)
    _version(observation.source_version)
    c09_text(observation.environment_reference)
    _integer(observation.revision, maximum=_I64)
    c09_utc(observation.observed_at)
    c09_utc(observation.valid_until)
    if not observation.observed_at <= now < observation.valid_until:
        raise C09Refused("C09_TIME_INVALID")


def _plan(plan):
    if type(plan) is not C09RuntimePlanV1:
        raise C09Refused()
    for value in (plan.plan_reference, plan.owner_reference, plan.environment_reference):
        c09_text(value)
    _version(plan.plan_version)
    if type(plan.queues) is not C09QueueBudgetV1 or type(plan.roles) is not tuple or not plan.roles:
        raise C09Refused()
    for field in dataclasses.fields(C09QueueBudgetV1):
        _integer(getattr(plan.queues, field.name), maximum=_I64 if field.name=="buffer_bytes" else _I32)
    seen = []
    for role in plan.roles:
        if type(role) is not C09RolePlanV1 or type(role.role) is not str or role.role not in _ROLES:
            raise C09Refused()
        if validate_c09_policy(role.policy):
            raise C09Refused("C09_POLICY_UNRESOLVED")
        c09_text(role.policy.policy_reference)
        _version(role.policy.policy_version)
        if role.role in seen or (seen and seen[-1] >= role.role):
            raise C09Refused()
        seen.append(role.role)
        # Première boucle de traitement sérialisée ; les processus restent
        # explicitement réplicables, jamais déduits des cœurs physiques.
        if role.role in ("WORKER", "SCHEDULER") and role.policy.max_concurrency != 1:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        if role.policy.max_connections < 2*role.policy.max_concurrency+1:
            raise C09Refused("C09_CAPACITY_INVALID")
        required_buffer = plan.queues.max_event_bytes*role.policy.polling_max_batch
        if (plan.queues.buffer_bytes < required_buffer
                or plan.queues.buffer_bytes >= role.policy.memory_mb*1024*1024):
            raise C09Refused("C09_CAPACITY_INVALID")
    return plan


def c09_role_plan(plan, role):
    _plan(plan)
    if type(role) is not str:
        raise C09Refused()
    matches = [item for item in plan.roles if item.role == role]
    if len(matches) != 1:
        raise C09Refused("C09_POLICY_UNRESOLVED")
    return matches[0]


def c09_runtime_plan_sha256(plan):
    _plan(plan)
    document = dataclasses.asdict(plan)
    for item, original in zip(document["roles"], plan.roles, strict=True):
        item["policy"]["effective_from"] = original.policy.effective_from.isoformat()
    wire = json.dumps(document, sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(wire).hexdigest()


def validate_c09_runtime_plan(plan, budget, *, now):
    """Retourne les cumuls demandés après contrôle du budget effectif courant."""
    _plan(plan)
    if type(budget) is not C09BudgetObservationV1:
        raise C09Refused("C09_POLICY_UNRESOLVED")
    _fresh(budget, now)
    if budget.environment_reference != plan.environment_reference:
        raise C09Refused()
    for field in ("detected_cpu_millicores", "detected_memory_mb"):
        if getattr(budget, field) is not None:
            _integer(getattr(budget, field))
    for field in ("granted_cpu_millicores", "granted_memory_mb", "granted_pg_connections",
                  "granted_processes", "granted_concurrency"):
        _integer(getattr(budget, field))
    for field in ("reserved_cpu_millicores", "reserved_memory_mb", "reserved_pg_connections"):
        _integer(getattr(budget, field), zero=True)
    totals = {
        "cpu_millicores": sum(r.policy.process_count*r.policy.cpu_millicores for r in plan.roles),
        "memory_mb": sum(r.policy.process_count*r.policy.memory_mb for r in plan.roles),
        "pg_connections": sum(r.policy.process_count*r.policy.max_connections for r in plan.roles),
        "processes": sum(r.policy.process_count for r in plan.roles),
        "concurrency": sum(r.policy.process_count*r.policy.max_concurrency for r in plan.roles),
    }
    for key in ("cpu_millicores", "memory_mb", "pg_connections"):
        total = _integer(totals[key], maximum=_I64)
        if total+getattr(budget,"reserved_"+key) > getattr(budget,"granted_"+key):
            raise C09Refused("C09_CAPACITY_INVALID")
    if (totals["processes"] > budget.granted_processes
            or totals["concurrency"] > budget.granted_concurrency):
        raise C09Refused("C09_CAPACITY_INVALID")
    return totals


def validate_c09_applied_observation(plan, budget, applied, *, role, process_index, process_reference, now):
    """Contrôle l'observation propriétaire ; un plan accepté n'est pas une application."""
    validate_c09_runtime_plan(plan, budget, now=now)
    selected = c09_role_plan(plan, role)
    _integer(process_index, zero=True)
    c09_text(process_reference)
    if process_index >= selected.policy.process_count:
        raise C09Refused("C09_CAPACITY_INVALID")
    if type(applied) is not C09AppliedObservationV1:
        raise C09Refused("C09_POLICY_UNRESOLVED")
    _fresh(applied, now)
    c09_text(applied.plan_sha256)
    if len(applied.plan_sha256) != 64 or any(c not in "0123456789abcdef" for c in applied.plan_sha256):
        raise C09Refused("C09_CONTENT_DIVERGENT")
    if (type(applied.state) is not str or applied.state != "APPLIED"
            or applied.environment_reference != plan.environment_reference
            or applied.plan_sha256 != c09_runtime_plan_sha256(plan)
            or type(applied.role) is not str or applied.role != role
            or type(applied.process_index) is not int or applied.process_index != process_index
            or type(applied.process_reference) is not str or applied.process_reference != process_reference):
        raise C09Refused("C09_POLICY_UNRESOLVED")
    for field in ("cpu_millicores","memory_mb","pg_connections","concurrency","buffer_bytes"):
        _integer(getattr(applied,field), maximum=_I64 if field=="buffer_bytes" else _I32)
    expected = (selected.policy.cpu_millicores, selected.policy.memory_mb,
                selected.policy.max_connections, selected.policy.max_concurrency, plan.queues.buffer_bytes)
    actual = (applied.cpu_millicores, applied.memory_mb, applied.pg_connections, applied.concurrency, applied.buffer_bytes)
    if actual != expected or type(applied.process_counts) is not tuple:
        raise C09Refused("C09_CAPACITY_INVALID")
    counts = {}
    for pair in applied.process_counts:
        if type(pair) is not tuple or len(pair)!=2 or type(pair[0]) is not str:
            raise C09Refused()
        name, count = pair
        _integer(count, zero=True)
        if name in counts:
            raise C09Refused()
        selected_count = c09_role_plan(plan,name).policy.process_count
        if count > selected_count:
            raise C09Refused("C09_CAPACITY_INVALID")
        counts[name] = count
    if set(counts) != {r.role for r in plan.roles} or counts[role] <= process_index:
        raise C09Refused("C09_CAPACITY_INVALID")
    return selected
