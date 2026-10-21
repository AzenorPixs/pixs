"""Autorisations Core : permissions, rôles, affectations, politiques, tombstones, sans moteur.

Niveaux : SQL = PK/UNIQUE/CHECK/FK PROTECT dernier ressort ; clean() = structure
sans IO (opaques, vocabulaires, JSON fermé, tombstone) ; gardes service (hors
modèle, sous verrou déterministe, ports propriétaires) = existence des
subject_ref opaques, cohérence même-tenant groupe/scope, collisions UUID
inter-tables refusées par validate_links (users/identités disjoints, unicité)
et validate_memberships (users/groupes disjoints, paires uniques) sous verrou
de namespace, révocations concurrentes, audit, publication C10. Aucun C04/C10
implémenté, aucune purge/restauration/transition inventée. NULL de gouvernance
= non classifié, aucune exposition. policy_version opaque distincte du CAS
entier `version` et du SemVer des contrats (D02). JSON interne seul via json +
constructeurs exacts, jamais eval ni pickle. deleted_at reste une chaîne UTC
canonique (source TombstoneProfile relue), jamais un datetime stocké.
Limite explicite : Policy(...) ne valide que la structure ; la validation
exhaustive catalogue/limites/coûts vit dans build_snapshot côté C04.
"""
from __future__ import annotations

import datetime
import json

from django.core.exceptions import ValidationError
from django.db import models

from pixs.core.authz.policy import (
    AuthenticationAssurance,
    Condition,
    Effect,
    FederationTrust,
    IdentityAssurance,
    Obligation,
    Policy,
    PolicyError,
    ScopeSelector,
    Selector,
)
from pixs.core.persistence.base import CoreBase
from pixs.core.scope.context import (
    ScopeContext,
    ScopeStructureError,
    ScopeType,
    validate_structure,
)
from pixs.kernel.data_tombstone_profile import (
    TombstoneProfile,
    validate_data_tombstone_profile,
)

FIXED_MESSAGE = "Autorisation Core invalide."

_POLICY_KEYS = frozenset(
    {
        "policy_id",
        "policy_version",
        "owner",
        "effect",
        "subject",
        "resource",
        "action",
        "scope",
        "conditions",
        "obligations",
        "valid_from",
        "valid_until",
        "min_identity_assurance",
        "min_authentication_assurance",
        "min_federation_trust",
        "max_auth_age_seconds",
    }
)
_SEL_KEYS = frozenset({"kind", "values"})
_SCOPE_KEYS = frozenset({"contexts"})
_CTX_KEYS = frozenset({"scope_type", "tenant_id", "scope_id"})
_COND_KEYS = frozenset({"attr", "op", "value"})
_OBL_KEYS = frozenset({"kind"})
_TOMB_KEYS = frozenset(
    {
        "resource_reference",
        "deletion_version",
        "deleted_at",
        "tenant_id",
        "scope_id",
        "retention_reference",
        "synchronization_reference",
        "deduplication_reference",
    }
)


def _is_opaque(value: object) -> bool:
    return type(value) is str and value != ""


def _scope_coherence_ok(scope_type: object, tenant_id: object, scope_id: object) -> bool:
    # Type exact avant toute égalité : aucun == sur objet non str.
    if type(scope_type) is not str:
        return False
    if scope_type == "PLATFORM":
        return tenant_id is None and scope_id is None
    if scope_type == "TENANT":
        if type(tenant_id) is not str or tenant_id == "":
            return False
        if scope_id is not None and (type(scope_id) is not str or scope_id == ""):
            return False
        return True
    return False


def _reject_constant(raw: str) -> None:
    raise ValueError("Constante JSON non admise.")


def _no_dup_dict(pairs: list[tuple[str, object]]) -> dict[str, object]:
    seen: set[str] = set()
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError("Clé JSON dupliquée.")
        seen.add(key)
        result[key] = value
    return result


def _loads_policy(payload: object) -> dict[str, object]:
    if type(payload) is not str or payload == "":
        raise PolicyError()
    try:
        doc = json.loads(
            payload,
            object_pairs_hook=_no_dup_dict,
            parse_constant=_reject_constant,
            parse_float=_reject_float,
            parse_int=_strict_int,
        )
    except (json.JSONDecodeError, ValueError, RecursionError):
        raise PolicyError() from None
    if type(doc) is not dict:
        raise PolicyError()
    return doc


def _reject_float(raw: str) -> None:
    raise ValueError("Flottant JSON non admis.")


def _strict_int(raw: str) -> int:
    return int(raw, 10)


def _loads_tombstone(payload: object) -> dict[str, object]:
    if type(payload) is not str or payload == "":
        raise ValidationError(FIXED_MESSAGE)
    try:
        doc = json.loads(
            payload,
            object_pairs_hook=_no_dup_dict,
            parse_constant=_reject_constant,
            parse_float=_reject_float,
            parse_int=_strict_int,
        )
    except (json.JSONDecodeError, ValueError, RecursionError):
        raise ValidationError(FIXED_MESSAGE) from None
    if type(doc) is not dict:
        raise ValidationError(FIXED_MESSAGE)
    return doc


def _parse_instant(raw: object) -> object:
    if raw is None:
        return None
    if type(raw) is not str or raw == "":
        raise PolicyError()
    try:
        parsed = datetime.datetime.fromisoformat(raw)
    except ValueError:
        raise PolicyError() from None
    if type(parsed) is not datetime.datetime:
        raise PolicyError()
    if parsed.tzinfo is not datetime.timezone.utc:
        raise PolicyError()
    return parsed


def _check_selector_block(doc: object, key: str, expected_kind: str) -> Selector:
    if type(doc) is not dict:
        raise PolicyError()
    block = doc[key]
    if type(block) is not dict:
        raise PolicyError()
    if set(block.keys()) != set(_SEL_KEYS):
        raise PolicyError()
    kind = block["kind"]
    values = block["values"]
    if type(kind) is not str or kind != expected_kind:
        raise PolicyError()
    # Type liste exigé : aucune coercition str -> tuple.
    if type(values) is not list or len(values) == 0:
        raise PolicyError()
    for item in values:
        if not _is_opaque(item):
            raise PolicyError()
    return Selector(kind, tuple(values))


def _check_scope_block(doc: object) -> ScopeSelector:
    if type(doc) is not dict:
        raise PolicyError()
    block = doc["scope"]
    if type(block) is not dict:
        raise PolicyError()
    if set(block.keys()) != set(_SCOPE_KEYS):
        raise PolicyError()
    contexts = block["contexts"]
    if type(contexts) is not list or len(contexts) == 0:
        raise PolicyError()
    built: list[ScopeContext] = []
    for entry in contexts:
        if type(entry) is not dict:
            raise PolicyError()
        if set(entry.keys()) != set(_CTX_KEYS):
            raise PolicyError()
        stype = entry["scope_type"]
        tenant = entry["tenant_id"]
        scp = entry["scope_id"]
        if type(stype) is not str or stype not in ("TENANT", "PLATFORM"):
            raise PolicyError()
        if tenant is not None and not _is_opaque(tenant):
            raise PolicyError()
        if scp is not None and not _is_opaque(scp):
            raise PolicyError()
        try:
            ctx = ScopeContext(ScopeType(stype), tenant, scp)
        except (ValueError, ScopeStructureError):
            raise PolicyError() from None
        try:
            validate_structure(ctx)
        except ScopeStructureError:
            raise PolicyError() from None
        built.append(ctx)
    return ScopeSelector(tuple(built))


def _check_value_eq(value: object) -> object:
    # v1 : str exact non vide ou int exact (bool refusé) ; flottants refusés.
    if type(value) is str:
        if value == "":
            raise PolicyError()
        return value
    if type(value) is int:
        return value
    raise PolicyError()


def _check_value_in(value: object) -> tuple[object, ...]:
    # Liste exigée, non vide, homogène str/int exacts ; pas de coercition.
    if type(value) is not list or len(value) == 0:
        raise PolicyError()
    kinds: set[str] = set()
    for item in value:
        if type(item) is str:
            if item == "":
                raise PolicyError()
            kinds.add("str")
        elif type(item) is int:
            kinds.add("int")
        else:
            raise PolicyError()
    if len(kinds) != 1:
        raise PolicyError()
    return tuple(value)


def _check_conditions(doc: object) -> tuple[Condition, ...]:
    if type(doc) is not dict:
        raise PolicyError()
    raw = doc["conditions"]
    if type(raw) is not list:
        raise PolicyError()
    built: list[Condition] = []
    for item in raw:
        if type(item) is not dict:
            raise PolicyError()
        if set(item.keys()) != set(_COND_KEYS):
            raise PolicyError()
        attr = item["attr"]
        op = item["op"]
        value = item["value"]
        if not _is_opaque(attr):
            raise PolicyError()
        if type(op) is not str or op not in ("eq", "in"):
            raise PolicyError()
        if op == "eq":
            built.append(Condition(attr, op, _check_value_eq(value)))
        else:
            built.append(Condition(attr, op, _check_value_in(value)))
    return tuple(built)


def _check_obligations(doc: object) -> tuple[Obligation, ...]:
    if type(doc) is not dict:
        raise PolicyError()
    raw = doc["obligations"]
    if type(raw) is not list:
        raise PolicyError()
    built: list[Obligation] = []
    for item in raw:
        if type(item) is not dict:
            raise PolicyError()
        if set(item.keys()) != set(_OBL_KEYS):
            raise PolicyError()
        kind = item["kind"]
        if type(kind) is not str or kind != "AUDIT":
            raise PolicyError()
        built.append(Obligation(kind))
    return tuple(built)


def _check_assurance(raw: object, enum_type: object) -> object:
    if raw is None:
        return None
    if type(raw) is not str or raw == "":
        raise PolicyError()
    try:
        return enum_type(raw)
    except ValueError:
        raise PolicyError() from None


def encode_policy(policy: Policy) -> str:
    """Sérialise un Policy exact vers JSON interne fermé, types vérifiés d'abord."""
    if type(policy) is not Policy:
        raise PolicyError()
    pid = object.__getattribute__(policy, "policy_id")
    pver = object.__getattribute__(policy, "policy_version")
    owner = object.__getattribute__(policy, "owner")
    effect = object.__getattribute__(policy, "effect")
    subject = object.__getattribute__(policy, "subject")
    resource = object.__getattribute__(policy, "resource")
    action = object.__getattribute__(policy, "action")
    scope = object.__getattribute__(policy, "scope")
    conditions = object.__getattribute__(policy, "conditions")
    obligations = object.__getattribute__(policy, "obligations")
    vfrom = object.__getattribute__(policy, "valid_from")
    vuntil = object.__getattribute__(policy, "valid_until")
    min_id = object.__getattribute__(policy, "min_identity_assurance")
    min_auth = object.__getattribute__(policy, "min_authentication_assurance")
    min_fed = object.__getattribute__(policy, "min_federation_trust")
    max_age = object.__getattribute__(policy, "max_auth_age_seconds")
    if not _is_opaque(pid) or not _is_opaque(pver) or not _is_opaque(owner):
        raise PolicyError()
    if type(effect) is not Effect:
        raise PolicyError()
    for sel, kind in ((subject, "subject"), (resource, "resource"), (action, "action")):
        if type(sel) is not Selector:
            raise PolicyError()
        skind = object.__getattribute__(sel, "kind")
        svals = object.__getattribute__(sel, "values")
        if type(skind) is not str or skind != kind:
            raise PolicyError()
        if type(svals) is not tuple or len(svals) == 0:
            raise PolicyError()
        for item in svals:
            if not _is_opaque(item):
                raise PolicyError()
    if type(scope) is not ScopeSelector:
        raise PolicyError()
    sctxs = object.__getattribute__(scope, "contexts")
    if type(sctxs) is not tuple or len(sctxs) == 0:
        raise PolicyError()
    for ctx in sctxs:
        if type(ctx) is not ScopeContext:
            raise PolicyError()
        try:
            validate_structure(ctx)
        except ScopeStructureError:
            raise PolicyError() from None
        tenant = object.__getattribute__(ctx, "tenant_id")
        scp = object.__getattribute__(ctx, "scope_id")
        if tenant is not None and not _is_opaque(tenant):
            raise PolicyError()
        if scp is not None and not _is_opaque(scp):
            raise PolicyError()
    if type(conditions) is not tuple or type(obligations) is not tuple:
        raise PolicyError()
    for cond in conditions:
        if type(cond) is not Condition:
            raise PolicyError()
        attr = object.__getattribute__(cond, "attr")
        op = object.__getattribute__(cond, "op")
        value = object.__getattribute__(cond, "value")
        if not _is_opaque(attr):
            raise PolicyError()
        if type(op) is not str or op not in ("eq", "in"):
            raise PolicyError()
        if op == "eq":
            _check_value_eq(value)
        else:
            if type(value) is not tuple:
                raise PolicyError()
            _check_value_in(list(value))
    for obl in obligations:
        if type(obl) is not Obligation:
            raise PolicyError()
        kind = object.__getattribute__(obl, "kind")
        if type(kind) is not str or kind != "AUDIT":
            raise PolicyError()
    for bound in (vfrom, vuntil):
        if bound is not None:
            if type(bound) is not datetime.datetime:
                raise PolicyError()
            if bound.tzinfo is not datetime.timezone.utc:
                raise PolicyError()
    if vfrom is not None and vuntil is not None and vfrom >= vuntil:
        raise PolicyError()
    if min_id is not None and type(min_id) is not IdentityAssurance:
        raise PolicyError()
    if min_auth is not None and type(min_auth) is not AuthenticationAssurance:
        raise PolicyError()
    if min_fed is not None and type(min_fed) is not FederationTrust:
        raise PolicyError()
    if max_age is not None and (type(max_age) is not int or max_age <= 0):
        raise PolicyError()
    # Construction vérifiée : itérations et méthodes seulement maintenant.
    doc = {
        "policy_id": pid,
        "policy_version": pver,
        "owner": owner,
        "effect": effect.value,
        "subject": {
            "kind": object.__getattribute__(subject, "kind"),
            "values": list(object.__getattribute__(subject, "values")),
        },
        "resource": {
            "kind": object.__getattribute__(resource, "kind"),
            "values": list(object.__getattribute__(resource, "values")),
        },
        "action": {
            "kind": object.__getattribute__(action, "kind"),
            "values": list(object.__getattribute__(action, "values")),
        },
        "scope": {
            "contexts": [
                {
                    "scope_type": object.__getattribute__(
                        object.__getattribute__(c, "scope_type"), "value"
                    ),
                    "tenant_id": object.__getattribute__(c, "tenant_id"),
                    "scope_id": object.__getattribute__(c, "scope_id"),
                }
                for c in sctxs
            ]
        },
        "conditions": [
            {
                "attr": object.__getattribute__(c, "attr"),
                "op": object.__getattribute__(c, "op"),
                "value": list(object.__getattribute__(c, "value"))
                if object.__getattribute__(c, "op") == "in"
                else object.__getattribute__(c, "value"),
            }
            for c in conditions
        ],
        "obligations": [
            {"kind": object.__getattribute__(o, "kind")} for o in obligations
        ],
        "valid_from": vfrom.isoformat() if vfrom is not None else None,
        "valid_until": vuntil.isoformat() if vuntil is not None else None,
        "min_identity_assurance": min_id.value if min_id is not None else None,
        "min_authentication_assurance": min_auth.value if min_auth is not None else None,
        "min_federation_trust": min_fed.value if min_fed is not None else None,
        "max_auth_age_seconds": max_age,
    }
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def decode_policy(payload: object) -> Policy:
    """Reconstruit un Policy exact depuis JSON interne fermé ; refuse tout le reste.

    Limite : la construction valide la structure ; l'appartenance au catalogue,
    les tailles, les coûts et la normalisation exhaustive restent du ressort de
    build_snapshot côté C04.
    """
    doc = _loads_policy(payload)
    if set(doc.keys()) != set(_POLICY_KEYS):
        raise PolicyError()
    pid = doc["policy_id"]
    pver = doc["policy_version"]
    owner = doc["owner"]
    raw_effect = doc["effect"]
    if not _is_opaque(pid) or not _is_opaque(pver) or not _is_opaque(owner):
        raise PolicyError()
    if type(raw_effect) is not str or raw_effect not in ("ALLOW", "DENY"):
        raise PolicyError()
    try:
        effect = Effect(raw_effect)
    except ValueError:
        raise PolicyError() from None
    subject = _check_selector_block(doc, "subject", "subject")
    resource = _check_selector_block(doc, "resource", "resource")
    action = _check_selector_block(doc, "action", "action")
    scope = _check_scope_block(doc)
    conditions = _check_conditions(doc)
    obligations = _check_obligations(doc)
    vfrom = _parse_instant(doc["valid_from"])
    vuntil = _parse_instant(doc["valid_until"])
    min_id = _check_assurance(doc["min_identity_assurance"], IdentityAssurance)
    min_auth = _check_assurance(doc["min_authentication_assurance"], AuthenticationAssurance)
    min_fed = _check_assurance(doc["min_federation_trust"], FederationTrust)
    max_age = doc["max_auth_age_seconds"]
    if max_age is not None and (type(max_age) is not int or max_age <= 0):
        raise PolicyError()
    try:
        return Policy(
            pid, pver, owner, effect, subject, resource, action, scope,
            conditions, obligations, vfrom, vuntil, min_id, min_auth, min_fed, max_age,
        )
    except PolicyError:
        raise
    except (TypeError, ValueError):
        raise PolicyError() from None


def encode_tombstone(profile: TombstoneProfile) -> str:
    """Sérialise un TombstoneProfile exact, validé d'abord, vers JSON fermé."""
    if type(profile) is not TombstoneProfile:
        raise ValidationError(FIXED_MESSAGE)
    if validate_data_tombstone_profile(profile):
        raise ValidationError(FIXED_MESSAGE)
    doc = {
        "resource_reference": profile.resource_reference,
        "deletion_version": profile.deletion_version,
        "deleted_at": profile.deleted_at,
        "tenant_id": profile.tenant_id,
        "scope_id": profile.scope_id,
        "retention_reference": profile.retention_reference,
        "synchronization_reference": profile.synchronization_reference,
        "deduplication_reference": profile.deduplication_reference,
    }
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def decode_tombstone(payload: object) -> TombstoneProfile:
    """Reconstruit un TombstoneProfile exact ; huit clés exigées, sans .get implicite."""
    doc = _loads_tombstone(payload)
    if set(doc.keys()) != set(_TOMB_KEYS):
        raise ValidationError(FIXED_MESSAGE)
    resource = doc["resource_reference"]
    version = doc["deletion_version"]
    instant = doc["deleted_at"]
    tenant = doc["tenant_id"]
    scp = doc["scope_id"]
    retention = doc["retention_reference"]
    sync = doc["synchronization_reference"]
    dedup = doc["deduplication_reference"]
    if not _is_opaque(resource):
        raise ValidationError(FIXED_MESSAGE)
    if type(version) is not int or version < 0:
        raise ValidationError(FIXED_MESSAGE)
    if not _is_opaque(instant):
        raise ValidationError(FIXED_MESSAGE)
    for opt in (tenant, scp, retention, sync, dedup):
        if opt is not None and not _is_opaque(opt):
            raise ValidationError(FIXED_MESSAGE)
    try:
        candidate = TombstoneProfile(
            resource, version, instant, tenant, scp, retention, sync, dedup
        )
    except TypeError:
        raise ValidationError(FIXED_MESSAGE) from None
    if validate_data_tombstone_profile(candidate):
        raise ValidationError(FIXED_MESSAGE)
    return candidate


class CorePermission(CoreBase):
    permission_id = models.TextField(primary_key=True)
    owner = models.TextField()
    resource_ref = models.TextField()
    action_ref = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_perm"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=~models.Q(permission_id=""), name="perm_nonempty"),
            models.CheckConstraint(condition=~models.Q(owner=""), name="perm_owner_nonempty"),
            models.CheckConstraint(condition=~models.Q(resource_ref=""), name="perm_res_nonempty"),
            models.CheckConstraint(condition=~models.Q(action_ref=""), name="perm_act_nonempty"),
        ]

    def clean(self) -> None:
        # Déclaration et persistance ne valent pas octroi ; C04 évalue.
        for field in ("permission_id", "owner", "resource_ref", "action_ref"):
            if not _is_opaque(getattr(self, field)):
                raise ValidationError(FIXED_MESSAGE)


class CoreRole(CoreBase):
    role_id = models.TextField(primary_key=True)
    scope_type = models.TextField()
    tenant = models.ForeignKey(
        "pixs_core.CoreTenant", on_delete=models.PROTECT, null=True, blank=True,
        default=None, related_name="+", db_column="tenant_id",
    )
    scope = models.ForeignKey(
        "pixs_core.CoreScope", on_delete=models.PROTECT, null=True, blank=True,
        default=None, related_name="+", db_column="scope_id",
    )

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_role"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=~models.Q(role_id=""), name="role_nonempty"),
            models.CheckConstraint(
                condition=models.Q(scope_type__in=["TENANT", "PLATFORM"]), name="role_scope_vocab"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(scope_type="TENANT", tenant__isnull=False)
                    | models.Q(scope_type="PLATFORM", tenant__isnull=True, scope__isnull=True)
                ),
                name="role_tenant_coherence",
            ),
        ]
        indexes = [models.Index(fields=["tenant"], name="role_tenant_ix")]

    def clean(self) -> None:
        # Aucun rôle administrateur implicite ; même-tenant rôle/scope = garde service.
        if not _is_opaque(self.role_id):
            raise ValidationError(FIXED_MESSAGE)
        if type(self.scope_type) is not str or self.scope_type not in ("TENANT", "PLATFORM"):
            raise ValidationError(FIXED_MESSAGE)
        if not _scope_coherence_ok(self.scope_type, self.tenant_id, self.scope_id):
            raise ValidationError(FIXED_MESSAGE)


class CoreRolePermission(CoreBase):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey("pixs_core.CoreRole", on_delete=models.PROTECT, related_name="+")
    permission = models.ForeignKey("pixs_core.CorePermission", on_delete=models.PROTECT, related_name="+")

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_roleperm"
        constraints = [
            *CoreBase.Meta.constraints,
            models.UniqueConstraint(fields=["role", "permission"], name="roleperm_role_perm_uq", condition=models.Q(persistence_state="ACTIVE")),
        ]


class CoreRoleAssignment(CoreBase):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey("pixs_core.CoreRole", on_delete=models.PROTECT, related_name="+")
    subject_type = models.TextField()
    subject_ref = models.TextField()
    scope_type = models.TextField()
    tenant = models.ForeignKey(
        "pixs_core.CoreTenant", on_delete=models.PROTECT, null=True, blank=True,
        default=None, related_name="+", db_column="tenant_id",
    )
    scope = models.ForeignKey(
        "pixs_core.CoreScope", on_delete=models.PROTECT, null=True, blank=True,
        default=None, related_name="+", db_column="scope_id",
    )

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_roleassign"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(subject_type__in=["USER", "IDENTITY", "GROUP"]),
                name="roleassign_subj_vocab",
            ),
            models.CheckConstraint(condition=~models.Q(subject_ref=""), name="roleassign_ref_nonempty"),
            models.CheckConstraint(
                condition=models.Q(scope_type__in=["TENANT", "PLATFORM"]), name="roleassign_scope_vocab"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(scope_type="TENANT", tenant__isnull=False)
                    | models.Q(scope_type="PLATFORM", tenant__isnull=True, scope__isnull=True)
                ),
                name="roleassign_tenant_coherence",
            ),
            # PG16 : NULLS NOT DISTINCT, les doublons à tenant/scope NULL sont
            # refusés par la contrainte elle-même, pas par le seul clean/service.
            # SQLite d'autodétection ne prouve pas cette sémantique (PG réel seul).
            models.UniqueConstraint(
                fields=["role", "subject_type", "subject_ref", "scope_type", "tenant", "scope"],
                name="roleassign_uq",
                nulls_distinct=False, condition=models.Q(persistence_state="ACTIVE")),
        ]
        indexes = [models.Index(fields=["tenant"], name="roleassign_tenant_ix")]

    def clean(self) -> None:
        # subject_ref opaque sans FK : existence vérifiée via port propriétaire.
        if type(self.subject_type) is not str or self.subject_type not in ("USER", "IDENTITY", "GROUP"):
            raise ValidationError(FIXED_MESSAGE)
        if not _is_opaque(self.subject_ref):
            raise ValidationError(FIXED_MESSAGE)
        if type(self.scope_type) is not str or self.scope_type not in ("TENANT", "PLATFORM"):
            raise ValidationError(FIXED_MESSAGE)
        if not _scope_coherence_ok(self.scope_type, self.tenant_id, self.scope_id):
            raise ValidationError(FIXED_MESSAGE)


class CorePolicy(CoreBase):
    id = models.BigAutoField(primary_key=True)
    policy_id = models.TextField()
    policy_version = models.TextField()
    owner = models.TextField()
    effect = models.TextField()
    definition = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_policy"
        constraints = [
            *CoreBase.Meta.constraints,
            models.UniqueConstraint(fields=["policy_id", "policy_version"], name="policy_id_ver_uq"),
            models.CheckConstraint(condition=~models.Q(policy_id=""), name="policy_id_nonempty"),
            models.CheckConstraint(condition=~models.Q(policy_version=""), name="policy_ver_nonempty"),
            models.CheckConstraint(condition=~models.Q(owner=""), name="policy_owner_nonempty"),
            models.CheckConstraint(condition=~models.Q(definition=""), name="policy_def_nonempty"),
            models.CheckConstraint(condition=models.Q(effect__in=["ALLOW", "DENY"]), name="policy_effect_vocab"),
        ]

    def clean(self) -> None:
        # policy_version opaque distincte du CAS `version` et du SemVer contrat.
        # Stockage seul : catalogue/limites exhaustifs dans build_snapshot (C04).
        for field in ("policy_id", "policy_version", "owner", "definition"):
            if not _is_opaque(getattr(self, field)):
                raise ValidationError(FIXED_MESSAGE)
        if type(self.effect) is not str or self.effect not in ("ALLOW", "DENY"):
            raise ValidationError(FIXED_MESSAGE)
        try:
            policy = decode_policy(self.definition)
        except PolicyError:
            raise ValidationError(FIXED_MESSAGE) from None
        if object.__getattribute__(policy, "policy_id") != self.policy_id:
            raise ValidationError(FIXED_MESSAGE)
        if object.__getattribute__(policy, "policy_version") != self.policy_version:
            raise ValidationError(FIXED_MESSAGE)
        if object.__getattribute__(policy, "owner") != self.owner:
            raise ValidationError(FIXED_MESSAGE)
        if object.__getattribute__(policy, "effect").value != self.effect:
            raise ValidationError(FIXED_MESSAGE)


class CoreTombstoneRef(CoreBase):
    id = models.BigAutoField(primary_key=True)
    resource_reference = models.TextField()
    deletion_version = models.IntegerField()
    deleted_at = models.TextField()
    tenant_ref = models.TextField(null=True, blank=True, default=None)
    scope_ref = models.TextField(null=True, blank=True, default=None)
    retention_reference = models.TextField(null=True, blank=True, default=None)
    synchronization_reference = models.TextField(null=True, blank=True, default=None)
    deduplication_reference = models.TextField(null=True, blank=True, default=None)

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_tombstone"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=~models.Q(resource_reference=""), name="tomb_res_nonempty"),
            models.CheckConstraint(condition=models.Q(deletion_version__gte=0), name="tomb_ver_gte0"),
            models.UniqueConstraint(
                fields=["resource_reference", "deletion_version"], name="tomb_res_ver_uq"
            ),
        ]

    def clean(self) -> None:
        # Conservation seule via les 8 champs exacts ; scope sans tenant refusé
        # par validate_data_tombstone_profile. Aucune purge/restauration.
        if type(self.deletion_version) is not int:
            raise ValidationError(FIXED_MESSAGE)
        try:
            candidate = TombstoneProfile(
                self.resource_reference,
                self.deletion_version,
                self.deleted_at,
                self.tenant_ref,
                self.scope_ref,
                self.retention_reference,
                self.synchronization_reference,
                self.deduplication_reference,
            )
        except TypeError:
            raise ValidationError(FIXED_MESSAGE) from None
        if validate_data_tombstone_profile(candidate):
            raise ValidationError(FIXED_MESSAGE)
