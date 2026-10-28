"""Fixture MODES TEST_ONLY, deux installations et un seul sujet C03 A.

A est Super Admin dans ROOT_INST et ordinaire dans ORD_INST, dont le binding
vise une identite B preparee sans credential C03. Ces donnees ne qualifient
ni enrollement C03 ordinaire, ni R01, PA, PZT, UTC natif ou C09. Les lignes
C08 initiales ont des metadonnees TEST_ONLY structurelles ; leur hash de
catalogue prepare ne prouve pas une attestation initiale C10 ou un commit
R01. Les operations testees utiliseront ensuite les vrais profils du TOML.
Le marqueur
est uniquement une preparation structurelle. Aucun scenario ne tourne a
l'import ; tous les fichiers de fixture restent sous la racine du projet.
"""
from __future__ import annotations
from contextlib import contextmanager, ExitStack
from pathlib import Path
import datetime, hashlib, json, os, tempfile
EXPECTED_ROOT = "/home/devops/datas/pixs"
ARTIFACT_REL = Path("output") / "tests" / "c08-modes"
TEST_ONLY = "TEST_ONLY"
ROOT_INST = "c08-test-modes-root-001"
ORD_INST = "c08-test-modes-ordinary-001"
DB_TARGET = "c08-test-target-001"
__all__ = ["make_modes_fixture", "EXPECTED_ROOT", "ARTIFACT_REL", "ROOT_INST", "ORD_INST"]

class _SharedClock:
    def __init__(self, offset_seconds=0):
        self._offset = offset_seconds
    def now(self):
        return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=self._offset)

def _all_parents(path_str):
    p = Path(path_str)
    chain = [p, *p.parents]
    out = []
    for q in chain:
        st = q.stat()
        out.append((st.st_uid, st.st_gid))
    return tuple(dict.fromkeys(out))

def _iso_z(v):
    return v.astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

@contextmanager
def make_modes_fixture(root_str):
    from django.db import transaction, connections
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.identity.models import IdentityType, IdentityState
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.persistence.models_identity import CoreIdentity, CoreSuperAdminBinding
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.authz.policy import Policy, Selector, ScopeSelector, Effect, Obligation
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
    from pixs.auth.identifiers import identity_reference
    from pixs.backend.installation.mode_values import ModeOperationKind
    from pixs.backend.installation.mode_commands import ModeCommandInput, MODE_SERIALIZER_VERSION, mode_resource_ref, mode_action_ref, mode_content_sha256
    from pixs.core.dto import CommandEnvelope
    from pixs.core.authz.ports import Request as C04Request
    from pixs.backend.installation.marker import MarkerConfig
    from pixs.backend.installation.mode_reader import C08InstalledModeReader
    from pixs.backend.c10_catalog import C10Catalog, CatalogConfig, ProfileBinding
    from pixs.backend.installation.mode_governance import C10ModeGovernanceAdapter
    from pixs.backend.installation.mode_service import execute_mode
    if str(Path(root_str).resolve()) != EXPECTED_ROOT:
        raise AssertionError("ROOT_INVALID")
    artifact = Path(root_str) / ARTIFACT_REL
    artifact.mkdir(parents=True, exist_ok=True)
    from test_auth_configuration_postgres import scenarios as configure
    configured = configure()
    if len(configured) != 24 or not all(configured.values()):
        raise AssertionError("CONFIGURATION_UNPROVED")
    clock = _SharedClock(offset_seconds=0)
    context = ScopeContext(ScopeType.PLATFORM)
    from pixs.auth import models as m
    trust_row = m.AuthLocalTrustSelection.objects.get(profile_ref="pixs.auth.local")
    gate_a = m.AuthAccountGate.objects.get(pk=trust_row.approval_operation.identity_id)
    ref_a = identity_reference(gate_a.pk)
    trust, assurance = create_local_auth_sources(alias="default", profile_id=trust_row.profile_ref, clock=clock)
    profile = trust.current_profile(context)
    password_a = "Vecteur public configuration C03, aucun secret réel"
    id_b = generate_uuid7()
    CoreIdentity.objects.create(identity_id=id_b, identity_type=IdentityType.HUMAN.value, state=IdentityState.ACTIVE.value)
    ref_b = identity_reference(id_b)
    CoreSuperAdminBinding.objects.create(installation_ref=ROOT_INST, identity=CoreIdentity.objects.get(pk=gate_a.pk))
    CoreSuperAdminBinding.objects.create(installation_ref=ORD_INST, identity=CoreIdentity.objects.get(pk=id_b))
    res_root = "pixs.backend.modes:" + ROOT_INST
    res_ord = "pixs.backend.modes:" + ORD_INST
    acts = ("pixs.backend.modes.finalize", "pixs.backend.modes.enter_maintenance", "pixs.backend.modes.exit_maintenance")
    def _mk(pid, res, act):
        p = Policy(pid, "1.0.0", "pixs.backend", Effect.ALLOW, Selector("subject", (ref_a,)), Selector("resource", (res,)), Selector("action", (act,)), ScopeSelector((context,)), obligations=(Obligation("AUDIT"),))
        CorePolicy.objects.create(policy_id=p.policy_id, policy_version=p.policy_version, owner=p.owner, effect=p.effect.value, definition=encode_policy(p))
    _mk("c08-test-root-maintenance", res_root, acts[1])
    _mk("c08-test-root-finalize", res_root, acts[0])
    _mk("c08-test-ord-maintenance", res_ord, acts[1])
    _mk("c08-test-ord-finalize", res_ord, acts[0])
    _mk("c08-test-ord-exit", res_ord, acts[2])
    cat_root = Catalog((ref_a, ref_b), (res_root, res_ord), acts, (context,), ())
    cat_ord = Catalog((ref_a, ref_b), (res_root, res_ord), acts, (context,), ())
    lim = Limits(128, 128, 10, 20, 20, 128, 256, 256, 100000000, 60, 3600)
    store_root = CoreAuthorizationStore(alias="default", installation_ref=ROOT_INST, base_epoch="c08-test-epoch-v1", catalog=cat_root, limits=lim)
    store_ord = CoreAuthorizationStore(alias="default", installation_ref=ORD_INST, base_epoch="c08-test-epoch-v1", catalog=cat_ord, limits=lim)
    gov = dict(metadata_profile_ref="profile:test", metadata_published_version="1.0.0", metadata_owner_component="pixs.backend", metadata_source_of_truth="declaration:test", governance_ref="gov:test", governance_status="GOVERNED", confidentiality="INTERNAL", personal="NONE", retention_policy="retention:test", deletion_policy="deletion:test", publication_ref="publication:test", catalog_version="cat-test-v1", catalog_sha256=hashlib.sha256(b"cat-test").hexdigest())
    with ExitStack() as stack:
        tmpdir = stack.enter_context(tempfile.TemporaryDirectory(dir=str(artifact), prefix="modes-"))
        tdir = Path(tmpdir)
        os.chmod(tdir, 0o700)
        parents = _all_parents(tmpdir)
        with connections["default"].cursor() as _rc:
            _rc.execute("SELECT current_schema(),(SELECT oid FROM pg_namespace WHERE nspname=current_schema()),(SELECT oid FROM pg_database WHERE datname=current_database()),(SELECT nspowner FROM pg_namespace WHERE nspname=current_schema())")
            _recipe_namespace, _recipe_schema_oid, _recipe_db_oid, _recipe_owner_oid = _rc.fetchone()
        def _seed(inst, target_ref):
            with transaction.atomic(using="default"):
                with connections["default"].cursor() as cur:
                    cur.execute("SELECT pg_backend_pid(),pg_current_xact_id()::text,(SELECT oid FROM pg_database WHERE datname=current_database()),(SELECT oid FROM pg_namespace WHERE nspname=current_schema())")
                    pid, xid, db_oid, sch_oid = cur.fetchone()
                stamped = clock.now()
                from pixs.backend.c08_installation_result_record import C08InstallationResultRecord as P
                from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord as S
                P.objects.using("default").create(installation_ref=inst, operation_id="c08-test-op-" + inst, plan_version="test-only-1.0.0", plan_sha256=hashlib.sha256(b"plan-test").hexdigest(), content_sha256=hashlib.sha256(b"content-test").hexdigest(), serializer_version="1", database_target_ref=DB_TARGET, operator_subject_ref=ref_a, operator_proof_ref="proof-test", authorization_ref="auth-test", target_identity_ref=target_ref, target_tenant_ref=None, closed_effects=["CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"], confirmations=["confirm-test"], correlation_id="corr-test", causation_id=None, idempotency_key="idem-" + inst, result_ref="pixs.core.binding:" + inst, result_version=1, transaction_token="tok-" + inst, scope_type="PLATFORM", tenant_id=None, scope_id=None, publication_ref="publication:test", catalog_version="cat-test-v1", catalog_sha256=hashlib.sha256(b"cat-test").hexdigest(), metadata_profile_ref="profile:test", metadata_published_version="1.0.0", metadata_owner_component="pixs.backend", metadata_source_of_truth="declaration:test", governance_ref="gov:test", confidentiality="INTERNAL", personal="NONE", retention_policy="retention:test", deletion_policy="deletion:test", database_oid=db_oid, schema_oid=sch_oid, pid=pid, xid=xid, prepared_at=stamped)
                sid = generate_uuid7()
                S.objects.create(record_id=sid, installation_id=inst, version=1, configuration_state="PENDING", operating_mode="FIRST_CONFIGURATION", origin="R01_INITIAL", predecessor_id=None, operation_receipt_id=None, creator_operation_id="c08-test-op-" + inst, pid=pid, xid=xid, database_oid=db_oid, schema_oid=sch_oid, created_at=stamped, **gov)
                return sid
        _seed(ROOT_INST, ref_a)
        _seed(ORD_INST, ref_b)
        def _marker(inst):
            path = str(tdir / ("marker-" + inst + ".json"))
            payload = {"format_version": "1.0.0", "installation_ref": inst, "result_ref": "pixs.core.binding:" + inst, "result_version": 1}
            Path(path).write_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))
            os.chmod(path, 0o600)
            return MarkerConfig(path=path, owner_uid=os.getuid(), owner_gid=os.getgid(), max_bytes=4096, max_ref_len=256, allowed_format_versions=("1.0.0",), parent_identities=parents)
        reader_root = C08InstalledModeReader(using="default", inspection_using="peer", marker_config=_marker(ROOT_INST), installation_ref=ROOT_INST, database_target_ref=DB_TARGET, clock=clock)
        reader_ord = C08InstalledModeReader(using="default", inspection_using="peer", marker_config=_marker(ORD_INST), installation_ref=ORD_INST, database_target_ref=DB_TARGET, clock=clock)
        marker_paths = {ROOT_INST: object.__getattribute__(reader_root, "_marker").path, ORD_INST: object.__getattribute__(reader_ord, "_marker").path}
        def _public_cfg(cfg):
            b = cfg.binding
            return {"catalog_path": cfg.catalog_path, "guard_path": cfg.guard_path, "owner_uid": cfg.owner_uid, "owner_gid": cfg.owner_gid, "parent_identities": [list(p) for p in cfg.parent_identities], "max_bytes": cfg.max_bytes, "max_ref_len": cfg.max_ref_len, "max_profiles": cfg.max_profiles, "max_refs": cfg.max_refs, "max_ttl_seconds": cfg.max_ttl_seconds, "max_freshness_seconds": cfg.max_freshness_seconds, "lock_timeout_ms": cfg.lock_timeout_ms, "retry_interval_ms": cfg.retry_interval_ms, "expected_catalog_version": cfg.expected_catalog_version, "expected_publication_ref": cfg.expected_publication_ref, "expected_sha256": cfg.expected_sha256, "binding": {"profile_ref": b.profile_ref, "data_asset_id": b.data_asset_id, "owner_component": b.owner_component, "source_of_truth": b.source_of_truth, "profile_version": b.profile_version}}
        def worker_recipe():
            return {"root_str": str(Path(root_str).resolve()), "namespace": _recipe_namespace, "schema_oid": int(_recipe_schema_oid), "db_oid": int(_recipe_db_oid), "owner_oid": int(_recipe_owner_oid), "artifact_dir": str(artifact), "tmpdir": str(tdir), "marker_paths": dict(marker_paths), "mode_cfg": _public_cfg(mode_cfg), "meta_cfg": _public_cfg(meta_cfg), "installations": [ROOT_INST, ORD_INST], "actor_ref": ref_a, "profile_id": profile.profile_id, "database_target_ref": DB_TARGET, "scope": "PLATFORM"}
        anchor = clock.now()
        vf = anchor - datetime.timedelta(hours=1)
        pub = anchor
        vu = anchor + datetime.timedelta(days=1)
        toml = "[catalog]\nschema_version=\"1.0.0\"\ncatalog_version=\"cat-test-v1\"\npublication_ref=\"publication:test\"\nvalid_from=" + _iso_z(vf) + "\nvalid_until=" + _iso_z(vu) + "\npublished_at=" + _iso_z(pub) + "\nrevoked=false\n"
        for name, asset, owner in (("c08mode", "asset:c08-mode-test", "pixs.backend"), ("c08metadata", "asset:c08-metadata-test", "test.c08.metadata")):
            toml += "\n[profiles." + name + "]\npublished_version=\"1.0.0\"\nresource_refs=[\"" + res_root + "\",\"" + res_ord + "\"]\nrevoked=false\n[profiles." + name + ".profile]\nprofile_version=\"1.0.0\"\ndata_asset_id=\"" + asset + "\"\nowner_component=\"" + owner + "\"\nsource_of_truth=\"declaration:test\"\ndata_classes=[]\nconfidentiality=\"INTERNAL\"\npersonal_data=\"NONE\"\npurpose_refs=[]\nretention_policy=\"retention:test\"\ndeletion_policy=\"deletion:test\"\nresidency_constraints=[]\nauthorized_consumers=[]\nprocessor_refs=[]\nexport_policy=\"export:test\"\nlineage=\"lineage:test\"\n"
        raw = toml.encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        mode_toml, mode_guard = str(tdir / "mode.toml"), str(tdir / "mode.guard")
        meta_toml, meta_guard = str(tdir / "metadata.toml"), str(tdir / "metadata.guard")
        for p in (mode_toml, meta_toml):
            Path(p).write_bytes(raw)
            os.chmod(p, 0o600)
        for g in (mode_guard, meta_guard):
            Path(g).write_bytes(b"")
            os.chmod(g, 0o600)
        mode_cfg = CatalogConfig(mode_toml, mode_guard, os.getuid(), os.getgid(), parents, 65536, 256, 8, 32, 90000, 3600, 5000, 50, "cat-test-v1", "publication:test", digest, ProfileBinding("c08mode", "asset:c08-mode-test", "pixs.backend", "declaration:test", "1.0.0"))
        meta_cfg = CatalogConfig(meta_toml, meta_guard, os.getuid(), os.getgid(), parents, 65536, 256, 8, 32, 90000, 3600, 5000, 50, "cat-test-v1", "publication:test", digest, ProfileBinding("c08metadata", "asset:c08-metadata-test", "test.c08.metadata", "declaration:test", "1.0.0"))
        mode_lease = stack.enter_context(C10Catalog(mode_cfg, now=clock.now).guard())
        meta_lease = stack.enter_context(C10Catalog(meta_cfg, now=clock.now).guard())
        from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
        audit = PostgresAuditParticipant(ExplicitAuditPolicySource(context, AuditPolicy("c08-test-audit", "1.0.0", TEST_ONLY, 1, 65536, 50, (), "c08-test-audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)), clock, "peer")
        filt = FilterConfig(10)
        stores = {ROOT_INST: store_root, ORD_INST: store_ord}
        readers = {ROOT_INST: reader_root, ORD_INST: reader_ord}
        def invoke(role, kind, expected, key, operation_id, correlation_id):
            if role not in ("root", "ordinary"):
                raise AssertionError("ROLE_FIXTURE_INVALID")
            inst = ROOT_INST if role == "root" else ORD_INST
            cmd = ModeCommandInput(installation_ref=inst, actor_ref=ref_a, kind=kind, expected_version=expected, idempotency_key=key)
            req = C04Request("decision:" + operation_id, ref_a, mode_resource_ref(cmd, max_ref_len=256), mode_action_ref(kind), context, correlation_id)
            env = CommandEnvelope(req, operation_id, key, mode_content_sha256(cmd, max_ref_len=256), MODE_SERIALIZER_VERSION, correlation_id, None)
            verifier = prepare_password_verifier(request=req, alias="default", operation_id=operation_id, profile=profile, trust_source=trust, assurance_source=assurance, facts_reader=CoreFactSource(), clock=clock, external_subject="initial-subject", password=password_a, category=SessionCategory.ORDINARY)
            src = AuthInvocationSource(verifier)
            current_governance = C10ModeGovernanceAdapter(
                using="default", installation_ref=inst, mode_lease=mode_lease,
                metadata_lease=meta_lease, clock=clock)
            try:
                return execute_mode(using="default", inspection_using="peer", clock=clock, envelope=env, command=cmd, reader=readers[inst], store=stores[inst], authentication_source=src, audit=audit, filter_config=filt, governance=current_governance, waiver_request=None)
            finally:
                src.close()
        @contextmanager
        def server_call(role, kind, expected, key, operation_id, correlation_id, fault=None):
            if role not in ("root", "ordinary"):
                raise AssertionError("ROLE_FIXTURE_INVALID")
            if fault not in (None, "cross_action", "bad_digest"):
                raise AssertionError("FAULT_FIXTURE_INVALID")
            inst = ROOT_INST if role == "root" else ORD_INST
            cmd_kind = kind
            req_kind = kind
            if fault == "cross_action":
                if kind is not ModeOperationKind.ENTER_MAINTENANCE:
                    raise AssertionError("FAULT_KIND_INVALID")
                req_kind = ModeOperationKind.FINALIZE_CONFIGURATION
            cmd = ModeCommandInput(installation_ref=inst, actor_ref=ref_a, kind=cmd_kind, expected_version=expected, idempotency_key=key)
            req = C04Request("decision:" + operation_id, ref_a, mode_resource_ref(cmd, max_ref_len=256), mode_action_ref(req_kind), context, correlation_id)
            good = mode_content_sha256(cmd, max_ref_len=256)
            if fault == "bad_digest":
                tail = "1" if good[-1] != "1" else "0"
                env_hash = good[:-1] + tail
            else:
                env_hash = good
            env = CommandEnvelope(req, operation_id, key, env_hash, MODE_SERIALIZER_VERSION, correlation_id, None)
            verifier = prepare_password_verifier(request=req, alias="default", operation_id=operation_id, profile=profile, trust_source=trust, assurance_source=assurance, facts_reader=CoreFactSource(), clock=clock, external_subject="initial-subject", password=password_a, category=SessionCategory.ORDINARY)
            src = AuthInvocationSource(verifier)
            try:
                current_governance = C10ModeGovernanceAdapter(using="default", installation_ref=inst, mode_lease=mode_lease, metadata_lease=meta_lease, clock=clock)
                yield {"using": "default", "inspection_using": "peer", "clock": clock, "envelope": env, "command": cmd, "reader": readers[inst], "store": stores[inst], "authentication_source": src, "audit": audit, "filter_config": filt, "governance": current_governance, "waiver_request": None}
            finally:
                src.close()
        def read_snapshot_peer(record_id):
            from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord as S2
            return S2.objects.using("peer").get(record_id=record_id)
        def read_receipt_peer(operation_id):
            from pixs.backend.c08_mode_operation_receipt_record import C08ModeOperationReceiptRecord as R2
            return R2.objects.using("peer").get(operation_id=operation_id)
        yield {"context": context, "clock": clock, "ref_a": ref_a, "ref_b": ref_b, "profile": profile, "trust": trust, "assurance": assurance, "stores": stores, "readers": readers, "audit": audit, "filter_config": filt, "invoke": invoke, "server_call": server_call, "read_snapshot_peer": read_snapshot_peer, "read_receipt_peer": read_receipt_peer, "test_only": TEST_ONLY, "worker_recipe": worker_recipe}
