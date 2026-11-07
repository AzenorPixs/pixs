"""Contrats publics dedies pixs.agent.management v2.0.0 : frontiere seule UTC six decimales.

Validation structurelle et comparaison a un contexte fourni, sans effet.
Ne prouve ni authentification, ni autorisation Core, ni persistance,
ni deduplication effective, ni transport, ni verification cryptographique,
ni autorite temporelle, ni synchronisation UTC, ni confiance.
Comparaison structurale a l'operation/cible/generation/scope fournis.
Stdlib + pixs.agent.contracts types publics et helpers prives stables,
pixs.agent.identifiers grammaire UTC6, pixs.core.scope,
pixs.kernel.contracts.models, pixs.kernel.diagnostics uniquement.
Aucun import Bulk, prive metier, Django, psycopg, reseau, horloge ou I/O.
Bornes et catalogue fournis par le profil de confiance existant, sans plafond
implicite ni defaut invente. Instants canoniques YYYY-MM-DDTHH:MM:SS.ffffffZ
compares a l'instant fourni exact, sans lecture d'horloge, sans flottant,
sans total_seconds, sans conversion vers v1. contracts.py et 1.0.0 inchanges.
Selection explicite via ce module v2, sans enregistrement automatique,
sans fallback, sans globals ni monkeypatch.
"""
from __future__ import annotations

import datetime

from pixs.agent import identifiers as ids
from pixs.agent.contracts import (
    _check_ids,
    _check_semver,
    _diag,
    _finalize,
    _is_opaque,
    _valid_spec,
    AgentManagementInstruction,
    AgentManagementResult,
    AgentManagementState,
    AgentValidationContext,
    AllowedCatalogEntry,
)
from pixs.core.scope import ScopeContext, ScopeStructureError, validate_structure
from pixs.kernel.contracts.models import ContractCategory, ContractDescriptor
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

CONTRACT_VERSION_V2 = "2.0.0"

_V2_COMMAND_ID = "pixs.agent.management.command"
_V2_QUERY_ID = "pixs.agent.management.query"
_V2_SERVICE_ID = "pixs.agent.management.service"

COMMAND_DESCRIPTOR_V2 = ContractDescriptor(
    contract_id=_V2_COMMAND_ID,
    category=ContractCategory.COMMAND,
    version=CONTRACT_VERSION_V2,
    owner_component="pixs.agent",
    guarantees_doc="Instruction de gestion PA hors PZT v2 : validation de frontiere seule UTC six decimales, sans effet ni transport ni autorite temporelle.",
)
QUERY_DESCRIPTOR_V2 = ContractDescriptor(
    contract_id=_V2_QUERY_ID,
    category=ContractCategory.QUERY,
    version=CONTRACT_VERSION_V2,
    owner_component="pixs.agent",
    guarantees_doc="Lecture d'etat de gestion PA v2 : validation de frontiere seule UTC six decimales, sans mutation ni confiance.",
)
SERVICE_DESCRIPTOR_V2 = ContractDescriptor(
    contract_id=_V2_SERVICE_ID,
    category=ContractCategory.SERVICE,
    version=CONTRACT_VERSION_V2,
    owner_component="pixs.agent",
    guarantees_doc="Point synchrone de gestion PA v2 : validation de frontiere seule UTC six decimales, sans execution ni autorite temporelle.",
)
ALL_AGENT_CONTRACTS_V2: tuple[ContractDescriptor, ...] = (
    COMMAND_DESCRIPTOR_V2,
    QUERY_DESCRIPTOR_V2,
    SERVICE_DESCRIPTOR_V2,
)


def _parse_v2(value: object) -> datetime.datetime | None:
    if type(value) is not str:
        return None
    try:
        ids.require_canonical_instant_v2(value)
    except ids.AgentIdentifierError:
        return None
    assert isinstance(value, str)
    try:
        return datetime.datetime(
            int(value[0:4]),
            int(value[5:7]),
            int(value[8:10]),
            int(value[11:13]),
            int(value[14:16]),
            int(value[17:19]),
            int(value[20:26]),
        )
    except ValueError:
        return None


def _age_us(now: datetime.datetime, earlier: datetime.datetime) -> int:
    delta = now - earlier
    return (delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds


def _valid_context_v2(ctx: object) -> bool:
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
    if _parse_v2(object.__getattribute__(ctx, "now_iso")) is None:
        return False
    return True


def _scope_v2(scope: object, expected: ScopeContext, prefix: str) -> list[Diagnostic]:
    if type(scope) is not ScopeContext:
        return [_diag(prefix + ".scope_context", "instance exacte ScopeContext exigee")]
    try:
        validate_structure(scope)
    except ScopeStructureError:
        return [_diag(prefix + ".scope_context", "structure ScopeContext refusee")]
    if scope != expected:
        return [_diag(prefix + ".binding.scope", "liaison scope fourni refusee")]
    return []


def _catalog_entries(allowed_catalog: object, max_id: int, max_params: int) -> tuple[list[AllowedCatalogEntry], list[Diagnostic]]:
    entries: list[AllowedCatalogEntry] = []
    if type(allowed_catalog) is not tuple:
        return entries, [_diag("agent.catalog", "tuple exact d'entrees fermees exige")]
    seen_ops: set[tuple[str, str]] = set()
    for entry in allowed_catalog:
        if type(entry) is not AllowedCatalogEntry:
            return [], [_diag("agent.catalog.entry", "entree exacte AllowedCatalogEntry exigee")]
        op = object.__getattribute__(entry, "operation")
        ver = object.__getattribute__(entry, "version")
        params = object.__getattribute__(entry, "params")
        if not _is_opaque(op, max_id) or not _check_semver(ver):
            return [], [_diag("agent.catalog.entry", "operation opaque et version SemVer exigees")]
        if type(params) is not tuple or len(params) > max_params:
            return [], [_diag("agent.catalog.params", "tuple exact de descripteurs borne exige")]
        names: set[str] = set()
        for spec in params:
            if not _valid_spec(spec, max_id):
                return [], [_diag("agent.catalog.param", "descripteur ferme type/borne exige")]
            spec_name = object.__getattribute__(spec, "name")
            if spec_name in names:
                return [], [_diag("agent.catalog.param", "nom de parametre duplique refuse")]
            names.add(spec_name)
        if (op, ver) in seen_ops:
            return [], [_diag("agent.catalog.entry", "doublon operation/version refuse")]
        seen_ops.add((op, ver))
        entries.append(entry)
    return entries, []


def validate_agent_instruction_v2(instruction: object, allowed_catalog: object, context: object) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    if type(instruction) is not AgentManagementInstruction:
        return _finalize([_diag("agent.instruction", "instance exacte AgentManagementInstruction exigee")])
    if not _valid_context_v2(context):
        return _finalize([_diag("agent.context", "contexte de comparaison fourni invalide")])
    max_id = object.__getattribute__(context, "max_id_len")
    max_ids = object.__getattribute__(context, "max_ids")
    max_params = object.__getattribute__(context, "max_params")
    schem = object.__getattribute__(instruction, "schema_version")
    if not (type(schem) is str and schem == CONTRACT_VERSION_V2):
        return _finalize([_diag("agent.instruction.schema_version", "version exacte 2.0.0 exigee")])
    for field in ("operation_id", "catalog_operation", "initial_actor", "pa_target", "mandate_ref", "idempotency_key"):
        if not _is_opaque(object.__getattribute__(instruction, field), max_id):
            out.append(_diag(f"agent.instruction.{field}", "chaine opaque exacte non vide bornee exigee"))
    if not _check_semver(object.__getattribute__(instruction, "catalog_version")):
        out.append(_diag("agent.instruction.catalog_version", "version SemVer exacte exigee"))
    gen = object.__getattribute__(instruction, "expected_generation")
    if not (type(gen) is int and gen >= 0):
        out.append(_diag("agent.instruction.expected_generation", "entier exact positif exige, bool refuse"))
    scope = object.__getattribute__(instruction, "scope_context")
    if type(scope) is not ScopeContext:
        out.append(_diag("agent.instruction.scope_context", "instance exacte ScopeContext exigee"))
    else:
        try:
            validate_structure(scope)
        except ScopeStructureError:
            out.append(_diag("agent.instruction.scope_context", "structure ScopeContext refusee"))
    if not _check_ids(object.__getattribute__(instruction, "correlation_ids"), max_id, max_ids):
        out.append(_diag("agent.instruction.correlation_ids", "tuple exact d'opaques bornes exige"))
    if not _check_ids(object.__getattribute__(instruction, "causation_ids"), max_id, max_ids):
        out.append(_diag("agent.instruction.causation_ids", "tuple exact d'opaques bornes exige"))
    params = object.__getattribute__(instruction, "params")
    if type(params) is not tuple or len(params) > max_params:
        out.append(_diag("agent.instruction.params", "tuple exact de parametres borne exige"))
        return _finalize(out)
    from pixs.agent.contracts import AgentParam as _AgentParam

    for param in params:
        if type(param) is not _AgentParam:
            out.append(_diag("agent.instruction.param", "instance exacte AgentParam exigee"))
            return _finalize(out)
        pname = object.__getattribute__(param, "name")
        pkind = object.__getattribute__(param, "kind")
        if not _is_opaque(pname, max_id):
            out.append(_diag("agent.instruction.param.name", "nom opaque exact exige, non hashable refuse"))
            continue
        if not (type(pkind) is str and (pkind == "str" or pkind == "int" or pkind == "bool")):
            out.append(_diag("agent.instruction.param.kind", "sorte exacte str/int/bool exigee"))
            continue
    if out:
        return _finalize(out)
    if object.__getattribute__(instruction, "initial_actor") != object.__getattribute__(context, "expected_actor"):
        out.append(_diag("agent.instruction.binding.actor", "liaison acteur fournie refusee"))
    if object.__getattribute__(instruction, "scope_context") != object.__getattribute__(context, "expected_scope"):
        out.append(_diag("agent.instruction.binding.scope", "liaison scope fourni refusee"))
    if object.__getattribute__(instruction, "pa_target") != object.__getattribute__(context, "expected_target"):
        out.append(_diag("agent.instruction.binding.target", "liaison cible fournie refusee"))
    if gen != object.__getattribute__(context, "expected_generation"):
        out.append(_diag("agent.instruction.binding.generation", "liaison generation fournie refusee"))
    if object.__getattribute__(instruction, "catalog_operation") != object.__getattribute__(context, "expected_operation"):
        out.append(_diag("agent.instruction.binding.operation", "liaison operation fournie refusee"))
    if object.__getattribute__(instruction, "catalog_version") != object.__getattribute__(context, "expected_version"):
        out.append(_diag("agent.instruction.binding.version", "liaison version fournie refusee"))
    if object.__getattribute__(instruction, "operation_id") != object.__getattribute__(context, "expected_operation_id"):
        out.append(_diag("agent.instruction.binding.operation_id", "liaison identifiant d'operation refusee"))
    if object.__getattribute__(instruction, "idempotency_key") != object.__getattribute__(context, "expected_idempotency_key"):
        out.append(_diag("agent.instruction.binding.idempotence", "liaison idempotence fournie refusee"))
    if object.__getattribute__(instruction, "correlation_ids") != object.__getattribute__(context, "expected_correlation_ids"):
        out.append(_diag("agent.instruction.binding.correlation", "liaison correlation fournie refusee"))
    if object.__getattribute__(instruction, "mandate_ref") != object.__getattribute__(context, "mandate_proof"):
        out.append(_diag("agent.instruction.binding.mandate", "preuve de mandat requise absente ou incoherente"))
    exp_instant = _parse_v2(object.__getattribute__(instruction, "expires_at"))
    now_instant = _parse_v2(object.__getattribute__(context, "now_iso"))
    if exp_instant is None:
        out.append(_diag("agent.instruction.expires_at", "instant canonique YYYY-MM-DDTHH:MM:SS.ffffffZ exige"))
    elif now_instant is None or exp_instant <= now_instant:
        out.append(_diag("agent.instruction.expires_at", "echeance expiree au regard de l'instant fourni"))
    if out:
        return _finalize(out)
    entries, errs = _catalog_entries(allowed_catalog, max_id, max_params)
    if errs:
        return _finalize(errs)
    match: AllowedCatalogEntry | None = None
    for entry in entries:
        if object.__getattribute__(entry, "operation") == object.__getattribute__(instruction, "catalog_operation") and object.__getattribute__(entry, "version") == object.__getattribute__(instruction, "catalog_version"):
            match = entry
            break
    if match is None:
        out.append(_diag("agent.instruction.catalog", "operation/version fermees inconnues refusees"))
        return _finalize(out)
    specs = {object.__getattribute__(s, "name"): s for s in object.__getattribute__(match, "params")}
    seen: set[str] = set()
    for param in params:
        pname = object.__getattribute__(param, "name")
        pkind = object.__getattribute__(param, "kind")
        if type(pname) is not str:
            continue
        if pname in seen:
            out.append(_diag("agent.instruction.param.name", "parametre duplique refuse"))
            continue
        seen.add(pname)
        spec = specs.get(pname)
        if spec is None:
            out.append(_diag("agent.instruction.param.name", "champ etranger hors catalogue refuse"))
            continue
        if pkind != object.__getattribute__(spec, "kind"):
            out.append(_diag("agent.instruction.param.kind", "sorte bool/int/str incoherente refusee"))
            continue
        svalue = object.__getattribute__(param, "str_value")
        ivalue = object.__getattribute__(param, "int_value")
        bvalue = object.__getattribute__(param, "bool_value")
        if pkind == "str":
            bound = object.__getattribute__(spec, "max_len")
            if not (type(svalue) is str and "\x00" not in svalue and len(svalue) <= bound):
                out.append(_diag("agent.instruction.param.str", "chaine typee bornee exigee"))
            if ivalue is not None or bvalue is not None:
                out.append(_diag("agent.instruction.param.exclusive", "valeur exclusive selon sorte exigee"))
        elif pkind == "int":
            low = object.__getattribute__(spec, "int_min")
            high = object.__getattribute__(spec, "int_max")
            if not (type(ivalue) is int and low <= ivalue <= high):
                out.append(_diag("agent.instruction.param.int", "entier type borne exige, bool refuse"))
            if svalue is not None or bvalue is not None:
                out.append(_diag("agent.instruction.param.exclusive", "valeur exclusive selon sorte exigee"))
        else:
            if type(bvalue) is not bool:
                out.append(_diag("agent.instruction.param.bool", "booleen exact exige, int refuse"))
            if svalue is not None or ivalue is not None:
                out.append(_diag("agent.instruction.param.exclusive", "valeur exclusive selon sorte exigee"))
    for sname, spec in specs.items():
        if object.__getattribute__(spec, "required") is True and sname not in seen:
            out.append(_diag("agent.instruction.param.required", "parametre requis absent refuse"))
    return _finalize(out)


def validate_agent_state_v2(state: object, context: object) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    if type(state) is not AgentManagementState:
        return _finalize([_diag("agent.state", "instance exacte AgentManagementState exigee")])
    if not _valid_context_v2(context):
        return _finalize([_diag("agent.context", "contexte de comparaison fourni invalide")])
    out.extend(_scope_v2(object.__getattribute__(state, "scope_context"), object.__getattribute__(context, "expected_scope"), "agent.state"))
    max_id = object.__getattribute__(context, "max_id_len")
    max_doc = object.__getattribute__(context, "max_doc_len")
    max_age = object.__getattribute__(context, "max_observation_age_seconds")
    now_instant = _parse_v2(object.__getattribute__(context, "now_iso"))
    assert now_instant is not None
    for field in ("operation_id", "pa_target"):
        if not _is_opaque(object.__getattribute__(state, field), max_id):
            out.append(_diag(f"agent.state.{field}", "chaine opaque exacte bornee exigee"))
    gen = object.__getattribute__(state, "generation")
    if not (type(gen) is int and gen >= 0):
        out.append(_diag("agent.state.generation", "entier exact positif exige, bool refuse"))
    desired = object.__getattribute__(state, "desired_doc")
    if not (type(desired) is str and desired != "" and "\x00" not in desired and len(desired) <= max_doc):
        out.append(_diag("agent.state.desired_doc", "document souhaite opaque borne exige"))
    observed = object.__getattribute__(state, "observed_doc")
    observed_at_raw = object.__getattribute__(state, "observed_at")
    observed_parsed = None
    if observed is None:
        if observed_at_raw is not None:
            out.append(_diag("agent.state.observed", "absence et date gardees distinctes"))
    else:
        if not _is_opaque(observed, max_doc):
            out.append(_diag("agent.state.observed_doc", "document observe opaque borne exige"))
        observed_parsed = _parse_v2(observed_at_raw)
        if observed_parsed is None or observed_parsed > now_instant:
            out.append(_diag("agent.state.observed_at", "instant observe canonique six decimales non futur exige"))
    last_doc = object.__getattribute__(state, "last_known_doc")
    last_at_raw = object.__getattribute__(state, "last_known_at")
    last_parsed = None
    if last_doc is None:
        if last_at_raw is not None:
            out.append(_diag("agent.state.last_known", "absence et date gardees distinctes"))
    else:
        if not _is_opaque(last_doc, max_doc):
            out.append(_diag("agent.state.last_known_doc", "document connu opaque borne exige"))
        last_parsed = _parse_v2(last_at_raw)
        if last_parsed is None or last_parsed > now_instant:
            out.append(_diag("agent.state.last_known_at", "instant connu canonique six decimales non futur exige"))
        elif observed_parsed is not None and last_parsed < observed_parsed:
            out.append(_diag("agent.state.last_known_at", "coherence temporelle observe/connue exigee"))
    proof = object.__getattribute__(state, "confirmation_proof")
    expected_proof = object.__getattribute__(context, "expected_confirmation_proof")
    if proof is None:
        pass
    else:
        if type(proof) is not str or proof != expected_proof:
            out.append(_diag("agent.state.confirmation", "preuve de confirmation attendue incoherente refusee"))
        elif observed is None or observed_parsed is None:
            out.append(_diag("agent.state.confirmation", "confirmation sans observe refusee"))
        elif _age_us(now_instant, observed_parsed) > max_age * 1000000:
            out.append(_diag("agent.state.confirmation", "observation perimee au regard de la fraicheur fournie"))
    if out:
        return _finalize(out)
    if object.__getattribute__(state, "operation_id") != object.__getattribute__(context, "expected_operation_id"):
        out.append(_diag("agent.state.binding.operation_id", "liaison identifiant d'operation refusee"))
    if object.__getattribute__(state, "pa_target") != object.__getattribute__(context, "expected_target"):
        out.append(_diag("agent.state.binding.target", "liaison cible fournie refusee"))
    if gen != object.__getattribute__(context, "expected_generation"):
        out.append(_diag("agent.state.binding.generation", "liaison generation fournie refusee"))
    return _finalize(out)


def validate_agent_result_v2(result: object, context: object) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    if type(result) is not AgentManagementResult:
        return _finalize([_diag("agent.result", "instance exacte AgentManagementResult exigee")])
    if not _valid_context_v2(context):
        return _finalize([_diag("agent.context", "contexte de comparaison fourni invalide")])
    out.extend(_scope_v2(object.__getattribute__(result, "scope_context"), object.__getattribute__(context, "expected_scope"), "agent.result"))
    max_id = object.__getattribute__(context, "max_id_len")
    max_ids = object.__getattribute__(context, "max_ids")
    now_instant = _parse_v2(object.__getattribute__(context, "now_iso"))
    assert now_instant is not None
    for field in ("operation_id", "pa_target"):
        if not _is_opaque(object.__getattribute__(result, field), max_id):
            out.append(_diag(f"agent.result.{field}", "chaine opaque exacte bornee exigee"))
    gen = object.__getattribute__(result, "generation")
    if not (type(gen) is int and gen >= 0):
        out.append(_diag("agent.result.generation", "entier exact positif exige, bool refuse"))
    outcome = object.__getattribute__(result, "outcome")
    if not (type(outcome) is str and (outcome == "ack" or outcome == "confirmed" or outcome == "failed" or outcome == "unknown")):
        out.append(_diag("agent.result.outcome", "issue fermee ack/confirmed/failed/unknown exigee"))
        return _finalize(out)
    if not _check_ids(object.__getattribute__(result, "correlation_ids"), max_id, max_ids):
        out.append(_diag("agent.result.correlation_ids", "tuple exact d'opaques bornes exige"))
    occurred_parsed = _parse_v2(object.__getattribute__(result, "occurred_at"))
    if occurred_parsed is None or occurred_parsed > now_instant:
        out.append(_diag("agent.result.occurred_at", "instant survenu canonique six decimales non futur exige"))
    proof = object.__getattribute__(result, "origin_proof")
    expected_origin = object.__getattribute__(context, "expected_origin_proof")
    if outcome == "unknown":
        if proof is not None:
            out.append(_diag("agent.result.origin", "issue inconnue sans preuve gardee distincte"))
    else:
        if type(proof) is not str or proof != expected_origin:
            out.append(_diag("agent.result.origin", "preuve d'origine attendue incoherente refusee"))
    if out:
        return _finalize(out)
    if object.__getattribute__(result, "operation_id") != object.__getattribute__(context, "expected_operation_id"):
        out.append(_diag("agent.result.binding.operation_id", "liaison identifiant d'operation refusee"))
    if object.__getattribute__(result, "pa_target") != object.__getattribute__(context, "expected_target"):
        out.append(_diag("agent.result.binding.target", "liaison cible fournie refusee"))
    if gen != object.__getattribute__(context, "expected_generation"):
        out.append(_diag("agent.result.binding.generation", "liaison generation fournie refusee"))
    if object.__getattribute__(result, "correlation_ids") != object.__getattribute__(context, "expected_correlation_ids"):
        out.append(_diag("agent.result.binding.correlation", "liaison correlation fournie refusee"))
    return _finalize(out)
