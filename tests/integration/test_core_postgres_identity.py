"""Recette PG réelle identité Core : schéma jetable, participants synthétiques."""
from __future__ import annotations
import hashlib
import re
__all__ = ["run_real_core_pg_identity"]
_SCHEMA = re.compile(r"c02_[0-9a-f]{16}")
_ACTOR = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"
_SERIALIZER = "1.0.0"
_REQUIRED_CASES = ["user_sans_identity","service_sans_user","rejeu_create_user","idt_group_collision_admise","user_vers_idt_refuse","idt_vers_user_refuse","user_group_refuse","uuid_v4_refuse","lien_cardinalites","db_cardinalites_actives","reference_absente","unlink_relink_cas","set_etat_cas","suppression_logique","fk_protect_liaison","envelope_divergent","mauvais_alias","contention_liaison_reelle","audit_refus_sans_outbox","c10_stage"]
def _envelope(env_digest: str, resource: str, action: str, correlation: str):
    from pixs.core.authz.ports import Request
    from pixs.core.dto import CommandEnvelope
    from pixs.core.scope.context import ScopeContext, ScopeType
    ctx = ScopeContext(ScopeType.PLATFORM, None, None)
    req = Request("synthetic:decision:" + correlation[-8:], _ACTOR, resource, action, ctx, correlation)
    return CommandEnvelope(req, "synthetic:op:" + correlation[-8:], "synthetic:key:" + correlation[-8:], env_digest, _SERIALIZER, correlation, None)
def run_real_core_pg_identity(root_str: str, schema_name: str | None = None) -> dict:
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
                        out["cases"] = _scenarios(support, participants)
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
def _scenarios(support, participants) -> dict:
    import datetime
    import hashlib
    import uuid as uuid_module
    from django.db import connections, transaction
    from django.db.models.deletion import ProtectedError
    from pixs.core.dto import CoreInputInvalid, IdentityCreateIdentityInput, IdentityCreateUserInput, IdentityLinkInput, IdentitySetStateInput, IdentityUnlinkInput, LogicalDeleteInput
    from pixs.core.identity.models import IdentityState, IdentityType
    from pixs.core.persistence.models_group import CoreGroup
    from pixs.core.persistence.models_identity import CoreIdentity, CoreIdentityLink, CoreUser
    from pixs.core.ports import CorePortError
    from pixs.core.services_common import CoreServiceError, lock_scopes as _lock_scopes
    from pixs.core.services_identity import create_identity, create_user, link_identity, logical_delete_identity, set_identity_state, unlink_identity
    from pixs.kernel.data_persistence_states import DataPersistenceState
    out: dict = {}
    def _u7() -> uuid_module.UUID:
        from pixs.core.persistence.uuid7 import generate_uuid7
        return generate_uuid7()
    def _corr(n: int) -> str:
        return "synthetic:idt:%04d" % n
    def _sha(*parts: str) -> str:
        return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    def _mk(ref: str, action: str, n: int):
        c = _corr(n)
        return _envelope(_sha(ref, action, c), ref, action, c)
    def _ports(alias: str = "default"):
        return participants.make_ports(alias, _ACTOR, {})
    def _count(model, **kw) -> int:
        return model.objects.using("default").filter(**kw).count()
    def _stage(kind: str, op: str) -> int:
        with connections["default"].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s;", [kind, op])
            return int(cur.fetchone()[0])
    def _confirmed(op: str) -> bool:
        with connections["default"].cursor() as cur:
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
    def _group_fixture(gid: uuid_module.UUID) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        obj = CoreGroup(group_id=gid, scope_type="PLATFORM", tenant=None, scope=None, version=1, created_at=now, updated_at=now, governance_ref=None, confidentiality=None, personal=None, persistence_state="ACTIVE", retention_state="RETAINED")
        obj.full_clean(validate_unique=False, validate_constraints=False)
        obj.save(using="default", force_insert=True)
    n = 200
    u1 = _u7()
    r_u1 = "pixs.core.user:" + str(u1)
    e_u1 = _mk(r_u1, "pixs.core.identity.user.create", n); n += 1
    res_u1 = create_user(command=IdentityCreateUserInput(user_id=u1, correlation_id=e_u1.correlation_id), envelope=e_u1, ports=_ports(), alias="default")
    out["user_sans_identity"] = res_u1.version == 1 and _count(CoreUser, user_id=u1, persistence_state="ACTIVE") == 1 and _count(CoreIdentityLink, user_id=u1) == 0 and _confirmed(e_u1.operation_id)
    s1 = _u7()
    r_s1 = "pixs.core.identity:" + str(s1)
    e_s1 = _mk(r_s1, "pixs.core.identity.identity.create", n); n += 1
    res_s1 = create_identity(command=IdentityCreateIdentityInput(identity_id=s1, identity_type=IdentityType.SERVICE, state=IdentityState.ACTIVE, correlation_id=e_s1.correlation_id), envelope=e_s1, ports=_ports(), alias="default")
    out["service_sans_user"] = res_s1.version == 1 and _count(CoreIdentity, identity_id=s1, persistence_state="ACTIVE") == 1 and _count(CoreIdentityLink, identity_id=s1) == 0
    g1 = _u7()
    _group_fixture(g1)
    r_g1 = "pixs.core.identity:" + str(g1)
    e_g1 = _mk(r_g1, "pixs.core.identity.identity.create", n); n += 1
    res_g1 = create_identity(command=IdentityCreateIdentityInput(identity_id=g1, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=e_g1.correlation_id), envelope=e_g1, ports=_ports(), alias="default")
    out["idt_group_collision_admise"] = res_g1.version == 1 and _count(CoreGroup, group_id=g1) == 1 and _count(CoreIdentity, identity_id=g1) == 1
    u2 = _u7()
    r_u2 = "pixs.core.user:" + str(u2)
    e2 = _mk(r_u2, "pixs.core.identity.user.create", n); n += 1
    create_user(command=IdentityCreateUserInput(user_id=u2, correlation_id=e2.correlation_id), envelope=e2, ports=_ports(), alias="default")
    r_u2i = "pixs.core.identity:" + str(u2)
    e2b = _mk(r_u2i, "pixs.core.identity.identity.create", n); n += 1
    out["user_vers_idt_refuse"] = _refuse(lambda: create_identity(command=IdentityCreateIdentityInput(identity_id=u2, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=e2b.correlation_id), envelope=e2b, ports=_ports(), alias="default"), "DISJONCTION_USER_IDENTITY") and _count(CoreIdentity, identity_id=u2) == 0
    i2 = _u7()
    r_i2 = "pixs.core.identity:" + str(i2)
    e_i2 = _mk(r_i2, "pixs.core.identity.identity.create", n); n += 1
    create_identity(command=IdentityCreateIdentityInput(identity_id=i2, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=e_i2.correlation_id), envelope=e_i2, ports=_ports(), alias="default")
    r_i2u = "pixs.core.user:" + str(i2)
    e_i2b = _mk(r_i2u, "pixs.core.identity.user.create", n); n += 1
    out["idt_vers_user_refuse"] = _refuse(lambda: create_user(command=IdentityCreateUserInput(user_id=i2, correlation_id=e_i2b.correlation_id), envelope=e_i2b, ports=_ports(), alias="default"), "DISJONCTION_USER_IDENTITY") and _count(CoreUser, user_id=i2) == 0
    g2 = _u7()
    _group_fixture(g2)
    r_g2u = "pixs.core.user:" + str(g2)
    e_g2b = _mk(r_g2u, "pixs.core.identity.user.create", n); n += 1
    out["user_group_refuse"] = _refuse(lambda: create_user(command=IdentityCreateUserInput(user_id=g2, correlation_id=e_g2b.correlation_id), envelope=e_g2b, ports=_ports(), alias="default"), "DISJONCTION_USER_GROUP") and _count(CoreUser, user_id=g2) == 0
    before_users = _count(CoreUser)
    try:
        IdentityCreateUserInput(user_id=uuid_module.uuid4(), correlation_id=_corr(n)); n += 1
        out["uuid_v4_refuse"] = False
    except CoreInputInvalid:
        out["uuid_v4_refuse"] = _count(CoreUser) == before_users
    ua, ia, ib, ub = _u7(), _u7(), _u7(), _u7()
    eu = _mk("pixs.core.user:" + str(ua), "pixs.core.identity.user.create", n); n += 1
    create_user(command=IdentityCreateUserInput(user_id=ua, correlation_id=eu.correlation_id), envelope=eu, ports=_ports(), alias="default")
    for iid in (ia, ib):
        ee = _mk("pixs.core.identity:" + str(iid), "pixs.core.identity.identity.create", n); n += 1
        create_identity(command=IdentityCreateIdentityInput(identity_id=iid, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=ee.correlation_id), envelope=ee, ports=_ports(), alias="default")
    eub = _mk("pixs.core.user:" + str(ub), "pixs.core.identity.user.create", n); n += 1
    create_user(command=IdentityCreateUserInput(user_id=ub, correlation_id=eub.correlation_id), envelope=eub, ports=_ports(), alias="default")
    r1 = "pixs.core.identity-link:" + str(ua) + "/" + str(ia)
    e1 = _mk(r1, "pixs.core.identity.link.create", n); n += 1
    link_identity(command=IdentityLinkInput(user_id=ua, identity_id=ia, correlation_id=e1.correlation_id), envelope=e1, ports=_ports(), alias="default")
    r2 = "pixs.core.identity-link:" + str(ua) + "/" + str(ib)
    e2c = _mk(r2, "pixs.core.identity.link.create", n); n += 1
    r3 = "pixs.core.identity-link:" + str(ub) + "/" + str(ia)
    e3 = _mk(r3, "pixs.core.identity.link.create", n); n += 1
    out["lien_cardinalites"] = _refuse(lambda: link_identity(command=IdentityLinkInput(user_id=ua, identity_id=ib, correlation_id=e2c.correlation_id), envelope=e2c, ports=_ports(), alias="default"), "CARDINALITE_USER") and _refuse(lambda: link_identity(command=IdentityLinkInput(user_id=ub, identity_id=ia, correlation_id=e3.correlation_id), envelope=e3, ports=_ports(), alias="default"), "CARDINALITE_IDENTITY")
    from django.db import IntegrityError, transaction as _tx2
    import datetime as _dt2
    now2 = _dt2.datetime.now(_dt2.timezone.utc)
    base_link = CoreIdentityLink.objects.using("default").get(user_id=ua, identity_id=ia, persistence_state="ACTIVE")
    gov2 = (base_link.governance_ref, base_link.confidentiality, base_link.personal)
    fk_ok = _count(CoreUser, user_id=ua, persistence_state="ACTIVE") == 1 and _count(CoreUser, user_id=ub, persistence_state="ACTIVE") == 1 and _count(CoreIdentity, identity_id=ia, persistence_state="ACTIVE") == 1 and _count(CoreIdentity, identity_id=ib, persistence_state="ACTIVE") == 1
    db_user_ok = False
    try:
        with _tx2.atomic(using="default"):
            obj1 = CoreIdentityLink(user_id=ua, identity_id=ib, version=1, created_at=now2, updated_at=now2, governance_ref=gov2[0], confidentiality=gov2[1], personal=gov2[2], persistence_state="ACTIVE", retention_state="RETAINED")
            obj1.full_clean(validate_unique=False, validate_constraints=False)
            obj1.save(using="default", force_insert=True)
    except IntegrityError as error:
        db_user_ok = getattr(getattr(error.__cause__, "diag", None), "constraint_name", None) == "idlink_user_uq"
    db_idt_ok = False
    try:
        with _tx2.atomic(using="default"):
            obj2 = CoreIdentityLink(user_id=ub, identity_id=ia, version=1, created_at=now2, updated_at=now2, governance_ref=gov2[0], confidentiality=gov2[1], personal=gov2[2], persistence_state="ACTIVE", retention_state="RETAINED")
            obj2.full_clean(validate_unique=False, validate_constraints=False)
            obj2.save(using="default", force_insert=True)
    except IntegrityError as error:
        db_idt_ok = getattr(getattr(error.__cause__, "diag", None), "constraint_name", None) == "idlink_idt_uq"
    out["db_cardinalites_actives"] = bool(db_user_ok and db_idt_ok and fk_ok and _count(CoreIdentityLink, user_id=ua, identity_id=ia, persistence_state="ACTIVE") == 1 and _count(CoreIdentityLink, user_id=ua, persistence_state="ACTIVE") == 1)
    ux, ix = _u7(), _u7()
    rx = "pixs.core.identity-link:" + str(ux) + "/" + str(ix)
    ex = _mk(rx, "pixs.core.identity.link.create", n); n += 1
    out["reference_absente"] = _refuse(lambda: link_identity(command=IdentityLinkInput(user_id=ux, identity_id=ix, correlation_id=ex.correlation_id), envelope=ex, ports=_ports(), alias="default"), "REFERENCE_ABSENTE")
    uh, ih = _u7(), _u7()
    euh = _mk("pixs.core.user:" + str(uh), "pixs.core.identity.user.create", n); n += 1
    create_user(command=IdentityCreateUserInput(user_id=uh, correlation_id=euh.correlation_id), envelope=euh, ports=_ports(), alias="default")
    eih = _mk("pixs.core.identity:" + str(ih), "pixs.core.identity.identity.create", n); n += 1
    create_identity(command=IdentityCreateIdentityInput(identity_id=ih, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=eih.correlation_id), envelope=eih, ports=_ports(), alias="default")
    rh = "pixs.core.identity-link:" + str(uh) + "/" + str(ih)
    eh1 = _mk(rh, "pixs.core.identity.link.create", n); n += 1
    r_first = link_identity(command=IdentityLinkInput(user_id=uh, identity_id=ih, correlation_id=eh1.correlation_id), envelope=eh1, ports=_ports(), alias="default")
    eh2 = _mk(rh, "pixs.core.identity.link.unlink", n); n += 1
    unlink_identity(command=IdentityUnlinkInput(user_id=uh, identity_id=ih, correlation_id=eh2.correlation_id, expected_version=r_first.version), envelope=eh2, ports=_ports(), alias="default")
    rows = list(CoreIdentityLink.objects.using("default").filter(user_id=uh, identity_id=ih).order_by("version"))
    eh3 = _mk(rh, "pixs.core.identity.link.create", n); n += 1
    r_third = link_identity(command=IdentityLinkInput(user_id=uh, identity_id=ih, correlation_id=eh3.correlation_id), envelope=eh3, ports=_ports(), alias="default")
    rows2 = list(CoreIdentityLink.objects.using("default").filter(user_id=uh, identity_id=ih).order_by("version"))
    eh_bad = _mk(rh, "pixs.core.identity.link.unlink", n); n += 1
    cas_old = _refuse(lambda: unlink_identity(command=IdentityUnlinkInput(user_id=uh, identity_id=ih, correlation_id=eh_bad.correlation_id, expected_version=1), envelope=eh_bad, ports=_ports(), alias="default"), "CONFLIT_CAS")
    states_ok = len(rows2) == 2 and rows2[0].persistence_state == "SOFT_DELETED" and rows2[0].version == 2 and rows2[1].persistence_state == "ACTIVE" and rows2[1].version == 3
    c10_ok = _stage("governance", eh2.operation_id) >= 1
    out["unlink_relink_cas"] = len(rows) == 1 and cas_old and states_ok and c10_ok and r_third.version == 3
    ise = _u7()
    r_ise = "pixs.core.identity:" + str(ise)
    eise = _mk(r_ise, "pixs.core.identity.identity.create", n); n += 1
    r0 = create_identity(command=IdentityCreateIdentityInput(identity_id=ise, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=eise.correlation_id), envelope=eise, ports=_ports(), alias="default")
    e2s = _mk(r_ise, "pixs.core.identity.state.set", n); n += 1
    r1s = set_identity_state(command=IdentitySetStateInput(identity_id=ise, state=IdentityState.SUSPENDED, correlation_id=e2s.correlation_id, expected_version=r0.version), envelope=e2s, ports=_ports(), alias="default")
    e3s = _mk(r_ise, "pixs.core.identity.state.set", n); n += 1
    out["set_etat_cas"] = r1s.version == 2 and _refuse(lambda: set_identity_state(command=IdentitySetStateInput(identity_id=ise, state=IdentityState.REVOKED, correlation_id=e3s.correlation_id, expected_version=r0.version), envelope=e3s, ports=_ports(), alias="default"), "CONFLIT_CAS")
    ul = _u7()
    r_ul = "pixs.core.user:" + str(ul)
    eul = _mk(r_ul, "pixs.core.identity.user.create", n); n += 1
    r0l = create_user(command=IdentityCreateUserInput(user_id=ul, correlation_id=eul.correlation_id), envelope=eul, ports=_ports(), alias="default")
    row0 = CoreUser.objects.using("default").get(user_id=ul)
    gov0 = (row0.governance_ref, row0.confidentiality, row0.personal)
    ed = _mk(r_ul, "pixs.core.identity.logical_delete", n); n += 1
    rd = logical_delete_identity(command=LogicalDeleteInput(resource_ref=r_ul, target_state=DataPersistenceState.ARCHIVED, correlation_id=ed.correlation_id, expected_version=r0l.version), envelope=ed, ports=_ports(), alias="default")
    row1 = CoreUser.objects.using("default").get(user_id=ul)
    ed2 = _mk(r_ul, "pixs.core.identity.user.create", n); n += 1
    reuse = _refuse(lambda: create_user(command=IdentityCreateUserInput(user_id=ul, correlation_id=ed2.correlation_id), envelope=ed2, ports=_ports(), alias="default"), "UUID_REUTILISE")
    out["suppression_logique"] = rd.persistence_state == DataPersistenceState.ARCHIVED and row1.version == 2 and (row1.governance_ref, row1.confidentiality, row1.personal) == gov0 and reuse and _stage("governance", ed.operation_id) >= 1
    from unittest.mock import patch
    user_ports = _ports()
    ed3 = _mk(r_ul, "pixs.core.identity.logical_delete", n); n += 1
    with patch.object(user_ports.governance, "authorize_state_change", wraps=user_ports.governance.authorize_state_change) as user_transition:
        rsoft = logical_delete_identity(command=LogicalDeleteInput(resource_ref=r_ul, target_state=DataPersistenceState.SOFT_DELETED, correlation_id=ed3.correlation_id, expected_version=rd.version), envelope=ed3, ports=user_ports, alias="default")
    user_current = user_transition.call_count == 1 and user_transition.call_args.kwargs["current_state"] == "ARCHIVED"
    row_soft = CoreUser.objects.using("default").get(user_id=ul)
    ei_arch = _mk(r_ise, "pixs.core.identity.logical_delete", n); n += 1
    ri_arch = logical_delete_identity(command=LogicalDeleteInput(resource_ref=r_ise, target_state=DataPersistenceState.ARCHIVED, correlation_id=ei_arch.correlation_id, expected_version=r1s.version), envelope=ei_arch, ports=_ports(), alias="default")
    id_before_soft = CoreIdentity.objects.using("default").get(identity_id=ise)
    id_governance = (id_before_soft.governance_ref, id_before_soft.confidentiality, id_before_soft.personal)
    identity_ports = _ports()
    ei_soft = _mk(r_ise, "pixs.core.identity.logical_delete", n); n += 1
    with patch.object(identity_ports.governance, "authorize_state_change", wraps=identity_ports.governance.authorize_state_change) as identity_transition:
        ri_soft = logical_delete_identity(command=LogicalDeleteInput(resource_ref=r_ise, target_state=DataPersistenceState.SOFT_DELETED, correlation_id=ei_soft.correlation_id, expected_version=ri_arch.version), envelope=ei_soft, ports=identity_ports, alias="default")
    id_current = identity_transition.call_count == 1 and identity_transition.call_args.kwargs["current_state"] == "ARCHIVED"
    id_after_soft = CoreIdentity.objects.using("default").get(identity_id=ise)
    no_restore_env = _mk(r_ul, "pixs.core.identity.logical_delete", n); n += 1
    no_restore = _refuse(lambda: logical_delete_identity(command=LogicalDeleteInput(resource_ref=r_ul, target_state=DataPersistenceState.ARCHIVED, correlation_id=no_restore_env.correlation_id, expected_version=rsoft.version), envelope=no_restore_env, ports=_ports(), alias="default"), "REFERENCE_ABSENTE")
    out["suppression_logique"] = bool(out["suppression_logique"] and rsoft.version == 3 and row_soft.persistence_state == "SOFT_DELETED" and (row_soft.governance_ref, row_soft.confidentiality, row_soft.personal) == gov0 and user_current and ri_soft.version == 4 and id_after_soft.persistence_state == "SOFT_DELETED" and id_after_soft.state == IdentityState.SUSPENDED.value and (id_after_soft.governance_ref, id_after_soft.confidentiality, id_after_soft.personal) == id_governance and id_current and no_restore)
    uf = _u7()
    inf = _u7()
    euf = _mk("pixs.core.user:" + str(uf), "pixs.core.identity.user.create", n); n += 1
    create_user(command=IdentityCreateUserInput(user_id=uf, correlation_id=euf.correlation_id), envelope=euf, ports=_ports(), alias="default")
    eif = _mk("pixs.core.identity:" + str(inf), "pixs.core.identity.identity.create", n); n += 1
    create_identity(command=IdentityCreateIdentityInput(identity_id=inf, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=eif.correlation_id), envelope=eif, ports=_ports(), alias="default")
    rf = "pixs.core.identity-link:" + str(uf) + "/" + str(inf)
    ef = _mk(rf, "pixs.core.identity.link.create", n); n += 1
    link_identity(command=IdentityLinkInput(user_id=uf, identity_id=inf, correlation_id=ef.correlation_id), envelope=ef, ports=_ports(), alias="default")
    fk_ok = False
    try:
        with transaction.atomic(using="default"):
            CoreUser.objects.using("default").get(user_id=uf).delete()
    except ProtectedError:
        fk_ok = True
    except (CoreServiceError, CorePortError):
        fk_ok = False
    out["fk_protect_liaison"] = fk_ok and _count(CoreUser, user_id=uf) == 1 and _count(CoreIdentityLink, user_id=uf, persistence_state="ACTIVE") == 1
    t_res = _u7()
    ref_res = "pixs.core.user:" + str(t_res)
    c_res = _corr(n); n += 1
    env_bad_res = _envelope(_sha(ref_res, "pixs.core.identity.user.create", c_res), "pixs.core.user:bad", "pixs.core.identity.user.create", c_res)
    cmd_res = IdentityCreateUserInput(user_id=t_res, correlation_id=c_res)
    res_div = _refuse(lambda: create_user(command=cmd_res, envelope=env_bad_res, ports=_ports(), alias="default"), "RESSOURCE_DIVERGENTE")
    cnt_res = _count(CoreUser, user_id=t_res) == 0
    t_act = _u7()
    ref_act = "pixs.core.user:" + str(t_act)
    c_act = _corr(n); n += 1
    env_bad_act = _envelope(_sha(ref_act, "pixs.core.identity.user.create.bad", c_act), ref_act, "pixs.core.identity.user.create.bad", c_act)
    cmd_act = IdentityCreateUserInput(user_id=t_act, correlation_id=c_act)
    act_div = _refuse(lambda: create_user(command=cmd_act, envelope=env_bad_act, ports=_ports(), alias="default"), "ACTION_DIVERGENTE")
    cnt_act = _count(CoreUser, user_id=t_act) == 0
    out["envelope_divergent"] = res_div and cnt_res and act_div and cnt_act
    t_bad = _u7()
    r_bad = "pixs.core.user:" + str(t_bad)
    c_bad = _corr(n); n += 1
    env_bad = _envelope(_sha(r_bad, "pixs.core.identity.user.create", c_bad), r_bad, "pixs.core.identity.user.create", c_bad)
    cmd_bad = IdentityCreateUserInput(user_id=t_bad, correlation_id=c_bad)
    out["mauvais_alias"] = _refuse(lambda: create_user(command=cmd_bad, envelope=env_bad, ports=_ports(), alias="bad"), "ALIAS_INCONNU") and _count(CoreUser, user_id=t_bad) == 0
    up = _u7()
    r_up = "pixs.core.user:" + str(up)
    ep = _mk(r_up, "pixs.core.identity.user.create", n); n += 1
    create_user(command=IdentityCreateUserInput(user_id=up, correlation_id=ep.correlation_id), envelope=ep, ports=participants.make_ports("peer", _ACTOR, {}), alias="peer")
    out["mauvais_alias"] = bool(out["mauvais_alias"]) and _count(CoreUser, user_id=up) == 0 and CoreUser.objects.using("peer").filter(user_id=up).count() == 1
    uc, ic1, ic2 = _u7(), _u7(), _u7()
    euc = _mk("pixs.core.user:" + str(uc), "pixs.core.identity.user.create", n); n += 1
    create_user(command=IdentityCreateUserInput(user_id=uc, correlation_id=euc.correlation_id), envelope=euc, ports=_ports(), alias="default")
    for iid in (ic1, ic2):
        ee = _mk("pixs.core.identity:" + str(iid), "pixs.core.identity.identity.create", n); n += 1
        create_identity(command=IdentityCreateIdentityInput(identity_id=iid, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id=ee.correlation_id), envelope=ee, ports=_ports(), alias="default")
    lock_held_ok = False
    with transaction.atomic(using="contender", durable=True):
        _lock_scopes("contender", ("uuid:" + uc.hex,))
        rr = "pixs.core.identity-link:" + str(uc) + "/" + str(ic1)
        ee = _mk(rr, "pixs.core.identity.link.create", n); n += 1
        lock_held_ok = _refuse(lambda: link_identity(command=IdentityLinkInput(user_id=uc, identity_id=ic1, correlation_id=ee.correlation_id), envelope=ee, ports=_ports(), alias="default"), "VERROU_CONCURRENT") and _count(CoreIdentityLink, user_id=uc) == 0
    rr1 = "pixs.core.identity-link:" + str(uc) + "/" + str(ic1)
    ee1 = _mk(rr1, "pixs.core.identity.link.create", n); n += 1
    link_identity(command=IdentityLinkInput(user_id=uc, identity_id=ic1, correlation_id=ee1.correlation_id), envelope=ee1, ports=_ports(), alias="default")
    rr2 = "pixs.core.identity-link:" + str(uc) + "/" + str(ic2)
    ee2 = _mk(rr2, "pixs.core.identity.link.create", n); n += 1
    second_refused = _refuse(lambda: link_identity(command=IdentityLinkInput(user_id=uc, identity_id=ic2, correlation_id=ee2.correlation_id), envelope=ee2, ports=_ports(), alias="default"), "CARDINALITE_USER")
    out["contention_liaison_reelle"] = lock_held_ok and second_refused and _count(CoreIdentityLink, user_id=uc, persistence_state="ACTIVE") == 1
    rc = "pixs.core.identity-link:" + str(ua) + "/" + str(ib)
    ec = _mk(rc, "pixs.core.identity.link.create", n); n += 1
    before_out = _stage("outbox", ec.operation_id)
    refused = _refuse(lambda: link_identity(command=IdentityLinkInput(user_id=ua, identity_id=ib, correlation_id=ec.correlation_id), envelope=ec, ports=_ports(), alias="default"), "CARDINALITE_USER")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s AND detail->>'effect'='DENY'", ["audit", ec.operation_id])
        aud = cur.fetchone()[0] == 1
    out["audit_refus_sans_outbox"] = refused and aud and _stage("outbox", ec.operation_id) == before_out
    out["c10_stage"] = _stage("governance", eh2.operation_id) >= 1 and _stage("governance", ed.operation_id) >= 1
    res_replay = create_user(command=IdentityCreateUserInput(user_id=u1, correlation_id=e_u1.correlation_id), envelope=e_u1, ports=_ports(), alias="default")
    out["rejeu_create_user"] = bool(res_replay == res_u1 and _count(CoreUser, user_id=u1) == 1 and _stage("outbox", e_u1.operation_id) == 1 and _confirmed(e_u1.operation_id))
    return out
