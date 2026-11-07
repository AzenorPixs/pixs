"""Helper worker frais : ouvre schema parent existant, sans reconfiguration C03."""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
import datetime, os, stat
EXPECTED_ROOT = "/home/devops/datas/pixs"
ARTIFACT_BASE = Path(EXPECTED_ROOT) / "output" / "tests" / "c08-modes"
__all__ = ["open_existing"]
class _LiveClock:
    def now(self):
        return datetime.datetime.now(datetime.timezone.utc)
def _req_str(v, lim=256):
    if type(v) is not str or not 0 < len(v) <= lim or not v.isprintable():
        raise AssertionError("RECIPE_INVALID")
def _req_oid(v):
    if type(v) is not int or type(v) is bool or not 1 <= v <= 2**32 - 1:
        raise AssertionError("RECIPE_INVALID")
def _strict_under(base_resolved, cand):
    import os as _os
    _req_str(cand, 4096)
    c = Path(cand)
    if not c.is_absolute():
        raise AssertionError("RECIPE_INVALID")
    if c.is_symlink():
        raise AssertionError("RECIPE_INVALID")
    for part in [c, *c.parents]:
        if part.is_symlink():
            raise AssertionError("RECIPE_INVALID")
    cr = c.resolve()
    if (str(c) != str(cr) or cr == base_resolved
            or _os.path.commonpath([str(base_resolved), str(cr)]) != str(base_resolved)):
        raise AssertionError("RECIPE_INVALID")
    return cr
@contextmanager
def open_existing(recipe):
    import re
    if type(recipe) is not dict:
        raise AssertionError("RECIPE_INVALID")
    expected = {"root_str", "namespace", "schema_oid", "db_oid", "owner_oid", "artifact_dir", "tmpdir", "marker_paths", "mode_cfg", "meta_cfg", "installations", "actor_ref", "profile_id", "database_target_ref", "scope"}
    if set(recipe) != expected:
        raise AssertionError("RECIPE_INVALID")
    for k in ("root_str", "namespace", "artifact_dir", "tmpdir", "actor_ref", "profile_id", "database_target_ref"):
        _req_str(recipe[k])
    if recipe["scope"] != "PLATFORM":
        raise AssertionError("RECIPE_INVALID")
    if recipe["root_str"] != EXPECTED_ROOT:
        raise AssertionError("ROOT_INVALID")
    if re.fullmatch(r"c08_[0-9a-f]{16}", recipe["namespace"]) is None:
        raise AssertionError("RECIPE_INVALID")
    for k in ("schema_oid", "db_oid", "owner_oid"):
        _req_oid(recipe[k])
    if recipe["artifact_dir"] != str(ARTIFACT_BASE):
        raise AssertionError("RECIPE_INVALID")
    tdir = Path(recipe["tmpdir"])
    if not tdir.is_absolute():
        raise AssertionError("RECIPE_INVALID")
    base = ARTIFACT_BASE.resolve()
    tr = _strict_under(base, recipe["tmpdir"])
    if not tr.is_dir():
        raise AssertionError("RECIPE_INVALID")
    st = tr.stat()
    if st.st_uid != os.getuid() or st.st_gid != os.getgid() or stat.S_IMODE(st.st_mode) != 0o700:
        raise AssertionError("RECIPE_INVALID")
    insts = recipe["installations"]
    if type(insts) is not list or len(insts) != 2:
        raise AssertionError("RECIPE_INVALID")
    for i in insts:
        _req_str(i)
    if insts[0] == insts[1]:
        raise AssertionError("RECIPE_INVALID")
    mp = recipe["marker_paths"]
    if type(mp) is not dict or set(mp) != set(insts):
        raise AssertionError("RECIPE_INVALID")
    for inst in insts:
        _req_str(mp[inst])
        _strict_under(tr, mp[inst])
    for key in ("mode_cfg", "meta_cfg"):
        d = recipe[key]
        if type(d) is not dict:
            raise AssertionError("RECIPE_INVALID")
        if set(d) != {"catalog_path", "guard_path", "owner_uid", "owner_gid", "parent_identities", "max_bytes", "max_ref_len", "max_profiles", "max_refs", "max_ttl_seconds", "max_freshness_seconds", "lock_timeout_ms", "retry_interval_ms", "expected_catalog_version", "expected_publication_ref", "expected_sha256", "binding"}:
            raise AssertionError("RECIPE_INVALID")
        b = d["binding"]
        if type(b) is not dict or set(b) != {"profile_ref", "data_asset_id", "owner_component", "source_of_truth", "profile_version"}:
            raise AssertionError("RECIPE_INVALID")
        for f in ("catalog_path", "guard_path", "expected_catalog_version", "expected_publication_ref", "expected_sha256"):
            _req_str(d[f])
        for f in ("owner_uid", "owner_gid", "max_bytes", "max_ref_len", "max_profiles", "max_refs", "max_ttl_seconds", "max_freshness_seconds", "lock_timeout_ms", "retry_interval_ms"):
            v = d[f]
            if type(v) is not int or type(v) is bool or v < 0 or v > 2**63 - 1:
                raise AssertionError("RECIPE_INVALID")
        for f in ("max_bytes", "max_ref_len", "max_profiles", "max_refs", "max_ttl_seconds", "max_freshness_seconds", "retry_interval_ms"):
            if d[f] < 1:
                raise AssertionError("RECIPE_INVALID")
        for f in ("profile_ref", "data_asset_id", "owner_component", "source_of_truth", "profile_version"):
            _req_str(b[f])
        _strict_under(tr, d["catalog_path"])
        _strict_under(tr, d["guard_path"])
    from django.conf import settings as dj_settings
    if dj_settings.configured:
        raise AssertionError("SETTINGS_PREEXISTING")
    from psycopg import sql as pg_sql
    import core_pg_test_support as core
    quoted = pg_sql.Identifier(recipe["namespace"]).as_string()
    options = core.pg_options(search_path_quoted=quoted)
    with core.mask_output():
        refs, failures = [], []
        configured = False
        try:
            env = core.read_project_env(recipe["root_str"])
            if env is None:
                raise AssertionError("ENV_INVALID")
            databases = {a: {"ENGINE": "django.db.backends.postgresql", "NAME": env["PG_DATABASE"], "USER": env["PG_USERNAME"], "PASSWORD": env["PG_PASSWORD"], "HOST": env["PG_HOST"], "PORT": env["PG_PORT"], "OPTIONS": {"options": options, "connect_timeout": 2}, "CONN_MAX_AGE": 0, "ATOMIC_REQUESTS": False, "AUTOCOMMIT": True} for a in ("default", "peer", "contender")}
            from pixs.auth.apps import DJANGO_REQUIRED_APPS
            dj_settings.configure(INSTALLED_APPS=DJANGO_REQUIRED_APPS + ("pixs.backend.apps.PixsCoreConfig", "pixs.backend.apps.PixsBackendConfig"), DATABASES=databases, USE_TZ=True, TIME_ZONE="UTC", LOGGING_CONFIG=None)
            configured = True
            import django
            django.setup()
            from django.db import connections
            from pixs.core.scope.context import ScopeContext, ScopeType
            from pixs.core.authz.snapshot import Catalog, Limits
            from pixs.core.authz.filter_plan import FilterConfig
            from pixs.core.services_runtime_store import CoreAuthorizationStore
            from pixs.core.query_source import CoreFactSource
            from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
            from pixs.core.audit_sink import PostgresAuditParticipant
            from pixs.auth.configuration import create_local_auth_sources
            from pixs.auth.runtime_verifier import prepare_password_verifier
            from pixs.auth.invocation import AuthInvocationSource
            from pixs.auth.policy import SessionCategory
            from pixs.backend.installation.mode_commands import ModeCommandInput, MODE_SERIALIZER_VERSION, mode_resource_ref, mode_action_ref, mode_content_sha256
            from pixs.core.dto import CommandEnvelope
            from pixs.core.authz.ports import Request as C04Request
            from pixs.backend.installation.marker import MarkerConfig
            from pixs.backend.installation.mode_reader import C08InstalledModeReader
            from pixs.backend.c10_catalog import C10Catalog, CatalogConfig, ProfileBinding
            from pixs.backend.installation.mode_governance import C10ModeGovernanceAdapter
            from pixs.backend.installation.mode_service import execute_mode
            from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
            clock = _LiveClock()
            context = ScopeContext(ScopeType.PLATFORM)
            conn = connections["default"]
            with conn.cursor() as cur:
                cur.execute("SELECT current_schema(),current_schemas(false),current_setting('server_version_num'),(SELECT oid FROM pg_namespace WHERE nspname=current_schema()),(SELECT oid FROM pg_database WHERE datname=current_database()),(SELECT nspowner FROM pg_namespace WHERE nspname=current_schema())")
                s2, p2, ver, o2, dbo2, ow2 = cur.fetchone()
                if type(ver) is not str or re.fullmatch(r"[0-9]+", ver) is None:
                    raise AssertionError("VERSION_UNPROVED")
                if s2 != recipe["namespace"] or list(p2) != [recipe["namespace"]] or o2 != recipe["schema_oid"] or dbo2 != recipe["db_oid"] or ow2 != recipe["owner_oid"]:
                    raise AssertionError("NAMESPACE_UNPROVED")
            def _mk_cfg(d):
                b = d["binding"]
                return CatalogConfig(d["catalog_path"], d["guard_path"], d["owner_uid"], d["owner_gid"], tuple(tuple(p) for p in d["parent_identities"]), d["max_bytes"], d["max_ref_len"], d["max_profiles"], d["max_refs"], d["max_ttl_seconds"], d["max_freshness_seconds"], d["lock_timeout_ms"], d["retry_interval_ms"], d["expected_catalog_version"], d["expected_publication_ref"], d["expected_sha256"], ProfileBinding(b["profile_ref"], b["data_asset_id"], b["owner_component"], b["source_of_truth"], b["profile_version"]))
            mode_cfg = _mk_cfg(recipe["mode_cfg"])
            meta_cfg = _mk_cfg(recipe["meta_cfg"])
            trust, assurance = create_local_auth_sources(alias="default", profile_id=recipe["profile_id"], clock=clock)
            profile = trust.current_profile(context)
            password_a = "Vecteur public configuration C03, aucun secret réel"
            got = {}
            from pixs.core.persistence.models_identity import CoreSuperAdminBinding
            from pixs.auth.identifiers import identity_reference
            for inst in insts:
                b = CoreSuperAdminBinding.objects.using("default").filter(installation_ref=inst).first()
                if b is None:
                    raise AssertionError("BINDING_ABSENT")
                got[inst] = identity_reference(b.identity_id)
            subjects = tuple(sorted(set([recipe["actor_ref"]] + list(got.values()))))
            res = {i: "pixs.backend.modes:" + i for i in insts}
            acts = ("pixs.backend.modes.finalize", "pixs.backend.modes.enter_maintenance", "pixs.backend.modes.exit_maintenance")
            stores, readers = {}, {}
            for inst in insts:
                cat = Catalog(subjects, (res[insts[0]], res[insts[1]]), acts, (context,), ())
                lim = Limits(128, 128, 10, 20, 20, 128, 256, 256, 100000000, 60, 3600)
                stores[inst] = CoreAuthorizationStore(alias="default", installation_ref=inst, base_epoch="c08-test-epoch-v1", catalog=cat, limits=lim)
                mp2 = recipe["marker_paths"][inst]
                readers[inst] = C08InstalledModeReader(using="default", inspection_using="peer", marker_config=MarkerConfig(path=mp2, owner_uid=os.getuid(), owner_gid=os.getgid(), max_bytes=4096, max_ref_len=256, allowed_format_versions=("1.0.0",), parent_identities=tuple(tuple(p) for p in recipe["mode_cfg"]["parent_identities"])), installation_ref=inst, database_target_ref=recipe["database_target_ref"], clock=clock)
            audit = PostgresAuditParticipant(ExplicitAuditPolicySource(context, AuditPolicy("c08-test-audit", "1.0.0", "TEST_ONLY", 1, 65536, 50, (), "c08-test-audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)), clock, "peer")
            filt = FilterConfig(10)
            mode_cat = C10Catalog(mode_cfg, now=clock.now)
            meta_cat = C10Catalog(meta_cfg, now=clock.now)
            def invoke(role, kind, expected, key, operation_id, correlation_id):
                if role not in ("root", "ordinary"):
                    raise AssertionError("ROLE_INVALID")
                inst = insts[0] if role == "root" else insts[1]
                cmd = ModeCommandInput(installation_ref=inst, actor_ref=recipe["actor_ref"], kind=kind, expected_version=expected, idempotency_key=key)
                req = C04Request("decision:" + operation_id, recipe["actor_ref"], mode_resource_ref(cmd, max_ref_len=256), mode_action_ref(kind), context, correlation_id)
                env = CommandEnvelope(req, operation_id, key, mode_content_sha256(cmd, max_ref_len=256), MODE_SERIALIZER_VERSION, correlation_id, None)
                verifier = prepare_password_verifier(request=req, alias="default", operation_id=operation_id, profile=profile, trust_source=trust, assurance_source=assurance, facts_reader=CoreFactSource(), clock=clock, external_subject="initial-subject", password=password_a, category=SessionCategory.ORDINARY)
                src = AuthInvocationSource(verifier)
                try:
                    with mode_cat.guard() as ml, meta_cat.guard() as el:
                        gov = C10ModeGovernanceAdapter(using="default", installation_ref=inst, mode_lease=ml, metadata_lease=el, clock=clock)
                        return execute_mode(using="default", inspection_using="peer", clock=clock, envelope=env, command=cmd, reader=readers[inst], store=stores[inst], authentication_source=src, audit=audit, filter_config=filt, governance=gov, waiver_request=None)
                finally:
                    src.close()
            def owner_physical():
                return connections["default"].connection
            def native_ro():
                with connections["peer"].cursor() as cur:
                    cur.execute("SELECT pg_backend_pid(),pg_current_xact_id()::text")
                    return cur.fetchone()
            yield {"context": context, "clock": clock, "stores": stores, "readers": readers, "audit": audit, "filter_config": filt, "invoke": invoke, "owner_physical": owner_physical, "native_ro": native_ro, "test_only": "TEST_ONLY", "pg_version_num": ver}
        finally:
            if configured:
                core.close_django_connections(refs, failures)
            if failures or any(not c.closed for c in refs):
                raise AssertionError("WORKER_CLEANUP_UNPROVED")
