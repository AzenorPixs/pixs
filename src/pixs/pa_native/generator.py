"""Génération du lien natif depuis un profil fermé et des objets inventoriés.

Empreintes/format ELF ne prouvent ni l'origine Cython ni un comportement :
les commandes de compilation, leur sortie et les recettes restent nécessaires.
Aucun objet n'est chargé ou exécuté par ce module.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path, PurePosixPath
import re
import struct

from .build_profile import BuildProfile, Operation, ProfileError

__all__ = ["ObjectRecord", "render_program"]
_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_HASH = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class ObjectRecord:
    module_name: str
    source: str
    object_path: str
    source_sha256: str
    object_sha256: str
    executables: tuple[str, ...]
    operations: tuple[Operation, ...]


_SYSTEM_PRIVATE_SOURCES = frozenset({
    "src/pixs/pa_native/libpq_inspection.pyx",
    "src/pixs/pa_native/nv_secret.pyx",
    "src/pixs/pa_native/nv_anchor.pyx",
    "src/pixs/pa_native/nv_journal.pyx",
    "src/pixs/pa_native/nv_intent.pyx",
    "src/pixs/pa_native/systemd_observation.pyx",
})


_INTENT_SOURCES = {
    "src/pixs/pa_native/nv_intent.pyx": "nv_intent",
    "src/pixs/pa_native/nv_anchor.pyx": "nv_anchor",
    "src/pixs/pa_native/nv_secret.pyx": "nv_secret",
    "src/pixs/pa_native/nv_journal.pyx": "nv_journal",
    "src/pixs/pa_native/postgresql_contracts.py": "postgresql_contracts",
}


def _check_intent_composition(records) -> None:
    if not any(record.source in ("src/pixs/pa_native/nv_intent.pyx",
                                  "src/pixs/pa_native/nv_anchor.pyx") for record in records):
        return
    for source, module in _INTENT_SOURCES.items():
        matches = [record for record in records if record.source == source]
        if (len(matches) != 1 or matches[0].module_name != module
                or "pixs-pa-system" not in matches[0].executables):
            raise ProfileError("PA01_INTENT_COMPOSITION_INCOMPLETE")


def _check_admin_composition(records) -> None:
    admins = [r for r in records if r.source == "src/pixs/pa_native/admin_withdrawal_contracts.py"]
    if not admins:
        return
    if len(admins) != 1 or admins[0].module_name != "admin_withdrawal_contracts" or tuple(admins[0].operations) != ():
        raise ProfileError("PA01_ADMIN_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_ADMIN_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in admins[0].executables):
        raise ProfileError("PA01_ADMIN_COMPOSITION_INCOMPLETE")


def _check_observation_composition(records) -> None:
    obs = [r for r in records if r.source == "src/pixs/pa_native/postgresql_observation.py"]
    if not obs:
        return
    if len(obs) != 1 or obs[0].module_name != "postgresql_observation" or tuple(obs[0].operations) != ():
        raise ProfileError("PA01_OBSERVATION_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_OBSERVATION_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in obs[0].executables):
        raise ProfileError("PA01_OBSERVATION_COMPOSITION_INCOMPLETE")


def _check_preconditions_composition(records) -> None:
    pre = [r for r in records if r.source == "src/pixs/pa_native/postgresql_preconditions.py"]
    if not pre:
        return
    if len(pre) != 1 or pre[0].module_name != "postgresql_preconditions" or tuple(pre[0].operations) != ():
        raise ProfileError("PA01_PRECONDITIONS_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_PRECONDITIONS_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in pre[0].executables):
        raise ProfileError("PA01_PRECONDITIONS_COMPOSITION_INCOMPLETE")


def _check_bootstrap_context_composition(records) -> None:
    ctx = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_context.py"]
    if not ctx:
        return
    if len(ctx) != 1 or ctx[0].module_name != "bootstrap_context" or tuple(ctx[0].operations) != ():
        raise ProfileError("PA01_BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in ctx[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE")


def _check_bootstrap_nv_profile_composition(records) -> None:
    nv = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_nv_profile.py"]
    if not nv:
        return
    if len(nv) != 1 or nv[0].module_name != "bootstrap_nv_profile" or tuple(nv[0].operations) != ():
        raise ProfileError("PA01_BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in nv[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE")


def _check_bootstrap_init_profile_composition(records) -> None:
    init = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_init_profile.py"]
    if not init:
        return
    if len(init) != 1 or init[0].module_name != "bootstrap_init_profile" or tuple(init[0].operations) != ():
        raise ProfileError("PA01_BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE")
    nv = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_nv_profile.py"]
    if len(nv) != 1 or nv[0].module_name != "bootstrap_nv_profile":
        raise ProfileError("PA01_BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in init[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE")
    if any(role not in nv[0].executables for role in init[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE")


def _check_bootstrap_base_composition(records) -> None:
    base = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_base.py"]
    if not base:
        return
    if len(base) != 1 or base[0].module_name != "bootstrap_base" or tuple(base[0].operations) != ():
        raise ProfileError("PA01_BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE")
    ctx = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_context.py"]
    if len(ctx) != 1 or ctx[0].module_name != "bootstrap_context":
        raise ProfileError("PA01_BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE")
    init = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_init_profile.py"]
    if len(init) != 1 or init[0].module_name != "bootstrap_init_profile":
        raise ProfileError("PA01_BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in base[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE")
    if any(role not in ctx[0].executables for role in base[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE")
    if any(role not in init[0].executables for role in base[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE")


def _check_bootstrap_resource_profile_composition(records) -> None:
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if not res:
        return
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile" or tuple(res[0].operations) != ():
        raise ProfileError("PA01_BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in res[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE")

def _check_bootstrap_policy_profile_composition(records) -> None:
    pol = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_policy_profile.py"]
    if not pol:
        return
    if len(pol) != 1 or pol[0].module_name != "bootstrap_policy_profile" or tuple(pol[0].operations) != ():
        raise ProfileError("PA01_BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE")
    nv = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_nv_profile.py"]
    if len(nv) != 1 or nv[0].module_name != "bootstrap_nv_profile":
        raise ProfileError("PA01_BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE")
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile":
        raise ProfileError("PA01_BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in pol[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE")
    if any(role not in nv[0].executables for role in pol[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE")
    if any(role not in res[0].executables for role in pol[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE")


def _check_bootstrap_prepublication_composition(records) -> None:
    pub = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_prepublication.py" or r.module_name == "bootstrap_prepublication"]
    if not pub:
        return
    if (len(pub) != 1 or pub[0].source != "src/pixs/pa_native/bootstrap_prepublication.py"
            or pub[0].module_name != "bootstrap_prepublication" or tuple(pub[0].operations) != ()):
        raise ProfileError("PA01_BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE")
    nv = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_nv_profile.py"]
    if len(nv) != 1 or nv[0].module_name != "bootstrap_nv_profile":
        raise ProfileError("PA01_BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE")
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile":
        raise ProfileError("PA01_BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in pub[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in nv[0].executables for role in pub[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in res[0].executables for role in pub[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE")


def _check_bootstrap_recipe_composition(records) -> None:
    rec = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_recipe.py" or r.module_name == "bootstrap_recipe"]
    if not rec:
        return
    if (len(rec) != 1 or rec[0].source != "src/pixs/pa_native/bootstrap_recipe.py"
            or rec[0].module_name != "bootstrap_recipe" or tuple(rec[0].operations) != ()):
        raise ProfileError("PA01_BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE")
    base = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_base.py"]
    if len(base) != 1 or base[0].module_name != "bootstrap_base":
        raise ProfileError("PA01_BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE")
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile":
        raise ProfileError("PA01_BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in rec[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE")
    if any(role not in base[0].executables for role in rec[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE")
    if any(role not in res[0].executables for role in rec[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE")


def _check_bootstrap_plan_composition(records) -> None:
    plan = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_plan.py" or r.module_name == "bootstrap_plan"]
    if not plan:
        return
    if (len(plan) != 1 or plan[0].source != "src/pixs/pa_native/bootstrap_plan.py"
            or plan[0].module_name != "bootstrap_plan" or tuple(plan[0].operations) != ()):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    base = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_base.py"]
    if len(base) != 1 or base[0].module_name != "bootstrap_base":
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    ctx = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_context.py"]
    if len(ctx) != 1 or ctx[0].module_name != "bootstrap_context":
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    nv = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_nv_profile.py"]
    if len(nv) != 1 or nv[0].module_name != "bootstrap_nv_profile":
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    pol = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_policy_profile.py"]
    if len(pol) != 1 or pol[0].module_name != "bootstrap_policy_profile":
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    pub = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_prepublication.py"]
    if len(pub) != 1 or pub[0].module_name != "bootstrap_prepublication":
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    rec = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_recipe.py"]
    if len(rec) != 1 or rec[0].module_name != "bootstrap_recipe":
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile":
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in plan[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in base[0].executables for role in plan[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in ctx[0].executables for role in plan[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in nv[0].executables for role in plan[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in pol[0].executables for role in plan[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in pub[0].executables for role in plan[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in rec[0].executables for role in plan[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in res[0].executables for role in plan[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE")


def _check_bootstrap_initial_record_composition(records) -> None:
    initial = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_initial_record.py" or r.module_name == "bootstrap_initial_record"]
    if not initial:
        return
    if (len(initial) != 1 or initial[0].source != "src/pixs/pa_native/bootstrap_initial_record.py"
            or initial[0].module_name != "bootstrap_initial_record" or tuple(initial[0].operations) != ()):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    base = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_base.py"]
    if len(base) != 1 or base[0].module_name != "bootstrap_base":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    ctx = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_context.py"]
    if len(ctx) != 1 or ctx[0].module_name != "bootstrap_context":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    nv = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_nv_profile.py"]
    if len(nv) != 1 or nv[0].module_name != "bootstrap_nv_profile":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    plan = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_plan.py"]
    if len(plan) != 1 or plan[0].module_name != "bootstrap_plan":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    pol = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_policy_profile.py"]
    if len(pol) != 1 or pol[0].module_name != "bootstrap_policy_profile":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    pub = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_prepublication.py"]
    if len(pub) != 1 or pub[0].module_name != "bootstrap_prepublication":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    rec = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_recipe.py"]
    if len(rec) != 1 or rec[0].module_name != "bootstrap_recipe":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile":
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in base[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in ctx[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in nv[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in plan[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in pol[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in pub[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in rec[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")
    if any(role not in res[0].executables for role in initial[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE")


def _check_bootstrap_history_composition(records) -> None:
    history = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_history.py" or r.module_name == "bootstrap_history"]
    if not history:
        return
    if (len(history) != 1 or history[0].source != "src/pixs/pa_native/bootstrap_history.py"
            or history[0].module_name != "bootstrap_history" or tuple(history[0].operations) != ()):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    base = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_base.py"]
    if len(base) != 1 or base[0].module_name != "bootstrap_base":
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    ctx = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_context.py"]
    if len(ctx) != 1 or ctx[0].module_name != "bootstrap_context":
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    r0 = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_initial_record.py"]
    if len(r0) != 1 or r0[0].module_name != "bootstrap_initial_record":
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    plan = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_plan.py"]
    if len(plan) != 1 or plan[0].module_name != "bootstrap_plan":
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    pol = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_policy_profile.py"]
    if len(pol) != 1 or pol[0].module_name != "bootstrap_policy_profile":
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    pub = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_prepublication.py"]
    if len(pub) != 1 or pub[0].module_name != "bootstrap_prepublication":
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile":
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in history[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    if any(role not in base[0].executables for role in history[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    if any(role not in ctx[0].executables for role in history[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    if any(role not in r0[0].executables for role in history[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    if any(role not in plan[0].executables for role in history[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    if any(role not in pol[0].executables for role in history[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    if any(role not in pub[0].executables for role in history[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")
    if any(role not in res[0].executables for role in history[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE")


def _check_bootstrap_provenance_composition(records) -> None:
    prov = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_provenance.py" or r.module_name == "bootstrap_provenance"]
    if not prov:
        return
    if (len(prov) != 1 or prov[0].source != "src/pixs/pa_native/bootstrap_provenance.py"
            or prov[0].module_name != "bootstrap_provenance" or tuple(prov[0].operations) != ()):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    base = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_base.py"]
    if len(base) != 1 or base[0].module_name != "bootstrap_base":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    ctx = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_context.py"]
    if len(ctx) != 1 or ctx[0].module_name != "bootstrap_context":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    init = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_init_profile.py"]
    if len(init) != 1 or init[0].module_name != "bootstrap_init_profile":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    r0 = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_initial_record.py"]
    if len(r0) != 1 or r0[0].module_name != "bootstrap_initial_record":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    nv = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_nv_profile.py"]
    if len(nv) != 1 or nv[0].module_name != "bootstrap_nv_profile":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    plan = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_plan.py"]
    if len(plan) != 1 or plan[0].module_name != "bootstrap_plan":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    pol = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_policy_profile.py"]
    if len(pol) != 1 or pol[0].module_name != "bootstrap_policy_profile":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    pub = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_prepublication.py"]
    if len(pub) != 1 or pub[0].module_name != "bootstrap_prepublication":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    rec = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_recipe.py"]
    if len(rec) != 1 or rec[0].module_name != "bootstrap_recipe":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile":
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in base[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in ctx[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in init[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in r0[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in nv[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in plan[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in pol[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in pub[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in rec[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")
    if any(role not in res[0].executables for role in prov[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PROVENANCE_COMPOSITION_INCOMPLETE")


def _check_bootstrap_publication_composition(records) -> None:
    fin = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_publication.py" or r.module_name == "bootstrap_publication"]
    if not fin:
        return
    if (len(fin) != 1 or fin[0].source != "src/pixs/pa_native/bootstrap_publication.py"
            or fin[0].module_name != "bootstrap_publication" or tuple(fin[0].operations) != ()):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    base = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_base.py"]
    if len(base) != 1 or base[0].module_name != "bootstrap_base":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    ctx = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_context.py"]
    if len(ctx) != 1 or ctx[0].module_name != "bootstrap_context":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    init = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_init_profile.py"]
    if len(init) != 1 or init[0].module_name != "bootstrap_init_profile":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    r0 = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_initial_record.py"]
    if len(r0) != 1 or r0[0].module_name != "bootstrap_initial_record":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    pre = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_prepublication.py"]
    if len(pre) != 1 or pre[0].module_name != "bootstrap_prepublication":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    pol = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_policy_profile.py"]
    if len(pol) != 1 or pol[0].module_name != "bootstrap_policy_profile":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    plan = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_plan.py"]
    if len(plan) != 1 or plan[0].module_name != "bootstrap_plan":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    prov = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_provenance.py"]
    if len(prov) != 1 or prov[0].module_name != "bootstrap_provenance":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    res = [r for r in records if r.source == "src/pixs/pa_native/bootstrap_resource_profile.py"]
    if len(res) != 1 or res[0].module_name != "bootstrap_resource_profile":
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in base[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in ctx[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in init[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in r0[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in pre[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in pol[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in plan[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in prov[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")
    if any(role not in res[0].executables for role in fin[0].executables):
        raise ProfileError("PA01_BOOTSTRAP_PUBLICATION_COMPOSITION_INCOMPLETE")


def _check_withdrawal_plan_composition(records) -> None:
    plans = [r for r in records if r.source == "src/pixs/pa_native/withdrawal_plan.py" or r.module_name == "withdrawal_plan"]
    if not plans:
        return
    if len(plans) != 1 or plans[0].source != "src/pixs/pa_native/withdrawal_plan.py" or plans[0].module_name != "withdrawal_plan" or tuple(plans[0].operations) != ():
        raise ProfileError("PA01_WITHDRAWAL_PLAN_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_WITHDRAWAL_PLAN_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in plans[0].executables):
        raise ProfileError("PA01_WITHDRAWAL_PLAN_COMPOSITION_INCOMPLETE")


def _check_withdrawal_confirmation_composition(records) -> None:
    confs = [r for r in records if r.source == "src/pixs/pa_native/withdrawal_confirmation.py" or r.module_name == "withdrawal_confirmation"]
    if not confs:
        return
    if len(confs) != 1 or confs[0].source != "src/pixs/pa_native/withdrawal_confirmation.py" or confs[0].module_name != "withdrawal_confirmation" or tuple(confs[0].operations) != ():
        raise ProfileError("PA01_WITHDRAWAL_CONFIRMATION_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_WITHDRAWAL_CONFIRMATION_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in confs[0].executables):
        raise ProfileError("PA01_WITHDRAWAL_CONFIRMATION_COMPOSITION_INCOMPLETE")


def _check_withdrawal_proofs_composition(records) -> None:
    proofs = [r for r in records if r.source == "src/pixs/pa_native/withdrawal_proofs.py" or r.module_name == "withdrawal_proofs"]
    if not proofs:
        return
    if len(proofs) != 1 or proofs[0].source != "src/pixs/pa_native/withdrawal_proofs.py" or proofs[0].module_name != "withdrawal_proofs" or tuple(proofs[0].operations) != ():
        raise ProfileError("PA01_WITHDRAWAL_PROOFS_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_WITHDRAWAL_PROOFS_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in proofs[0].executables):
        raise ProfileError("PA01_WITHDRAWAL_PROOFS_COMPOSITION_INCOMPLETE")


def _check_withdrawal_intent_composition(records) -> None:
    intents = [r for r in records if r.source == "src/pixs/pa_native/withdrawal_intent.py" or r.module_name == "withdrawal_intent"]
    if not intents:
        return
    if len(intents) != 1 or intents[0].source != "src/pixs/pa_native/withdrawal_intent.py" or intents[0].module_name != "withdrawal_intent" or tuple(intents[0].operations) != ():
        raise ProfileError("PA01_WITHDRAWAL_INTENT_COMPOSITION_INCOMPLETE")
    pg = [r for r in records if r.source == "src/pixs/pa_native/postgresql_contracts.py"]
    if len(pg) != 1 or pg[0].module_name != "postgresql_contracts":
        raise ProfileError("PA01_WITHDRAWAL_INTENT_COMPOSITION_INCOMPLETE")
    if any(role not in pg[0].executables for role in intents[0].executables):
        raise ProfileError("PA01_WITHDRAWAL_INTENT_COMPOSITION_INCOMPLETE")


def _check_private_roles(source: object, executables: tuple[str, ...]) -> None:
    if type(source) is not str:
        raise ProfileError("objet : source invalide")
    if source in _SYSTEM_PRIVATE_SOURCES and executables != ("pixs-pa-system",):
        raise ProfileError("PA01_PRIVATE_SOURCE_ROLE_FORBIDDEN")


def _relative(value: object) -> str:
    if type(value) is not str or not value or "\\" in value:
        raise ProfileError("objet : chemin relatif canonique requis")
    if PurePosixPath(value).is_absolute() or any(p in ("", ".", "..") for p in value.split("/")):
        raise ProfileError("objet : chemin sortant ou non canonique")
    return value


def _bytes(root: Path, relative: str, *, source: bool) -> bytes:
    relative = _relative(relative)
    if source:
        allowed = (relative.startswith("src/pixs/pa_native/")
                   or relative == "src/pixs/kernel/manifest/semver.py")
        if not allowed or PurePosixPath(relative).suffix not in (".py", ".pyx"):
            raise ProfileError("objet : source hors noyau natif autorisé")
        if any(p.startswith(".") or p in ("__pycache__", "env", "venv", "node_modules")
               or ".env." in p for p in relative.split("/")):
            raise ProfileError("objet : source exclue")
    elif PurePosixPath(relative).suffix != ".o":
        raise ProfileError("objet : fichier objet attendu")
    try:
        base = root.resolve(strict=True)
        path = base / relative
        current = base
        for part in PurePosixPath(relative).parts:
            current = current / part
            if current.is_symlink():
                raise ProfileError("objet : lien symbolique dans le chemin")
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(base) or not resolved.is_file():
            raise ProfileError("objet : fichier hors racine ou lien symbolique")
        return resolved.read_bytes()
    except OSError as error:
        raise ProfileError("objet : fichier indisponible") from error


def _check_hash(data: bytes, expected: object) -> None:
    if type(expected) is not str or _HASH.fullmatch(expected) is None:
        raise ProfileError("objet : empreinte invalide")
    if hashlib.sha256(data).hexdigest() != expected:
        raise ProfileError("objet : contenu changé depuis compilation")


def _checked_records(profile: BuildProfile, records: tuple[ObjectRecord, ...],
                     source_root: Path, object_root: Path) -> dict[str, ObjectRecord]:
    if type(records) is not tuple or not records:
        raise ProfileError("objets : inventaire explicite requis")
    roles = {e.name: e for e in profile.executables}
    expected = {o.name: o for o in profile.operations}
    names: dict[str, ObjectRecord] = {}
    paths = set()
    operations = {}
    for record in records:
        if type(record) is not ObjectRecord or type(record.module_name) is not str:
            raise ProfileError("objet : type invalide")
        if _NAME.fullmatch(record.module_name) is None or record.module_name in names:
            raise ProfileError("objet : module inconnu ou en doublon")
        _relative(record.object_path)
        if record.object_path in paths:
            raise ProfileError("objet : fichier lié plusieurs fois")
        if (type(record.executables) is not tuple or not record.executables
                or any(type(role) is not str or role not in roles for role in record.executables)
                or len(set(record.executables)) != len(record.executables)):
            raise ProfileError("objet : rôles de livraison invalides")
        _check_private_roles(record.source, record.executables)
        if type(record.operations) is not tuple:
            raise ProfileError("objet : opérations déclarées attendues")
        _check_hash(_bytes(source_root, record.source, source=True), record.source_sha256)
        content = _bytes(object_root, record.object_path, source=False)
        _check_hash(content, record.object_sha256)
        if (len(content) < 64 or content[:6] != b"\x7fELF\x02\x01"
                or struct.unpack_from("<HH", content, 16) != (1, 62)):
            raise ProfileError("objet : ELF relogeable x86_64 attendu")
        declared = {}
        for operation in record.operations:
            if (type(operation) is not Operation or type(operation.name) is not str or operation.name in operations
                    or expected.get(operation.name) != operation or operation.source != record.source):
                raise ProfileError("objet : opération absente, dupliquée ou incompatible")
            if any(operation.mode not in roles[role].modes for role in record.executables):
                raise ProfileError("objet : opération livrée au mauvais rôle")
            operations[operation.name] = operation
            declared[operation.name] = operation
        source_operations = {o.name: o for o in profile.operations if o.source == record.source}
        if declared != source_operations:
            raise ProfileError("objet : opérations de la source non représentées exactement")
        names[record.module_name] = record
        paths.add(record.object_path)
    if operations != expected:
        raise ProfileError("objets : catalogue compilé incomplet ou divergent")
    _check_intent_composition(records)
    _check_admin_composition(records)
    _check_observation_composition(records)
    _check_preconditions_composition(records)
    _check_bootstrap_context_composition(records)
    _check_bootstrap_nv_profile_composition(records)
    _check_bootstrap_init_profile_composition(records)
    _check_bootstrap_base_composition(records)
    _check_bootstrap_resource_profile_composition(records)
    _check_bootstrap_policy_profile_composition(records)
    _check_bootstrap_prepublication_composition(records)
    _check_bootstrap_recipe_composition(records)
    _check_bootstrap_plan_composition(records)
    _check_bootstrap_initial_record_composition(records)
    _check_bootstrap_history_composition(records)
    _check_bootstrap_provenance_composition(records)
    _check_bootstrap_publication_composition(records)
    _check_withdrawal_plan_composition(records)
    _check_withdrawal_confirmation_composition(records)
    _check_withdrawal_proofs_composition(records)
    _check_withdrawal_intent_composition(records)
    return names


def render_program(profile: BuildProfile, executable: str, entry_module: str,
                   records: tuple[ObjectRecord, ...], *, source_root: Path,
                   object_root: Path) -> str:
    """Produit du C, sans écrire, compiler, lier ou exécuter de fichier.

    Les enregistrements viennent du build de confiance et sont recoupés
    avec les octets source/objet. Ils ne sont pas des instructions réseau.
    La vérification du compilateur/provenance et les tests restent distincts.
    """
    names = _checked_records(profile, records, source_root, object_root)
    roles = {e.name: e for e in profile.executables}
    if type(executable) is not str or executable not in roles:
        raise ProfileError("lien : exécutable absent du profil")
    if type(entry_module) is not str or entry_module not in names:
        raise ProfileError("lien : module d'entrée absent")
    selected = sorted((r for r in records if executable in r.executables), key=lambda r: r.module_name)
    if names[entry_module] not in selected or names[entry_module].source != roles[executable].source:
        raise ProfileError("lien : entrée incompatible avec le rôle ou la source")
    expected = {o.name: o for o in profile.operations if o.mode in roles[executable].modes}
    delivered = {o.name: o for r in selected for o in r.operations}
    if delivered != expected:
        raise ProfileError("lien : catalogue du rôle divergent")
    lines = ['/* Généré depuis les objets inventoriés ; ne pas éditer. */',
             '#include "launcher.h"', ""]
    lines += ["PyMODINIT_FUNC PyInit_" + r.module_name + "(void);" for r in selected]
    lines += ["", "static struct _inittab pa01_builtin_modules[] = {"]
    lines += ['    {"' + r.module_name + '", PyInit_' + r.module_name + "}," for r in selected]
    lines += ["    {NULL, NULL}", "};", "",
              "const struct pa01_embedded_program pa01_program = {",
              '    1, "' + executable + '", "' + entry_module + '", pa01_builtin_modules',
              "};", ""]
    return "\n".join(lines)
