"""Query refs Core : mapping ferme, sans exposition C04."""
from __future__ import annotations
import json as _j
import urllib.parse as _up
import uuid as _uu
from pixs.core.persistence.models_authz import CorePermission as _Pm, CorePolicy as _Po, CoreRole as _Ro, CoreRoleAssignment as _Ra, CoreRolePermission as _Rp, CoreTombstoneRef as _Tb
from pixs.core.persistence.models_group import CoreGroup as _Gr, CoreIdentityTenantMembership as _Tm, CoreUserGroupMembership as _Ug
from pixs.core.persistence.models_identity import CoreIdentity as _Id, CoreIdentityLink as _Lk, CoreSuperAdminBinding as _Bd, CoreSuperAdminTenantGrant as _Gt, CoreUser as _Us
from pixs.core.persistence.models_scope import CoreScope as _Sc, CoreTenant as _Tn
from pixs.core.persistence.uuid7 import Uuid7Error as _UE, check_uuid7 as _chk
from pixs.core.scope.context import ScopeContext as _Cx, ScopeStructureError, validate_structure
from pixs.core.services_common import CoreServiceError as _SE
__all__ = ["collection_ref"]
def _uuid(s: str) -> str:
    if type(s) is not str:
        raise _SE("REFERENCE_INVALIDE") from None
    try:
        v = _uu.UUID(s)
    except ValueError as e:
        raise _SE("REFERENCE_INVALIDE") from e
    if str(v) != s:
        raise _SE("REFERENCE_INVALIDE") from None
    try:
        _chk(v)
    except _UE as e:
        raise _SE("REFERENCE_INVALIDE") from e
    return s
def _opaque(s: str) -> str:
    if type(s) is not str or s == "":
        raise _SE("REFERENCE_INVALIDE") from None
    return s
def _unq(s: str) -> str:
    try:
        v = _up.unquote(s, encoding="utf-8", errors="strict")
    except UnicodeError as e:
        raise _SE("REFERENCE_INVALIDE") from e
    if _up.quote(v, safe="") != s:
        raise _SE("REFERENCE_INVALIDE") from None
    return _opaque(v)
_KINDS = {
    "USER": (_Us, "pixs.core.user:", ("user_id",), ("user_id",), (), "request"),
    "IDENTITY": (_Id, "pixs.core.identity:", ("identity_id",), ("identity_id", "identity_type", "state"), (), "request"),
    "LINK": (_Lk, "pixs.core.identity-link:", ("user_id", "identity_id"), ("user_id", "identity_id"), ("user", "identity"), "request"),
    "GROUP": (_Gr, "pixs.core.group:", ("group_id",), ("group_id", "scope_type", "tenant_id", "scope_id"), ("tenant", "scope"), "row"),
    "USER_GROUP": (_Ug, "pixs.core.user-group:", ("user_id", "group_id"), ("user_id", "group_id"), ("user", "group"), "request"),
    "TENANT_MEMBERSHIP": (_Tm, "pixs.core.identity-tenant:", ("identity_id", "tenant_id"), ("identity_id", "tenant_id", "activation"), ("identity", "tenant"), "request"),
    "TENANT": (_Tn, "pixs.core.tenant:", ("tenant_id",), ("tenant_id",), (), "platform"),
    "SCOPE": (_Sc, "pixs.core.scope:", ("scope_id",), ("scope_id", "tenant_id", "parent_scope_id"), ("tenant",), "row"),
    "PERMISSION": (_Pm, "pixs.core.permission:", ("permission_id",), ("permission_id", "owner", "resource_ref", "action_ref"), (), "request"),
    "ROLE": (_Ro, "pixs.core.role:", ("role_id",), ("role_id", "scope_type", "tenant_id", "scope_id"), ("tenant", "scope"), "row"),
    "ROLE_PERMISSION": (_Rp, "pixs.core.role-permission:", ("role_id", "permission_id"), ("role_id", "permission_id"), ("role", "permission"), "request"),
    "ROLE_ASSIGNMENT": (_Ra, "pixs.core.role-assignment:", ("role_id", "subject_type", "subject_ref"), ("role_id", "subject_type", "subject_ref", "scope_type", "tenant_id", "scope_id"), ("role",), "row"),
    "POLICY": (_Po, "pixs.core.policy:", ("policy_id", "policy_version"), ("policy_id", "policy_version", "owner", "effect", "definition"), (), "request"),
    "TOMBSTONE": (_Tb, "pixs.core.tombstone:", ("resource_reference", "deletion_version"), ("resource_reference", "deletion_version", "deleted_at", "tenant_ref", "scope_ref", "retention_reference", "synchronization_reference", "deduplication_reference"), (), "request"),
    "BINDING": (_Bd, "pixs.core.binding:", ("installation_ref",), ("installation_ref", "identity_id"), ("identity",), "request"),
    "GRANT": (_Gt, "pixs.core.super-admin-grant:", ("binding_id", "tenant_id"), ("installation_ref", "tenant_id"), ("binding", "tenant"), "request"),
}
def _parse_ref(kind: str, ref: str) -> tuple:
    if type(kind) is not str or kind not in _KINDS or type(ref) is not str:
        raise _SE("REFERENCE_INVALIDE") from None
    prefix = _KINDS[kind][1]
    if not ref.startswith(prefix):
        raise _SE("REFERENCE_INVALIDE") from None
    tail = ref[len(prefix):]
    if kind in ("USER", "IDENTITY", "GROUP"):
        return (_uuid(tail),)
    if kind == "LINK":
        if tail.count("/") != 1:
            raise _SE("REFERENCE_INVALIDE") from None
        a, b = tail.split("/", 1)
        return (_uuid(a), _uuid(b))
    if kind == "USER_GROUP":
        if tail.count("/") != 1:
            raise _SE("REFERENCE_INVALIDE") from None
        a, b = tail.split("/", 1)
        return (_uuid(a), _uuid(b))
    if kind == "TENANT_MEMBERSHIP":
        if "/" not in tail:
            raise _SE("REFERENCE_INVALIDE") from None
        a, b = tail.split("/", 1)
        return (_uuid(a), _opaque(b))
    if kind in ("TENANT", "SCOPE", "PERMISSION", "ROLE", "BINDING"):
        return (_opaque(tail),)
    if kind == "ROLE_PERMISSION":
        if tail.count("/") != 1:
            raise _SE("REFERENCE_INVALIDE") from None
        a, b = tail.split("/", 1)
        return (_unq(a), _unq(b))
    if kind == "ROLE_ASSIGNMENT":
        if tail.count("/") != 2:
            raise _SE("REFERENCE_INVALIDE") from None
        a, st, su = tail.split("/", 2)
        r = _unq(a)
        if st not in ("USER", "IDENTITY", "GROUP"):
            raise _SE("REFERENCE_INVALIDE") from None
        return (r, st, _uuid(su))
    if kind == "POLICY":
        if tail.count("/") != 1:
            raise _SE("REFERENCE_INVALIDE") from None
        a, b = tail.split("/", 1)
        return (_unq(a), _unq(b))
    if kind == "TOMBSTONE":
        if tail.count("/") != 1:
            raise _SE("REFERENCE_INVALIDE") from None
        a, b = tail.split("/", 1)
        r = _unq(a)
        if not b.isdigit() or str(int(b, 10)) != b:
            raise _SE("REFERENCE_INVALIDE") from None
        return (r, int(b, 10))
    if kind == "GRANT":
        if tail.count("/") != 1:
            raise _SE("REFERENCE_INVALIDE") from None
        a, b = tail.split("/", 1)
        return (_unq(a), _unq(b))
    raise _SE("REFERENCE_INVALIDE") from None
def _make_ref(kind: str, values: tuple) -> str:
    if type(kind) is not str or kind not in _KINDS or type(values) is not tuple:
        raise _SE("REFERENCE_INVALIDE") from None
    prefix = _KINDS[kind][1]
    if kind in ("USER", "IDENTITY", "GROUP", "TENANT", "SCOPE", "PERMISSION", "ROLE", "BINDING"):
        if len(values) != 1:
            raise _SE("REFERENCE_INVALIDE") from None
        v = values[0]
        if kind in ("USER", "IDENTITY", "GROUP"):
            _uuid(v)
            return prefix + v
        return prefix + _opaque(v)
    if kind in ("LINK", "USER_GROUP"):
        if len(values) != 2:
            raise _SE("REFERENCE_INVALIDE") from None
        return prefix + _uuid(values[0]) + "/" + _uuid(values[1])
    if kind == "TENANT_MEMBERSHIP":
        if len(values) != 2:
            raise _SE("REFERENCE_INVALIDE") from None
        return prefix + _uuid(values[0]) + "/" + _opaque(values[1])
    if kind in ("ROLE_PERMISSION", "POLICY", "GRANT"):
        if len(values) != 2:
            raise _SE("REFERENCE_INVALIDE") from None
        return prefix + _up.quote(_opaque(values[0]), safe="") + "/" + _up.quote(_opaque(values[1]), safe="")
    if kind == "ROLE_ASSIGNMENT":
        if len(values) != 3 or type(values[1]) is not str or values[1] not in ("USER", "IDENTITY", "GROUP"):
            raise _SE("REFERENCE_INVALIDE") from None
        return prefix + _up.quote(_opaque(values[0]), safe="") + "/" + values[1] + "/" + _uuid(values[2])
    if kind == "TOMBSTONE":
        if len(values) != 2 or type(values[1]) is not int or values[1] < 0:
            raise _SE("REFERENCE_INVALIDE") from None
        return prefix + _up.quote(_opaque(values[0]), safe="") + "/" + str(values[1])
    raise _SE("REFERENCE_INVALIDE") from None
def collection_ref(kind: str, context: _Cx) -> str:
    if type(kind) is not str or kind not in _KINDS or type(context) is not _Cx:
        raise _SE("COLLECTION_INVALIDE") from None
    try:
        validate_structure(context)
    except ScopeStructureError as error:
        raise _SE("CONTEXTE_INVALIDE") from error
    st = object.__getattribute__(context, "scope_type").value
    payload = _j.dumps([kind, st, object.__getattribute__(context, "tenant_id"), object.__getattribute__(context, "scope_id")], separators=(",", ":"), ensure_ascii=False)
    return "pixs.core.query-collection:" + kind + ":" + _up.quote(payload, safe="")

from django.core.exceptions import ValidationError
from django.db import connections as _conns, transaction as _tx
from django.db.models import Q as _Q, TextField
from django.db.models.functions import Cast
from django.utils.connection import ConnectionDoesNotExist
from pixs.core.authz.policy import PolicyError
from pixs.core.dto import CorePageItem as _Item
from pixs.core.persistence.models_authz import decode_policy
from pixs.core.scope.context import ScopeType as _T
from pixs.core.services_common import lock_scopes as _locks
from pixs.core.services_scope import _validate_context_under_locks as _vctx
__all__ += ["selected_rows", "CoreFactSource"]

def _source_inputs(kind, context, alias, limit):
    if type(kind) is not str or kind not in _KINDS:
        raise _SE("GENRE_INVALIDE") from None
    if type(context) is not _Cx:
        raise _SE("CONTEXTE_INVALIDE") from None
    try:
        validate_structure(context)
    except ScopeStructureError as error:
        raise _SE("CONTEXTE_INVALIDE") from error
    if type(alias) is not str or not alias or type(limit) is not int or limit < 1:
        raise _SE("ENTREES_INVALIDES") from None
    try:
        conn = _conns[alias]
    except ConnectionDoesNotExist as error:
        raise _SE("ALIAS_INCONNU") from error
    if conn.vendor != "postgresql":
        raise _SE("MOTEUR_NON_PG_REFUSE") from None
    return conn

def _base_queryset(kind, context, alias):
    qs = _KINDS[kind][0].objects.using(alias).filter(persistence_state="ACTIVE")
    required = {
        "LINK": ("user", "identity"), "USER_GROUP": ("user", "group"),
        "TENANT_MEMBERSHIP": ("identity", "tenant"), "SCOPE": ("tenant",),
        "ROLE_PERMISSION": ("role", "permission"), "ROLE_ASSIGNMENT": ("role",),
        "BINDING": ("identity",), "GRANT": ("binding", "binding__identity", "tenant"),
    }
    for path in required.get(kind, ()):
        qs = qs.filter(**{path + "__persistence_state": "ACTIVE"})
    nullable = {
        "GROUP": ("tenant", "scope"), "ROLE": ("tenant", "scope"),
        "USER_GROUP": ("group__tenant", "group__scope"),
        "ROLE_PERMISSION": ("role__tenant", "role__scope"),
        "ROLE_ASSIGNMENT": ("tenant", "scope", "role__tenant", "role__scope"),
    }
    for path in nullable.get(kind, ()):
        qs = qs.filter(_Q(**{path + "__isnull": True}) | _Q(**{path + "__persistence_state": "ACTIVE"}))
    if kind == "SCOPE":
        qs = qs.filter(_Q(parent__isnull=True) | _Q(parent__persistence_state="ACTIVE"))
    if kind == "TENANT_MEMBERSHIP":
        qs = qs.filter(activation="ACTIVE")
    if kind == "BINDING":
        qs = qs.exclude(identity__identity_type="SERVICE")
    if kind == "GRANT":
        qs = qs.exclude(binding__identity__identity_type="SERVICE")
    paths = {"GROUP": "", "ROLE": "", "ROLE_ASSIGNMENT": "", "USER_GROUP": "group__", "ROLE_PERMISSION": "role__"}
    if kind in paths:
        prefix = paths[kind]
        qs = qs.filter(**{prefix + "scope_type": context.scope_type.value, prefix + "tenant_id": context.tenant_id, prefix + "scope_id": context.scope_id})
    if kind in ("TENANT", "SCOPE", "TENANT_MEMBERSHIP", "GRANT") and context.scope_type is _T.TENANT:
        qs = qs.filter(tenant_id=context.tenant_id)
        if kind == "SCOPE" and context.scope_id is not None:
            qs = qs.filter(scope_id=context.scope_id)
    if kind == "TOMBSTONE" and context.scope_type is _T.TENANT:
        qs = qs.filter(tenant_ref=context.tenant_id, scope_ref=context.scope_id)
    if kind == "ROLE_ASSIGNMENT":
        subjects = _Q(pk__in=[])
        for name, model, pk in (("USER", _Us, "user_id"), ("IDENTITY", _Id, "identity_id"), ("GROUP", _Gr, "group_id")):
            active = model.objects.using(alias).filter(persistence_state="ACTIVE").annotate(canonical_ref=Cast(pk, output_field=TextField())).values("canonical_ref")
            subjects |= _Q(subject_type=name, subject_ref__in=active)
        qs = qs.filter(subjects)
    return qs

def _row_data(kind, row):
    aliases = {"parent_scope_id": "parent_id"}
    if kind == "GRANT":
        aliases["installation_ref"] = "binding_id"
    result = []
    for field in _KINDS[kind][3]:
        value = getattr(row, aliases.get(field, field))
        if type(value) is _uu.UUID:
            value = str(value)
        result.append((field, value))
    return tuple(result)

def _row_context(kind, row, fallback):
    if kind in ("GROUP", "ROLE", "ROLE_ASSIGNMENT"):
        return _Cx(_T(row.scope_type), row.tenant_id, row.scope_id)
    if kind == "USER_GROUP":
        owner = row.group
        return _Cx(_T(owner.scope_type), owner.tenant_id, owner.scope_id)
    if kind == "ROLE_PERMISSION":
        owner = row.role
        return _Cx(_T(owner.scope_type), owner.tenant_id, owner.scope_id)
    if kind in ("TENANT", "TENANT_MEMBERSHIP", "GRANT"):
        return _Cx(_T.TENANT, row.tenant_id, None)
    if kind == "SCOPE":
        return _Cx(_T.TENANT, row.tenant_id, row.scope_id)
    if kind == "TOMBSTONE" and row.tenant_ref is not None:
        return _Cx(_T.TENANT, row.tenant_ref, row.scope_ref)
    return fallback

def selected_rows(kind, refs, context, alias, *, governance_waived, limit, after=None, page_limit=None):
    """Adapter interne : seules les références du plan source C04 sont matérialisées."""
    conn = _source_inputs(kind, context, alias, limit)
    if type(refs) is not tuple or any(type(r) is not str or not r for r in refs):
        raise _SE("REFERENCES_INVALIDES") from None
    if len(set(refs)) != len(refs) or len(refs) > limit or type(governance_waived) is not bool:
        raise _SE("BORNE_INVALIDE") from None
    if page_limit is not None and (type(page_limit) is not int or not 1 <= page_limit <= limit):
        raise _SE("BORNE_INVALIDE") from None
    if after is not None and (type(after) is not str or not after or page_limit is None):
        raise _SE("BORNE_INVALIDE") from None
    after_keys = None if after is None else _parse_ref(kind, after)
    if not conn.in_atomic_block:
        raise _SE("HORS_TRANSACTION") from None
    if not refs:
        return ()
    if context.scope_type is _T.TENANT:
        _locks(alias, ("tenant:" + context.tenant_id,))
    _vctx(alias, context)
    key_fields = _KINDS[kind][2]
    where = _Q(pk__in=[])
    for ref in refs:
        keys = _parse_ref(kind, ref)
        where |= _Q(**dict(zip(key_fields, keys)))
    qs = _base_queryset(kind, context, alias).filter(where)
    if governance_waived is not True:
        qs = qs.filter(governance_ref__isnull=False, confidentiality__isnull=False, personal__isnull=False)
    if after_keys is not None:
        lexicographic = _Q(pk__in=[])
        for position, field in enumerate(key_fields):
            branch = {key_fields[earlier]: after_keys[earlier] for earlier in range(position)}
            branch[field + "__gt"] = after_keys[position]
            lexicographic |= _Q(**branch)
        qs = qs.filter(lexicographic)
    bound = limit if page_limit is None else page_limit
    rows = list(qs.order_by(*key_fields)[:bound + 1])
    if len(rows) > limit:
        raise _SE("DEPASSEMENT_LOT") from None
    contexts = [_row_context(kind, row, context) for row in rows]
    tenants = tuple(sorted({"tenant:" + c.tenant_id for c in contexts if c.scope_type is _T.TENANT}))
    if tenants:
        _locks(alias, tenants)
    for current in contexts:
        _vctx(alias, current)
    by_ref = {}
    for row, current in zip(rows, contexts):
        if kind == "POLICY":
            try:
                policy = decode_policy(row.definition)
            except PolicyError as error:
                raise _SE("POLITIQUE_CORROMPUE") from error
            if (policy.policy_id, policy.policy_version, policy.owner, policy.effect.value) != (row.policy_id, row.policy_version, row.owner, row.effect):
                raise _SE("POLITIQUE_CORROMPUE") from None
        if kind == "TOMBSTONE":
            try:
                row.full_clean(validate_unique=False, validate_constraints=False)
            except ValidationError as error:
                raise _SE("TOMBSTONE_CORROMPU") from error
        values = tuple(str(getattr(row, f)) if type(getattr(row, f)) is _uu.UUID else getattr(row, f) for f in key_fields)
        ref = _make_ref(kind, values)
        if ref in by_ref:
            raise _SE("REFERENCE_AMBIGUE") from None
        by_ref[ref] = _Item(kind, ref, current, row.version, row.persistence_state, row.retention_state, row.governance_ref, row.confidentiality, row.personal, _row_data(kind, row))
    if page_limit is not None:
        return tuple(by_ref.values())
    return tuple(by_ref[ref] for ref in refs if ref in by_ref)

class CoreFactSource:
    """Capacité de composition C03/C04/C08, réservée aux validations internes.

    Ne jamais publier cet objet via une QUERY, une façade ou un paramètre client.
    La tolérance NULL de gouvernance ne vaut aucune permission d'exposition.
    """
    def read_facts(self, kind, refs, context, alias, limit):
        _source_inputs(kind, context, alias, limit)
        with _tx.atomic(using=alias):
            return selected_rows(kind, refs, context, alias, governance_waived=True, limit=limit)
    def candidates(self, kind, context, alias, limit):
        _source_inputs(kind, context, alias, limit)
        with _tx.atomic(using=alias):
            if context.scope_type is _T.TENANT:
                _locks(alias, ("tenant:" + context.tenant_id,))
            _vctx(alias, context)
            keys = _KINDS[kind][2]
            rows = list(_base_queryset(kind, context, alias).order_by(*keys).values_list(*keys)[:limit + 1])
            if len(rows) > limit:
                raise _SE("DEPASSEMENT_LOT") from None
            return tuple(_make_ref(kind, tuple(str(v) if type(v) is _uu.UUID else v for v in row)) for row in rows)
