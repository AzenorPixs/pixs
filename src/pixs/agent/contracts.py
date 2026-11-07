"""Contrats publics dédiés pixs.agent.management v1.0.0 : frontière seule.

Validation structurelle et comparaison à un contexte fourni, sans effet.
Ne prouve ni authentification, ni autorisation Core, ni persistance,
ni déduplication effective, ni transport, ni vérification cryptographique.
Comparaison structurale à l'opération/cible/génération/scope fournis :
un résultat ou état d'une autre opération est refusé, sans valoir preuve
d'identité, d'autorisation ou d'origine cryptographique.
Stdlib + `pixs.kernel.contracts.models`, `pixs.kernel.diagnostics`,
`pixs.core.scope`, `pixs.kernel.manifest.semver` uniquement.
Aucun import Bulk, privé, Django, psycopg, réseau, horloge ou I/O.
Bornes et catalogue fournis par le profil de confiance, sans plafond
implicite ni défaut inventé. Instants canoniques `YYYY-MM-DDTHH:MM:SSZ`,
comparés à l'instant fourni, sans lecture d'horloge.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass

from pixs.core.scope import ScopeContext, ScopeStructureError, validate_structure
from pixs.kernel.contracts.models import ContractCategory, ContractDescriptor
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "ALL_AGENT_CONTRACTS",
    "AgentManagementInstruction",
    "AgentManagementResult",
    "AgentManagementState",
    "AgentParam",
    "AgentParamSpec",
    "AgentValidationContext",
    "AllowedCatalogEntry",
    "CONTRACT_VERSION",
    "validate_agent_instruction",
    "validate_agent_result",
    "validate_agent_state",
]

CONTRACT_VERSION = "1.0.0"

_COMMAND_ID = "pixs.agent.management.command"
_QUERY_ID = "pixs.agent.management.query"
_SERVICE_ID = "pixs.agent.management.service"

COMMAND_DESCRIPTOR = ContractDescriptor(
    contract_id=_COMMAND_ID,
    category=ContractCategory.COMMAND,
    version=CONTRACT_VERSION,
    owner_component="pixs.agent",
    guarantees_doc="Instruction de gestion PA hors PZT : validation de frontière seule, sans effet ni transport.",
)
QUERY_DESCRIPTOR = ContractDescriptor(
    contract_id=_QUERY_ID,
    category=ContractCategory.QUERY,
    version=CONTRACT_VERSION,
    owner_component="pixs.agent",
    guarantees_doc="Lecture d'état de gestion PA : validation de frontière seule, sans mutation.",
)
SERVICE_DESCRIPTOR = ContractDescriptor(
    contract_id=_SERVICE_ID,
    category=ContractCategory.SERVICE,
    version=CONTRACT_VERSION,
    owner_component="pixs.agent",
    guarantees_doc="Point synchrone de gestion PA : validation de frontière seule, sans exécution.",
)
ALL_AGENT_CONTRACTS: tuple[ContractDescriptor, ...] = (
    COMMAND_DESCRIPTOR,
    QUERY_DESCRIPTOR,
    SERVICE_DESCRIPTOR,
)


def _diag(element: str, rule: str) -> Diagnostic:
    constraint = f"{element}: {rule}"
    return Diagnostic(step=VALIDATE, element=element, constraint=constraint, message=constraint)


def _finalize(items: list[Diagnostic]) -> list[Diagnostic]:
    seen: dict[tuple[str, str, str], Diagnostic] = {}
    for item in items:
        seen.setdefault((item.element, item.constraint, item.message), item)
    return sorted(seen.values(), key=lambda d: (d.element, d.constraint, d.message))


def _is_opaque(v: object, max_len: int) -> bool:
    return type(v) is str and v != "" and "\x00" not in v and len(v) <= max_len


def _check_semver(v: object) -> bool:
    if type(v) is not str:
        return False
    try:
        parse_version(v)
    except ValueError:
        return False
    return True


def _parse_canonical(v: object) -> datetime.datetime | None:
    if type(v) is not str or len(v) != 20:
        return None
    if v[4] != "-" or v[7] != "-" or v[10] != "T" or v[13] != ":" or v[16] != ":" or v[19] != "Z":
        return None
    for i in (0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18):
        if not "0" <= v[i] <= "9":
            return None
    try:
        return datetime.datetime(
            int(v[0:4]), int(v[5:7]), int(v[8:10]),
            int(v[11:13]), int(v[14:16]), int(v[17:19]),
        )
    except ValueError:
        return None


def _redacted(name: str) -> str:
    return name + "(<redacted>)"


def _check_ids(values: object, max_len: int, max_count: int) -> bool:
    if type(values) is not tuple or len(values) > max_count:
        return False
    for item in values:
        if not _is_opaque(item, max_len):
            return False
    return True


@dataclass(frozen=True, slots=True, repr=False)
class AgentParamSpec:
    name: str
    kind: str
    max_len: int | None
    int_min: int | None
    int_max: int | None
    required: bool

    def __repr__(self) -> str:
        return _redacted("AgentParamSpec")

    def __str__(self) -> str:
        return _redacted("AgentParamSpec")


@dataclass(frozen=True, slots=True, repr=False)
class AllowedCatalogEntry:
    operation: str
    version: str
    params: tuple[AgentParamSpec, ...]

    def __repr__(self) -> str:
        return _redacted("AllowedCatalogEntry")

    def __str__(self) -> str:
        return _redacted("AllowedCatalogEntry")


@dataclass(frozen=True, slots=True, repr=False)
class AgentParam:
    name: str
    kind: str
    str_value: str | None
    int_value: int | None
    bool_value: bool | None

    def __repr__(self) -> str:
        return _redacted("AgentParam")

    def __str__(self) -> str:
        return _redacted("AgentParam")


@dataclass(frozen=True, slots=True, repr=False)
class AgentValidationContext:
    expected_actor: str
    expected_scope: ScopeContext
    expected_target: str
    expected_generation: int
    expected_operation: str
    expected_version: str
    expected_operation_id: str
    expected_idempotency_key: str
    expected_correlation_ids: tuple[str, ...]
    now_iso: str
    mandate_proof: str
    expected_origin_proof: str | None
    expected_confirmation_proof: str | None
    max_id_len: int
    max_doc_len: int
    max_ids: int
    max_params: int
    max_observation_age_seconds: int

    def __repr__(self) -> str:
        return _redacted("AgentValidationContext")

    def __str__(self) -> str:
        return _redacted("AgentValidationContext")


@dataclass(frozen=True, slots=True, repr=False)
class AgentManagementInstruction:
    schema_version: str
    operation_id: str
    catalog_operation: str
    catalog_version: str
    initial_actor: str
    scope_context: ScopeContext
    pa_target: str
    expected_generation: int
    mandate_ref: str
    expires_at: str
    correlation_ids: tuple[str, ...]
    causation_ids: tuple[str, ...]
    idempotency_key: str
    params: tuple[AgentParam, ...]

    def __repr__(self) -> str:
        return _redacted("AgentManagementInstruction")

    def __str__(self) -> str:
        return _redacted("AgentManagementInstruction")


@dataclass(frozen=True, slots=True, repr=False)
class AgentManagementState:
    operation_id: str
    pa_target: str
    generation: int
    scope_context: ScopeContext
    desired_doc: str
    observed_doc: str | None
    observed_at: str | None
    last_known_doc: str | None
    last_known_at: str | None
    confirmation_proof: str | None

    def __repr__(self) -> str:
        return _redacted("AgentManagementState")

    def __str__(self) -> str:
        return _redacted("AgentManagementState")


@dataclass(frozen=True, slots=True, repr=False)
class AgentManagementResult:
    operation_id: str
    pa_target: str
    generation: int
    scope_context: ScopeContext
    outcome: str
    correlation_ids: tuple[str, ...]
    occurred_at: str
    origin_proof: str | None

    def __repr__(self) -> str:
        return _redacted("AgentManagementResult")

    def __str__(self) -> str:
        return _redacted("AgentManagementResult")


def _valid_spec(spec: object, max_id_len: int) -> bool:
    if type(spec) is not AgentParamSpec:
        return False
    name = object.__getattribute__(spec, "name")
    kind = object.__getattribute__(spec, "kind")
    max_len = object.__getattribute__(spec, "max_len")
    int_min = object.__getattribute__(spec, "int_min")
    int_max = object.__getattribute__(spec, "int_max")
    required = object.__getattribute__(spec, "required")
    if not _is_opaque(name, max_id_len):
        return False
    if not (type(kind) is str and (kind == "str" or kind == "int" or kind == "bool")):
        return False
    if type(required) is not bool:
        return False
    if kind == "str":
        if not (type(max_len) is int and max_len >= 1):
            return False
        if int_min is not None or int_max is not None:
            return False
    elif kind == "int":
        if max_len is not None:
            return False
        if not (type(int_min) is int and type(int_max) is int and int_min <= int_max):
            return False
    else:
        if max_len is not None or int_min is not None or int_max is not None:
            return False
    return True


def _valid_context(ctx: object) -> bool:
    if type(ctx) is not AgentValidationContext:
        return False
    scope = object.__getattribute__(ctx, "expected_scope")
    if type(scope) is not ScopeContext:
        return False
    try:
        validate_structure(scope)
    except ScopeStructureError:
        return False
    max_id = object.__getattribute__(ctx, "max_id_len")
    max_doc = object.__getattribute__(ctx, "max_doc_len")
    max_ids = object.__getattribute__(ctx, "max_ids")
    max_params = object.__getattribute__(ctx, "max_params")
    max_age = object.__getattribute__(ctx, "max_observation_age_seconds")
    for bound in (max_id, max_doc, max_ids, max_params, max_age):
        if type(bound) is not int or bound < 1:
            return False
    for field in ("expected_actor", "expected_target", "expected_operation", "expected_operation_id", "expected_idempotency_key", "mandate_proof"):
        if not _is_opaque(object.__getattribute__(ctx, field), max_id):
            return False
    for field in ("expected_origin_proof", "expected_confirmation_proof"):
        value = object.__getattribute__(ctx, field)
        if value is not None and not _is_opaque(value, max_id):
            return False
    if not _check_semver(object.__getattribute__(ctx, "expected_version")):
        return False
    if not (type(object.__getattribute__(ctx, "expected_generation")) is int and object.__getattribute__(ctx, "expected_generation") >= 0):
        return False
    if not _check_ids(object.__getattribute__(ctx, "expected_correlation_ids"), max_id, max_ids):
        return False
    if _parse_canonical(object.__getattribute__(ctx, "now_iso")) is None:
        return False
    return True


def validate_agent_instruction(instruction: object, allowed_catalog: object, context: object) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    if type(instruction) is not AgentManagementInstruction:
        return _finalize([_diag("agent.instruction", "instance exacte AgentManagementInstruction exigée")])
    if type(allowed_catalog) is not tuple:
        return _finalize([_diag("agent.catalog", "tuple exact d'entrées fermées exigé")])
    if not _valid_context(context):
        return _finalize([_diag("agent.context", "contexte de comparaison fourni invalide")])
    max_id = object.__getattribute__(context, "max_id_len")
    max_ids = object.__getattribute__(context, "max_ids")
    max_params = object.__getattribute__(context, "max_params")
    entries: list[AllowedCatalogEntry] = []
    seen_ops: set[tuple[str, str]] = set()
    for entry in allowed_catalog:
        if type(entry) is not AllowedCatalogEntry:
            return _finalize([_diag("agent.catalog.entry", "entrée exacte AllowedCatalogEntry exigée")])
        op = object.__getattribute__(entry, "operation")
        ver = object.__getattribute__(entry, "version")
        params = object.__getattribute__(entry, "params")
        if not _is_opaque(op, max_id) or not _check_semver(ver):
            return _finalize([_diag("agent.catalog.entry", "opération opaque et version SemVer exigées")])
        if type(params) is not tuple or len(params) > max_params:
            return _finalize([_diag("agent.catalog.params", "tuple exact de descripteurs borné exigé")])
        names: set[str] = set()
        for spec in params:
            if not _valid_spec(spec, max_id):
                return _finalize([_diag("agent.catalog.param", "descripteur fermé type/borne exigé")])
            spec_name = object.__getattribute__(spec, "name")
            if spec_name in names:
                return _finalize([_diag("agent.catalog.param", "nom de paramètre dupliqué refusé")])
            names.add(spec_name)
        if (op, ver) in seen_ops:
            return _finalize([_diag("agent.catalog.entry", "doublon opération/version refusé")])
        seen_ops.add((op, ver))
        entries.append(entry)
    schem = object.__getattribute__(instruction, "schema_version")
    if not (type(schem) is str and schem == "1.0.0"):
        out.append(_diag("agent.instruction.schema_version", "version exacte 1.0.0 exigée"))
    for field in ("operation_id", "catalog_operation", "initial_actor", "pa_target", "mandate_ref", "idempotency_key"):
        if not _is_opaque(object.__getattribute__(instruction, field), max_id):
            out.append(_diag(f"agent.instruction.{field}", "chaîne opaque exacte non vide bornée exigée"))
    if not _check_semver(object.__getattribute__(instruction, "catalog_version")):
        out.append(_diag("agent.instruction.catalog_version", "version SemVer exacte exigée"))
    gen = object.__getattribute__(instruction, "expected_generation")
    if not (type(gen) is int and gen >= 0):
        out.append(_diag("agent.instruction.expected_generation", "entier exact positif exigé, bool refusé"))
    scope = object.__getattribute__(instruction, "scope_context")
    if type(scope) is not ScopeContext:
        out.append(_diag("agent.instruction.scope_context", "instance exacte ScopeContext exigée"))
    else:
        try:
            validate_structure(scope)
        except ScopeStructureError:
            out.append(_diag("agent.instruction.scope_context", "structure ScopeContext refusée"))
    if not _check_ids(object.__getattribute__(instruction, "correlation_ids"), max_id, max_ids):
        out.append(_diag("agent.instruction.correlation_ids", "tuple exact d'opaques bornés exigé"))
    if not _check_ids(object.__getattribute__(instruction, "causation_ids"), max_id, max_ids):
        out.append(_diag("agent.instruction.causation_ids", "tuple exact d'opaques bornés exigé"))
    params = object.__getattribute__(instruction, "params")
    if type(params) is not tuple or len(params) > max_params:
        out.append(_diag("agent.instruction.params", "tuple exact de paramètres borné exigé"))
        return _finalize(out)
    for param in params:
        if type(param) is not AgentParam:
            out.append(_diag("agent.instruction.param", "instance exacte AgentParam exigée"))
            return _finalize(out)
        pname = object.__getattribute__(param, "name")
        pkind = object.__getattribute__(param, "kind")
        if not _is_opaque(pname, max_id):
            out.append(_diag("agent.instruction.param.name", "nom opaque exact exigé, non hashable refusé"))
            continue
        if not (type(pkind) is str and (pkind == "str" or pkind == "int" or pkind == "bool")):
            out.append(_diag("agent.instruction.param.kind", "sorte exacte str/int/bool exigée"))
            continue
    if out:
        return _finalize(out)
    if object.__getattribute__(instruction, "initial_actor") != object.__getattribute__(context, "expected_actor"):
        out.append(_diag("agent.instruction.binding.actor", "liaison acteur fournie refusée"))
    if object.__getattribute__(instruction, "scope_context") != object.__getattribute__(context, "expected_scope"):
        out.append(_diag("agent.instruction.binding.scope", "liaison scope fourni refusée"))
    if object.__getattribute__(instruction, "pa_target") != object.__getattribute__(context, "expected_target"):
        out.append(_diag("agent.instruction.binding.target", "liaison cible fournie refusée"))
    if gen != object.__getattribute__(context, "expected_generation"):
        out.append(_diag("agent.instruction.binding.generation", "liaison génération fournie refusée"))
    if object.__getattribute__(instruction, "catalog_operation") != object.__getattribute__(context, "expected_operation"):
        out.append(_diag("agent.instruction.binding.operation", "liaison opération fournie refusée"))
    if object.__getattribute__(instruction, "catalog_version") != object.__getattribute__(context, "expected_version"):
        out.append(_diag("agent.instruction.binding.version", "liaison version fournie refusée"))
    if object.__getattribute__(instruction, "operation_id") != object.__getattribute__(context, "expected_operation_id"):
        out.append(_diag("agent.instruction.binding.operation_id", "liaison identifiant d'opération refusée"))
    if object.__getattribute__(instruction, "idempotency_key") != object.__getattribute__(context, "expected_idempotency_key"):
        out.append(_diag("agent.instruction.binding.idempotence", "liaison idempotence fournie refusée"))
    if object.__getattribute__(instruction, "correlation_ids") != object.__getattribute__(context, "expected_correlation_ids"):
        out.append(_diag("agent.instruction.binding.correlation", "liaison corrélation fournie refusée"))
    if object.__getattribute__(instruction, "mandate_ref") != object.__getattribute__(context, "mandate_proof"):
        out.append(_diag("agent.instruction.binding.mandate", "preuve de mandat requise absente ou incohérente"))
    exp_instant = _parse_canonical(object.__getattribute__(instruction, "expires_at"))
    now_instant = _parse_canonical(object.__getattribute__(context, "now_iso"))
    if exp_instant is None:
        out.append(_diag("agent.instruction.expires_at", "instant canonique YYYY-MM-DDTHH:MM:SSZ exigé"))
    elif now_instant is None or exp_instant <= now_instant:
        out.append(_diag("agent.instruction.expires_at", "échéance expirée au regard de l'instant fourni"))
    match: AllowedCatalogEntry | None = None
    for entry in entries:
        if object.__getattribute__(entry, "operation") == object.__getattribute__(instruction, "catalog_operation") and object.__getattribute__(entry, "version") == object.__getattribute__(instruction, "catalog_version"):
            match = entry
            break
    if match is None:
        out.append(_diag("agent.instruction.catalog", "opération/version fermées inconnues refusées"))
        return _finalize(out)
    specs = {object.__getattribute__(s, "name"): s for s in object.__getattribute__(match, "params")}
    seen: set[str] = set()
    for param in params:
        pname = object.__getattribute__(param, "name")
        pkind = object.__getattribute__(param, "kind")
        if type(pname) is not str:
            continue
        if pname in seen:
            out.append(_diag("agent.instruction.param.name", "paramètre dupliqué refusé"))
            continue
        seen.add(pname)
        spec = specs.get(pname)
        if spec is None:
            out.append(_diag("agent.instruction.param.name", "champ étranger hors catalogue refusé"))
            continue
        if pkind != object.__getattribute__(spec, "kind"):
            out.append(_diag("agent.instruction.param.kind", "sorte bool/int/str incohérente refusée"))
            continue
        svalue = object.__getattribute__(param, "str_value")
        ivalue = object.__getattribute__(param, "int_value")
        bvalue = object.__getattribute__(param, "bool_value")
        if pkind == "str":
            bound = object.__getattribute__(spec, "max_len")
            if not (type(svalue) is str and "\x00" not in svalue and len(svalue) <= bound):
                out.append(_diag("agent.instruction.param.str", "chaîne typée bornée exigée"))
            if ivalue is not None or bvalue is not None:
                out.append(_diag("agent.instruction.param.exclusive", "valeur exclusive selon sorte exigée"))
        elif pkind == "int":
            low = object.__getattribute__(spec, "int_min")
            high = object.__getattribute__(spec, "int_max")
            if not (type(ivalue) is int and low <= ivalue <= high):
                out.append(_diag("agent.instruction.param.int", "entier typé borné exigé, bool refusé"))
            if svalue is not None or bvalue is not None:
                out.append(_diag("agent.instruction.param.exclusive", "valeur exclusive selon sorte exigée"))
        else:
            if type(bvalue) is not bool:
                out.append(_diag("agent.instruction.param.bool", "booléen exact exigé, int refusé"))
            if svalue is not None or ivalue is not None:
                out.append(_diag("agent.instruction.param.exclusive", "valeur exclusive selon sorte exigée"))
    for sname, spec in specs.items():
        if object.__getattribute__(spec, "required") is True and sname not in seen:
            out.append(_diag("agent.instruction.param.required", "paramètre requis absent refusé"))
    return _finalize(out)


def _scope_diagnostics(scope: object, expected: ScopeContext, prefix: str) -> list[Diagnostic]:
    if type(scope) is not ScopeContext:
        return [_diag(prefix + ".scope_context", "instance exacte ScopeContext exigée")]
    try:
        validate_structure(scope)
    except ScopeStructureError:
        return [_diag(prefix + ".scope_context", "structure ScopeContext refusée")]
    if scope != expected:
        return [_diag(prefix + ".binding.scope", "liaison scope fourni refusée")]
    return []


def validate_agent_state(state: object, context: object) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    if type(state) is not AgentManagementState:
        return _finalize([_diag("agent.state", "instance exacte AgentManagementState exigée")])
    if not _valid_context(context):
        return _finalize([_diag("agent.context", "contexte de comparaison fourni invalide")])
    out.extend(_scope_diagnostics(
        object.__getattribute__(state, "scope_context"),
        object.__getattribute__(context, "expected_scope"),
        "agent.state",
    ))
    max_id = object.__getattribute__(context, "max_id_len")
    max_doc = object.__getattribute__(context, "max_doc_len")
    max_age = object.__getattribute__(context, "max_observation_age_seconds")
    now_instant = _parse_canonical(object.__getattribute__(context, "now_iso"))
    for field in ("operation_id", "pa_target"):
        if not _is_opaque(object.__getattribute__(state, field), max_id):
            out.append(_diag(f"agent.state.{field}", "chaîne opaque exacte bornée exigée"))
    gen = object.__getattribute__(state, "generation")
    if not (type(gen) is int and gen >= 0):
        out.append(_diag("agent.state.generation", "entier exact positif exigé, bool refusé"))
    desired = object.__getattribute__(state, "desired_doc")
    if not (type(desired) is str and desired != "" and "\x00" not in desired and len(desired) <= max_doc):
        out.append(_diag("agent.state.desired_doc", "document souhaité opaque borné exigé"))
    observed = object.__getattribute__(state, "observed_doc")
    observed_at_raw = object.__getattribute__(state, "observed_at")
    observed_parsed = None
    if observed is None:
        if observed_at_raw is not None:
            out.append(_diag("agent.state.observed", "absence et date gardées distinctes"))
    else:
        if not _is_opaque(observed, max_doc):
            out.append(_diag("agent.state.observed_doc", "document observé opaque borné exigé"))
        observed_parsed = _parse_canonical(observed_at_raw)
        if observed_parsed is None or observed_parsed > now_instant:
            out.append(_diag("agent.state.observed_at", "instant observé canonique non futur exigé"))
    last_doc = object.__getattribute__(state, "last_known_doc")
    last_at_raw = object.__getattribute__(state, "last_known_at")
    last_parsed = None
    if last_doc is None:
        if last_at_raw is not None:
            out.append(_diag("agent.state.last_known", "absence et date gardées distinctes"))
    else:
        if not _is_opaque(last_doc, max_doc):
            out.append(_diag("agent.state.last_known_doc", "document connu opaque borné exigé"))
        last_parsed = _parse_canonical(last_at_raw)
        if last_parsed is None or last_parsed > now_instant:
            out.append(_diag("agent.state.last_known_at", "instant connu canonique non futur exigé"))
        elif observed_parsed is not None and last_parsed < observed_parsed:
            out.append(_diag("agent.state.last_known_at", "cohérence temporelle observé/connue exigée"))
    proof = object.__getattribute__(state, "confirmation_proof")
    expected_proof = object.__getattribute__(context, "expected_confirmation_proof")
    if proof is None:
        pass
    else:
        if type(proof) is not str or proof != expected_proof:
            out.append(_diag("agent.state.confirmation", "preuve de confirmation attendue incohérente refusée"))
        elif observed is None or observed_parsed is None:
            out.append(_diag("agent.state.confirmation", "confirmation sans observé refusée"))
        elif (now_instant - observed_parsed).total_seconds() > max_age:
            out.append(_diag("agent.state.confirmation", "observation périmée au regard de la fraîcheur fournie"))
    if out:
        return _finalize(out)
    if object.__getattribute__(state, "operation_id") != object.__getattribute__(context, "expected_operation_id"):
        out.append(_diag("agent.state.binding.operation_id", "liaison identifiant d'opération refusée"))
    if object.__getattribute__(state, "pa_target") != object.__getattribute__(context, "expected_target"):
        out.append(_diag("agent.state.binding.target", "liaison cible fournie refusée"))
    if gen != object.__getattribute__(context, "expected_generation"):
        out.append(_diag("agent.state.binding.generation", "liaison génération fournie refusée"))
    return _finalize(out)


def validate_agent_result(result: object, context: object) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    if type(result) is not AgentManagementResult:
        return _finalize([_diag("agent.result", "instance exacte AgentManagementResult exigée")])
    if not _valid_context(context):
        return _finalize([_diag("agent.context", "contexte de comparaison fourni invalide")])
    out.extend(_scope_diagnostics(
        object.__getattribute__(result, "scope_context"),
        object.__getattribute__(context, "expected_scope"),
        "agent.result",
    ))
    max_id = object.__getattribute__(context, "max_id_len")
    max_ids = object.__getattribute__(context, "max_ids")
    now_instant = _parse_canonical(object.__getattribute__(context, "now_iso"))
    for field in ("operation_id", "pa_target"):
        if not _is_opaque(object.__getattribute__(result, field), max_id):
            out.append(_diag(f"agent.result.{field}", "chaîne opaque exacte bornée exigée"))
    gen = object.__getattribute__(result, "generation")
    if not (type(gen) is int and gen >= 0):
        out.append(_diag("agent.result.generation", "entier exact positif exigé, bool refusé"))
    outcome = object.__getattribute__(result, "outcome")
    if not (type(outcome) is str and (outcome == "ack" or outcome == "confirmed" or outcome == "failed" or outcome == "unknown")):
        out.append(_diag("agent.result.outcome", "issue fermée ack/confirmed/failed/unknown exigée"))
        return _finalize(out)
    if not _check_ids(object.__getattribute__(result, "correlation_ids"), max_id, max_ids):
        out.append(_diag("agent.result.correlation_ids", "tuple exact d'opaques bornés exigé"))
    occurred_parsed = _parse_canonical(object.__getattribute__(result, "occurred_at"))
    if occurred_parsed is None or occurred_parsed > now_instant:
        out.append(_diag("agent.result.occurred_at", "instant survenu canonique non futur exigé"))
    proof = object.__getattribute__(result, "origin_proof")
    expected_origin = object.__getattribute__(context, "expected_origin_proof")
    if outcome == "unknown":
        if proof is not None:
            out.append(_diag("agent.result.origin", "issue inconnue sans preuve gardée distincte"))
    else:
        if type(proof) is not str or proof != expected_origin:
            out.append(_diag("agent.result.origin", "preuve d'origine attendue incohérente refusée"))
    if out:
        return _finalize(out)
    if object.__getattribute__(result, "operation_id") != object.__getattribute__(context, "expected_operation_id"):
        out.append(_diag("agent.result.binding.operation_id", "liaison identifiant d'opération refusée"))
    if object.__getattribute__(result, "pa_target") != object.__getattribute__(context, "expected_target"):
        out.append(_diag("agent.result.binding.target", "liaison cible fournie refusée"))
    if gen != object.__getattribute__(context, "expected_generation"):
        out.append(_diag("agent.result.binding.generation", "liaison génération fournie refusée"))
    if object.__getattribute__(result, "correlation_ids") != object.__getattribute__(context, "expected_correlation_ids"):
        out.append(_diag("agent.result.binding.correlation", "liaison corrélation fournie refusée"))
    return _finalize(out)
