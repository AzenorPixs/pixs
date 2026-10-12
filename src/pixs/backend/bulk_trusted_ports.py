"""Composition serveur des ports Bulk v1 et frontières internes de confiance.

Module sans entrée/sortie directe, ORM, Django, psycopg, settings,
environnement, réseau, processus, import dynamique, sérialisation, provider de
production ni état global mutable. La composition est partielle : elle ne
peut annoncer un runtime de production prêt. Tous les états de déclaration
(mapping_descriptors, owner_declarations) sont fournis explicitement à la
composition, capturés et fixés par instance ; aucun registre global n'est
inventé ni muté. Les méthodes déclaratives des ports optionnels (gouvernance,
commande et projection de propriétaire, audit) ne sont jamais invoquées dans
ce lot : seule leur structure Python explorable statiquement est validée,
sans immuabilité arbitraire de provider ni atomicité transactionnelle déduite.
Les références du contexte serveur et les réponses de ports ne sont jamais
une preuve d'authentification de production ; un refus produit uniquement des
diagnostics statiques triés et dédupliqués, sans valeur fournie, sans
référence de contexte exploitable et sans second appel ni repli.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from types import FunctionType, MappingProxyType, MethodType

from pixs.backend.bulk_runtime_contracts import (
    _AuthorityAssessmentSnapshot,
    _ContractRefused,
    _MappingDescriptorSnapshot,
    _MAPPING_KEYS,
    _MAPPING_SCOPE,
    _exact_mapping,
    _tuple_of_exact_str,
    _bindings_type_refusals,
    _OPAQUE_RULE,
    _build_authority_assessment_snapshot,
    _build_mapping_descriptor_snapshot,
    _is_complete_semver,
    _is_opaque_text,
    _pack,
    _refusal,
    validate_mapping_descriptor_values,
)
from pixs.kernel.diagnostics import Diagnostic

__all__ = [
    "declare_bulk_mapping_descriptor",
    "compose_bulk_trusted_ports",
    "validate_governance_contract",
    "validate_owner_command_contract",
    "validate_owner_projection_contract",
    "validate_audit_contract",
]

_ACTIONS = frozenset({"ADMIT", "EXECUTE", "CANCEL", "READ_RESULT"})

_CHECK_SCOPE = "bulk_trusted_ports.check_authority"
_RESOLVE_SCOPE = "bulk_trusted_ports.resolve_mapping"
_GOVERNANCE_SCOPE = "bulk_governance_port"
_OWNER_COMMAND_SCOPE = "bulk_owner_command_port"
_OWNER_PROJECTION_SCOPE = "bulk_owner_projection_port"
_AUDIT_SCOPE = "bulk_audit_port"
_COMPOSE_AUTHORITY_SCOPE = "bulk_authority_port"
_COMPOSE_RESOLVER_SCOPE = "bulk_mapping_resolver"

_AUTHORITY_METHODS = ("check",)
_RESOLVER_METHODS = ("resolve",)
_GOVERNANCE_METHODS = ("resolve",)
_OWNER_COMMAND_METHODS = ("validate", "execute", "canonical_bytes")
_OWNER_PROJECTION_METHODS = (
    "filter_authorized",
    "acquire_consistency",
    "iterate_projection",
)
_AUDIT_METHODS = ("append_minimized",)

_MAPPING_DECLARATIONS_REFUSAL = "déclarations de mapping refusées en composition"
_OWNER_DECLARATIONS_REFUSAL = "déclarations de propriétaires refusées en composition"
_OWNER_AMBIGUOUS_REFUSAL = "déclarations divergentes pour un même propriétaire"
_MAPPING_AMBIGUOUS_REFUSAL = "déclarations divergentes pour un même triplet de mapping"
_OWNER_UNDECLARED_REFUSAL = "propriétaire de mapping non déclaré en composition"
_TARGET_FIELDS_REFUSAL = "cibles hors champs publics déclarés du propriétaire"
_AUTHORITY_PORT_REFUSAL = "port d'autorité serveur inexploitable"
_RESOLVER_REFUSAL = "résolveur de mapping serveur inexploitable"
_OPTIONAL_PORT_REFUSAL = "port serveur optionnel inexploitable"

_COMPONENT_RULE = "composant serveur requis"
_METHOD_RULE = "méthode Python statique explorable attendue"
_STR_RULE = "str exact attendu"
_UNAVAILABLE_RULE = "port serveur indisponible sans contexte exploitable ni repli"
_REFUSAL_RULE = "autorité refusée sans contexte exploitable"
_CONTEXT_RULE = "contexte résolu serveur valide attendu"
_NOT_DECLARED_RULE = "mapping non déclaré côté serveur attendu"
_DIVERGENT_RULE = "mapping résolu identique à la déclaration serveur immuable attendu"


class _CompositionRefused(ValueError):
    """Refus statique de composition ; aucun message ne porte de valeur fournie."""


@dataclass(frozen=True, slots=True)
class _OwnerDeclarationSnapshot:
    owner_reference: str
    contract_version: str
    declared_codes: tuple[str, ...]
    declared_fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _BulkTrustedPorts:
    _authority_port: object
    _mapping_resolver: object
    _mapping_lookup: MappingProxyType[tuple[str, str, str], _MappingDescriptorSnapshot]
    _owner_lookup: MappingProxyType[str, _OwnerDeclarationSnapshot]
    _governance_port: object
    _owner_command_port: object
    _owner_projection_port: object
    _audit_port: object

    def check_authority(
        self,
        *,
        server_context: object,
        action: object,
        operation_reference: object,
        resource_reference: object,
    ) -> tuple[_AuthorityAssessmentSnapshot | None, list[Diagnostic]]:
        """Délègue une fois le port d'autorité composé ; refus sans contexte ni repli.

        Le contexte provient exclusivement du code serveur : il n'est ni
        sérialisé ni inspecté, et sa persistance ne prouve aucune
        authentification de production.
        """
        refusals: list[Diagnostic] = []
        if type(action) is not str:
            refusals.append(_refusal(_CHECK_SCOPE, "action", _STR_RULE))
        elif action not in _ACTIONS:
            refusals.append(
                _refusal(
                    _CHECK_SCOPE,
                    "action",
                    "membre ADMIT, EXECUTE, CANCEL ou READ_RESULT attendu",
                )
            )
        if not _is_opaque_text(operation_reference):
            refusals.append(
                _refusal(_CHECK_SCOPE, "operation_reference", _OPAQUE_RULE)
            )
        if resource_reference is not None and not _is_opaque_text(
            resource_reference
        ):
            refusals.append(
                _refusal(
                    _CHECK_SCOPE,
                    "resource_reference",
                    "référence opaque str ou None explicite attendu",
                )
            )
        if refusals:
            return (None, _pack(refusals))
        try:
            assessment = self._authority_port(
                server_context, action, operation_reference, resource_reference
            )
        except Exception:
            # Frontière sûre : l'exception du provider n'est jamais convertie,
            # journalisée ni transférée au worker.
            return (None, _pack([_refusal(_CHECK_SCOPE, "decision", _UNAVAILABLE_RULE)]))
        try:
            snapshot = _build_authority_assessment_snapshot(assessment)
        except (_ContractRefused, KeyError, TypeError):
            return (None, _pack([_refusal(_CHECK_SCOPE, "resolved_context", _CONTEXT_RULE)]))
        if snapshot.decision != "ALLOW":
            return (None, _pack([_refusal(_CHECK_SCOPE, "decision", _REFUSAL_RULE)]))
        return (snapshot, [])

    def resolve_mapping(
        self,
        mapping_reference: object,
        mapping_version: object,
        owner_reference: object,
    ) -> tuple[_MappingDescriptorSnapshot | None, list[Diagnostic]]:
        """Résolveur serveur appelé une fois ; identité stricte avec la déclaration."""
        refusals: list[Diagnostic] = []
        for name, value in (
            ("mapping_reference", mapping_reference),
            ("mapping_version", mapping_version),
            ("owner_reference", owner_reference),
        ):
            if type(value) is not str:
                refusals.append(_refusal(_RESOLVE_SCOPE, name, _STR_RULE))
        if refusals:
            return (None, _pack(refusals))
        if not _is_opaque_text(mapping_reference):
            refusals.append(
                _refusal(_RESOLVE_SCOPE, "mapping_reference", _OPAQUE_RULE)
            )
        if not _is_opaque_text(owner_reference):
            refusals.append(
                _refusal(_RESOLVE_SCOPE, "owner_reference", _OPAQUE_RULE)
            )
        if not _is_complete_semver(mapping_version):
            refusals.append(
                _refusal(
                    _RESOLVE_SCOPE,
                    "mapping_version",
                    "version SemVer complète exacte attendue",
                )
            )
        if refusals:
            return (None, _pack(refusals))
        key = (mapping_reference, mapping_version, owner_reference)
        declared = self._mapping_lookup.get(key)
        if declared is None:
            return (None, _pack([_refusal(_RESOLVE_SCOPE, "mapping", _NOT_DECLARED_RULE)]))
        try:
            resolved = self._mapping_resolver(
                mapping_reference, mapping_version, owner_reference
            )
        except Exception:
            # Aucun repli sur le cache déclaré lorsque le résolveur est indisponible.
            return (None, _pack([_refusal(_RESOLVE_SCOPE, "mapping", _UNAVAILABLE_RULE)]))
        refusals = validate_mapping_descriptor_values(resolved)
        if refusals:
            return (None, _pack(refusals))
        try:
            snapshot = _build_mapping_descriptor_snapshot(resolved)
        except (_ContractRefused, KeyError, TypeError):
            return (None, _pack([_refusal(_RESOLVE_SCOPE, "mapping", _DIVERGENT_RULE)]))
        if snapshot.as_values() != declared.as_values():
            return (None, _pack([_refusal(_RESOLVE_SCOPE, "mapping", _DIVERGENT_RULE)]))
        return (declared, [])


def _capture_python_method(component: object, name: str) -> object | None:
    if type(component) is type:
        return None
    missing = object()
    try:
        value = inspect.getattr_static(component, name, missing)
    except Exception:
        return None
    if value is missing:
        return None
    if type(value) is FunctionType:
        try:
            class_value = inspect.getattr_static(type(component), name, missing)
        except Exception:
            return None
        if class_value is value:
            return MethodType(value, component)
        return value
    if type(value) is MethodType and type(value.__func__) is FunctionType:
        return value
    return None


def _structural_refusals(
    component: object, slots: tuple[str, ...], scope: str
) -> list[Diagnostic]:
    if component is None:
        return [_refusal(scope, "component", _COMPONENT_RULE)]
    refusals: list[Diagnostic] = []
    for name in slots:
        if _capture_python_method(component, name) is None:
            refusals.append(_refusal(scope, name, _METHOD_RULE))
    return _pack(refusals)


def validate_governance_contract(component: object) -> list[Diagnostic]:
    """Structure du port de gouvernance : resolve Python explorable seulement."""
    return _structural_refusals(component, _GOVERNANCE_METHODS, _GOVERNANCE_SCOPE)


def validate_owner_command_contract(component: object) -> list[Diagnostic]:
    """Structure du port de commande du propriétaire ; aucune méthode invoquée."""
    return _structural_refusals(component, _OWNER_COMMAND_METHODS, _OWNER_COMMAND_SCOPE)


def validate_owner_projection_contract(component: object) -> list[Diagnostic]:
    """Structure du port de projection du propriétaire ; aucune méthode invoquée."""
    return _structural_refusals(
        component, _OWNER_PROJECTION_METHODS, _OWNER_PROJECTION_SCOPE
    )


def validate_audit_contract(component: object) -> list[Diagnostic]:
    """Structure du port d'audit ; aucune méthode invoquée."""
    return _structural_refusals(component, _AUDIT_METHODS, _AUDIT_SCOPE)


def declare_bulk_mapping_descriptor(
    values: object,
) -> _MappingDescriptorSnapshot:
    """Construit un snapshot validé ; aucune écriture dans un état global."""
    if validate_mapping_descriptor_values(values):
        raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL)
    try:
        return _build_mapping_descriptor_snapshot(values)
    except (_ContractRefused, KeyError, TypeError):
        raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL) from None


def _capture_catalog(value: object) -> tuple[str, ...]:
    kind = type(value)
    if kind is not tuple and kind is not frozenset:
        raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
    elements = tuple(value)
    if any(not _is_opaque_text(item) for item in elements):
        raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
    if kind is tuple:
        return elements
    return tuple(sorted(elements))


def _capture_owner_declaration(entry: object) -> _OwnerDeclarationSnapshot:
    if type(entry) is not tuple or len(entry) != 4:
        raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
    owner_reference, contract_version, codes, fields = entry
    if type(owner_reference) is not str or type(contract_version) is not str:
        raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
    declared_codes = _capture_catalog(codes)
    declared_fields = _capture_catalog(fields)
    if not _is_opaque_text(owner_reference):
        raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
    if not _is_complete_semver(contract_version):
        raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
    return _OwnerDeclarationSnapshot(
        owner_reference=owner_reference,
        contract_version=contract_version,
        declared_codes=declared_codes,
        declared_fields=declared_fields,
    )


def _same_declaration(
    first: _OwnerDeclarationSnapshot, second: _OwnerDeclarationSnapshot
) -> bool:
    if first.contract_version != second.contract_version:
        return False
    if frozenset(first.declared_codes) != frozenset(second.declared_codes):
        return False
    return frozenset(first.declared_fields) == frozenset(second.declared_fields)


def _capture_mapping_lookup(
    mapping_descriptors: tuple[object, ...],
) -> dict[tuple[str, str, str], _MappingDescriptorSnapshot]:
    mappings: dict[tuple[str, str, str], _MappingDescriptorSnapshot] = {}
    for item in mapping_descriptors:
        if validate_mapping_descriptor_values(item):
            raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL)
        try:
            snapshot = _build_mapping_descriptor_snapshot(item)
        except (_ContractRefused, KeyError, TypeError):
            raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL) from None
        key = (
            snapshot.mapping_reference,
            snapshot.mapping_version,
            snapshot.owner_reference,
        )
        existing = mappings.get(key)
        if existing is None:
            mappings[key] = snapshot
        elif existing.as_values() != snapshot.as_values():
            raise _CompositionRefused(_MAPPING_AMBIGUOUS_REFUSAL)
    return mappings


def _capture_owner_lookup(
    owner_declarations: tuple[object, ...],
) -> dict[str, _OwnerDeclarationSnapshot]:
    owners: dict[str, _OwnerDeclarationSnapshot] = {}
    for entry in owner_declarations:
        declaration = _capture_owner_declaration(entry)
        existing = owners.get(declaration.owner_reference)
        if existing is None:
            owners[declaration.owner_reference] = declaration
        elif not _same_declaration(existing, declaration):
            raise _CompositionRefused(_OWNER_AMBIGUOUS_REFUSAL)
    return owners


def _preflight_metadata_types(
    mapping_descriptors: object, owner_declarations: object
) -> tuple[tuple[dict, ...], tuple[tuple, ...]]:
    if type(mapping_descriptors) is not tuple:
        raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL)
    if type(owner_declarations) is not tuple:
        raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
    captured_mappings = []
    for item in mapping_descriptors:
        values, refusals = _exact_mapping(
            item, _MAPPING_SCOPE, _MAPPING_KEYS, "neuf clés exactes attendues"
        )
        if values is None:
            raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL)
        for name in ("mapping_reference", "mapping_version", "owner_reference", "variant", "format"):
            if type(values[name]) is not str:
                raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL)
        for name in ("source_fields", "target_fields", "required_source_fields", "field_bindings"):
            if type(values[name]) is not tuple:
                raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL)
        for name in ("source_fields", "target_fields", "required_source_fields"):
            if _tuple_of_exact_str(values, name):
                raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL)
        if _bindings_type_refusals(values):
            raise _CompositionRefused(_MAPPING_DECLARATIONS_REFUSAL)
        captured_mappings.append(values)
    captured_owners = []
    for entry in owner_declarations:
        if type(entry) is not tuple or len(entry) != 4:
            raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
        reference, version, codes, fields = entry
        if type(reference) is not str or type(version) is not str:
            raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
        copied_catalogues = []
        for catalogue in (codes, fields):
            kind = type(catalogue)
            if kind is not tuple and kind is not frozenset:
                raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
            elements = tuple(catalogue)
            if any(type(element) is not str for element in elements):
                raise _CompositionRefused(_OWNER_DECLARATIONS_REFUSAL)
            copied_catalogues.append(elements)
        captured_owners.append((reference, version, copied_catalogues[0], copied_catalogues[1]))
    return tuple(captured_mappings), tuple(captured_owners)


def compose_bulk_trusted_ports(
    *,
    authority_adapter: object,
    mapping_resolver: object,
    mapping_descriptors: object,
    owner_declarations: object,
    governance_adapter: object,
    owner_command_adapter: object,
    owner_projection_adapter: object,
    audit_adapter: object,
) -> _BulkTrustedPorts:
    """Compose les ports serveur pour cette instance ; composition partielle admise.

    Les deux premiers slots sont obligatoires ; les quatre autres acceptent un
    objet serveur ou None explicite (absence = capacité non composée, jamais
    un provider implicite). Les métadonnées imbriquées et catalogues sont
    capturés avant toute comparaison, hash ou inspection d'adaptateurs.
    """
    mapping_descriptors, owner_declarations = _preflight_metadata_types(
        mapping_descriptors, owner_declarations
    )
    mappings = _capture_mapping_lookup(mapping_descriptors)
    owners = _capture_owner_lookup(owner_declarations)
    for snapshot in mappings.values():
        declaration = owners.get(snapshot.owner_reference)
        if declaration is None:
            raise _CompositionRefused(_OWNER_UNDECLARED_REFUSAL)
        if not frozenset(snapshot.target_fields) <= frozenset(
            declaration.declared_fields
        ):
            raise _CompositionRefused(_TARGET_FIELDS_REFUSAL)
    authority_check = _capture_python_method(authority_adapter, "check")
    if authority_check is None:
        raise _CompositionRefused(_AUTHORITY_PORT_REFUSAL)
    mapping_resolve = _capture_python_method(mapping_resolver, "resolve")
    if mapping_resolve is None:
        raise _CompositionRefused(_RESOLVER_REFUSAL)
    for component, validator in (
        (governance_adapter, validate_governance_contract),
        (owner_command_adapter, validate_owner_command_contract),
        (owner_projection_adapter, validate_owner_projection_contract),
        (audit_adapter, validate_audit_contract),
    ):
        if component is not None and validator(component):
            raise _CompositionRefused(_OPTIONAL_PORT_REFUSAL)
    return _BulkTrustedPorts(
        _authority_port=authority_check,
        _mapping_resolver=mapping_resolve,
        _mapping_lookup=MappingProxyType(mappings),
        _owner_lookup=MappingProxyType(owners),
        _governance_port=governance_adapter,
        _owner_command_port=owner_command_adapter,
        _owner_projection_port=owner_projection_adapter,
        _audit_port=audit_adapter,
    )
