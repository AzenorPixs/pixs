"""Recette PG reelle topologie/groupes/waivers : schemas jetables, participants synthetiques."""
from __future__ import annotations
import hashlib
import re
__all__ = ["run_real_core_pg_topology_authz"]
_SCHEMA = re.compile(r"c02_[0-9a-f]{16}")
_ACTOR = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"
_SERIALIZER = "1.0.0"
_REQUIRED_CASES = ["tenant_create_platform_ok","scope_root_child_ok","scope_parent_absent_refuse","scope_intertenant_refuse","scope_cycle_refuse","scope_cas_old_refuse","contention_tenant_lock","group_platform_tenant_ok","group_collision_identity_admise","group_collision_user_refuse","group_bad_ref_context_refuse","ugroup_nn_pairs","ugroup_duplicate_active_refuse","ugroup_remove_recreate_cas","ugroup_sql_unique_active","group_persistence_archived_softdeleted","tenant_membership_service_activate","tenant_membership_revoke_reactivate","tenant_context_wrong_refuse","tenant_sql_unique_pair","alias_peer_isolation","waiver_audit_none_gov_waived_ok","waiver_audit_none_no_waiver_refuse","waiver_gov_none_refuse","waiver_bool_invalid_refuse"]
def _envelope(env_digest: str, resource: str, action: str, correlation: str, context):
    from pixs.core.authz.ports import Request
    from pixs.core.dto import CommandEnvelope
    req = Request("synthetic:decision:" + correlation[-8:], _ACTOR, resource, action, context, correlation)
    return CommandEnvelope(req, "synthetic:op:" + correlation[-8:], "synthetic:key:" + correlation[-8:], env_digest, _SERIALIZER, correlation, None)
def run_real_core_pg_topology_authz(root_str: str, schema_name: str | None = None) -> dict:
    import core_pg_test_support as support
    out = {"real_pg": False, "cases": {}, "cleanup": True, "conns_closed": False, "code": "NONE", "phase": "INIT", "failure_type": "", "django_version_num": "", "pg_version_num": ""}
    refs, close_failures, private_values = [], [], []
    owned, owned_peer, configured = False, False, False
    if type(root_str) is not str or root_str == "":
        out["code"] = "RACINE_INVALIDE"
        return out
    schema = support.safe_schema_name() if schema_name is None else schema_name
    peer_schema = support.safe_schema_name()
    if type(schema) is not str or _SCHEMA.fullmatch(schema) is None:
        out["code"] = "SCHEMA_INVALIDE"
        return out
    if type(peer_schema) is not str or _SCHEMA.fullmatch(peer_schema) is None:
        out["code"] = "SCHEMA_INVALIDE"
        return out
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None:
                out["code"] = "ENV_REFUSE"
            else:
                private_values = list(env.values())
                with support.managed_pg_connection(env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"], env["PG_USERNAME"], env["PG_PASSWORD"], refs, close_failures) as admin:
                    try:
                        owned, reason = support.create_schema(admin, schema)
                        if not owned or reason != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                        owned_peer, reason2 = support.create_schema(admin, peer_schema)
                        if not owned_peer or reason2 != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                        out["cleanup"] = False
                        opt = support.pg_options(support.quote_search_path(admin, schema))
                        opt_peer = support.pg_options(support.quote_search_path(admin, peer_schema))
                        spec = {"dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"], "password": env["PG_PASSWORD"], "host": env["PG_HOST"], "port": env["PG_PORT"], "options": opt}
                        spec_peer = {"dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"], "password": env["PG_PASSWORD"], "host": env["PG_HOST"], "port": env["PG_PORT"], "options": opt_peer}
                        support.configure_django_core_pg({"default": dict(spec), "peer": dict(spec_peer), "contender": dict(spec)})
                        configured = True
                        import django
                        django.setup()
                        from django.db import connections
                        from pixs.core.migration_lock import run_core_initial
                        import core_pg_participants as participants
                        out["phase"] = "MIGRATION"
                        run_core_initial("default", origin=None, target="0.1.0")
                        run_core_initial("peer", origin=None, target="0.1.0")
                        run_core_initial("contender", origin=None, target="0.1.0")
                        participants.create_synthetic_tables("default")
                        participants.create_synthetic_tables("peer")
                        participants.create_synthetic_tables("contender")
                        out["django_version_num"] = django.get_version()
                        with connections["default"].cursor() as cur:
                            cur.execute("SELECT current_setting('server_version_num')")
                            out["pg_version_num"] = cur.fetchone()[0]
                        if any(type(out[k]) is not str or re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", out[k]) is None for k in ("django_version_num", "pg_version_num")):
                            raise RuntimeError("VERSION_NON_PROUVEE")
                        out["phase"] = "SCENARIOS"
                        _scenarios(support, participants, out["cases"])
                    finally:
                        if configured:
                            support.close_django_connections(refs, close_failures)
                        ok = True
                        if owned:
                            ok = support.drop_schema_if_owned(admin, schema, True) and ok
                        if owned_peer:
                            ok = support.drop_schema_if_owned(admin, peer_schema, True) and ok
                        out["cleanup"] = bool(ok)
        except Exception as error:
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            cand = getattr(error, "code", None)
            if type(cand) is str and re.fullmatch(r"[A-Z][A-Z0-9_]{2,80}", cand) is not None:
                out["code"] = cand
        finally:
            out["conns_closed"] = not close_failures and all(bool(c.closed) for c in refs)
            expected = set(_REQUIRED_CASES)
            got = set(out["cases"])
            all_bool_true = all(type(v) is bool and v for v in out["cases"].values())
            out["real_pg"] = bool(out["code"] == "NONE" and out["cleanup"] and out["conns_closed"] and got == expected and all_bool_true)
            if not out["real_pg"] and out["code"] == "NONE":
                out["code"] = "CAS_NON_PROUVE"
            for k, v in tuple(out.items()):
                if type(v) is str:
                    out[k] = support.scrub_text(v, private_values)
    return out
def _scenarios(support, participants, out: dict) -> None:
    import dataclasses
    import datetime
    import hashlib
    import uuid as uuid_module
    from django.db import connections, transaction
    from pixs.core.dto import GroupCreateInput, IdentityCreateIdentityInput, IdentityCreateUserInput, LogicalDeleteInput, ScopeCreateInput, ScopeMoveInput, TenantCreateInput, TenantMembershipAddInput, TenantMembershipRevokeInput, UserGroupAddInput, UserGroupRemoveInput
    from pixs.core.identity.models import IdentityState, IdentityType
    from pixs.core.persistence.models_group import CoreGroup, CoreIdentityTenantMembership, CoreUserGroupMembership
    from pixs.core.persistence.models_identity import CoreIdentity, CoreIdentityLink, CoreUser
    from pixs.core.persistence.models_scope import CoreScope, CoreTenant
    from pixs.core.ports import CorePortError
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_common import CoreServiceError, lock_scopes as _lock_scopes
    from pixs.core.services_groups import activate_tenant_membership, add_user_group, change_group_persistence, create_group, remove_user_group, revoke_tenant_membership
    from pixs.core.services_identity import create_identity, create_user
    from pixs.core.services_scope import create_scope, create_tenant, move_scope
    from pixs.kernel.data_persistence_states import DataPersistenceState
    def _u7() -> uuid_module.UUID:
        from pixs.core.persistence.uuid7 import generate_uuid7
        return generate_uuid7()
    def _corr(n: int) -> str:
        return "synthetic:topo:%04d" % n
    def _sha(*parts: str) -> str:
        return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    def _plat():
        return ScopeContext(ScopeType.PLATFORM, None, None)
    def _ten(t: str):
        return ScopeContext(ScopeType.TENANT, t, None)
    def _mk(ref: str, action: str, n: int, ctx):
        c = _corr(n)
        return _envelope(_sha(ref, action, c), ref, action, c, ctx)
    def _ports(alias: str = "default"):
        return participants.make_ports(alias, _ACTOR, {})
    def _count(model, **kw) -> int:
        return model.objects.using("default").filter(**kw).count()
    def _stage(kind: str, op: str, alias: str = "default") -> int:
        with connections[alias].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s;", [kind, op])
            return int(cur.fetchone()[0])
    def _confirmed(op: str, alias: str = "default") -> bool:
        with connections[alias].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c02_syn_idem WHERE result->>'operation_id'=%s", [op])
            return cur.fetchone()[0] == 1
    def _refuse(fn, code: str) -> bool:
        try:
            fn()
        except CoreServiceError as err:
            return err.code == code
        except CorePortError as err:
            return err.code == code
        return False
    n = 500
    ta = " tenant alpha "
    ra = "pixs.core.tenant:" + ta
    ea = _mk(ra, "pixs.core.scope.tenant.create", n, _plat()); n += 1
    resa = create_tenant(command=TenantCreateInput(tenant_id=ta, correlation_id=ea.correlation_id), envelope=ea, ports=_ports(), alias="default")
    out["tenant_create_platform_ok"] = resa.version == 1 and _count(CoreTenant, tenant_id=ta, persistence_state="ACTIVE") == 1 and _confirmed(ea.operation_id)
    rroot = " root-a "
    eroot = _mk("pixs.core.scope:" + rroot, "pixs.core.scope.node.create", n, _ten(ta)); n += 1
    create_scope(command=ScopeCreateInput(scope_id=rroot, tenant_id=ta, parent_scope_id=None, correlation_id=eroot.correlation_id), envelope=eroot, ports=_ports(), alias="default")
    rchild = "child-a"
    echild = _mk("pixs.core.scope:" + rchild, "pixs.core.scope.node.create", n, _ten(ta)); n += 1
    resc = create_scope(command=ScopeCreateInput(scope_id=rchild, tenant_id=ta, parent_scope_id=rroot, correlation_id=echild.correlation_id), envelope=echild, ports=_ports(), alias="default")
    out["scope_root_child_ok"] = resc.version == 1 and _count(CoreScope, scope_id=rchild, persistence_state="ACTIVE") == 1 and _confirmed(echild.operation_id)
    ebad = _mk("pixs.core.scope:orphan-x", "pixs.core.scope.node.create", n, _ten(ta)); n += 1
    out["scope_parent_absent_refuse"] = _refuse(lambda: create_scope(command=ScopeCreateInput(scope_id="orphan-x", tenant_id=ta, parent_scope_id="no-such-parent", correlation_id=ebad.correlation_id), envelope=ebad, ports=_ports(), alias="default"), "PORTEE_ORPHELINE") and _count(CoreScope, scope_id="orphan-x") == 0 and _stage("outbox", ebad.operation_id) == 0
    tb = "tenant beta"
    eb = _mk("pixs.core.tenant:" + tb, "pixs.core.scope.tenant.create", n, _plat()); n += 1
    create_tenant(command=TenantCreateInput(tenant_id=tb, correlation_id=eb.correlation_id), envelope=eb, ports=_ports(), alias="default")
    einter = _mk("pixs.core.scope:cross-x", "pixs.core.scope.node.create", n, _ten(tb)); n += 1
    out["scope_intertenant_refuse"] = _refuse(lambda: create_scope(command=ScopeCreateInput(scope_id="cross-x", tenant_id=tb, parent_scope_id=rroot, correlation_id=einter.correlation_id), envelope=einter, ports=_ports(), alias="default"), "INTERTENANT_REFUSE") and _count(CoreScope, scope_id="cross-x") == 0
    emv = _mk("pixs.core.scope:" + rroot, "pixs.core.scope.node.move", n, _ten(ta)); n += 1
    out["scope_cycle_refuse"] = _refuse(lambda: move_scope(command=ScopeMoveInput(scope_id=rroot, tenant_id=ta, parent_scope_id=rchild, correlation_id=emv.correlation_id, expected_version=1), envelope=emv, ports=_ports(), alias="default"), "CYCLE_REFUSE") and _count(CoreScope, scope_id=rroot, persistence_state="ACTIVE") == 1
    efresh = _mk("pixs.core.scope:" + rchild, "pixs.core.scope.node.move", n, _ten(ta)); n += 1
    moved = move_scope(command=ScopeMoveInput(scope_id=rchild, tenant_id=ta, parent_scope_id=None, correlation_id=efresh.correlation_id, expected_version=1), envelope=efresh, ports=_ports(), alias="default")
    emv2 = _mk("pixs.core.scope:" + rchild, "pixs.core.scope.node.move", n, _ten(ta)); n += 1
    out["scope_cas_old_refuse"] = moved.version == 2 and _refuse(lambda: move_scope(command=ScopeMoveInput(scope_id=rchild, tenant_id=ta, parent_scope_id=rroot, correlation_id=emv2.correlation_id, expected_version=1), envelope=emv2, ports=_ports(), alias="default"), "CONFLIT_CAS") and CoreScope.objects.using("default").get(scope_id=rchild).parent_id is None and _stage("outbox", emv2.operation_id) == 0
    tc = "tenant gamma"
    ec = _mk("pixs.core.tenant:" + tc, "pixs.core.scope.tenant.create", n, _plat()); n += 1
    create_tenant(command=TenantCreateInput(tenant_id=tc, correlation_id=ec.correlation_id), envelope=ec, ports=_ports(), alias="default")
    held_ok = False
    with transaction.atomic(using="contender", durable=True):
        _lock_scopes("contender", ("tenant:" + ta,))
        rr = "pixs.core.scope:contended-x"
        ee = _mk(rr, "pixs.core.scope.node.create", n, _ten(ta)); n += 1
        held_ok = _refuse(lambda: create_scope(command=ScopeCreateInput(scope_id="contended-x", tenant_id=ta, parent_scope_id=None, correlation_id=ee.correlation_id), envelope=ee, ports=_ports(), alias="default"), "VERROU_CONCURRENT") and _count(CoreScope, scope_id="contended-x") == 0
        rr2 = "pixs.core.scope:other-tenant-y"
        ee2 = _mk(rr2, "pixs.core.scope.node.create", n, _ten(tc)); n += 1
        other_ok = create_scope(command=ScopeCreateInput(scope_id="other-tenant-y", tenant_id=tc, parent_scope_id=None, correlation_id=ee2.correlation_id), envelope=ee2, ports=_ports(), alias="default").version == 1
        held_ok = held_ok and other_ok
    out["contention_tenant_lock"] = held_ok and _count(CoreScope, scope_id="other-tenant-y", persistence_state="ACTIVE") == 1
    gp, gt = _u7(), _u7()
    ctx_plat = _plat()
    egp = _mk("pixs.core.group:" + str(gp), "pixs.core.groups.group.create", n, ctx_plat); n += 1
    create_group(command=GroupCreateInput(group_id=gp, context=ScopeContext(ScopeType.PLATFORM, None, None), correlation_id=egp.correlation_id), envelope=egp, ports=_ports(), alias="default")
    ctx_ten = ScopeContext(ScopeType.TENANT, ta, rchild)
    egt = _mk("pixs.core.group:" + str(gt), "pixs.core.groups.group.create", n, ctx_ten); n += 1
    create_group(command=GroupCreateInput(group_id=gt, context=ctx_ten, correlation_id=egt.correlation_id), envelope=egt, ports=_ports(), alias="default")
    out["group_platform_tenant_ok"] = _count(CoreGroup, group_id=gp, persistence_state="ACTIVE") == 1 and _count(CoreGroup, group_id=gt, persistence_state="ACTIVE") == 1
    gi = _u7()
    egi = _mk("pixs.core.identity:" + str(gi), "pixs.core.identity.identity.create", n, _plat()); n += 1
    create_identity(command=IdentityCreateIdentityInput(identity_id=gi, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=egi.correlation_id), envelope=egi, ports=_ports(), alias="default")
    egc = _mk("pixs.core.group:" + str(gi), "pixs.core.groups.group.create", n, ctx_plat); n += 1
    out["group_collision_identity_admise"] = create_group(command=GroupCreateInput(group_id=gi, context=ScopeContext(ScopeType.PLATFORM, None, None), correlation_id=egc.correlation_id), envelope=egc, ports=_ports(), alias="default").version == 1
    gu = _u7()
    euu = _mk("pixs.core.user:" + str(gu), "pixs.core.identity.user.create", n, _plat()); n += 1
    create_user(command=IdentityCreateUserInput(user_id=gu, correlation_id=euu.correlation_id), envelope=euu, ports=_ports(), alias="default")
    egu = _mk("pixs.core.group:" + str(gu), "pixs.core.groups.group.create", n, ctx_plat); n += 1
    out["group_collision_user_refuse"] = _refuse(lambda: create_group(command=GroupCreateInput(group_id=gu, context=ScopeContext(ScopeType.PLATFORM, None, None), correlation_id=egu.correlation_id), envelope=egu, ports=_ports(), alias="default"), "DISJONCTION_USER_GROUP") and _count(CoreGroup, group_id=gu) == 0
    gb = _u7()
    egb = _mk("pixs.core.group:" + str(gb), "pixs.core.groups.group.create", n, ctx_ten); n += 1
    out["group_bad_ref_context_refuse"] = _refuse(lambda: create_group(command=GroupCreateInput(group_id=gb, context=ScopeContext(ScopeType.PLATFORM, None, None), correlation_id=egb.correlation_id), envelope=egb, ports=_ports(), alias="default"), "CONTEXTE_INVALIDE") and _count(CoreGroup, group_id=gb) == 0
    ua1, ua2 = _u7(), _u7()
    for u in (ua1, ua2):
        eu = _mk("pixs.core.user:" + str(u), "pixs.core.identity.user.create", n, _plat()); n += 1
        create_user(command=IdentityCreateUserInput(user_id=u, correlation_id=eu.correlation_id), envelope=eu, ports=_ports(), alias="default")
    gg1, gg2 = _u7(), _u7()
    for g in (gg1, gg2):
        eg = _mk("pixs.core.group:" + str(g), "pixs.core.groups.group.create", n, ctx_plat); n += 1
        create_group(command=GroupCreateInput(group_id=g, context=ScopeContext(ScopeType.PLATFORM, None, None), correlation_id=eg.correlation_id), envelope=eg, ports=_ports(), alias="default")
    pairs = [(ua1, gg1), (ua1, gg2), (ua2, gg1)]
    for (u, g) in pairs:
        rr = "pixs.core.user-group:" + str(u) + "/" + str(g)
        ee = _mk(rr, "pixs.core.groups.user-group.add", n, ctx_plat); n += 1
        add_user_group(command=UserGroupAddInput(user_id=u, group_id=g, correlation_id=ee.correlation_id), envelope=ee, ports=_ports(), alias="default")
    out["ugroup_nn_pairs"] = all(CoreUserGroupMembership.objects.using("default").filter(user_id=u, group_id=g, persistence_state="ACTIVE").count() == 1 for (u, g) in pairs)
    rdup = "pixs.core.user-group:" + str(ua1) + "/" + str(gg1)
    edup = _mk(rdup, "pixs.core.groups.user-group.add", n, ctx_plat); n += 1
    out["ugroup_duplicate_active_refuse"] = _refuse(lambda: add_user_group(command=UserGroupAddInput(user_id=ua1, group_id=gg1, correlation_id=edup.correlation_id), envelope=edup, ports=_ports(), alias="default"), "MEMBRE_DEJA_ACTIF")
    ru = "pixs.core.user-group:" + str(ua1) + "/" + str(gg1)
    ug_before = CoreUserGroupMembership.objects.using("default").get(user_id=ua1, group_id=gg1, persistence_state="ACTIVE")
    ug_classification = (ug_before.governance_ref, ug_before.confidentiality, ug_before.personal)
    er = _mk(ru, "pixs.core.groups.user-group.remove", n, ctx_plat); n += 1
    rr1 = remove_user_group(command=UserGroupRemoveInput(user_id=ua1, group_id=gg1, correlation_id=er.correlation_id, expected_version=1), envelope=er, ports=_ports(), alias="default")
    rows = list(CoreUserGroupMembership.objects.using("default").filter(user_id=ua1, group_id=gg1).order_by("version"))
    er2 = _mk(ru, "pixs.core.groups.user-group.add", n, ctx_plat); n += 1
    rr2 = add_user_group(command=UserGroupAddInput(user_id=ua1, group_id=gg1, correlation_id=er2.correlation_id), envelope=er2, ports=_ports(), alias="default")
    rows2 = list(CoreUserGroupMembership.objects.using("default").filter(user_id=ua1, group_id=gg1).order_by("version"))
    erbad = _mk(ru, "pixs.core.groups.user-group.remove", n, ctx_plat); n += 1
    out["ugroup_remove_recreate_cas"] = rr1.version == 2 and rr2.version == 3 and len(rows2) == 2 and rows2[0].persistence_state == "SOFT_DELETED" and rows2[1].persistence_state == "ACTIVE" and _refuse(lambda: remove_user_group(command=UserGroupRemoveInput(user_id=ua1, group_id=gg1, correlation_id=erbad.correlation_id, expected_version=1), envelope=erbad, ports=_ports(), alias="default"), "CONFLIT_CAS")
    from django.db import IntegrityError as _IError
    import datetime as _dt
    nowx = _dt.datetime.now(_dt.timezone.utc)
    base = CoreUserGroupMembership.objects.using("default").get(user_id=ua2, group_id=gg1, persistence_state="ACTIVE")
    sql_ok = False
    try:
        with transaction.atomic(using="default"):
            dup = CoreUserGroupMembership(user_id=ua2, group_id=gg1, version=9, created_at=nowx, updated_at=nowx, governance_ref=base.governance_ref, confidentiality=base.confidentiality, personal=base.personal, persistence_state="ACTIVE", retention_state="RETAINED")
            dup._state.db = "default"
            dup.full_clean(validate_unique=False, validate_constraints=False)
            dup.save(using="default", force_insert=True)
    except _IError as err:
        sql_ok = getattr(getattr(err.__cause__, "diag", None), "constraint_name", None) == "ugroup_user_grp_uq"
    out["ugroup_sql_unique_active"] = bool(sql_ok and _count(CoreUserGroupMembership, user_id=ua2, group_id=gg1, persistence_state="ACTIVE") == 1)
    gcy = _u7()
    egcy = _mk("pixs.core.group:" + str(gcy), "pixs.core.groups.group.create", n, ctx_plat); n += 1
    create_group(command=GroupCreateInput(group_id=gcy, context=ScopeContext(ScopeType.PLATFORM, None, None), correlation_id=egcy.correlation_id), envelope=egcy, ports=_ports(), alias="default")
    group_before = CoreGroup.objects.using("default").get(group_id=gcy)
    group_classification = (group_before.governance_ref, group_before.confidentiality, group_before.personal)
    rcy = "pixs.core.group:" + str(gcy)
    ea1 = _mk(rcy, "pixs.core.groups.group.persistence.change", n, ctx_plat); n += 1
    ra1 = change_group_persistence(command=LogicalDeleteInput(resource_ref=rcy, target_state=DataPersistenceState.ARCHIVED, correlation_id=ea1.correlation_id, expected_version=1), envelope=ea1, ports=_ports(), alias="default")
    ea2 = _mk(rcy, "pixs.core.groups.group.persistence.change", n, ctx_plat); n += 1
    ra2 = change_group_persistence(command=LogicalDeleteInput(resource_ref=rcy, target_state=DataPersistenceState.SOFT_DELETED, correlation_id=ea2.correlation_id, expected_version=2), envelope=ea2, ports=_ports(), alias="default")
    out["group_persistence_archived_softdeleted"] = ra1.version == 2 and ra2.version == 3 and _stage("governance", ea1.operation_id) >= 1 and _stage("governance", ea2.operation_id) >= 1 and _count(CoreGroup, group_id=gcy) == 1
    si = _u7()
    esi = _mk("pixs.core.identity:" + str(si), "pixs.core.identity.identity.create", n, _plat()); n += 1
    create_identity(command=IdentityCreateIdentityInput(identity_id=si, identity_type=IdentityType.SERVICE, state=IdentityState.ACTIVE, correlation_id=esi.correlation_id), envelope=esi, ports=_ports(), alias="default")
    rtm = "pixs.core.identity-tenant:" + str(si) + "/" + ta
    etm = _mk(rtm, "pixs.core.groups.tenant-membership.activate", n, _ten(ta)); n += 1
    ract = activate_tenant_membership(command=TenantMembershipAddInput(identity_id=si, tenant_id=ta, correlation_id=etm.correlation_id, expected_version=None), envelope=etm, ports=_ports(), alias="default")
    member_before = CoreIdentityTenantMembership.objects.using("default").get(identity_id=si, tenant_id=ta)
    member_classification = (member_before.governance_ref, member_before.confidentiality, member_before.personal)
    out["tenant_membership_service_activate"] = ract.version == 1 and _count(CoreIdentityTenantMembership, identity_id=si, tenant_id=ta) == 1
    erv = _mk(rtm, "pixs.core.groups.tenant-membership.revoke", n, _ten(ta)); n += 1
    rrev = revoke_tenant_membership(command=TenantMembershipRevokeInput(identity_id=si, tenant_id=ta, correlation_id=erv.correlation_id, expected_version=1), envelope=erv, ports=_ports(), alias="default")
    member_revoked = CoreIdentityTenantMembership.objects.using("default").get(identity_id=si, tenant_id=ta)
    ere_none = _mk(rtm, "pixs.core.groups.tenant-membership.activate", n, _ten(ta)); n += 1
    none_req = _refuse(lambda: activate_tenant_membership(command=TenantMembershipAddInput(identity_id=si, tenant_id=ta, correlation_id=ere_none.correlation_id, expected_version=None), envelope=ere_none, ports=_ports(), alias="default"), "CAS_REQUIS")
    ere_old = _mk(rtm, "pixs.core.groups.tenant-membership.activate", n, _ten(ta)); n += 1
    old_req = _refuse(lambda: activate_tenant_membership(command=TenantMembershipAddInput(identity_id=si, tenant_id=ta, correlation_id=ere_old.correlation_id, expected_version=1), envelope=ere_old, ports=_ports(), alias="default"), "CONFLIT_CAS")
    ere_ok = _mk(rtm, "pixs.core.groups.tenant-membership.activate", n, _ten(ta)); n += 1
    rok = activate_tenant_membership(command=TenantMembershipAddInput(identity_id=si, tenant_id=ta, correlation_id=ere_ok.correlation_id, expected_version=2), envelope=ere_ok, ports=_ports(), alias="default")
    out["tenant_membership_revoke_reactivate"] = rrev.version == 2 and none_req and old_req and rok.version == 3 and _count(CoreIdentityTenantMembership, identity_id=si, tenant_id=ta) == 1 and _stage("governance", erv.operation_id) == 0
    ewrong = _mk(rtm, "pixs.core.groups.tenant-membership.activate", n, _ten(tb)); n += 1
    out["tenant_context_wrong_refuse"] = _refuse(lambda: activate_tenant_membership(command=TenantMembershipAddInput(identity_id=si, tenant_id=ta, correlation_id=ewrong.correlation_id, expected_version=None), envelope=ewrong, ports=_ports(), alias="default"), "CONTEXTE_INVALIDE") and _count(CoreIdentityTenantMembership, identity_id=si, tenant_id=ta) == 1
    import datetime as _dt2
    now2 = _dt2.datetime.now(_dt2.timezone.utc)
    base2 = CoreIdentityTenantMembership.objects.using("default").get(identity_id=si, tenant_id=ta)
    sql_pair_ok = False
    try:
        with transaction.atomic(using="default"):
            dup2 = CoreIdentityTenantMembership(identity_id=si, tenant_id=ta, activation="ACTIVE", version=9, created_at=now2, updated_at=now2, governance_ref=base2.governance_ref, confidentiality=base2.confidentiality, personal=base2.personal, persistence_state="ARCHIVED", retention_state="RETAINED")
            dup2._state.db = "default"
            dup2.full_clean(validate_unique=False, validate_constraints=False)
            dup2.save(using="default", force_insert=True)
    except _IError as err:
        sql_pair_ok = getattr(getattr(err.__cause__, "diag", None), "constraint_name", None) == "idtenant_idt_ten_uq"
    out["tenant_sql_unique_pair"] = bool(sql_pair_ok)
    tp = "tenant peer-iso"
    ept = _mk("pixs.core.tenant:" + tp, "pixs.core.scope.tenant.create", n, _plat()); n += 1
    create_tenant(command=TenantCreateInput(tenant_id=tp, correlation_id=ept.correlation_id), envelope=ept, ports=participants.make_ports("peer", _ACTOR, {}), alias="peer")
    spt = "scope-peer-1"
    ept2 = _mk("pixs.core.scope:" + spt, "pixs.core.scope.node.create", n, ScopeContext(ScopeType.TENANT, tp, None)); n += 1
    create_scope(command=ScopeCreateInput(scope_id=spt, tenant_id=tp, parent_scope_id=None, correlation_id=ept2.correlation_id), envelope=ept2, ports=participants.make_ports("peer", _ACTOR, {}), alias="peer")
    gpt = _u7()
    ept3 = _mk("pixs.core.group:" + str(gpt), "pixs.core.groups.group.create", n, ScopeContext(ScopeType.TENANT, tp, spt)); n += 1
    create_group(command=GroupCreateInput(group_id=gpt, context=ScopeContext(ScopeType.TENANT, tp, spt), correlation_id=ept3.correlation_id), envelope=ept3, ports=participants.make_ports("peer", _ACTOR, {}), alias="peer")
    out["alias_peer_isolation"] = _count(CoreTenant, tenant_id=tp) == 0 and CoreTenant.objects.using("peer").filter(tenant_id=tp).count() == 1 and _count(CoreGroup, group_id=gpt) == 0
    uw = _u7()
    rw = "pixs.core.user:" + str(uw)
    ctxw = _plat()
    ew = _mk(rw, "pixs.core.identity.user.create", n, ctxw); n += 1
    import dataclasses as _dc
    base_ports = _ports()
    waived_ports = _dc.replace(base_ports, audit=None, governance=None, decider=type("W", (), {"decide": lambda self, req: base_ports.decider.decide(req), "revalidate_under_locks": lambda self, req, **kw: base_ports.decider.revalidate_under_locks(req, **kw), "audit_waived": lambda self, req, dec, **kw: True, "governance_waived": lambda self, req, dec, **kw: True})())
    resw = create_user(command=IdentityCreateUserInput(user_id=uw, correlation_id=ew.correlation_id), envelope=ew, ports=waived_ports, alias="default")
    out["waiver_audit_none_gov_waived_ok"] = resw.version == 1 and _stage("audit", ew.operation_id) == 0 and _stage("outbox", ew.operation_id) == 1 and _confirmed(ew.operation_id)
    un = _u7()
    rn = "pixs.core.user:" + str(un)
    en = _mk(rn, "pixs.core.identity.user.create", n, ctxw); n += 1
    refused_n = _refuse(lambda: create_user(command=IdentityCreateUserInput(user_id=un, correlation_id=en.correlation_id), envelope=en, ports=_dc.replace(base_ports, audit=None), alias="default"), "AUDIT_REFUS_INDISPONIBLE")
    out["waiver_audit_none_no_waiver_refuse"] = refused_n and _count(CoreUser, user_id=un) == 0 and _stage("outbox", en.operation_id) == 0
    ug = _u7()
    rg = "pixs.core.user:" + str(ug)
    eg = _mk(rg, "pixs.core.identity.user.create", n, ctxw); n += 1
    refused_g = _refuse(lambda: create_user(command=IdentityCreateUserInput(user_id=ug, correlation_id=eg.correlation_id), envelope=eg, ports=_dc.replace(base_ports, governance=None), alias="default"), "GOUVERNANCE_ABSENTE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s AND detail->>'effect'='DENY'", ["audit", eg.operation_id])
        aud_g = cur.fetchone()[0] == 1
    out["waiver_gov_none_refuse"] = refused_g and aud_g and _count(CoreUser, user_id=ug) == 0 and _stage("outbox", eg.operation_id) == 0
    ub = _u7()
    rb = "pixs.core.user:" + str(ub)
    ebb = _mk(rb, "pixs.core.identity.user.create", n, ctxw); n += 1
    bad_dec = type("B", (), {"decide": lambda self, req: base_ports.decider.decide(req), "revalidate_under_locks": lambda self, req, **kw: base_ports.decider.revalidate_under_locks(req, **kw), "audit_waived": lambda self, req, dec, **kw: "yes", "governance_waived": lambda self, req, dec, **kw: False})()
    out["waiver_bool_invalid_refuse"] = _refuse(lambda: create_user(command=IdentityCreateUserInput(user_id=ub, correlation_id=ebb.correlation_id), envelope=ebb, ports=_dc.replace(base_ports, decider=bad_dec), alias="default"), "DEROGATION_INVALIDE") and _count(CoreUser, user_id=ub) == 0

    group_tenant_row = CoreGroup.objects.using("default").get(group_id=gt)
    group_platform_row = CoreGroup.objects.using("default").get(group_id=gp)
    out["group_platform_tenant_ok"] = out["group_platform_tenant_ok"] and (group_tenant_row.scope_type, group_tenant_row.tenant_id, group_tenant_row.scope_id) == ("TENANT", ta, rchild) and (group_platform_row.scope_type, group_platform_row.tenant_id, group_platform_row.scope_id) == ("PLATFORM", None, None)
    out["ugroup_remove_recreate_cas"] = out["ugroup_remove_recreate_cas"] and [r.version for r in rows2] == [2, 3] and all((r.governance_ref, r.confidentiality, r.personal) == ug_classification for r in rows2) and _stage("governance", er.operation_id) == 1 and CoreUserGroupMembership.objects.using("default").get(user_id=ua1, group_id=gg1, persistence_state="ACTIVE").version == 3
    group_after = CoreGroup.objects.using("default").get(group_id=gcy)
    out["group_persistence_archived_softdeleted"] = out["group_persistence_archived_softdeleted"] and group_after.persistence_state == "SOFT_DELETED" and group_after.version == 3 and (group_after.governance_ref, group_after.confidentiality, group_after.personal) == group_classification and (group_after.scope_type, group_after.tenant_id, group_after.scope_id) == ("PLATFORM", None, None)
    out["tenant_membership_service_activate"] = out["tenant_membership_service_activate"] and CoreIdentity.objects.using("default").get(identity_id=si).identity_type == "SERVICE" and not CoreIdentityLink.objects.using("default").filter(identity_id=si).exists()
    member_after = CoreIdentityTenantMembership.objects.using("default").get(identity_id=si, tenant_id=ta)
    out["tenant_membership_revoke_reactivate"] = out["tenant_membership_revoke_reactivate"] and (member_revoked.activation, member_revoked.persistence_state, member_revoked.version) == ("REVOKED", "ACTIVE", 2) and (member_after.activation, member_after.persistence_state, member_after.version) == ("ACTIVE", "ACTIVE", 3) and member_after.pk == member_before.pk and (member_after.governance_ref, member_after.confidentiality, member_after.personal) == member_classification
    out["alias_peer_isolation"] = out["alias_peer_isolation"] and CoreGroup.objects.using("peer").get(group_id=gpt).scope_id == spt and not CoreScope.objects.using("default").filter(scope_id=spt).exists()
    waiver_row = CoreUser.objects.using("default").get(user_id=uw)
    out["waiver_audit_none_gov_waived_ok"] = out["waiver_audit_none_gov_waived_ok"] and (waiver_row.governance_ref, waiver_row.confidentiality, waiver_row.personal) == (None, None, None) and _stage("governance-attest", ew.operation_id) == 0 and _stage("governance", ew.operation_id) == 0
    wrong_group_ref = "pixs.core.user-group:" + str(ua1) + "/" + str(gt)
    wrong_group_env = _mk(wrong_group_ref, "pixs.core.groups.user-group.add", n, _ten(tb)); n += 1
    wrong_group_refused = _refuse(lambda: add_user_group(command=UserGroupAddInput(user_id=ua1, group_id=gt, correlation_id=wrong_group_env.correlation_id), envelope=wrong_group_env, ports=_ports(), alias="default"), "CONTEXTE_INVALIDE")
    out["group_bad_ref_context_refuse"] = out["group_bad_ref_context_refuse"] and wrong_group_refused and _count(CoreUserGroupMembership, user_id=ua1, group_id=gt) == 0 and _stage("outbox", wrong_group_env.operation_id) == 0
    _authz_scenarios(participants, out)

_REQUIRED_CASES += ["authz_perm_declare_ok","authz_perm_no_decl_refuse","authz_perm_verify_false_refuse","authz_roles_platform_tenant_ok","authz_role_absent_perm_refuse","authz_role_dup_compo_refuse","authz_role_replace_aba_ok","authz_roleperm_sql_uq","authz_assign_three_subjects_ok","authz_assign_absent_refuse","authz_assign_bad_refs_refuse","authz_assign_reassign_cas_ok","authz_assign_sql_uq_platform","authz_policy_two_versions_ok","authz_policy_dup_sql_refuse","authz_policy_no_decl_refuse","authz_state_cycle_ok","authz_sa_grant_cycle_ok","authz_sa_sql_uq","authz_sa_guards_refuse","authz_sa_deny_refuse"]
def _authz_scenarios(participants, out: dict) -> None:
    import dataclasses as _dc
    import datetime as _dt
    import hashlib as _hl
    import urllib.parse as _up
    import uuid as _uu
    from django.db import IntegrityError as _IE, connections as _conns, transaction as _tx
    from pixs.core.authz.policy import Effect as _Eff, Policy as _Pol, Selector as _Sel, ScopeSelector as _SSel
    from pixs.core.dto import CoreInputInvalid as _CII, IdentityCreateIdentityInput as _ICI, IdentityCreateUserInput as _ICU, LogicalDeleteInput as _LD, PermissionDeclareInput as _PDI, PolicyPersistInput as _PPI, RoleAssignInput as _RAI, RoleCreateInput as _RCI, RoleUnassignInput as _RUI, SuperAdminGrantInput as _SGI
    from pixs.core.identity.models import IdentityState as _IS, IdentityType as _IT
    from pixs.core.persistence.models_authz import CorePermission as _CP, CorePolicy as _CPo, CoreRole as _CR, CoreRoleAssignment as _CRA, CoreRolePermission as _CRP
    from pixs.core.persistence.models_group import CoreGroup as _CG
    from pixs.core.persistence.models_identity import CoreIdentity as _CI, CoreSuperAdminBinding as _SB, CoreSuperAdminTenantGrant as _SG, CoreUser as _CU
    from pixs.core.persistence.models_scope import CoreTenant as _CT
    from pixs.core.persistence.uuid7 import generate_uuid7 as _g7
    from pixs.core.ports import CorePortError as _CPE
    from pixs.core.scope.context import ScopeContext as _SC, ScopeType as _ST
    from pixs.core.services_authz import assign_role as _assign, change_authz_persistence as _chg, create_role as _crole, declare_permission as _decl, grant_super_admin_tenant as _grant, persist_policy as _persist, revoke_super_admin_tenant as _revoke, set_role_permissions as _setperms, unassign_role as _unassign
    from pixs.core.services_common import CoreServiceError as _CSE
    from pixs.core.services_identity import create_identity as _cident, create_user as _cuser
    from pixs.core.services_scope import create_scope as _cscope, create_tenant as _ctenant
    from pixs.kernel.data_persistence_states import DataPersistenceState as _DPS
    def _u7() -> _uu.UUID:
        return _g7()
    def _corr(n: int) -> str:
        return "synthetic:authz:%05d" % n
    def _sha(*parts: str) -> str:
        return _hl.sha256("|".join(parts).encode("utf-8")).hexdigest()
    def _plat() -> _SC:
        return _SC(_ST.PLATFORM, None, None)
    def _ten(t: str) -> _SC:
        return _SC(_ST.TENANT, t, None)
    def _mk(ref: str, action: str, n: int, ctx: _SC):
        c = _corr(n)
        return _envelope(_sha(ref, action, c), ref, action, c, ctx)
    def _ports(alias: str = "default", flags: dict | None = None):
        return participants.make_ports(alias, _ACTOR, {} if flags is None else flags)
    def _count(model: object, **kw: object) -> int:
        return model.objects.using("default").filter(**kw).count()
    def _stage(kind: str, op: str) -> int:
        with _conns["default"].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s;", [kind, op])
            return int(cur.fetchone()[0])
    def _policy_ref(pid: str, version: str) -> str:
        return "pixs.core.policy:" + _up.quote(pid, safe="") + "/" + _up.quote(version, safe="")
    def _grant_ref(installation: str, tenant: str) -> str:
        return "pixs.core.super-admin-grant:" + _up.quote(installation, safe="") + "/" + _up.quote(tenant, safe="")
    def _refuse(fn: object, code: str) -> bool:
        try:
            fn()
        except _CSE as err:
            return err.code == code
        except _CPE as err:
            return err.code == code
        return False
    n = 90000
    pa, pb, pc = "perm-authz-a", "perm-authz-b", "perm-authz-c"
    _perm_envs = {}
    for pid, owner, res, act in ((pa, "owner-a", "res-a", "act-a"), (pb, "owner-b", "res-b", "act-b"), (pc, "owner-c", "res-c", "act-c")):
        rr = "pixs.core.permission:" + pid
        ee = _mk(rr, "pixs.core.authz.permission.declare", n, _plat()); n += 1
        _decl(command=_PDI(permission_id=pid, owner_component=owner, resource_ref=res, action_ref=act, correlation_id=ee.correlation_id), envelope=ee, ports=_ports(), alias="default")
        _perm_envs[pid] = ee
    out["authz_perm_declare_ok"] = _count(_CP, permission_id=pa) == 1 and _count(_CP, permission_id=pb) == 1
    rn, ee = "pixs.core.permission:perm-authz-none", _mk("pixs.core.permission:perm-authz-none", "pixs.core.authz.permission.declare", n, _plat()); n += 1
    out["authz_perm_no_decl_refuse"] = _refuse(lambda: _decl(command=_PDI(permission_id="perm-authz-none", owner_component="o", resource_ref="r", action_ref="a", correlation_id=ee.correlation_id), envelope=ee, ports=_dc.replace(_ports(), declarations=None), alias="default"), "DECLARATION_ABSENTE") and _count(_CP, permission_id="perm-authz-none") == 0 and _stage("outbox", ee.operation_id) == 0
    class _BadDecl:
        def __init__(self, inner: object) -> None:
            self._inner = inner
        def validate_permission(self, **kw: object) -> object:
            return self._inner.validate_permission(**kw)
        def validate_policy(self, **kw: object) -> object:
            return self._inner.validate_policy(**kw)
        def verify_staged(self, proof: object) -> bool:
            return False
    _bp = _ports()
    _bad = _dc.replace(_bp, declarations=_BadDecl(_bp.declarations))
    _eb = _mk("pixs.core.permission:perm-authz-badver", "pixs.core.authz.permission.declare", n, _plat()); n += 1
    _bad_refused = _refuse(lambda: _decl(command=_PDI(permission_id="perm-authz-badver", owner_component="o", resource_ref="r", action_ref="a", correlation_id=_eb.correlation_id), envelope=_eb, ports=_bad, alias="default"), "PREUVE_INVALIDE")
    with _conns["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s AND detail->>'effect'='DENY'", ["audit", _eb.operation_id])
        _aud = cur.fetchone()[0] == 1
    out["authz_perm_verify_false_refuse"] = bool(_bad_refused and _aud and _count(_CP, permission_id="perm-authz-badver") == 0 and _stage("outbox", _eb.operation_id) == 0)
    _ta, _sa, _rc = "authz tenant ra", "authz-scope-ra", "authz-scope-ra-child"
    _et = _mk("pixs.core.tenant:" + _ta, "pixs.core.scope.tenant.create", n, _plat()); n += 1
    from pixs.core.dto import TenantCreateInput as _TCI, ScopeCreateInput as _SCI
    _ctenant(command=_TCI(tenant_id=_ta, correlation_id=_et.correlation_id), envelope=_et, ports=_ports(), alias="default")
    _er = _mk("pixs.core.scope:" + _sa, "pixs.core.scope.node.create", n, _ten(_ta)); n += 1
    _cscope(command=_SCI(scope_id=_sa, tenant_id=_ta, parent_scope_id=None, correlation_id=_er.correlation_id), envelope=_er, ports=_ports(), alias="default")
    _ec = _mk("pixs.core.scope:" + _rc, "pixs.core.scope.node.create", n, _ten(_ta)); n += 1
    _cscope(command=_SCI(scope_id=_rc, tenant_id=_ta, parent_scope_id=_sa, correlation_id=_ec.correlation_id), envelope=_ec, ports=_ports(), alias="default")
    _rp, _rt = "role-authz-p", "role-authz-t"
    _ep = _mk("pixs.core.role:" + _rp, "pixs.core.authz.role.create", n, _plat()); n += 1
    _crole(command=_RCI(role_id=_rp, context=_plat(), permission_ids=(pa,), correlation_id=_ep.correlation_id, expected_version=None), envelope=_ep, ports=_ports(), alias="default")
    _ctx_t = _SC(_ST.TENANT, _ta, _rc)
    _eg = _mk("pixs.core.role:" + _rt, "pixs.core.authz.role.create", n, _ctx_t); n += 1
    _crole(command=_RCI(role_id=_rt, context=_ctx_t, permission_ids=(pa, pb), correlation_id=_eg.correlation_id, expected_version=None), envelope=_eg, ports=_ports(), alias="default")
    out["authz_roles_platform_tenant_ok"] = _count(_CR, role_id=_rp) == 1 and _count(_CR, role_id=_rt) == 1 and _CR.objects.using("default").get(role_id=_rt).tenant_id == _ta
    _ex = _mk("pixs.core.role:role-authz-abs", "pixs.core.authz.role.create", n, _plat()); n += 1
    out["authz_role_absent_perm_refuse"] = _refuse(lambda: _crole(command=_RCI(role_id="role-authz-abs", context=_plat(), permission_ids=("perm-absent-x",), correlation_id=_ex.correlation_id, expected_version=None), envelope=_ex, ports=_ports(), alias="default"), "PERMISSION_ABSENTE") and _count(_CR, role_id="role-authz-abs") == 0
    _ed = _mk("pixs.core.role:role-authz-dup", "pixs.core.authz.role.create", n, _plat()); n += 1
    out["authz_role_dup_compo_refuse"] = _refuse(lambda: _crole(command=_RCI(role_id="role-authz-dup", context=_plat(), permission_ids=(pa, pa), correlation_id=_ed.correlation_id, expected_version=None), envelope=_ed, ports=_ports(), alias="default"), "COMPOSITION_DUPLIQUEE") and _count(_CR, role_id="role-authz-dup") == 0
    _rr, _e1 = "role-authz-aba", _mk("pixs.core.role:role-authz-aba", "pixs.core.authz.role.create", n, _plat()); n += 1
    _crole(command=_RCI(role_id=_rr, context=_plat(), permission_ids=(pa,), correlation_id=_e1.correlation_id, expected_version=None), envelope=_e1, ports=_ports(), alias="default")
    _row1 = _CR.objects.using("default").get(role_id=_rr)
    _cls1 = (_row1.governance_ref, _row1.confidentiality, _row1.personal)
    _e2 = _mk("pixs.core.role:" + _rr, "pixs.core.authz.role.permissions.set", n, _plat()); n += 1
    _r2 = _setperms(command=_RCI(role_id=_rr, context=_plat(), permission_ids=(pb,), correlation_id=_e2.correlation_id, expected_version=1), envelope=_e2, ports=_ports(), alias="default")
    _e3 = _mk("pixs.core.role:" + _rr, "pixs.core.authz.role.permissions.set", n, _plat()); n += 1
    _r3 = _setperms(command=_RCI(role_id=_rr, context=_plat(), permission_ids=(pa,), correlation_id=_e3.correlation_id, expected_version=2), envelope=_e3, ports=_ports(), alias="default")
    _links = list(_CRP.objects.using("default").filter(role_id=_rr).order_by("permission_id", "version"))
    _old = [x for x in _links if x.permission_id == pb]
    _new = [x for x in _links if x.permission_id == pa and x.persistence_state == "ACTIVE"]
    _eold = _mk("pixs.core.role:" + _rr, "pixs.core.authz.role.permissions.set", n, _plat()); n += 1
    _old_cas = _refuse(lambda: _setperms(command=_RCI(role_id=_rr, context=_plat(), permission_ids=(pc,), correlation_id=_eold.correlation_id, expected_version=1), envelope=_eold, ports=_ports(), alias="default"), "CONFLIT_CAS")
    out["authz_role_replace_aba_ok"] = bool(_r2.version == 2 and _r3.version == 3 and len(_old) == 1 and _old[0].persistence_state == "SOFT_DELETED" and _old[0].version == 2 and len(_new) == 1 and _new[0].version == 3 and (_new[0].governance_ref, _new[0].confidentiality, _new[0].personal) == _cls1 and _old_cas)
    _sql_rp = False
    try:
        with _tx.atomic(using="default"):
            _b = _CRP.objects.using("default").get(role_id=_rr, permission_id=pa, persistence_state="ACTIVE")
            _now = _dt.datetime.now(_dt.timezone.utc)
            _dup = _CRP(role=_b.role, permission=_b.permission, version=9, created_at=_now, updated_at=_now, governance_ref=_b.governance_ref, confidentiality=_b.confidentiality, personal=_b.personal, persistence_state="ACTIVE", retention_state="RETAINED")
            _dup._state.db = "default"
            _dup.full_clean(validate_unique=False, validate_constraints=False)
            _dup.save(using="default", force_insert=True)
    except _IE as err:
        _sql_rp = getattr(getattr(err.__cause__, "diag", None), "constraint_name", None) == "roleperm_role_perm_uq"
    out["authz_roleperm_sql_uq"] = bool(_sql_rp)
    _uu1, _uu2, _uu3 = _u7(), _u7(), _u7()
    for _u, _ty in ((_uu1, _IT.HUMAN), (_uu2, _IT.DEVICE), (_uu3, _IT.FEDERATED)):
        _ei = _mk("pixs.core.identity:" + str(_u), "pixs.core.identity.identity.create", n, _plat()); n += 1
        _cident(command=_ICI(identity_id=_u, identity_type=_ty, state=_IS.ACTIVE, correlation_id=_ei.correlation_id), envelope=_ei, ports=_ports(), alias="default")
    _gu = _u7()
    _eu = _mk("pixs.core.user:" + str(_gu), "pixs.core.identity.user.create", n, _plat()); n += 1
    _cuser(command=_ICU(user_id=_gu, correlation_id=_eu.correlation_id), envelope=_eu, ports=_ports(), alias="default")
    _gg = _u7()
    _egr = _mk("pixs.core.group:" + str(_gg), "pixs.core.groups.group.create", n, _plat()); n += 1
    from pixs.core.dto import GroupCreateInput as _GCI
    from pixs.core.services_groups import create_group as _cgrp
    _cgrp(command=_GCI(group_id=_gg, context=_plat(), correlation_id=_egr.correlation_id), envelope=_egr, ports=_ports(), alias="default")
    _ra = "role-authz-assign"
    _era = _mk("pixs.core.role:" + _ra, "pixs.core.authz.role.create", n, _plat()); n += 1
    _crole(command=_RCI(role_id=_ra, context=_plat(), permission_ids=(pa,), correlation_id=_era.correlation_id, expected_version=None), envelope=_era, ports=_ports(), alias="default")
    import urllib.parse as _qp
    def _aref(rid: str, st: str, su: _uu.UUID) -> str:
        return "pixs.core.role-assignment:" + _qp.quote(rid, safe="") + "/" + st + "/" + str(su)
    for _st, _su in (("USER", _gu), ("IDENTITY", _uu1), ("GROUP", _gg)):
        _rf = _aref(_ra, _st, _su)
        _ee = _mk(_rf, "pixs.core.authz.role.assign", n, _plat()); n += 1
        _assign(command=_RAI(role_id=_ra, subject_type=_st, subject_ref=str(_su), correlation_id=_ee.correlation_id), envelope=_ee, ports=_ports(), alias="default")
    out["authz_assign_three_subjects_ok"] = _count(_CRA, role_id=_ra, persistence_state="ACTIVE") == 3
    _ghost = _u7()
    _rg = _aref(_ra, "USER", _ghost)
    _egx = _mk(_rg, "pixs.core.authz.role.assign", n, _plat()); n += 1
    out["authz_assign_absent_refuse"] = _refuse(lambda: _assign(command=_RAI(role_id=_ra, subject_type="USER", subject_ref=str(_ghost), correlation_id=_egx.correlation_id), envelope=_egx, ports=_ports(), alias="default"), "SUJET_ABSENT")
    _bad4 = _uu.UUID("12345678-1234-4234-8234-123456789012")
    _rb4 = _aref(_ra, "USER", _bad4)
    _eb4 = _mk(_rb4, "pixs.core.authz.role.assign", n, _plat()); n += 1
    _b4 = _refuse(lambda: _assign(command=_RAI(role_id=_ra, subject_type="USER", subject_ref=str(_bad4), correlation_id=_eb4.correlation_id), envelope=_eb4, ports=_ports(), alias="default"), "REFERENCE_INVALIDE")
    _eti = _mk(_aref(_ra, "ALIEN", _gu), "pixs.core.authz.role.assign", n, _plat()); n += 1
    _b5 = False
    try:
        _RAI(role_id=_ra, subject_type="ALIEN", subject_ref=str(_gu), correlation_id=_eti.correlation_id)
    except _CII:
        _b5 = True
    _rw = _aref(_rt, "USER", _gu)
    _ewr = _mk(_rw, "pixs.core.authz.role.assign", n, _ten("authz tenant ra")); n += 1
    _b6 = _refuse(lambda: _assign(command=_RAI(role_id=_rt, subject_type="USER", subject_ref=str(_gu), correlation_id=_ewr.correlation_id), envelope=_ewr, ports=_ports(), alias="default"), "CONTEXTE_INVALIDE")
    out["authz_assign_bad_refs_refuse"] = bool(_b4 and _b5 and _b6)
    _su2 = _u7()
    _es2 = _mk("pixs.core.identity:" + str(_su2), "pixs.core.identity.identity.create", n, _plat()); n += 1
    _cident(command=_ICI(identity_id=_su2, identity_type=_IT.HUMAN, state=_IS.ACTIVE, correlation_id=_es2.correlation_id), envelope=_es2, ports=_ports(), alias="default")
    _rf2 = _aref(_ra, "IDENTITY", _su2)
    _e21 = _mk(_rf2, "pixs.core.authz.role.assign", n, _plat()); n += 1
    _a1 = _assign(command=_RAI(role_id=_ra, subject_type="IDENTITY", subject_ref=str(_su2), correlation_id=_e21.correlation_id), envelope=_e21, ports=_ports(), alias="default")
    _e22 = _mk(_rf2, "pixs.core.authz.role.unassign", n, _plat()); n += 1
    _a2 = _unassign(command=_RUI(role_id=_ra, subject_type="IDENTITY", subject_ref=str(_su2), correlation_id=_e22.correlation_id, expected_version=1), envelope=_e22, ports=_ports(), alias="default")
    _e23 = _mk(_rf2, "pixs.core.authz.role.assign", n, _plat()); n += 1
    _a3 = _assign(command=_RAI(role_id=_ra, subject_type="IDENTITY", subject_ref=str(_su2), correlation_id=_e23.correlation_id), envelope=_e23, ports=_ports(), alias="default")
    _e24 = _mk(_rf2, "pixs.core.authz.role.unassign", n, _plat()); n += 1
    _cas_old = _refuse(lambda: _unassign(command=_RUI(role_id=_ra, subject_type="IDENTITY", subject_ref=str(_su2), correlation_id=_e24.correlation_id, expected_version=1), envelope=_e24, ports=_ports(), alias="default"), "CONFLIT_CAS")
    out["authz_assign_reassign_cas_ok"] = bool(_a1.version == 1 and _a2.version == 2 and _a3.version == 3 and _cas_old)
    _sql_ra = False
    try:
        with _tx.atomic(using="default"):
            _ex = _CRA.objects.using("default").get(role_id=_ra, subject_type="USER", subject_ref=str(_gu), persistence_state="ACTIVE")
            _nw = _dt.datetime.now(_dt.timezone.utc)
            _dd = _CRA(role=_ex.role, subject_type="USER", subject_ref=str(_gu), scope_type="PLATFORM", tenant=None, scope=None, version=9, created_at=_nw, updated_at=_nw, governance_ref=_ex.governance_ref, confidentiality=_ex.confidentiality, personal=_ex.personal, persistence_state="ACTIVE", retention_state="RETAINED")
            _dd._state.db = "default"
            _dd.full_clean(validate_unique=False, validate_constraints=False)
            _dd.save(using="default", force_insert=True)
    except _IE as err:
        _sql_ra = getattr(getattr(err.__cause__, "diag", None), "constraint_name", None) == "roleassign_uq"
    out["authz_assign_sql_uq_platform"] = bool(_sql_ra and _count(_CRA, role_id=_ra, subject_type="USER", subject_ref=str(_gu), persistence_state="ACTIVE") == 1)
    _subj = _Sel("subject", ("authz-sub",))
    _reso = _Sel("resource", ("authz-res",))
    _acto = _Sel("action", ("authz-act",))
    _scop = _SSel((_plat(),))
    _pol1 = _Pol("pol-authz-1", "z", "owner-p", _Eff.ALLOW, _subj, _reso, _acto, _scop, (), (), None, None, None, None, None, None)
    _pol2 = _Pol("pol-authz-1", "a", "owner-p", _Eff.ALLOW, _subj, _reso, _acto, _scop, (), (), None, None, None, None, None, None)
    _pr1 = _policy_ref("pol-authz-1", "z")
    _ep1 = _mk(_pr1, "pixs.core.authz.policy.persist", n, _plat()); n += 1
    _v1 = _persist(command=_PPI(policy=_pol1, correlation_id=_ep1.correlation_id), envelope=_ep1, ports=_ports(), alias="default")
    _pr2 = _policy_ref("pol-authz-1", "a")
    _ep2 = _mk(_pr2, "pixs.core.authz.policy.persist", n, _plat()); n += 1
    _v2 = _persist(command=_PPI(policy=_pol2, correlation_id=_ep2.correlation_id), envelope=_ep2, ports=_ports(), alias="default")
    from pixs.core.persistence.models_authz import decode_policy as _decpol
    _d1 = _decpol(_CPo.objects.using("default").get(policy_id="pol-authz-1", policy_version="z").definition)
    out["authz_policy_two_versions_ok"] = bool(_v1.version == 1 and _v2.version == 2 and _d1 == _pol1 and _count(_CPo, policy_id="pol-authz-1") == 2)
    _epd = _mk(_pr1, "pixs.core.authz.policy.persist", n, _plat()); n += 1
    _dup_pol = _refuse(lambda: _persist(command=_PPI(policy=_pol1, correlation_id=_epd.correlation_id), envelope=_epd, ports=_ports(), alias="default"), "POLITIQUE_REUTILISEE")
    _sql_pol = False
    try:
        with _tx.atomic(using="default"):
            _bp = _CPo.objects.using("default").get(policy_id="pol-authz-1", policy_version="z")
            _nwt = _dt.datetime.now(_dt.timezone.utc)
            _dp = _CPo(policy_id="pol-authz-1", policy_version="z", owner=_bp.owner, effect=_bp.effect, definition=_bp.definition, version=9, created_at=_nwt, updated_at=_nwt, governance_ref=_bp.governance_ref, confidentiality=_bp.confidentiality, personal=_bp.personal, persistence_state="ARCHIVED", retention_state="RETAINED")
            _dp._state.db = "default"
            _dp.full_clean(validate_unique=False, validate_constraints=False)
            _dp.save(using="default", force_insert=True)
    except _IE as err:
        _sql_pol = getattr(getattr(err.__cause__, "diag", None), "constraint_name", None) == "policy_id_ver_uq"
    out["authz_policy_dup_sql_refuse"] = bool(_dup_pol and _sql_pol)
    _epn = _mk(_policy_ref("pol-authz-x", "v1"), "pixs.core.authz.policy.persist", n, _plat()); n += 1
    _qn = _Pol("pol-authz-x", "v1", "owner-p", _Eff.ALLOW, _subj, _reso, _acto, _scop, (), (), None, None, None, None, None, None)
    out["authz_policy_no_decl_refuse"] = _refuse(lambda: _persist(command=_PPI(policy=_qn, correlation_id=_epn.correlation_id), envelope=_epn, ports=_dc.replace(_ports(), declarations=None), alias="default"), "DECLARATION_ABSENTE") and _count(_CPo, policy_id="pol-authz-x") == 0
    _pc, _rc2, _plc = "perm-authz/cyc", "role-authz/cyc", "pol-authz/cyc"
    _epc = _mk("pixs.core.permission:" + _pc, "pixs.core.authz.permission.declare", n, _plat()); n += 1
    _decl(command=_PDI(permission_id=_pc, owner_component="o", resource_ref="r", action_ref="a", correlation_id=_epc.correlation_id), envelope=_epc, ports=_ports(), alias="default")
    _erc = _mk("pixs.core.role:" + _rc2, "pixs.core.authz.role.create", n, _plat()); n += 1
    _crole(command=_RCI(role_id=_rc2, context=_plat(), permission_ids=(_pc,), correlation_id=_erc.correlation_id, expected_version=None), envelope=_erc, ports=_ports(), alias="default")
    _pqc = _Pol(_plc, "v1", "owner-p", _Eff.ALLOW, _subj, _reso, _acto, _scop, (), (), None, None, None, None, None, None)
    _eqc = _mk(_policy_ref(_plc, "v1"), "pixs.core.authz.policy.persist", n, _plat()); n += 1
    _persist(command=_PPI(policy=_pqc, correlation_id=_eqc.correlation_id), envelope=_eqc, ports=_ports(), alias="default")
    _c1 = _CR.objects.using("default").get(role_id=_rc2)
    _g1 = (_c1.governance_ref, _c1.confidentiality, _c1.personal)
    _s1 = _mk("pixs.core.permission:" + _pc, "pixs.core.authz.state.change", n, _plat()); n += 1
    _r_pm = _chg(command=_LD(resource_ref="pixs.core.permission:" + _pc, target_state=_DPS.ARCHIVED, correlation_id=_s1.correlation_id, expected_version=1), envelope=_s1, ports=_ports(), alias="default")
    _s2 = _mk("pixs.core.role:" + _rc2, "pixs.core.authz.state.change", n, _plat()); n += 1
    _r_rm = _chg(command=_LD(resource_ref="pixs.core.role:" + _rc2, target_state=_DPS.ARCHIVED, correlation_id=_s2.correlation_id, expected_version=1), envelope=_s2, ports=_ports(), alias="default")
    _s3 = _mk(_policy_ref(_plc, "v1"), "pixs.core.authz.state.change", n, _plat()); n += 1
    _r_qm = _chg(command=_LD(resource_ref=_policy_ref(_plc, "v1"), target_state=_DPS.SOFT_DELETED, correlation_id=_s3.correlation_id, expected_version=1), envelope=_s3, ports=_ports(), alias="default")
    out["authz_state_cycle_ok"] = bool(_r_pm.version == 2 and _r_rm.version == 2 and _r_qm.version == 2 and _stage("governance", _s1.operation_id) >= 1 and _stage("governance", _s2.operation_id) >= 1 and _stage("governance", _s3.operation_id) >= 1 and _CR.objects.using("default").filter(role_id=_rc2).count() == 1 and (_CR.objects.using("default").get(role_id=_rc2).governance_ref, _CR.objects.using("default").get(role_id=_rc2).confidentiality, _CR.objects.using("default").get(role_id=_rc2).personal) == _g1)
    _si = _u7()
    _esi = _mk("pixs.core.identity:" + str(_si), "pixs.core.identity.identity.create", n, _plat()); n += 1
    _cident(command=_ICI(identity_id=_si, identity_type=_IT.DEVICE, state=_IS.ACTIVE, correlation_id=_esi.correlation_id), envelope=_esi, ports=_ports(), alias="default")
    _inst, _tga, _tgb = "inst/a-1", "tenant/x-1", "tenant/x-2"
    for _t in (_tga, _tgb):
        _etx = _mk("pixs.core.tenant:" + _t, "pixs.core.scope.tenant.create", n, _plat()); n += 1
        from pixs.core.dto import TenantCreateInput as _TC2
        _ctenant(command=_TC2(tenant_id=_t, correlation_id=_etx.correlation_id), envelope=_etx, ports=_ports(), alias="default")
    _nowb = _dt.datetime.now(_dt.timezone.utc)
    _ident_obj = _CI.objects.using("default").get(identity_id=_si)
    _bind = _SB(installation_ref=_inst, identity=_ident_obj, version=1, created_at=_nowb, updated_at=_nowb, governance_ref=None, confidentiality=None, personal=None, persistence_state="ACTIVE", retention_state="RETAINED")
    _bind._state.db = "default"
    _bind.full_clean(validate_unique=False, validate_constraints=False)
    _bind.save(using="default", force_insert=True)
    _gr = _grant_ref(_inst, _tga)
    _egr0 = _mk(_gr, "pixs.core.authz.super-admin.tenant.grant", n, _plat()); n += 1
    _g1v = _grant(command=_SGI(installation_ref=_inst, tenant_id=_tga, correlation_id=_egr0.correlation_id), envelope=_egr0, ports=_ports(), alias="default")
    _egd = _mk(_gr, "pixs.core.authz.super-admin.tenant.grant", n, _plat()); n += 1
    _dup_g = _refuse(lambda: _grant(command=_SGI(installation_ref=_inst, tenant_id=_tga, correlation_id=_egd.correlation_id), envelope=_egd, ports=_ports(), alias="default"), "GRANT_DEJA_ACTIF")
    _egr1 = _mk(_gr, "pixs.core.authz.super-admin.tenant.revoke", n, _plat()); n += 1
    _rv = _revoke(command=_LD(resource_ref=_gr, target_state=_DPS.SOFT_DELETED, correlation_id=_egr1.correlation_id, expected_version=1), envelope=_egr1, ports=_ports(), alias="default")
    _egr2 = _mk(_gr, "pixs.core.authz.super-admin.tenant.grant", n, _plat()); n += 1
    _g3 = _grant(command=_SGI(installation_ref=_inst, tenant_id=_tga, correlation_id=_egr2.correlation_id), envelope=_egr2, ports=_ports(), alias="default")
    _egr3 = _mk(_gr, "pixs.core.authz.super-admin.tenant.revoke", n, _plat()); n += 1
    _cas_g = _refuse(lambda: _revoke(command=_LD(resource_ref=_gr, target_state=_DPS.SOFT_DELETED, correlation_id=_egr3.correlation_id, expected_version=1), envelope=_egr3, ports=_ports(), alias="default"), "CONFLIT_CAS")
    _no_b = _count(_SG, binding__installation_ref=_inst, tenant__tenant_id=_tgb) == 0
    out["authz_sa_grant_cycle_ok"] = bool(_g1v.version == 1 and _dup_g and _rv.version == 2 and _g3.version == 3 and _cas_g and _no_b)
    _sql_sg = False
    try:
        with _tx.atomic(using="default"):
            _exg = _SG.objects.using("default").get(binding__installation_ref=_inst, tenant__tenant_id=_tga, persistence_state="ACTIVE")
            _nwg = _dt.datetime.now(_dt.timezone.utc)
            _dg = _SG(binding=_exg.binding, tenant=_exg.tenant, version=9, created_at=_nwg, updated_at=_nwg, governance_ref=_exg.governance_ref, confidentiality=_exg.confidentiality, personal=_exg.personal, persistence_state="ACTIVE", retention_state="RETAINED")
            _dg._state.db = "default"
            _dg.full_clean(validate_unique=False, validate_constraints=False)
            _dg.save(using="default", force_insert=True)
    except _IE as err:
        _sql_sg = getattr(getattr(err.__cause__, "diag", None), "constraint_name", None) == "sugrant_bind_tenant_uq"
    out["authz_sa_sql_uq"] = bool(_sql_sg)
    _sv = _u7()
    _esv = _mk("pixs.core.identity:" + str(_sv), "pixs.core.identity.identity.create", n, _plat()); n += 1
    _cident(command=_ICI(identity_id=_sv, identity_type=_IT.SERVICE, state=_IS.ACTIVE, correlation_id=_esv.correlation_id), envelope=_esv, ports=_ports(), alias="default")
    _sobj = _CI.objects.using("default").get(identity_id=_sv)
    _nws = _dt.datetime.now(_dt.timezone.utc)
    _bs = _SB(installation_ref="inst/service-1", identity=_sobj, version=1, created_at=_nws, updated_at=_nws, governance_ref=None, confidentiality=None, personal=None, persistence_state="ACTIVE", retention_state="RETAINED")
    _bs._state.db = "default"
    _bs.full_clean(validate_unique=False, validate_constraints=False)
    _bs.save(using="default", force_insert=True)
    _egs = _mk(_grant_ref("inst/service-1", _tga), "pixs.core.authz.super-admin.tenant.grant", n, _plat()); n += 1
    _srv_ref = _refuse(lambda: _grant(command=_SGI(installation_ref="inst/service-1", tenant_id=_tga, correlation_id=_egs.correlation_id), envelope=_egs, ports=_ports(), alias="default"), "DELEGATION_INTERDITE")
    _egm = _mk(_grant_ref("inst/missing-1", _tga), "pixs.core.authz.super-admin.tenant.grant", n, _plat()); n += 1
    _miss = _refuse(lambda: _grant(command=_SGI(installation_ref="inst/missing-1", tenant_id=_tga, correlation_id=_egm.correlation_id), envelope=_egm, ports=_ports(), alias="default"), "BINDING_ABSENT")
    _egt = _mk(_grant_ref(_inst, _tga), "pixs.core.authz.super-admin.tenant.grant", n, _ten(_tgb)); n += 1
    _wrong = _refuse(lambda: _grant(command=_SGI(installation_ref=_inst, tenant_id=_tga, correlation_id=_egt.correlation_id), envelope=_egt, ports=_ports(), alias="default"), "CONTEXTE_INVALIDE")
    out["authz_sa_guards_refuse"] = bool(_srv_ref and _miss and _wrong)
    _deny_ports = participants.make_ports("default", _ACTOR, {"deny": True})
    _egd2 = _mk(_grant_ref(_inst, _tgb), "pixs.core.authz.super-admin.tenant.grant", n, _plat()); n += 1
    _den = _refuse(lambda: _grant(command=_SGI(installation_ref=_inst, tenant_id=_tgb, correlation_id=_egd2.correlation_id), envelope=_egd2, ports=_deny_ports, alias="default"), "DECISION_REFUSEE")
    with _conns["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s AND detail->>'effect'='DENY'", ["audit", _egd2.operation_id])
        _ad = cur.fetchone()[0] == 1
    out["authz_sa_deny_refuse"] = bool(_den and _ad and _count(_SG, binding__installation_ref=_inst, tenant__tenant_id=_tgb) == 0 and _stage("outbox", _egd2.operation_id) == 0)

    _pactual = _CP.objects.using("default").get(permission_id=pa)
    out["authz_perm_declare_ok"] = out["authz_perm_declare_ok"] and (_pactual.owner, _pactual.resource_ref, _pactual.action_ref) == ("owner-a", "res-a", "act-a") and _stage("declaration", _perm_envs[pa].operation_id) == 1 and _stage("outbox", _perm_envs[pa].operation_id) == 1
    _a_history = list(_CRP.objects.using("default").filter(role_id=_rr, permission_id=pa).order_by("version").values_list("persistence_state", "version"))
    out["authz_role_replace_aba_ok"] = out["authz_role_replace_aba_ok"] and _a_history == [("SOFT_DELETED", 2), ("ACTIVE", 3)] and (_CR.objects.using("default").get(role_id=_rr).governance_ref, _CR.objects.using("default").get(role_id=_rr).confidentiality, _CR.objects.using("default").get(role_id=_rr).personal) == _cls1 and _stage("governance", _e2.operation_id) == 1 and _stage("governance", _e3.operation_id) == 1
    _assignment_history = list(_CRA.objects.using("default").filter(role_id=_ra, subject_type="IDENTITY", subject_ref=str(_su2)).order_by("version"))
    out["authz_assign_reassign_cas_ok"] = out["authz_assign_reassign_cas_ok"] and [(x.persistence_state, x.version) for x in _assignment_history] == [("SOFT_DELETED", 2), ("ACTIVE", 3)] and all((x.governance_ref, x.confidentiality, x.personal) == _cls1 for x in _assignment_history) and _stage("governance", _e22.operation_id) == 1
    _grant_history = list(_SG.objects.using("default").filter(binding__installation_ref=_inst, tenant__tenant_id=_tga).order_by("version"))
    out["authz_sa_grant_cycle_ok"] = out["authz_sa_grant_cycle_ok"] and [(x.persistence_state, x.version) for x in _grant_history] == [("SOFT_DELETED", 2), ("ACTIVE", 3)] and _stage("governance", _egr1.operation_id) == 1 and _count(_SB, installation_ref=_inst) == 1
    _inactive = _SB(installation_ref="inst/inactive-1", identity=_CI.objects.using("default").get(identity_id=_uu2), version=1, created_at=_nowb, updated_at=_nowb, governance_ref=None, confidentiality=None, personal=None, persistence_state="ARCHIVED", retention_state="RETAINED")
    _inactive._state.db = "default"
    _inactive.full_clean(validate_unique=False, validate_constraints=False)
    _inactive.save(using="default", force_insert=True)
    _egi = _mk(_grant_ref("inst/inactive-1", _tga), "pixs.core.authz.super-admin.tenant.grant", n, _plat()); n += 1
    _inactive_refused = _refuse(lambda: _grant(command=_SGI(installation_ref="inst/inactive-1", tenant_id=_tga, correlation_id=_egi.correlation_id), envelope=_egi, ports=_ports(), alias="default"), "BINDING_ABSENT")
    out["authz_sa_guards_refuse"] = out["authz_sa_guards_refuse"] and _inactive_refused and _count(_SG, binding__installation_ref="inst/inactive-1") == 0 and _count(_SG, binding__installation_ref="inst/service-1") == 0
