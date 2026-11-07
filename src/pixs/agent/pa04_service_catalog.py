"""Catalogue local PA04 1A-2B-3A : validation integree, sans effet ni transport.

Noms locaux proposes a examiner, pas wire PZT. Version catalogue, bornes et allowlist fournies par profil serveur. Bornes locales en octets UTF-8, appliquees uniformement apres validation generique.
"""
from __future__ import annotations

from pixs.agent.contracts import AgentManagementInstruction, AgentParamSpec, AgentValidationContext, AllowedCatalogEntry, validate_agent_instruction
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.manifest.semver import parse_version

__all__ = ["PA04_OPERATIONS", "PA04_ALLOWED_ACTIONS", "build_pa04_catalog", "validate_pa04_instruction"]

PA04_OPERATIONS = ("OBSERVE", "PREPARE_PLAN", "START", "STOP", "READ_RESULT")

PA04_ALLOWED_ACTIONS = ("START", "STOP")


def _is_int_pos(value: object) -> bool:
    return type(value) is int and value >= 1


def _opaque_bytes_bounded(value: object, max_bytes: int) -> bool:
    if type(value) is not str or value == "":
        return False
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127 or 128 <= code <= 159:
            return False
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        return False
    return size <= max_bytes


def _check_allowlist(*, allowlist: object, max_bytes: int) -> tuple[str, ...] | None:
    if type(allowlist) is not tuple or not allowlist:
        return None
    seen: set[str] = set()
    for item in allowlist:
        if type(item) is not str:
            return None
        if not _opaque_bytes_bounded(item, max_bytes):
            return None
        if item in seen:
            return None
        seen.add(item)
    return allowlist


def _check_version(value: object) -> bool:
    if type(value) is not str:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def build_pa04_catalog(*, allowlist: tuple[str, ...], catalog_version: str, max_service_ref_len: int, max_plan_ref_len: int, max_operation_ref_len: int, max_action_len: int) -> tuple[AllowedCatalogEntry, ...]:
    for bound in (max_service_ref_len, max_plan_ref_len, max_operation_ref_len, max_action_len):
        if not _is_int_pos(bound):
            raise ValueError("borne explicite invalide")
    min_action = max(len(action.encode("utf-8")) for action in PA04_ALLOWED_ACTIONS)
    if max_action_len < min_action:
        raise ValueError("borne explicite insuffisante pour actions")
    checked = _check_allowlist(allowlist=allowlist, max_bytes=max_service_ref_len)
    if checked is None:
        raise ValueError("allowlist explicite invalide")
    if not _check_version(catalog_version):
        raise ValueError("version catalogue explicite invalide")
    service = AgentParamSpec(name="service_ref", kind="str", max_len=max_service_ref_len, int_min=None, int_max=None, required=True)
    plan = AgentParamSpec(name="plan_ref", kind="str", max_len=max_plan_ref_len, int_min=None, int_max=None, required=True)
    action = AgentParamSpec(name="action", kind="str", max_len=max_action_len, int_min=None, int_max=None, required=True)
    opref = AgentParamSpec(name="operation_ref", kind="str", max_len=max_operation_ref_len, int_min=None, int_max=None, required=True)
    shapes: dict[str, tuple[AgentParamSpec, ...]] = {"OBSERVE": (service,), "PREPARE_PLAN": (service, action), "START": (service, plan), "STOP": (service, plan), "READ_RESULT": (service, opref)}
    out: list[AllowedCatalogEntry] = []
    for operation in PA04_OPERATIONS:
        out.append(AllowedCatalogEntry(operation=operation, version=catalog_version, params=shapes[operation]))
    return tuple(out)


def validate_pa04_instruction(*, instruction: AgentManagementInstruction, context: AgentValidationContext, allowlist: tuple[str, ...], catalog_version: str, max_service_ref_len: int, max_plan_ref_len: int, max_operation_ref_len: int, max_action_len: int) -> tuple[Diagnostic, ...]:
    catalog = build_pa04_catalog(allowlist=allowlist, catalog_version=catalog_version, max_service_ref_len=max_service_ref_len, max_plan_ref_len=max_plan_ref_len, max_operation_ref_len=max_operation_ref_len, max_action_len=max_action_len)
    base = validate_agent_instruction(instruction, catalog, context)
    if base:
        return tuple(base)
    if instruction.catalog_operation not in PA04_OPERATIONS:
        return (Diagnostic(step=VALIDATE, element="agent.instruction.catalog", constraint="operation locale fermee exigee", message="operation locale fermee exigee"),)
    if instruction.catalog_version != catalog_version:
        return (Diagnostic(step=VALIDATE, element="agent.instruction.binding.version", constraint="version catalogue locale exigee", message="version catalogue locale exigee"),)
    values: dict[str, str] = {}
    for param in instruction.params:
        if param.kind != "str" or type(param.str_value) is not str:
            return (Diagnostic(step=VALIDATE, element="agent.instruction.param.kind", constraint="sorte str exacte exigee", message="sorte str exacte exigee"),)
        values[param.name] = param.str_value
    service_ref = values.get("service_ref")
    if service_ref is None or not _opaque_bytes_bounded(service_ref, max_service_ref_len) or service_ref not in allowlist:
        return (Diagnostic(step=VALIDATE, element="agent.instruction.param.name", constraint="service autorise inscrit exige", message="service autorise inscrit exige"),)
    if instruction.catalog_operation == "PREPARE_PLAN":
        action = values.get("action")
        if action is None or not _opaque_bytes_bounded(action, max_action_len) or action not in PA04_ALLOWED_ACTIONS:
            return (Diagnostic(step=VALIDATE, element="agent.instruction.param.name", constraint="action START ou STOP exigee", message="action START ou STOP exigee"),)
    if instruction.catalog_operation in ("START", "STOP"):
        plan_ref = values.get("plan_ref")
        if plan_ref is None or not _opaque_bytes_bounded(plan_ref, max_plan_ref_len):
            return (Diagnostic(step=VALIDATE, element="agent.instruction.param.required", constraint="reference syntaxique plan_ref exigee", message="reference syntaxique plan_ref exigee"),)
    if instruction.catalog_operation == "READ_RESULT":
        operation_ref = values.get("operation_ref")
        if operation_ref is None or not _opaque_bytes_bounded(operation_ref, max_operation_ref_len):
            return (Diagnostic(step=VALIDATE, element="agent.instruction.param.required", constraint="reference de resultat exigee", message="reference de resultat exigee"),)
    return ()
