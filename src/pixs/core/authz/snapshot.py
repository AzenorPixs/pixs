"""Snapshot PDP : activation bornée avec normalisation réelle."""

from dataclasses import dataclass

from ..scope.context import ScopeContext, validate_structure
from .policy import (
    AuthenticationAssurance,
    Condition,
    Effect,
    FederationTrust,
    IdentityAssurance,
    Obligation,
    Policy,
    ScopeSelector,
    Selector,
    _is_utc_aware,
)


class SnapshotError(ValueError):
    def __init__(self):
        super().__init__("Snapshot PDP invalide.")
        self.code = "PDP_SNAPSHOT_INVALID"
        self.element = "pdp_snapshot"
        self.step = "build_snapshot"


_FORBIDDEN = ("*", "?", "[", "]")


def _clean_id(value, max_id):
    if type(value) is not str or value == "":
        raise SnapshotError()
    if len(value) > max_id:
        raise SnapshotError()
    for ch in _FORBIDDEN:
        if ch in value:
            raise SnapshotError()
    return True


def _is_member(value, enum_type):
    if value is None:
        return True
    for member in enum_type:
        if value is member:
            return True
    return False


@dataclass(frozen=True, slots=True, repr=False)
class Limits:
    max_policies: int
    max_selector_values: int
    max_conditions_per_policy: int
    max_set_values: int
    max_attributes: int
    max_memberships: int
    max_id_length: int
    max_value_length: int
    max_cost: int
    ttl_seconds: int
    max_freshness_seconds: int

    def __post_init__(self):
        for name in (
            "max_policies", "max_selector_values",
            "max_conditions_per_policy", "max_set_values",
            "max_attributes", "max_memberships", "max_id_length",
            "max_value_length", "max_cost", "ttl_seconds",
            "max_freshness_seconds",
        ):
            try:
                value = object.__getattribute__(self, name)
            except Exception:
                raise SnapshotError() from None
            if type(value) is bool or type(value) is not int or value <= 0:
                raise SnapshotError()


@dataclass(frozen=True, slots=True, repr=False)
class Catalog:
    subject_ids: tuple
    resource_ids: tuple
    action_ids: tuple
    scope_contexts: tuple
    attribute_types: tuple

    def __post_init__(self):
        for name in (
            "subject_ids", "resource_ids", "action_ids",
            "scope_contexts", "attribute_types",
        ):
            try:
                value = object.__getattribute__(self, name)
            except Exception:
                raise SnapshotError() from None
            if type(value) is not tuple:
                raise SnapshotError()


@dataclass(frozen=True, slots=True, repr=False)
class Snapshot:
    epoch: str
    catalog: Catalog
    limits: Limits
    policies: tuple

    def __post_init__(self):
        try:
            epoch = object.__getattribute__(self, "epoch")
            catalog = object.__getattribute__(self, "catalog")
            limits = object.__getattribute__(self, "limits")
            policies = object.__getattribute__(self, "policies")
        except Exception:
            raise SnapshotError() from None
        if type(epoch) is not str or type(catalog) is not Catalog:
            raise SnapshotError()
        if type(limits) is not Limits or type(policies) is not tuple:
            raise SnapshotError()

    @property
    def version(self):
        epoch = object.__getattribute__(self, "epoch")
        policies = object.__getattribute__(self, "policies")
        return (
            epoch,
            tuple(
                (
                    object.__getattribute__(p, "policy_id"),
                    object.__getattribute__(p, "policy_version"),
                )
                for p in policies
            ),
        )


def _scope_key(ctx):
    stype = object.__getattribute__(ctx, "scope_type")
    tenant = object.__getattribute__(ctx, "tenant_id")
    scp = object.__getattribute__(ctx, "scope_id")
    return (
        object.__getattribute__(stype, "value"),
        tenant if tenant is not None else "",
        scp if scp is not None else "",
    )


def validate_snapshot(snapshot):
    try:
        if type(snapshot) is not Snapshot:
            raise SnapshotError()
        return build_snapshot(
            object.__getattribute__(snapshot, "epoch"),
            object.__getattribute__(snapshot, "policies"),
            object.__getattribute__(snapshot, "catalog"),
            object.__getattribute__(snapshot, "limits"),
        )
    except SnapshotError:
        raise
    except Exception:
        raise SnapshotError() from None


def build_snapshot(epoch, policies, catalog, limits):
    try:
        if type(limits) is not Limits:
            raise SnapshotError()
        vals = {}
        for name in (
            "max_policies", "max_selector_values",
            "max_conditions_per_policy", "max_set_values",
            "max_attributes", "max_memberships", "max_id_length",
            "max_value_length", "max_cost", "ttl_seconds",
            "max_freshness_seconds",
        ):
            value = object.__getattribute__(limits, name)
            if type(value) is bool or type(value) is not int or value <= 0:
                raise SnapshotError()
            vals[name] = value
        max_id = vals["max_id_length"]
        max_val = vals["max_value_length"]
        max_cost = vals["max_cost"]
        cost = [0]

        def _spend(units):
            cost[0] += units
            if cost[0] > max_cost:
                raise SnapshotError()

        def _sorted_bounded(items, key=None):
            n = len(items)
            _spend(n * max(1, n.bit_length()) + n)
            if key is None:
                return sorted(items)
            return sorted(items, key=key)

        if type(epoch) is not str or epoch == "" or len(epoch) > max_id:
            raise SnapshotError()
        for ch in _FORBIDDEN:
            if ch in epoch:
                raise SnapshotError()
        if type(catalog) is not Catalog or type(policies) is not tuple:
            raise SnapshotError()
        if len(policies) > vals["max_policies"]:
            raise SnapshotError()
        _spend(1 + len(policies))
        subjects = object.__getattribute__(catalog, "subject_ids")
        resources = object.__getattribute__(catalog, "resource_ids")
        actions = object.__getattribute__(catalog, "action_ids")
        scopes = object.__getattribute__(catalog, "scope_contexts")
        attr_types = object.__getattribute__(catalog, "attribute_types")
        for coll in (subjects, resources, actions, scopes, attr_types):
            if type(coll) is not tuple:
                raise SnapshotError()
        if (
            len(subjects) == 0 or len(subjects) > vals["max_selector_values"]
            or len(resources) == 0
            or len(resources) > vals["max_selector_values"]
            or len(actions) == 0 or len(actions) > vals["max_selector_values"]
            or len(scopes) == 0 or len(scopes) > vals["max_selector_values"]
            or len(attr_types) > vals["max_attributes"]
        ):
            raise SnapshotError()
        _spend(len(subjects) + len(resources) + len(actions)
               + len(scopes) + len(attr_types))
        for coll in (subjects, resources, actions):
            _spend(len(coll))
            for value in coll:
                _clean_id(value, max_id)
                _spend(1 + len(value))
        attr_map = {}
        for entry in attr_types:
            if type(entry) is not tuple or len(entry) != 2:
                raise SnapshotError()
            name, tag = entry
            if type(name) is not str or name == "" or len(name) > max_id:
                raise SnapshotError()
            for ch in _FORBIDDEN:
                if ch in name:
                    raise SnapshotError()
            if type(tag) is not str or tag not in ("STR", "INT"):
                raise SnapshotError()
            if name in attr_map:
                raise SnapshotError()
            attr_map[name] = tag
            _spend(1 + len(name))
        scope_map = {}
        for ctx in scopes:
            if type(ctx) is not ScopeContext:
                raise SnapshotError()
            try:
                validate_structure(ctx)
            except Exception:
                raise SnapshotError() from None
            tenant = object.__getattribute__(ctx, "tenant_id")
            scp = object.__getattribute__(ctx, "scope_id")
            if tenant is not None:
                _clean_id(tenant, max_id)
                _spend(1 + len(tenant))
            if scp is not None:
                _clean_id(scp, max_id)
                _spend(1 + len(scp))
            key = _scope_key(ctx)
            if key in scope_map:
                raise SnapshotError()
            scope_map[key] = ctx
            _spend(2)
        if (len(set(subjects)) != len(subjects)
                or len(set(resources)) != len(resources)
                or len(set(actions)) != len(actions)):
            raise SnapshotError()
        _spend(len(subjects) + len(resources) + len(actions))
        subject_pool = set(subjects)
        resource_pool = set(resources)
        action_pool = set(actions)
        scope_pool = set(scope_map.keys())
        canon_subjects = tuple(_sorted_bounded(list(subject_pool)))
        canon_resources = tuple(_sorted_bounded(list(resource_pool)))
        canon_actions = tuple(_sorted_bounded(list(action_pool)))
        canon_scopes = tuple(
            _sorted_bounded(list(scope_map.values()), key=_scope_key))
        canon_attrs = tuple(
            _sorted_bounded(list(attr_map.items())))
        canon_catalog = Catalog(
            canon_subjects, canon_resources, canon_actions,
            canon_scopes, canon_attrs)
        norm_policies = []
        seen_ids = set()
        for policy in policies:
            if type(policy) is not Policy:
                raise SnapshotError()
            _spend(5)
            pid = object.__getattribute__(policy, "policy_id")
            ver = object.__getattribute__(policy, "policy_version")
            owner = object.__getattribute__(policy, "owner")
            for field in (pid, ver, owner):
                _clean_id(field, max_id)
                _spend(1 + len(field))
            if pid in seen_ids:
                raise SnapshotError()
            seen_ids.add(pid)
            _spend(1)
            effect = object.__getattribute__(policy, "effect")
            if type(effect) is not Effect:
                raise SnapshotError()
            subj = object.__getattribute__(policy, "subject")
            res = object.__getattribute__(policy, "resource")
            act = object.__getattribute__(policy, "action")
            scp_sel = object.__getattribute__(policy, "scope")
            if (type(subj) is not Selector or type(res) is not Selector
                    or type(act) is not Selector
                    or type(scp_sel) is not ScopeSelector):
                raise SnapshotError()
            norm_sels = {}
            for sel, pool, kind in (
                (subj, subject_pool, "subject"),
                (res, resource_pool, "resource"),
                (act, action_pool, "action"),
            ):
                skind = object.__getattribute__(sel, "kind")
                svals = object.__getattribute__(sel, "values")
                if type(skind) is not str or skind != kind:
                    raise SnapshotError()
                if type(svals) is not tuple or len(svals) == 0:
                    raise SnapshotError()
                if len(svals) > vals["max_selector_values"]:
                    raise SnapshotError()
                _spend(len(svals))
                for value in svals:
                    _clean_id(value, max_id)
                    if value not in pool:
                        raise SnapshotError()
                    _spend(1)
                norm_sels[kind] = Selector(
                    kind, tuple(_sorted_bounded(list(set(svals)))))
            sctxs = object.__getattribute__(scp_sel, "contexts")
            if type(sctxs) is not tuple or len(sctxs) == 0:
                raise SnapshotError()
            if len(sctxs) > vals["max_selector_values"]:
                raise SnapshotError()
            _spend(len(sctxs))
            smap = {}
            for ctx in sctxs:
                if type(ctx) is not ScopeContext:
                    raise SnapshotError()
                try:
                    validate_structure(ctx)
                except Exception:
                    raise SnapshotError() from None
                for field in ("tenant_id", "scope_id"):
                    value = object.__getattribute__(ctx, field)
                    if value is not None:
                        _clean_id(value, max_id)
                        _spend(1 + len(value))
                key = _scope_key(ctx)
                if key not in scope_pool:
                    raise SnapshotError()
                if key not in smap:
                    smap[key] = ctx
                _spend(2)
            norm_scope = ScopeSelector(
                tuple(_sorted_bounded(list(smap.values()), key=_scope_key)))
            conds = object.__getattribute__(policy, "conditions")
            obls = object.__getattribute__(policy, "obligations")
            if type(conds) is not tuple or type(obls) is not tuple:
                raise SnapshotError()
            if len(conds) > vals["max_conditions_per_policy"]:
                raise SnapshotError()
            if len(obls) > vals["max_set_values"]:
                raise SnapshotError()
            _spend(len(conds) + len(obls))
            norm_conds = []
            for cond in conds:
                if type(cond) is not Condition:
                    raise SnapshotError()
                attr = object.__getattribute__(cond, "attr")
                op = object.__getattribute__(cond, "op")
                value = object.__getattribute__(cond, "value")
                _clean_id(attr, max_id)
                _spend(1 + len(attr))
                if attr not in attr_map:
                    raise SnapshotError()
                if type(op) is not str or op not in ("eq", "in"):
                    raise SnapshotError()
                tag = attr_map[attr]
                if op == "eq":
                    if tag == "STR":
                        if type(value) is not str or value == "":
                            raise SnapshotError()
                        if len(value) > max_val:
                            raise SnapshotError()
                        _spend(1 + len(value))
                        norm_conds.append(Condition(attr, op, value))
                    else:
                        if type(value) is not int or type(value) is bool:
                            raise SnapshotError()
                        if value.bit_length() > max_val:
                            raise SnapshotError()
                        _spend(2)
                        norm_conds.append(Condition(attr, op, value))
                else:
                    if type(value) is not tuple or len(value) == 0:
                        raise SnapshotError()
                    if len(value) > vals["max_set_values"]:
                        raise SnapshotError()
                    _spend(len(value))
                    items = []
                    for item in value:
                        if tag == "STR":
                            if type(item) is not str or item == "":
                                raise SnapshotError()
                            if len(item) > max_val:
                                raise SnapshotError()
                            _spend(1 + len(item))
                        else:
                            if type(item) is not int or type(item) is bool:
                                raise SnapshotError()
                            if item.bit_length() > max_val:
                                raise SnapshotError()
                            _spend(2)
                        items.append(item)
                    norm_items = tuple(_sorted_bounded(list(set(items))))
                    norm_conds.append(Condition(attr, op, norm_items))
            norm_conds = tuple(_sorted_bounded(
                norm_conds,
                key=lambda c: (
                    object.__getattribute__(c, "attr"),
                    object.__getattribute__(c, "op"),
                    object.__getattribute__(c, "value"),
                )))
            for obl in obls:
                if type(obl) is not Obligation:
                    raise SnapshotError()
                kind = object.__getattribute__(obl, "kind")
                if type(kind) is not str or kind != "AUDIT":
                    raise SnapshotError()
                _spend(1)
            norm_obls = (Obligation("AUDIT"),) if len(obls) > 0 else ()
            vfrom = object.__getattribute__(policy, "valid_from")
            vuntil = object.__getattribute__(policy, "valid_until")
            for bound in (vfrom, vuntil):
                if bound is not None and not _is_utc_aware(bound):
                    raise SnapshotError()
            if (vfrom is not None and vuntil is not None
                    and vfrom >= vuntil):
                raise SnapshotError()
            if not _is_member(
                    object.__getattribute__(policy, "min_identity_assurance"),
                    IdentityAssurance):
                raise SnapshotError()
            if not _is_member(
                    object.__getattribute__(
                        policy, "min_authentication_assurance"),
                    AuthenticationAssurance):
                raise SnapshotError()
            if not _is_member(
                    object.__getattribute__(policy, "min_federation_trust"),
                    FederationTrust):
                raise SnapshotError()
            max_age = object.__getattribute__(policy, "max_auth_age_seconds")
            if max_age is not None:
                if type(max_age) is bool or type(max_age) is not int:
                    raise SnapshotError()
                if max_age <= 0 or max_age.bit_length() > max_val:
                    raise SnapshotError()
            norm_policies.append(
                Policy(
                    pid, ver, owner, effect, norm_sels["subject"],
                    norm_sels["resource"], norm_sels["action"],
                    norm_scope, tuple(norm_conds), norm_obls,
                    vfrom, vuntil,
                    object.__getattribute__(
                        policy, "min_identity_assurance"),
                    object.__getattribute__(
                        policy, "min_authentication_assurance"),
                    object.__getattribute__(policy, "min_federation_trust"),
                    max_age,
                )
            )
        norm_policies = tuple(_sorted_bounded(
            norm_policies,
            key=lambda p: (
                object.__getattribute__(p, "policy_id"),
                object.__getattribute__(p, "policy_version"),
            )))
        return Snapshot(epoch, canon_catalog, limits, norm_policies)
    except SnapshotError:
        raise
    except Exception:
        raise SnapshotError() from None


__all__ = [
    "SnapshotError",
    "Limits",
    "Catalog",
    "Snapshot",
    "build_snapshot",
    "validate_snapshot",
]
