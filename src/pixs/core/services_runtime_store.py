"""Store autorisation runtime C04 : backend explicite, epingle TX, cles C02 exactes.

Configuration : alias, installation_ref, base_epoch, Catalog, Limits.
Snapshot epingle avant effets dans cette TX, cache immuable cle par
transaction_identity reelle + pile savepoints + acteur + contexte.
Aucune table Auth/Audit importee. Mapping C02 : subject_ref brut canonique
typé valide, resolu vers objet exact puis compile pour acteur prefixe.
Topologie vraie CoreScope/CoreTenant avec ancetres depuis PLATFORM.
Version : (epoch:str, tuple[(policy_id, policy_version)]), epoch = SHA256
complet 64 caracteres, refuse si max_id_length < 64.
Etats Root : ORDINARY / PERMITTED / UNGRANTED.
"""
from __future__ import annotations

import hashlib
import json
import uuid
import threading
from dataclasses import fields, replace

from django.db import connections

from pixs.core.authz.policy import Effect, Policy, PolicyError, Selector, ScopeSelector, Obligation
from pixs.core.authz.snapshot import Catalog, Limits, Snapshot, build_snapshot
from pixs.core.persistence.models_authz import encode_policy
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.query_source import CoreFactSource, _make_ref
from pixs.core.scope.context import ScopeContext, ScopeType, validate_structure
from pixs.core.scope.topology import ScopeNode, TopologySnapshot
from pixs.core.services_authorization_guard import (
    acquire_catalog_guard,
    transaction_identity,
)
from pixs.core.services_common import CoreServiceError, lock_scopes
from pixs.core.services_scope import _validate_context_under_locks

__all__ = ["CoreAuthorizationStore", "ACTOR_PREFIX", "ROOT_ORDINARY", "ROOT_PERMITTED", "ROOT_UNGRANTED"]

ACTOR_PREFIX = "pixs.core.identity:"
USER_PREFIX = "pixs.core.user:"
GROUP_PREFIX = "pixs.core.group:"
ROOT_ORDINARY = "ORDINARY"
ROOT_PERMITTED = "PERMITTED"
ROOT_UNGRANTED = "UNGRANTED"
_FORBIDDEN = ("*", "?", "[", "]")


def _is_id(v: object) -> bool:
    return type(v) is str and v != ""


def _identity_tail(actor_ref: object) -> str:
    if type(actor_ref) is not str or not actor_ref.startswith(ACTOR_PREFIX):
        raise CoreServiceError("SUJET_DIVERGENT") from None
    tail = actor_ref[len(ACTOR_PREFIX):]
    try:
        parsed = uuid.UUID(tail)
    except (ValueError, AttributeError, TypeError):
        raise CoreServiceError("SUJET_DIVERGENT") from None
    if str(parsed) != tail:
        raise CoreServiceError("SUJET_DIVERGENT") from None
    try:
        check_uuid7(parsed)
    except Uuid7Error:
        raise CoreServiceError("SUJET_DIVERGENT") from None
    return tail


def _hex(tail: str) -> str:
    return object.__getattribute__(uuid.UUID(tail), "hex")


def _is_raw_uuid7(value: object) -> bool:
    if type(value) is not str or value == "":
        return False
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError, TypeError):
        return False
    if str(parsed) != value:
        return False
    try:
        check_uuid7(parsed)
    except Uuid7Error:
        return False
    return True


def _check_literal(value: object) -> None:
    if type(value) is not str or value == "":
        raise CoreServiceError("FAITS_INVALIDES") from None
    for ch in _FORBIDDEN:
        if ch in value:
            raise CoreServiceError("FAITS_INVALIDES") from None
    if value.startswith("resourceType:"):
        raise CoreServiceError("FAITS_INVALIDES") from None


def _data(item) -> dict:
    return {k: v for k, v in object.__getattribute__(item, "data")}


def _context_key(context: ScopeContext) -> tuple:
    return (
        object.__getattribute__(context, "scope_type").value,
        object.__getattribute__(context, "tenant_id"),
        object.__getattribute__(context, "scope_id"),
    )


class CoreAuthorizationStore:
    """Backend explicite avec cache epingle pre-effet dans cette TX."""

    def __init__(self, *, alias: str, installation_ref: str, base_epoch: str, catalog: Catalog, limits: Limits) -> None:
        if type(alias) is not str or alias == "":
            raise CoreServiceError("ALIAS_INVALIDE") from None
        if type(installation_ref) is not str or installation_ref == "":
            raise CoreServiceError("FAITS_INVALIDES") from None
        if type(base_epoch) is not str or base_epoch == "" or any(c in base_epoch for c in _FORBIDDEN):
            raise CoreServiceError("FAITS_INVALIDES") from None
        if type(catalog) is not Catalog or type(limits) is not Limits:
            raise CoreServiceError("FAITS_INVALIDES") from None
        try:
            catalog.__post_init__()
            limits.__post_init__()
        except Exception as error:
            raise CoreServiceError("FAITS_INVALIDES") from error
        if limits.max_id_length < 64:
            raise CoreServiceError("FAITS_INVALIDES") from None
        self._alias = alias
        self._installation = installation_ref
        self._base_epoch = base_epoch
        self._catalog = catalog
        self._limits = limits
        self._facts = CoreFactSource()
        self._cache: dict = {}
        self._cache_transaction = None
        self._mutex = threading.RLock()
        self._material = []

    def catalog_guard(self, *, exclusive: bool) -> None:
        if type(exclusive) is not bool:
            raise CoreServiceError("SCOPES_INVALIDES") from None
        acquire_catalog_guard(self._alias, exclusive)

    def required_scopes(self, *, context: ScopeContext, actor_ref: str) -> tuple[str, ...]:
        tail = _identity_tail(actor_ref)
        try:
            validate_structure(context)
        except Exception as error:
            raise CoreServiceError("CONTEXTE_INVALIDE") from error
        scopes: set[str] = set()
        scopes.add("uuid:" + _hex(tail))
        scopes.add("binding:" + self._installation)
        if context.scope_type is ScopeType.TENANT:
            scopes.add("tenant:" + context.tenant_id)
        return tuple(sorted(scopes))

    def _savepoint_key(self) -> tuple:
        try:
            ids = object.__getattribute__(connections[self._alias], "savepoint_ids")
            return tuple(ids)
        except Exception as error:
            raise CoreServiceError("BASE_INDETERMINEE") from error

    def _read_refs(self, kind: str, refs: tuple[str, ...], context: ScopeContext, limit: int):
        items = self._facts.read_facts(kind, refs, context, self._alias, limit)
        if type(items) is not tuple or len(items) > limit:
            raise CoreServiceError("BORNE_INVALIDE") from None
        self._material.append((kind, _context_key(context),
                               tuple((i.ref, i.version, i.data) for i in items)))
        return items

    def _read_bounded(self, kind: str, context: ScopeContext, limit: int):
        refs = self._facts.candidates(kind, context, self._alias, limit)
        if type(refs) is not tuple or len(refs) > limit:
            raise CoreServiceError("BORNE_INVALIDE") from None
        return self._read_refs(kind, refs, context, limit)

    def _load_topology(self, context: ScopeContext) -> TopologySnapshot:
        if context.scope_type is ScopeType.PLATFORM:
            return TopologySnapshot()
        # Racine du seul tenant : tous les ancêtres sont inclus, sans lire les autres tenants.
        root = ScopeContext(ScopeType.TENANT, context.tenant_id, None)
        tenants = self._read_bounded("TENANT", root, self._limits.max_selector_values)
        scopes = self._read_bounded("SCOPE", root, self._limits.max_selector_values)
        return TopologySnapshot(
            tuple(sorted(_data(i)["tenant_id"] for i in tenants)),
            tuple(ScopeNode(d["scope_id"], d["tenant_id"], d["parent_scope_id"])
                  for d in (_data(i) for i in scopes)),
        )

    def _load_actor_stepwise(self, context: ScopeContext, actor_ref: str) -> dict:
        tail = _identity_tail(actor_ref)
        identities = self._read_refs("IDENTITY", (actor_ref,), context, 1)
        found = None
        for item in identities:
            data = _data(item)
            if data.get("identity_id") == tail:
                found = data
        if found is None or found.get("state") != "ACTIVE":
            raise CoreServiceError("SUJET_DIVERGENT") from None
        actor = {"identity_id": tail, "identity_type": found["identity_type"],
                 "user_id": None, "groups": (), "direct_roles": (),
                 "user_roles": (), "group_roles": ()}
        state, sources = self._load_super_admin(context, actor)
        actor["root_state"], actor["root_sources"] = state, sources
        if state != ROOT_ORDINARY:
            return actor
        links = self._read_bounded("LINK", context, self._limits.max_selector_values)
        user_ref: str | None = None
        for item in links:
            data = _data(item)
            if data.get("identity_id") == tail:
                if user_ref is not None:
                    raise CoreServiceError("FAITS_INVALIDES") from None
                if not _is_raw_uuid7(data.get("user_id")):
                    raise CoreServiceError("FAITS_INVALIDES") from None
                user_ref = data.get("user_id")
        if user_ref is not None:
            lock_scopes(self._alias, ("uuid:" + uuid.UUID(user_ref).hex,), shared=True)
            users = self._read_refs("USER", (USER_PREFIX + user_ref,), context, 1)
            if len(users) != 1:
                raise CoreServiceError("SUJET_DIVERGENT") from None
        memberships = self._read_bounded("USER_GROUP", context, self._limits.max_selector_values) if user_ref is not None else ()
        groups: set[str] = set()
        for item in memberships:
            data = _data(item)
            if data.get("user_id") == user_ref:
                if not _is_raw_uuid7(data.get("group_id")):
                    raise CoreServiceError("FAITS_INVALIDES") from None
                groups.add(data.get("group_id"))
        if groups:
            lock_scopes(self._alias, tuple(sorted("uuid:" + uuid.UUID(g).hex for g in groups)), shared=True)
            recheck = self._read_bounded("GROUP", context, self._limits.max_selector_values)
            present = {d.get("group_id") for d in (_data(i) for i in recheck)}
            if not set(groups) <= set(present):
                raise CoreServiceError("FAITS_INVALIDES") from None
        assignments = self._read_bounded("ROLE_ASSIGNMENT", context, self._limits.max_selector_values)
        direct_roles: set[str] = set()
        user_roles: set[str] = set()
        group_roles: set[str] = set()
        for item in assignments:
            data = _data(item)
            stype = data.get("subject_type")
            sref = data.get("subject_ref")
            if stype not in ("USER", "IDENTITY", "GROUP") or not _is_raw_uuid7(sref):
                raise CoreServiceError("FAITS_INVALIDES") from None
            if stype == "IDENTITY" and sref == tail:
                direct_roles.add(data.get("role_id"))
            elif stype == "USER" and user_ref is not None and sref == user_ref:
                user_roles.add(data.get("role_id"))
            elif stype == "GROUP" and sref in groups:
                group_roles.add(data.get("role_id"))
        actor.update(user_id=user_ref, groups=tuple(sorted(groups)),
                     direct_roles=tuple(sorted(direct_roles)),
                     user_roles=tuple(sorted(user_roles)), group_roles=tuple(sorted(group_roles)))
        return actor

    def _load_persisted_policies(self, context: ScopeContext, actor_tail: str) -> tuple[Policy, ...]:
        items = self._read_bounded("POLICY", context, self._limits.max_policies)
        by_id: dict[str, Policy] = {}
        for item in items:
            data = _data(item)
            from pixs.core.persistence.models_authz import decode_policy as _decode
            try:
                policy = _decode(data.get("definition"))
            except PolicyError as error:
                raise CoreServiceError("POLITIQUE_CORROMPUE") from error
            if (policy.policy_id, policy.policy_version, policy.owner, policy.effect.value) != (data.get("policy_id"), data.get("policy_version"), data.get("owner"), data.get("effect")):
                raise CoreServiceError("POLITIQUE_CORROMPUE") from None
            if policy.policy_id in by_id:
                raise CoreServiceError("POLITIQUE_CORROMPUE") from None
            for value in policy.subject.values:
                if _is_raw_uuid7(value):
                    raise CoreServiceError("POLITIQUE_CORROMPUE") from None
                if value.startswith(USER_PREFIX) or value.startswith(GROUP_PREFIX):
                    continue
                _check_literal(value)
            for sel in (policy.resource, policy.action):
                for value in sel.values:
                    _check_literal(value)
            by_id[policy.policy_id] = policy
        return tuple(sorted(by_id.values(), key=lambda p: (p.policy_id, p.policy_version)))

    def _compile_role_policies(self, context: ScopeContext, actor_ref: str, actor: dict) -> tuple[Policy, ...]:
        used_roles = set(actor["direct_roles"]) | set(actor["user_roles"]) | set(actor["group_roles"])
        if not used_roles:
            return ()
        roles = self._read_bounded("ROLE", context, self._limits.max_selector_values)
        present = set()
        for item in roles:
            data = _data(item)
            if data["role_id"] in used_roles:
                actual = ScopeContext(ScopeType(data["scope_type"]), data["tenant_id"], data["scope_id"])
                if actual != context:
                    raise CoreServiceError("CONTEXTE_DIVERGENT") from None
                present.add(data["role_id"])
        if present != used_roles:
            raise CoreServiceError("ROLE_ABSENT") from None
        role_perms = self._read_bounded("ROLE_PERMISSION", context, self._limits.max_selector_values)
        perms = self._read_bounded("PERMISSION", context, self._limits.max_selector_values)
        perm_by_id = {_data(i)["permission_id"]: _data(i) for i in perms}
        out = []
        for item in role_perms:
            data = _data(item)
            rid, pid = data["role_id"], data["permission_id"]
            if rid not in used_roles:
                continue
            if pid not in perm_by_id:
                raise CoreServiceError("PERMISSION_ABSENTE") from None
            perm = perm_by_id[pid]
            for value in (rid, pid, perm["owner"], perm["resource_ref"], perm["action_ref"]):
                _check_literal(value)
            policy_id = hashlib.sha256(json.dumps(
                ["C04_ROLE", rid, pid, actor_ref, _context_key(context)],
                separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
            out.append(Policy(
                policy_id, str(item.version), perm["owner"], Effect.ALLOW,
                Selector("subject", (actor_ref,)),
                Selector("resource", (perm["resource_ref"],)),
                Selector("action", (perm["action_ref"],)), ScopeSelector((context,)),
                obligations=(Obligation("AUDIT"),),
            ))
        return tuple(sorted(out, key=lambda p: p.policy_id))

    def _expand_user_group_policies(self, persisted: tuple[Policy, ...], actor_ref: str, actor: dict) -> tuple[Policy, ...]:
        result = []
        for policy in persisted:
            matched = False
            for value in policy.subject.values:
                for prefix, accepted in (
                    (USER_PREFIX, () if actor["user_id"] is None else (actor["user_id"],)),
                    (GROUP_PREFIX, actor["groups"]),
                ):
                    if value.startswith(prefix):
                        tail = value[len(prefix):]
                        if not _is_raw_uuid7(tail):
                            raise CoreServiceError("POLITIQUE_CORROMPUE") from None
                        matched = matched or tail in accepted
            if matched and actor_ref not in policy.subject.values:
                # Même politique et mêmes conditions ; ajoute seulement la résolution propriétaire.
                policy = replace(policy, subject=Selector(
                    "subject", tuple(sorted(set(policy.subject.values) | {actor_ref}))))
            result.append(policy)
        return tuple(result)

    def _load_super_admin(self, context: ScopeContext, actor: dict) -> tuple[str, tuple[str, ...]]:
        bindings = self._read_refs("BINDING",
            (_make_ref("BINDING", (self._installation,)),), context, 1)
        matched = [_data(i) for i in bindings
                   if _data(i)["installation_ref"] == self._installation
                   and _data(i)["identity_id"] == actor["identity_id"]]
        if not matched or actor["identity_type"] == "SERVICE":
            return ROOT_ORDINARY, ()
        if len(matched) != 1:
            raise CoreServiceError("BINDING_AMBIGU") from None
        sources = (self._installation, actor["identity_id"])
        if context.scope_type is ScopeType.PLATFORM:
            return ROOT_PERMITTED, sources
        refs = (_make_ref("GRANT", (self._installation, context.tenant_id)),)
        grants = self._read_refs("GRANT", refs, context, 1)
        permitted = any(_data(i)["installation_ref"] == self._installation
                        and _data(i)["tenant_id"] == context.tenant_id for i in grants)
        return (ROOT_PERMITTED if permitted else ROOT_UNGRANTED), sources

    def _fingerprint(self, *, policies, actor, topology, state) -> str:
        doc = {
            "base_epoch": self._base_epoch, "installation": self._installation,
            "state": state, "actor": actor, "sources": self._material,
            "policies": [encode_policy(p) for p in policies],
            "topology": [topology.tenants, [(n.scope_id, n.tenant_id, n.parent_scope_id)
                                         for n in topology.scopes]],
            "catalog": [sorted(self._catalog.subject_ids), sorted(self._catalog.resource_ids),
                        sorted(self._catalog.action_ids),
                        sorted((_context_key(x) for x in self._catalog.scope_contexts),
                               key=lambda x: json.dumps(x)),
                        sorted(self._catalog.attribute_types)],
            "limits": {f.name: getattr(self._limits, f.name) for f in fields(Limits)},
        }
        return hashlib.sha256(json.dumps(
            doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def catalog(self) -> Catalog:
        return self._catalog

    @property
    def limits(self) -> Limits:
        return self._limits

    def pinned_snapshot(self, *, context: ScopeContext, actor_ref: str) -> tuple[Snapshot, TopologySnapshot, tuple[int, int, int, int], str, str]:
        """Retour immuable : snapshot, topologie, identité SQL, epoch, état Root.

        Cache pré-effet limité à la même transaction et pile native de savepoints.
        Tout autre contexte SQL oublie ce cache. Aucun token appelant ne le prouve.
        """
        with self._mutex:
            return self._pinned_snapshot(context=context, actor_ref=actor_ref)

    def _pinned_snapshot(self, *, context, actor_ref):
        _identity_tail(actor_ref)
        validate_structure(context)
        if actor_ref not in self._catalog.subject_ids or context not in self._catalog.scope_contexts:
            raise CoreServiceError("CONTEXTE_DIVERGENT") from None
        pin = transaction_identity(self._alias)
        savepoints = self._savepoint_key()
        transaction_key = (pin, savepoints)
        if self._cache_transaction != transaction_key:
            self._cache.clear()
            self._cache_transaction = transaction_key
        key = (actor_ref, _context_key(context))
        self.catalog_guard(exclusive=False)
        cached = self._cache.get(key)
        if cached is not None:
            snapshot, topology, epoch, state, scopes = cached
            lock_scopes(self._alias, scopes, shared=True)
            return snapshot, topology, pin, epoch, state
        if len(self._cache) >= self._limits.max_selector_values:
            raise CoreServiceError("BORNE_INVALIDE") from None
        self._material = []
        base = self.required_scopes(context=context, actor_ref=actor_ref)
        lock_scopes(self._alias, base, shared=True)
        # Borne le graphe avant le parcours propriétaire des ancêtres.
        topology = self._load_topology(context)
        _validate_context_under_locks(self._alias, context)
        actor = self._load_actor_stepwise(context, actor_ref)
        extra = set()
        if actor["user_id"] is not None:
            extra.add("uuid:" + _hex(actor["user_id"]))
        extra.update("uuid:" + _hex(group) for group in actor["groups"])
        full = tuple(sorted(set(base) | extra))
        lock_scopes(self._alias, full, shared=True)
        state = actor["root_state"]
        if state == ROOT_ORDINARY:
            persisted = self._load_persisted_policies(context, actor["identity_id"])
            policies = self._expand_user_group_policies(persisted, actor_ref, actor)
            policies += self._compile_role_policies(context, actor_ref, actor)
        else:
            # L'exception runtime ne dépend pas des ACL ni du profil PDP préparatoire.
            policies = ()
        policies = tuple(sorted(policies, key=lambda p: (p.policy_id, p.policy_version)))
        epoch = self._fingerprint(policies=policies, actor=actor, topology=topology, state=state)
        snapshot = build_snapshot(epoch, policies, self._catalog, self._limits)
        if transaction_identity(self._alias) != pin or self._savepoint_key() != savepoints:
            raise CoreServiceError("VERSION_DIVERGENTE") from None
        self._cache[key] = snapshot, topology, epoch, state, full
        return snapshot, topology, pin, epoch, state
