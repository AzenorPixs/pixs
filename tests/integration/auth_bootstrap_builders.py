"""Builders TEST concrets pour la fixture F1 : writer C08 et bridge C10 reels.

Cycle de vie : le test entre dans builders(), recoit les 2 callbacks exacts
attendus par F1, execute la fixture F1 a l'interieur, puis sort : gardes et
fichiers sont liberes par l'ExitStack proprietaire, sans oubli possible.
Aucun global mutable, aucun release manuel. Plan/enveloppe/confirmations
derives du draft et de l'intent recus ; rien ne depend d'un draft precrée.
TEST uniquement, aucun secret, aucune execution PG, aucun effet d'import.
Source seulement, realisee a tester en phase2 si un futur mandat l'ecrit.
"""
from __future__ import annotations
import datetime as _dt
import hashlib as _hashlib
import os as _os
import posixpath as _posix
import shutil as _shutil
import stat as _stat
import tempfile as _tempfile
import uuid as _uuid
from contextlib import ExitStack as _Stack
from contextlib import contextmanager as _context
from urllib.parse import quote as _quote
from pixs.auth.bootstrap_session import AuthBootstrapSession as _Session
from pixs.auth.bootstrap_session import BootstrapDraft as _Draft
from pixs.auth.bootstrap_session import PlannedBootstrapResource as _Planned
from pixs.backend.c10_catalog import C10Catalog as _Catalog
from pixs.backend.c10_catalog import CatalogConfig as _CatalogCfg
from pixs.backend.c10_catalog import ProfileBinding as _ProfileBinding
from pixs.backend.installation.act_content import ActContentFields as _ActContent
from pixs.backend.installation.act_content import act_content_sha256 as _act_digest
from pixs.backend.installation.auth_creation_bridge import C10AuthCreationBridge as _Bridge
from pixs.backend.installation.marker import MarkerConfig as _MarkerCfg
from pixs.backend.installation.plan import InstallationPlan as _Plan
from pixs.backend.installation.plan import PlanLimits as _PlanLimits
from pixs.backend.installation.plan import bind_confirmation as _bind
from pixs.backend.installation.result_writer import C08TransactionalResultWriter as _Writer
from pixs.backend.installation.storage import PlanStoreConfig as _StoreCfg
from pixs.backend.installation.storage import initialize_plan_guard as _init_guard
from pixs.backend.installation.storage import publish_plan as _publish
from pixs.core.authz.ports import Request as _Request
from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION as _ACTION
from pixs.core.bootstrap_operator import BOOTSTRAP_EFFECTS as _EFFECTS
from pixs.core.dto import BootstrapActInput as _Act
from pixs.core.dto import BootstrapTargetSpec as _Spec
from pixs.core.dto import CommandEnvelope as _Envelope
from pixs.core.identity.models import IdentityState as _IState
from pixs.core.identity.models import IdentityType as _IType
from pixs.core.ports import CorePortError as _PortError
from pixs.core.scope.context import ScopeContext as _Ctx
from pixs.core.scope.context import ScopeType as _ST

__all__ = ["builders"]

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
_TEST_SUBJECT = "operator-subject-test"
_TEST_DB_TARGET = "database-target-test"
_TEST_CORR = "correlation-test-1"
_TEST_IDEM = "idempotency-test-1"
_TEST_CONF = "confirmation-test-1"
_VERSION = "1.0.0"
_CREATE_TRIPLE = tuple(_EFFECTS[:3])


def _fail():
    raise _PortError()


def _chain(directory):
    try:
        anchor = _os.lstat("/")
    except OSError as error:
        raise _PortError() from error
    if not _stat.S_ISDIR(anchor.st_mode):
        _fail()
    walked, prefix = [("/", anchor)], ""
    for name in directory.split("/")[1:]:
        prefix = prefix + "/" + name
        try:
            st = _os.lstat(prefix)
        except OSError as error:
            raise _PortError() from error
        if not _stat.S_ISDIR(st.st_mode):
            _fail()
        walked.append((prefix, st))
    for _, st in walked[:-1]:
        if st.st_mode & 0o002 and not (st.st_uid == 0 and st.st_mode & _stat.S_ISVTX):
            _fail()
    return tuple((st.st_uid, st.st_gid) for _, st in walked)


def _write(path, data, *, allow_empty=False):
    try:
        fd = _os.open(path, _os.O_WRONLY | _os.O_CREAT | _os.O_EXCL | _os.O_NOFOLLOW, 0o600)
    except OSError as error:
        raise _PortError() from error
    try:
        view, done = memoryview(data), 0
        while done < len(data):
            wrote = _os.write(fd, view[done:])
            if wrote <= 0:
                _fail()
            done += wrote
        _os.fsync(fd)
    except OSError as error:
        raise _PortError() from error
    finally:
        try:
            _os.close(fd)
        except OSError as error:
            raise _PortError() from error
    try:
        st = _os.lstat(path)
    except OSError as error:
        raise _PortError() from error
    if (not _stat.S_ISREG(st.st_mode) or _stat.S_IMODE(st.st_mode) != 0o600
            or st.st_nlink != 1 or st.st_size != len(data)
            or (not allow_empty and st.st_size < 1)):
        _fail()


def _iso_z(moment):
    if type(moment) is not _dt.datetime or moment.tzinfo is not _dt.timezone.utc:
        _fail()
    return moment.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _catalog(stack, tmpdir, parents, clock, name, owner, asset, refs):
    anchor = clock.now()
    if type(anchor) is not _dt.datetime or anchor.tzinfo is not _dt.timezone.utc:
        _fail()
    vf, pub = anchor - _dt.timedelta(hours=1), anchor
    vu = anchor + _dt.timedelta(days=1)
    toml = ("[catalog]\nschema_version=\"1.0.0\"\ncatalog_version=\"cat-test-v1\"\npublication_ref=\"publication:test\"\nvalid_from=" + _iso_z(vf) + "\nvalid_until=" + _iso_z(vu) + "\npublished_at=" + _iso_z(pub) + "\nrevoked=false\n"
            + "\n[profiles." + name + "]\npublished_version=\"1.0.0\"\nresource_refs=[" + ",".join("\"" + r + "\"" for r in refs) + "]\nrevoked=false\n[profiles." + name + ".profile]\nprofile_version=\"1.0.0\"\ndata_asset_id=\"" + asset + "\"\nowner_component=\"" + owner + "\"\nsource_of_truth=\"declaration:test\"\ndata_classes=[]\nconfidentiality=\"INTERNAL\"\npersonal_data=\"NONE\"\npurpose_refs=[]\nretention_policy=\"retention:test\"\ndeletion_policy=\"deletion:test\"\nresidency_constraints=[]\nauthorized_consumers=[]\nprocessor_refs=[]\nexport_policy=\"export:test\"\nlineage=\"lineage:test\"\n")
    raw = toml.encode("utf-8")
    digest = _hashlib.sha256(raw).hexdigest()
    toml_p, guard_p = tmpdir + "/" + name + ".toml", tmpdir + "/" + name + ".guard"
    _write(toml_p, raw, allow_empty=False)
    _write(guard_p, b"", allow_empty=True)
    cfg = _CatalogCfg(catalog_path=toml_p, guard_path=guard_p, owner_uid=_os.getuid(), owner_gid=_os.getgid(), parent_identities=parents, max_bytes=65536, max_ref_len=256, max_profiles=8, max_refs=32, max_ttl_seconds=90000, max_freshness_seconds=3600, lock_timeout_ms=5000, retry_interval_ms=50, expected_catalog_version="cat-test-v1", expected_publication_ref="publication:test", expected_sha256=digest, binding=_ProfileBinding(name, asset, owner, "declaration:test", "1.0.0"))
    catalog = _Catalog(cfg, now=clock.now)
    return stack.enter_context(catalog.guard())


def _limits():
    return _PlanLimits(max_bytes=65536, max_ref_len=256, max_effects=8, allowed_schema_versions=("1.0.0",), allowed_plan_versions=("1.0.0",))


@_context
def builders(workdir=None):
    if workdir is None:
        candidate = _os.path.dirname(_os.path.abspath(__file__))
    elif type(workdir) is not str:
        _fail()
    else:
        candidate = workdir
    if _posix.normpath(candidate) != candidate or not _os.path.isabs(candidate):
        _fail()
    real = _os.path.realpath(candidate)
    if real != _ROOT and not real.startswith(_ROOT + _os.path.sep):
        _fail()
    try:
        anchor = _os.lstat(real)
    except OSError as error:
        raise _PortError() from error
    if not _stat.S_ISDIR(anchor.st_mode):
        _fail()
    with _Stack() as stack:
        try:
            sandbox = _tempfile.mkdtemp(dir=real, prefix="authpub-b-")
        except OSError as error:
            raise _PortError() from error
        stack.callback(_shutil.rmtree, sandbox, False)
        try:
            _os.chmod(sandbox, 0o700)
        except OSError as error:
            raise _PortError() from error

        def make_writer(*, session, draft, credential_intent_ref):
            if type(session) is not _Session or type(draft) is not _Draft:
                _fail()
            if type(session.describe(draft)) is not _Planned:
                _fail()
            if type(credential_intent_ref) is not str or not credential_intent_ref:
                _fail()
            if tuple(draft.closed_effects) != _CREATE_TRIPLE:
                _fail()
            if type(draft.target_identity_ref) is not str or not draft.target_identity_ref.startswith("pixs.core.identity:"):
                _fail()
            try:
                identity = _uuid.UUID(draft.target_identity_ref[len("pixs.core.identity:"):])
            except ValueError as error:
                raise _PortError() from error
            try:
                subdir = _tempfile.mkdtemp(dir=sandbox, prefix="writer-")
            except OSError as error:
                raise _PortError() from error
            stack.callback(_shutil.rmtree, subdir, False)
            try:
                _os.chmod(subdir, 0o700)
            except OSError as error:
                raise _PortError() from error
            parents = _chain(subdir)
            limits = _limits()
            ctx = _Ctx(_ST.PLATFORM)
            spec = _Spec(identity_id=identity, identity_type=_IType.HUMAN, identity_state=_IState.ACTIVE, expected_binding_version=None, expected_identity_version=None, tenant_id=None, expected_tenant_version=None)
            plan = _Plan(schema_version=_VERSION, plan_version=_VERSION, operation_id=draft.operation_id, installation_ref=draft.installation_ref, database_target_ref=_TEST_DB_TARGET, observed_database_state="ABSENT", database_action="PREPARATION", operator_subject_ref=_TEST_SUBJECT, target_identity_ref=draft.target_identity_ref, target_tenant_ref=None, target_spec=spec, closed_effects=draft.closed_effects, credential_intent_ref=credential_intent_ref, correlation_id=_TEST_CORR, causation_id=None, idempotency_key=_TEST_IDEM)
            io = _MarkerCfg(path=subdir + "/plan-store.json", owner_uid=_os.getuid(), owner_gid=_os.getgid(), max_bytes=65536, max_ref_len=256, allowed_format_versions=("1.0.0",), parent_identities=parents)
            store = _StoreCfg(io=io, lock_basename="plan.lock", limits=limits)
            _init_guard(store)
            _publish(store, plan)
            link = _bind(plan, _TEST_CONF, limits)
            content = _ActContent(operation_id=draft.operation_id, plan_version=_VERSION, installation_ref=draft.installation_ref, mode="INSTALLER", operator_proof_ref=draft.operator_proof_ref, operator_subject_ref=_TEST_SUBJECT, authorization_ref=draft.authorization_ref, target_identity_ref=draft.target_identity_ref, target_tenant_ref=None, closed_effects=draft.closed_effects, confirmations=(_TEST_CONF,), context=ctx, correlation_id=_TEST_CORR, causation_id=None, idempotency_key=_TEST_IDEM, serializer_version=_VERSION)
            digest = _act_digest(plan, content, limits)
            act = _Act(operation_id=draft.operation_id, plan_version=_VERSION, installation_ref=draft.installation_ref, mode="INSTALLER", operator_proof_ref=draft.operator_proof_ref, operator_subject_ref=_TEST_SUBJECT, authorization_ref=draft.authorization_ref, target_identity_ref=draft.target_identity_ref, target_tenant_ref=None, closed_effects=draft.closed_effects, confirmations=(_TEST_CONF,), context=ctx, correlation_id=_TEST_CORR, causation_id=None, idempotency_key=_TEST_IDEM, content_sha256=digest, serializer_version=_VERSION)
            resource = "pixs.core.bootstrap:" + _quote(draft.installation_ref, safe="")
            request = _Request(decision_id=draft.authorization_ref, subject_id=_TEST_SUBJECT, resource_id=resource, action_id=_ACTION, context=ctx, correlation_id=_TEST_CORR)
            request.__post_init__()
            envelope = _Envelope(request, draft.operation_id, _TEST_IDEM, digest, _VERSION, _TEST_CORR, None)
            envelope.__post_init__()
            lease = _catalog(stack, subdir, parents, session.clock, "c08backend", "pixs.backend", "asset:c08-backend-test", (resource,))
            return _Writer(using=session.using, store=store, act=act, envelope=envelope, confirmations=(link,), metadata_lease=lease, clock=session.clock, result_version=1)

        def make_classification(*, session, draft):
            if type(session) is not _Session or type(draft) is not _Draft:
                _fail()
            if type(session.describe(draft)) is not _Planned:
                _fail()
            try:
                subdir = _tempfile.mkdtemp(dir=sandbox, prefix="classif-")
            except OSError as error:
                raise _PortError() from error
            stack.callback(_shutil.rmtree, subdir, False)
            try:
                _os.chmod(subdir, 0o700)
            except OSError as error:
                raise _PortError() from error
            parents = _chain(subdir)
            lease = _catalog(stack, subdir, parents, session.clock, "c08auth", "pixs.auth", "asset:c08-auth-test", ("pixs.auth.bootstrap:" + str(draft.pk),))
            return _Bridge(using=session.using, session=session, draft=draft, metadata_lease=lease)

        yield (make_writer, make_classification)
