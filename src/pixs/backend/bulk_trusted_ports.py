"""Composition serveur des ports Bulk v1 et frontières internes de confiance.

Module sans entrée/sortie directe, ORM, Django, psycopg, settings,
environnement, réseau, processus, import dynamique, sérialisation, provider de
production ni état global mutable. La composition est partielle : elle ne
peut annoncer un runtime de production prêt. Tous les états de déclaration
(mapping_descriptors, owner_declarations) sont fournis explicitement à la
composition, capturés et fixés par instance ; aucun registre global n'est
inventé ni muté. Les méthodes déclaratives des ports optionnels de commande,
projection de propriétaire et audit ne sont jamais invoquées dans ce lot :
seule leur structure Python explorable statiquement est validée, sans
immuabilité arbitraire de provider ni atomicité transactionnelle déduite.
La méthode resolve du port de gouvernance composé est invoquée une seule fois
par resolve_governance, sans repli ni défaut ; la composition elle-même reste
sans invocation. Les références du contexte serveur et les réponses de ports
ne sont jamais une preuve d'authentification de production ; un refus produit
uniquement des diagnostics statiques triés et dédupliqués, sans valeur
fournie, sans référence de contexte exploitable et sans second appel ni repli.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from types import FunctionType, MappingProxyType, MethodType

from pixs.backend.bulk_execution_values import (
    _POLICY_INT_FIELDS,
    _POLICY_KEYS,
    _POLICY_LIST_FIELDS,
    validate_bulk_policy_values,
)
from pixs.backend.bulk_runtime_contracts import (
    _AuthorityAssessmentSnapshot,
    _ContractRefused,
    _MappingDescriptorSnapshot,
    _MAPPING_KEYS,
    _MAPPING_SCOPE,
    _ServerContextRefsSnapshot,
    _build_authority_assessment_snapshot,
    _build_mapping_descriptor_snapshot,
    _build_server_context_refs_snapshot,
    _exact_mapping,
    _tuple_of_exact_str,
    _bindings_type_refusals,
    _OPAQUE_RULE,
    _is_complete_semver,
    _is_opaque_text,
    _pack,
    _refusal,
    validate_mapping_descriptor_values,
    validate_server_context_refs_values,
)
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_governance_profile import (
    DataGovernanceProfile,
    validate_data_governance_profile,
)
from pixs.kernel.diagnostics import Diagnostic

__all__ = [
    "declare_bulk_mapping_descriptor",
    "compose_bulk_trusted_ports",
    "validate_governance_contract",
    "validate_owner_command_contract",
    "validate_owner_projection_contract",
    "validate_audit_contract",
    "validate_publisher_contract",
    "validate_download_contract",
]

_ACTIONS = frozenset({"ADMIT", "EXECUTE", "CANCEL", "READ_RESULT"})

_CHECK_SCOPE = "bulk_trusted_ports.check_authority"
_RESOLVE_SCOPE = "bulk_trusted_ports.resolve_mapping"
_GOVERNANCE_SCOPE = "bulk_governance_port"
_GOVERNANCE_RESOLVE_SCOPE = "bulk_trusted_ports.resolve_governance"
_OWNER_COMMAND_SCOPE = "bulk_owner_command_port"
_OWNER_PROJECTION_SCOPE = "bulk_owner_projection_port"
_AUDIT_SCOPE = "bulk_audit_port"
_PUBLISHER_SCOPE = "bulk_publisher_port"
_DOWNLOAD_SCOPE = "bulk_download_port"
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
_PUBLISHER_METHODS = ("publish_declared_event",)
_DOWNLOAD_METHODS = ("authorize_then_issue_temporary_reference",)

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

_GOVERNANCE_KEYS = (
    "resolution_version",
    "decision",
    "resolved_context",
    "policy",
    "profile",
    "obligations",
)
_GOVERNANCE_VERSION = "1.0.0"
_GOVERNANCE_DECISIONS = frozenset({"RESOLVED", "DENY", "UNAVAILABLE"})
_GOVERNANCE_POLICY_KEYS = ("policy_reference", "policy_version", "limits")
_GOVERNANCE_CONTEXT_KEYS = (
    "subject_id",
    "tenant_id",
    "perimeter_reference",
    "context_reference",
)
_GOVERNANCE_UNAVAILABLE_RULE = "port de gouvernance indisponible sans contexte exploitable ni repli"
_GOVERNANCE_REFUSED_RULE = "gouvernance refusée sans contexte exploitable"
_GOVERNANCE_DIVERGENT_RULE = "contexte gouvernance identique à l'autorité courante attendu"


class _CompositionRefused(ValueError):
    """Refus statique de composition ; aucun message ne porte de valeur fournie."""


@dataclass(frozen=True, slots=True)
class _OwnerDeclarationSnapshot:
    owner_reference: str
    contract_version: str
    declared_codes: tuple[str, ...]
    declared_fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _GovernancePolicySnapshot:
    policy_reference: str
    policy_version: str
    _limits_frozen: MappingProxyType

    def as_values(self) -> dict:
        frozen = dict(self._limits_frozen)
        owned: dict = {}
        for key, value in frozen.items():
            if type(value) is list:
                owned[key] = list(value)
            elif type(value) is tuple:
                owned[key] = list(value)
            else:
                owned[key] = value
        return {
            "policy_reference": self.policy_reference,
            "policy_version": self.policy_version,
            "limits": owned,
        }


@dataclass(frozen=True, slots=True)
class _GovernanceResolutionSnapshot:
    resolution_version: str
    decision: str
    resolved_context: _ServerContextRefsSnapshot | None
    policy: _GovernancePolicySnapshot | None
    profile: DataGovernanceProfile | None
    obligations: tuple[str, ...] | None

    def as_values(self) -> dict:
        if self.resolved_context is None:
            context_values = None
        else:
            context_values = self.resolved_context.as_values()
        if self.policy is None:
            policy_values = None
        else:
            policy_values = self.policy.as_values()
        if self.profile is None:
            profile_values = None
        else:
            current = self.profile
            profile_values = DataGovernanceProfile(
                profile_version=current.profile_version,
                data_asset_id=current.data_asset_id,
                owner_component=current.owner_component,
                source_of_truth=current.source_of_truth,
                data_classes=frozenset(current.data_classes),
                confidentiality=current.confidentiality,
                personal_data=current.personal_data,
                purpose_refs=frozenset(current.purpose_refs),
                retention_policy=current.retention_policy,
                deletion_policy=current.deletion_policy,
                residency_constraints=frozenset(current.residency_constraints),
                authorized_consumers=frozenset(current.authorized_consumers),
                processor_refs=frozenset(current.processor_refs),
                export_policy=current.export_policy,
                lineage=current.lineage,
            )
        if self.obligations is None:
            obligations_values = None
        else:
            obligations_values = tuple(self.obligations)
        return {
            "resolution_version": self.resolution_version,
            "decision": self.decision,
            "resolved_context": context_values,
            "policy": policy_values,
            "profile": profile_values,
            "obligations": obligations_values,
        }


def _expected_authority_context(
    snapshot: object,
) -> tuple[dict | None, list[Diagnostic]]:
    if type(snapshot) is not _AuthorityAssessmentSnapshot:
        return None, [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "authority_snapshot", _CONTEXT_RULE)]
    decision = snapshot.decision
    if type(decision) is not str:
        return None, [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "authority_snapshot.decision", _STR_RULE)]
    if decision != "ALLOW":
        return None, [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "authority_snapshot", _CONTEXT_RULE)]
    context = snapshot.resolved_context
    if type(context) is not _ServerContextRefsSnapshot:
        return None, [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "authority_snapshot", _CONTEXT_RULE)]
    for field in _GOVERNANCE_CONTEXT_KEYS:
        if type(getattr(context, field)) is not str:
            return (
                None,
                [_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"authority_snapshot.{field}", _STR_RULE)],
            )
    return context.as_values(), []


def _mapping_contract_typed(contract: object) -> tuple[dict | None, list[Diagnostic]]:
    values, shape = _exact_mapping(
        contract, _GOVERNANCE_RESOLVE_SCOPE, _MAPPING_KEYS, "neuf clés exactes attendues"
    )
    if values is None:
        return None, shape
    for name in ("mapping_reference", "mapping_version", "owner_reference", "variant", "format"):
        if type(values[name]) is not str:
            return None, [_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"governance_contract.{name}", _STR_RULE)]
    for name in ("source_fields", "target_fields", "required_source_fields", "field_bindings"):
        if type(values[name]) is not tuple:
            return (
                None,
                [_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"governance_contract.{name}", "tuple exact attendu")],
            )
    for name in ("source_fields", "target_fields", "required_source_fields"):
        for item in values[name]:
            if type(item) is not str:
                return (
                    None,
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"governance_contract.{name}", _STR_RULE)],
                )
    for pair in values["field_bindings"]:
        if type(pair) is not tuple or len(pair) != 2:
            return (
                None,
                [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance_contract.field_bindings", "couples tuple exacts attendus")],
            )
        if type(pair[0]) is not str or type(pair[1]) is not str:
            return (
                None,
                [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance_contract.field_bindings", _STR_RULE)],
            )
    return values, []


def _governance_references_typed(
    references: object,
) -> tuple[tuple[str, str] | None, list[Diagnostic]]:
    if type(references) is not tuple or len(references) != 2:
        return None, [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance_references", "tuple exact de deux str attendu")]
    if type(references[0]) is not str or type(references[1]) is not str:
        return None, [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance_references", _STR_RULE)]
    return (references[0], references[1]), []


def _profile_types_only(candidate: object) -> list[Diagnostic]:
    if type(candidate) is not DataGovernanceProfile:
        return [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "profile", "profil de gouvernance exact attendu")]
    for name in (
        "profile_version",
        "data_asset_id",
        "owner_component",
        "source_of_truth",
        "retention_policy",
        "deletion_policy",
        "export_policy",
        "lineage",
    ):
        if type(getattr(candidate, name)) is not str:
            return [_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"profile.{name}", _STR_RULE)]
    for name in (
        "data_classes",
        "purpose_refs",
        "residency_constraints",
        "authorized_consumers",
        "processor_refs",
    ):
        if type(getattr(candidate, name)) is not frozenset:
            return [_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"profile.{name}", "frozenset exact attendu")]
        for item in tuple(getattr(candidate, name)):
            if type(item) is not str:
                return [_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"profile.{name}", _STR_RULE)]
    if type(candidate.confidentiality) is not ConfidentialityLevel:
        if not any(member is candidate.confidentiality for member in ConfidentialityLevel):
            return [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "profile.confidentiality", _STR_RULE)]
    if type(candidate.personal_data) is not PersonalDataLevel:
        if not any(member is candidate.personal_data for member in PersonalDataLevel):
            return [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "profile.personal_data", _STR_RULE)]
    return []


def _limits_types_only(limits: object) -> list[Diagnostic]:
    values, shape = _exact_mapping(
        limits,
        f"{_GOVERNANCE_RESOLVE_SCOPE}.policy.limits",
        _POLICY_KEYS,
        "vingt-quatre clés exactes attendues",
    )
    if values is None:
        return shape
    for name in _POLICY_INT_FIELDS:
        if type(values[name]) is not int:
            return [_refusal(f"{_GOVERNANCE_RESOLVE_SCOPE}.policy.limits", name, "int exact attendu")]
    for name in _POLICY_LIST_FIELDS:
        if type(values[name]) is not list:
            return [_refusal(f"{_GOVERNANCE_RESOLVE_SCOPE}.policy.limits", name, "liste exacte attendue")]
        for item in values[name]:
            if type(item) is not int:
                return [_refusal(f"{_GOVERNANCE_RESOLVE_SCOPE}.policy.limits", name, "éléments int exacts attendus")]
    return []


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

    def resolve_governance(
        self,
        *,
        server_context: object,
        authority_snapshot: object,
        governance_contract: object,
        governance_references: object,
    ) -> tuple[_GovernanceResolutionSnapshot | None, list[Diagnostic]]:
        """Résolution effective GovernanceResolutionV1 par appel unique, sans repli.

        Les entrées sont bornées : contrat MappingDescriptorV1 neuf clés et
        références tuple exact de deux str policy_reference et policy_version.
        Le contrat et les références ne constituent jamais une preuve.
        """
        if self._governance_port is None:
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance", _GOVERNANCE_UNAVAILABLE_RULE)]
                ),
            )
        expected_context, authority_refusals = _expected_authority_context(authority_snapshot)
        if expected_context is None:
            return (None, _pack(authority_refusals))
        contract_typed, contract_type_refusals = _mapping_contract_typed(governance_contract)
        if contract_typed is None:
            return (None, _pack(contract_type_refusals))
        references_typed, references_type_refusals = _governance_references_typed(
            governance_references
        )
        if references_typed is None:
            return (None, _pack(references_type_refusals))
        contract_owned = {
            "mapping_reference": contract_typed["mapping_reference"],
            "mapping_version": contract_typed["mapping_version"],
            "owner_reference": contract_typed["owner_reference"],
            "variant": contract_typed["variant"],
            "format": contract_typed["format"],
            "source_fields": tuple(contract_typed["source_fields"]),
            "target_fields": tuple(contract_typed["target_fields"]),
            "required_source_fields": tuple(contract_typed["required_source_fields"]),
            "field_bindings": tuple(
                (pair[0], pair[1]) for pair in contract_typed["field_bindings"]
            ),
        }
        if validate_mapping_descriptor_values(contract_owned):
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance_contract", "MappingDescriptorV1 valide attendu")]
                ),
            )
        if not _is_opaque_text(references_typed[0]):
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance_references", _OPAQUE_RULE)]),
            )
        if not _is_opaque_text(references_typed[1]):
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance_references", _OPAQUE_RULE)]),
            )
        if not _is_complete_semver(references_typed[1]):
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance_references", "version SemVer complète exacte attendue")]
                ),
            )
        if validate_server_context_refs_values(dict(expected_context)):
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "authority_snapshot", _CONTEXT_RULE)]
                ),
            )
        references_owned = (references_typed[0], references_typed[1])
        return self._resolve_governance_owned(
            server_context=server_context,
            expected_context=expected_context,
            contract_owned=contract_owned,
            references_owned=references_owned,
        )

    def _resolve_governance_owned(
        self,
        *,
        server_context: object,
        expected_context: object,
        contract_owned: object,
        references_owned: object,
    ) -> tuple[_GovernanceResolutionSnapshot | None, list[Diagnostic]]:
        """Invocation unique et validation profonde complète, commune B01/B04."""
        resolve_fn = _capture_python_method(self._governance_port, "resolve")
        if resolve_fn is None:
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "governance", _GOVERNANCE_UNAVAILABLE_RULE)]
                ),
            )
        try:
            response = resolve_fn(server_context, contract_owned, references_owned)
        except Exception:
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "decision", _GOVERNANCE_UNAVAILABLE_RULE)]
                ),
            )
        values, shape_refusals = _exact_mapping(
            response,
            _GOVERNANCE_RESOLVE_SCOPE,
            _GOVERNANCE_KEYS,
            "six clés exactes attendues",
        )
        if values is None:
            return (None, _pack(shape_refusals))
        if type(values["resolution_version"]) is not str:
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "resolution_version", _STR_RULE)]),
            )
        if type(values["decision"]) is not str:
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "decision", _STR_RULE)]),
            )
        raw_context = values["resolved_context"]
        if raw_context is not None and type(raw_context) is not dict:
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "resolved_context", "dict exact ou None attendu")]),
            )
        raw_policy = values["policy"]
        if raw_policy is not None and type(raw_policy) is not dict:
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "policy", "dict exact ou None attendu")]),
            )
        raw_profile = values["profile"]
        if raw_profile is not None and type(raw_profile) is not DataGovernanceProfile:
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "profile", "profil de gouvernance exact ou None attendu")]),
            )
        raw_obligations = values["obligations"]
        if raw_obligations is not None and type(raw_obligations) is not tuple:
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "obligations", "tuple exact ou None attendu")]),
            )
        if raw_context is not None:
            context_typed, context_shape = _exact_mapping(
                raw_context,
                f"{_GOVERNANCE_RESOLVE_SCOPE}.resolved_context",
                _GOVERNANCE_CONTEXT_KEYS,
                "quatre clés exactes attendues",
            )
            if context_typed is None:
                return (None, _pack(context_shape))
            for field in _GOVERNANCE_CONTEXT_KEYS:
                if type(context_typed[field]) is not str:
                    return (
                        None,
                        _pack(
                            [_refusal(f"{_GOVERNANCE_RESOLVE_SCOPE}.resolved_context", field, _STR_RULE)]
                        ),
                    )
        if raw_policy is not None:
            policy_typed, policy_shape = _exact_mapping(
                raw_policy,
                f"{_GOVERNANCE_RESOLVE_SCOPE}.policy",
                _GOVERNANCE_POLICY_KEYS,
                "trois clés exactes attendues",
            )
            if policy_typed is None:
                return (None, _pack(policy_shape))
            if type(policy_typed["policy_reference"]) is not str:
                return (
                    None,
                    _pack([_refusal(f"{_GOVERNANCE_RESOLVE_SCOPE}.policy", "policy_reference", _STR_RULE)]),
                )
            if type(policy_typed["policy_version"]) is not str:
                return (
                    None,
                    _pack([_refusal(f"{_GOVERNANCE_RESOLVE_SCOPE}.policy", "policy_version", _STR_RULE)]),
                )
            if type(policy_typed["limits"]) is not dict:
                return (
                    None,
                    _pack([_refusal(f"{_GOVERNANCE_RESOLVE_SCOPE}.policy", "limits", "dict exact attendu")]),
                )
            limits_type_refusals = _limits_types_only(policy_typed["limits"])
            if limits_type_refusals:
                return (None, _pack(limits_type_refusals))
        if raw_profile is not None:
            profile_type_refusals = _profile_types_only(raw_profile)
            if profile_type_refusals:
                return (None, _pack(profile_type_refusals))
        if raw_obligations is not None:
            for item in tuple(raw_obligations):
                if type(item) is not str:
                    return (
                        None,
                        _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "obligations", _STR_RULE)]),
                    )
        if values["resolution_version"] != _GOVERNANCE_VERSION:
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "resolution_version", "1.0.0 exact attendu")]
                ),
            )
        if values["decision"] not in _GOVERNANCE_DECISIONS:
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "decision", "membre RESOLVED, DENY ou UNAVAILABLE attendu")]
                ),
            )
        if values["decision"] in ("DENY", "UNAVAILABLE"):
            for field in ("resolved_context", "policy", "profile", "obligations"):
                if values[field] is not None:
                    return (
                        None,
                        _pack(
                            [_refusal(_GOVERNANCE_RESOLVE_SCOPE, field, "None attendu pour DENY ou UNAVAILABLE")]
                        ),
                    )
            if values["decision"] == "DENY":
                return (
                    None,
                    _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "decision", _GOVERNANCE_REFUSED_RULE)]),
                )
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "decision", _GOVERNANCE_UNAVAILABLE_RULE)]
                ),
            )
        for field in ("resolved_context", "policy", "profile", "obligations"):
            if values[field] is None:
                return (
                    None,
                    _pack(
                        [_refusal(_GOVERNANCE_RESOLVE_SCOPE, field, "valeur non None attendue pour RESOLVED")]
                    ),
                )
        context_owned = dict(context_typed)
        policy_owned = {
            "policy_reference": policy_typed["policy_reference"],
            "policy_version": policy_typed["policy_version"],
            "limits": dict(policy_typed["limits"]),
        }
        for key, value in tuple(policy_owned["limits"].items()):
            if type(value) is list:
                policy_owned["limits"][key] = list(value)
        obligations_owned = tuple(raw_obligations)
        source_profile = raw_profile
        profile_owned = DataGovernanceProfile(
            profile_version=source_profile.profile_version,
            data_asset_id=source_profile.data_asset_id,
            owner_component=source_profile.owner_component,
            source_of_truth=source_profile.source_of_truth,
            data_classes=frozenset(source_profile.data_classes),
            confidentiality=source_profile.confidentiality,
            personal_data=source_profile.personal_data,
            purpose_refs=frozenset(source_profile.purpose_refs),
            retention_policy=source_profile.retention_policy,
            deletion_policy=source_profile.deletion_policy,
            residency_constraints=frozenset(source_profile.residency_constraints),
            authorized_consumers=frozenset(source_profile.authorized_consumers),
            processor_refs=frozenset(source_profile.processor_refs),
            export_policy=source_profile.export_policy,
            lineage=source_profile.lineage,
        )
        for field in _GOVERNANCE_CONTEXT_KEYS:
            if not _is_opaque_text(context_owned[field]):
                return (
                    None,
                    _pack(
                        [
                            _refusal(
                                f"{_GOVERNANCE_RESOLVE_SCOPE}.resolved_context",
                                field,
                                _OPAQUE_RULE,
                            )
                        ]
                    ),
                )
        if not _is_opaque_text(policy_owned["policy_reference"]):
            return (
                None,
                _pack(
                    [_refusal(f"{_GOVERNANCE_RESOLVE_SCOPE}.policy", "policy_reference", _OPAQUE_RULE)]
                ),
            )
        if not _is_complete_semver(policy_owned["policy_version"]):
            return (
                None,
                _pack(
                    [
                        _refusal(
                            f"{_GOVERNANCE_RESOLVE_SCOPE}.policy",
                            "policy_version",
                            "version SemVer complète exacte attendue",
                        )
                    ]
                ),
            )
        if validate_server_context_refs_values(context_owned):
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "resolved_context", _CONTEXT_RULE)]
                ),
            )
        for field in _GOVERNANCE_CONTEXT_KEYS:
            if context_owned[field] != expected_context[field]:
                return (
                    None,
                    _pack(
                        [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "resolved_context", _GOVERNANCE_DIVERGENT_RULE)]
                    ),
                )
        if validate_bulk_policy_values(policy_owned["limits"]):
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "policy.limits", "PolicyV1 exacte valide attendue")]),
            )
        if policy_owned["policy_reference"] != references_owned[0]:
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "policy.policy_reference", _GOVERNANCE_DIVERGENT_RULE)]
                ),
            )
        if policy_owned["policy_version"] != references_owned[1]:
            return (
                None,
                _pack(
                    [_refusal(_GOVERNANCE_RESOLVE_SCOPE, "policy.policy_version", _GOVERNANCE_DIVERGENT_RULE)]
                ),
            )
        for field in (
            "profile_version", "data_asset_id", "owner_component", "source_of_truth",
            "retention_policy", "deletion_policy", "export_policy", "lineage",
        ):
            if not _is_opaque_text(getattr(profile_owned, field)):
                return (None, _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"profile.{field}", _OPAQUE_RULE)]))
        for field in (
            "data_classes", "purpose_refs", "residency_constraints",
            "authorized_consumers", "processor_refs",
        ):
            for value in getattr(profile_owned, field):
                if not _is_opaque_text(value):
                    return (None, _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, f"profile.{field}", _OPAQUE_RULE)]))
        if validate_data_governance_profile(profile_owned):
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "profile", "profil de gouvernance exact valide attendu")]),
            )
        for item in obligations_owned:
            if not _is_opaque_text(item):
                return (
                    None,
                    _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "obligations", _OPAQUE_RULE)]),
                )
        try:
            context_snapshot = _build_server_context_refs_snapshot(context_owned)
        except (_ContractRefused, KeyError, TypeError):
            return (
                None,
                _pack([_refusal(_GOVERNANCE_RESOLVE_SCOPE, "resolved_context", _CONTEXT_RULE)]),
            )
        frozen_limits: dict = {}
        for key, value in policy_owned["limits"].items():
            if type(value) is list:
                frozen_limits[key] = tuple(value)
            else:
                frozen_limits[key] = value
        policy_snapshot = _GovernancePolicySnapshot(
            policy_reference=policy_owned["policy_reference"],
            policy_version=policy_owned["policy_version"],
            _limits_frozen=MappingProxyType(dict(frozen_limits)),
        )
        snapshot = _GovernanceResolutionSnapshot(
            resolution_version=_GOVERNANCE_VERSION,
            decision="RESOLVED",
            resolved_context=context_snapshot,
            policy=policy_snapshot,
            profile=profile_owned,
            obligations=obligations_owned,
        )
        return (snapshot, [])


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


def validate_publisher_contract(component: object) -> list[Diagnostic]:
    """Structure du port publisher ; aucune méthode invoquée."""
    return _structural_refusals(component, _PUBLISHER_METHODS, _PUBLISHER_SCOPE)


def validate_download_contract(component: object) -> list[Diagnostic]:
    """Structure du port de téléchargement ; aucune méthode invoquée."""
    return _structural_refusals(component, _DOWNLOAD_METHODS, _DOWNLOAD_SCOPE)


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
