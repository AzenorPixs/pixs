"""Configuration désirée PZT : révision projetée, aucune lecture en base."""

from __future__ import annotations

from dataclasses import dataclass

from pixs.kernel.config.resolution import SecretReference
from pixs.kernel.data_governance_profile import DataGovernanceProfile, validate_data_governance_profile

__all__ = ["DesiredPztConfig", "validate_desired_pzt_config", "check_cas"]
SCHEMA_VERSION = "1.0.0"


def _is_str(v: object) -> bool:
    return type(v) is str and v != ""


def _is_int(v: object) -> bool:
    return type(v) is int


def _is_bool(v: object) -> bool:
    return type(v) is bool


@dataclass(frozen=True, slots=True, repr=False)
class DesiredPztConfig:
    schema_version: str
    owner_id: str
    config_revision: int
    v6_enabled: bool
    plan_ref: str
    budget_ref: str
    governance: DataGovernanceProfile
    secret_refs: tuple


def _check_each_secret(refs: object, out: list) -> None:
    if type(refs) is not tuple:
        out.append("PZT_SECRET_REFS_TYPE")
        return
    for r in refs:
        if type(r) is not SecretReference:
            out.append("PZT_SECRET_REF_TYPE")
            return
        if not _is_str(r.owner_id) or not _is_str(r.entry_id) or not _is_str(r.source):
            out.append("PZT_SECRET_REF_FIELDS")
            return


def validate_desired_pzt_config(cfg: object) -> list:
    if type(cfg) is not DesiredPztConfig:
        return ["PZT_CONFIG_TYPE"]
    out: list = []
    if type(cfg.schema_version) is not str or cfg.schema_version != SCHEMA_VERSION:
        out.append("PZT_SCHEMA_VERSION_INVALID")
    if not _is_str(cfg.owner_id) or cfg.owner_id != "pixs.pzt":
        out.append("PZT_OWNER_INVALID")
    if not _is_int(cfg.config_revision) or cfg.config_revision < 1:
        out.append("PZT_REVISION_INVALID")
    if not _is_bool(cfg.v6_enabled):
        out.append("PZT_V6_INVALID")
    if not _is_str(cfg.plan_ref):
        out.append("PZT_PLAN_INVALID")
    if not _is_str(cfg.budget_ref):
        out.append("PZT_BUDGET_INVALID")
    if type(cfg.governance) is not DataGovernanceProfile:
        out.append("PZT_GOVERNANCE_TYPE")
    else:
        if validate_data_governance_profile(cfg.governance):
            out.append("PZT_GOVERNANCE_INVALID")
        elif cfg.governance.owner_component != "pixs.pzt":
            out.append("PZT_GOVERNANCE_OWNER_INVALID")
    _check_each_secret(cfg.secret_refs, out)
    return sorted(set(out))


def check_cas(expected_revision: object, current_revision: object) -> list:
    if type(expected_revision) is bool or type(current_revision) is bool:
        return ["PZT_CAS_TYPE"]
    if not _is_int(expected_revision) or not _is_int(current_revision):
        return ["PZT_CAS_TYPE"]
    if expected_revision < 0 or current_revision < 0:
        return ["PZT_CAS_NEGATIVE"]
    if expected_revision != current_revision:
        return ["PZT_CAS_MISMATCH"]
    return []
