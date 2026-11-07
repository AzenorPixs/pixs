"""Configuration désirée DNS : révision projetée, aucune lecture en base."""

from __future__ import annotations

from dataclasses import dataclass

from pixs.kernel.config.resolution import SecretReference
from pixs.kernel.data_governance_profile import DataGovernanceProfile, validate_data_governance_profile

__all__ = ["DesiredDnsConfig", "validate_desired_dns_config", "check_cas"]
SCHEMA_VERSION = "1.0.0"


def _is_str(v: object) -> bool:
    return type(v) is str and v != ""


def _is_int(v: object) -> bool:
    return type(v) is int


@dataclass(frozen=True, slots=True, repr=False)
class DesiredDnsConfig:
    schema_version: str
    owner_id: str
    config_revision: int
    suffix: str
    ttl_positive: int
    ttl_negative: int
    views: tuple
    governance: DataGovernanceProfile
    secret_refs: tuple


def _check_each_secret(refs: object, out: list) -> None:
    if type(refs) is not tuple:
        out.append("DNS_SECRET_REFS_TYPE")
        return
    for r in refs:
        if type(r) is not SecretReference:
            out.append("DNS_SECRET_REF_TYPE")
            return
        if not _is_str(r.owner_id) or not _is_str(r.entry_id) or not _is_str(r.source):
            out.append("DNS_SECRET_REF_FIELDS")
            return


def validate_desired_dns_config(cfg: object) -> list:
    if type(cfg) is not DesiredDnsConfig:
        return ["DNS_CONFIG_TYPE"]
    out: list = []
    if type(cfg.schema_version) is not str or cfg.schema_version != SCHEMA_VERSION:
        out.append("DNS_SCHEMA_VERSION_INVALID")
    if not _is_str(cfg.owner_id) or cfg.owner_id != "pixs.dns":
        out.append("DNS_OWNER_INVALID")
    if not _is_int(cfg.config_revision) or cfg.config_revision < 1:
        out.append("DNS_REVISION_INVALID")
    if not _is_str(cfg.suffix):
        out.append("DNS_SUFFIX_INVALID")
    if not _is_int(cfg.ttl_positive) or not 0 <= cfg.ttl_positive <= 30:
        out.append("DNS_TTL_POSITIVE_INVALID")
    if not _is_int(cfg.ttl_negative) or not 0 <= cfg.ttl_negative <= 5:
        out.append("DNS_TTL_NEGATIVE_INVALID")
    if type(cfg.views) is not tuple or len(cfg.views) == 0:
        out.append("DNS_VIEWS_INVALID")
    else:
        for v in cfg.views:
            if not _is_str(v):
                out.append("DNS_VIEWS_INVALID")
                break
    if type(cfg.governance) is not DataGovernanceProfile:
        out.append("DNS_GOVERNANCE_TYPE")
    else:
        if validate_data_governance_profile(cfg.governance):
            out.append("DNS_GOVERNANCE_INVALID")
        elif cfg.governance.owner_component != "pixs.dns":
            out.append("DNS_GOVERNANCE_OWNER_INVALID")
    _check_each_secret(cfg.secret_refs, out)
    return sorted(set(out))


def check_cas(expected_revision: object, current_revision: object) -> list:
    if type(expected_revision) is bool or type(current_revision) is bool:
        return ["DNS_CAS_TYPE"]
    if not _is_int(expected_revision) or not _is_int(current_revision):
        return ["DNS_CAS_TYPE"]
    if expected_revision < 0 or current_revision < 0:
        return ["DNS_CAS_NEGATIVE"]
    if expected_revision != current_revision:
        return ["DNS_CAS_MISMATCH"]
    return []
