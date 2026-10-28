"""Entrées HTTP C14 fermées vers les DTO publics, sans autorisation ni transport."""
from __future__ import annotations

from dataclasses import fields

from pixs.backend.api_pzt_dns_catalog import C14_HTTP_VERSION, C14HttpCatalogError, c14_http_binding
from pixs.core.authz.ports import Request
from pixs.core.command_metadata import CommandMetadata
from pixs.dns.configuration import DesiredDnsConfig, validate_desired_dns_config
from pixs.dns.contracts import (
    DeclareDesiredDns, RetireDesiredDns, DeclareName, RetireName,
    GetDesiredDns, GetAppliedDns, ResolveViewPolicy,
    validate_declare_desired_dns, validate_retire_desired_dns,
    validate_declare_name, validate_retire_name, validate_get_desired_dns,
    validate_get_applied_dns, validate_resolve_view_policy,
)
from pixs.kernel.config.resolution import SecretReference
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_governance_profile import DataGovernanceProfile, validate_data_governance_profile
from pixs.pzt.configuration import DesiredPztConfig, validate_desired_pzt_config
from pixs.pzt.contracts import (
    DeclareDesiredPzt, RetireDesiredPzt, GetDesiredPzt, GetAppliedPzt,
    validate_declare_desired_pzt, validate_retire_desired_pzt,
    validate_get_desired_pzt, validate_get_applied_pzt,
)

__all__ = ["C14HttpInputError", "parse_c14_http_input"]


class C14HttpInputError(ValueError):
    code = "C14_HTTP_INPUT_INVALID"

    def __init__(self):
        super().__init__("Entrée HTTP PZT/DNS invalide.")


def _text(value):
    if type(value) is not str or not value or "\x00" in value:
        raise C14HttpInputError()
    try:
        value.encode("utf-8")
    except UnicodeError:
        raise C14HttpInputError() from None
    return value


def _integer(value):
    if type(value) is not int:
        raise C14HttpInputError()
    return value


def _boolean(value):
    if type(value) is not bool:
        raise C14HttpInputError()
    return value


def _object(value, names):
    if (type(value) is not dict or any(type(k) is not str for k in value)
            or set(value) != set(names)):
        raise C14HttpInputError()
    return value


def _strings(value, *, unique=False):
    if type(value) is not list:
        raise C14HttpInputError()
    result = tuple(_text(item) for item in value)
    if unique and len(set(result)) != len(result):
        raise C14HttpInputError()
    return result


_GOV_SETS = frozenset(("data_classes", "purpose_refs", "residency_constraints",
                       "authorized_consumers", "processor_refs"))
_GOV_ENUMS = {"confidentiality": ConfidentialityLevel, "personal_data": PersonalDataLevel}


def _governance(value):
    data = _object(value, (f.name for f in fields(DataGovernanceProfile)))
    kwargs = {}
    for name, item in data.items():
        if name in _GOV_SETS:
            kwargs[name] = frozenset(_strings(item, unique=True))
        elif name in _GOV_ENUMS:
            try:
                kwargs[name] = _GOV_ENUMS[name](_text(item))
            except ValueError:
                raise C14HttpInputError() from None
        else:
            kwargs[name] = _text(item)
    profile = DataGovernanceProfile(**kwargs)
    if validate_data_governance_profile(profile):
        raise C14HttpInputError()
    # La validité du DTO ne donne aucune autorité à cette déclaration cliente.
    return profile


def _secrets(value):
    if type(value) is not list:
        raise C14HttpInputError()
    result = []
    for item in value:
        data = _object(item, ("owner_id", "entry_id", "source"))
        result.append(SecretReference(**{key: _text(v) for key, v in data.items()}))
    return tuple(result)


def _configuration(owner, value):
    cls, validator = ((DesiredPztConfig, validate_desired_pzt_config) if owner == "pixs.pzt"
                      else (DesiredDnsConfig, validate_desired_dns_config))
    data = _object(value, (f.name for f in fields(cls)))
    kwargs = {
        "schema_version": _text(data["schema_version"]),
        "owner_id": _text(data["owner_id"]),
        "config_revision": _integer(data["config_revision"]),
        "governance": _governance(data["governance"]),
        "secret_refs": _secrets(data["secret_refs"]),
    }
    if owner == "pixs.pzt":
        kwargs.update(v6_enabled=_boolean(data["v6_enabled"]), plan_ref=_text(data["plan_ref"]),
                      budget_ref=_text(data["budget_ref"]))
    else:
        kwargs.update(suffix=_text(data["suffix"]), ttl_positive=_integer(data["ttl_positive"]),
                      ttl_negative=_integer(data["ttl_negative"]), views=_strings(data["views"]))
    config = cls(**kwargs)
    if validator(config):
        raise C14HttpInputError()
    return config


_DECLARATION = ("schema_version", "resource_id", "expected_revision", "configuration")
_RETIREMENT = ("schema_version", "resource_id", "expected_revision", "reason")
_NAME_DECLARATION = ("schema_version", "resource_id", "expected_revision", "name", "view", "target_ref")
_NAME_RETIREMENT = ("schema_version", "resource_id", "expected_revision", "name", "view")
_DEFINITIONS = {
    "declare_desired_pzt": (DeclareDesiredPzt, validate_declare_desired_pzt, _DECLARATION),
    "retire_desired_pzt": (RetireDesiredPzt, validate_retire_desired_pzt, _RETIREMENT),
    "get_desired_pzt": (GetDesiredPzt, validate_get_desired_pzt, ("resource_id",)),
    "get_applied_pzt": (GetAppliedPzt, validate_get_applied_pzt, ("resource_id",)),
    "declare_desired_dns": (DeclareDesiredDns, validate_declare_desired_dns, _DECLARATION),
    "retire_desired_dns": (RetireDesiredDns, validate_retire_desired_dns, _RETIREMENT),
    "declare_name": (DeclareName, validate_declare_name, _NAME_DECLARATION),
    "retire_name": (RetireName, validate_retire_name, _NAME_RETIREMENT),
    "get_desired_dns": (GetDesiredDns, validate_get_desired_dns, ("resource_id",)),
    "get_applied_dns": (GetAppliedDns, validate_get_applied_dns, ("resource_id",)),
    "resolve_view_policy": (ResolveViewPolicy, validate_resolve_view_policy, ("resource_id", "view", "name")),
}


def parse_c14_http_input(owner, kind, name, payload, *, request, metadata=None):
    """Request et CommandMetadata viennent du serveur ; le JSON ne peut les fournir."""
    try:
        binding = c14_http_binding(owner, kind, name)
    except C14HttpCatalogError:
        raise C14HttpInputError() from None
    if type(request) is not Request:
        raise C14HttpInputError()
    if ((binding.kind == "COMMAND" and type(metadata) is not CommandMetadata)
            or (binding.kind == "QUERY" and metadata is not None)):
        raise C14HttpInputError()
    cls, validator, names = _DEFINITIONS[binding.name]
    data = _object(payload, names)
    kwargs = {"schema_version": C14_HTTP_VERSION, "request": request}
    if binding.kind == "COMMAND":
        if _text(data["schema_version"]) != C14_HTTP_VERSION:
            raise C14HttpInputError()
        kwargs["metadata"] = metadata
    for field, item in data.items():
        if field == "schema_version":
            continue
        if field == "configuration":
            kwargs[field] = _configuration(binding.owner, item)
        elif field == "expected_revision":
            kwargs[field] = _integer(item)
        else:
            kwargs[field] = _text(item)
    dto = cls(**kwargs)
    if validator(dto):
        raise C14HttpInputError()
    return dto
