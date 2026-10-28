"""Fixture publication Auth/C05 : montage reel session -> intent -> writer -> binding -> fichiers.

Ordre impose par les contrats proprietaires : la reservation Auth cree les
references, prepare_initial retourne l'intent reel, le writer C08 est construit
apres (miroir du draft + intent), C08AuthPlanBinding realise bind_plan, les
fichiers sont ecrits depuis le challenge reel, la classification C10 est fournie
par l'appelant au bon moment. Aucun objet dependant du draft n'est preconstruit.
Cle TEST et credential TEST uniquement, jamais ecrits hors fichiers de preuve.
"""
from __future__ import annotations
import hashlib as _hashlib
import json as _json
import os as _os
import posixpath as _posix
import shutil as _shutil
import stat as _stat
import tempfile as _tempfile
from contextlib import ExitStack as _Stack
from contextlib import contextmanager as _context
from pixs.auth.bootstrap_file_sources import FileProofSource as _Proofs
from pixs.auth.bootstrap_file_sources import FileProofSourceConfig as _ProofCfg
from pixs.auth.bootstrap_file_sources import FileTrustSource as _Trust
from pixs.auth.bootstrap_file_sources import FileTrustSourceConfig as _TrustCfg
from pixs.auth.bootstrap_file_sources import ProtectedSourceFile as _Prot
from pixs.auth.bootstrap_session import AuthBootstrapSession as _Session
from pixs.auth.bootstrap_session import AuthBootstrapSessionError as _SessionError
from pixs.auth.bootstrap_session import BootstrapDraft as _Draft
from pixs.auth.bootstrap_session import BootstrapSigningChallenge as _Challenge
from pixs.auth.configuration import InitialLocalAuthSelection as _Selection
from pixs.auth.r01 import BootstrapTrustPolicy as _Policy
from pixs.auth.r01 import SignedBootstrapProof as _Proof
from pixs.backend.installation.auth_creation_bridge import C10AuthCreationBridge as _Bridge
from pixs.backend.installation.auth_plan_binding import C08AuthPlanBinding as _Binding
from pixs.backend.installation.result_writer import C08TransactionalResultWriter as _Writer
from pixs.core.audit_contracts import AuditPolicy as _AuditPolicy
from pixs.core.audit_contracts import ExplicitAuditPolicySource as _AuditSrc
from pixs.core.audit_sink import PostgresAuditParticipant as _Audit
from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION as _ACTION
from pixs.core.bootstrap_operator import BootstrapOperatorFacts as _Facts
from pixs.core.ports import CorePortError as _PortError
from pixs.core.query_source import CoreFactSource as _FactsReader
from pixs.core.scope.context import ScopeContext as _Ctx
from pixs.core.scope.context import ScopeType as _ST

__all__ = ["publication_fixture"]

# Racine du depot derivee de ce fichier de test (tests/integration -> racine).
# Hypothese locale de test, jamais un contrat produit.
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
# Valeur observee bootstrap_file_sources.py:32, jamais devine ni import prive.
_POLICY_SCHEMA = "pixs.auth.bootstrap-trust.v1"
_PASSWORD = "Publication Auth TEST, aucun secret reel"
_SUBJECT = "initial-subject-test"


def _fail():
    raise _PortError()


def _need(value):
    if type(value) is not str or not value:
        _fail()


def _rmtree(path):
    _shutil.rmtree(path, ignore_errors=False)


def _chain(tmpdir):
    # Inclut '/' : _parent parcourt depuis la racine, chaque ancetre non final
    # doit figurer dans parent_identities (bootstrap_file_sources.py:162-172).
    try:
        anchor = _os.lstat("/")
    except OSError as error:
        raise _PortError() from error
    if not _stat.S_ISDIR(anchor.st_mode):
        _fail()
    walked, prefix = [("/", anchor)], ""
    for name in tmpdir.split("/")[1:]:
        prefix = prefix + "/" + name
        try:
            st = _os.lstat(prefix)
        except OSError as error:
            raise _PortError() from error
        if not _stat.S_ISDIR(st.st_mode):
            _fail()
        walked.append((prefix, st))
    return walked


def _write(path, data):
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
            or st.st_nlink != 1 or st.st_size != len(data) or st.st_size < 1):
        _fail()


def _protect(path, data, final, parents, maxb):
    try:
        st = _os.lstat(path)
    except OSError as error:
        raise _PortError() from error
    return _Prot(path, _hashlib.sha256(data).hexdigest(), st.st_uid, st.st_gid,
                 final.st_uid, final.st_gid, parents, maxb)


@_context
def publication_fixture(*, alias, clock, max_password_bytes, workdir, operation_id,
                        installation_ref, target_identity_ref, closed_effects, key_id,
                        trust_policy_version, selection, audit_policy, peer_alias,
                        component_version, make_writer, make_classification):
    for value in (alias, workdir, operation_id, installation_ref, target_identity_ref,
                  key_id, trust_policy_version, peer_alias, component_version):
        _need(value)
    if (not callable(getattr(clock, "now", None))
            or type(max_password_bytes) is not int or max_password_bytes < 1
            or type(closed_effects) is not tuple
            or type(selection) is not _Selection
            or type(audit_policy) is not _AuditPolicy
            or not callable(make_writer) or not callable(make_classification)):
        _fail()
    if _posix.normpath(workdir) != workdir or not _os.path.isabs(workdir):
        _fail()
    real = _os.path.realpath(workdir)
    if real != _ROOT and not real.startswith(_ROOT + _os.path.sep):
        _fail()
    try:
        anchor = _os.lstat(real)
    except OSError as error:
        raise _PortError() from error
    if not _stat.S_ISDIR(anchor.st_mode):
        _fail()
    if len(_PASSWORD) > max_password_bytes or len(_PASSWORD.encode("utf-8")) > max_password_bytes:
        _fail()
    with _Stack() as stack:
        try:
            session = _Session(alias=alias, clock=clock, max_password_bytes=max_password_bytes)
        except _SessionError as error:
            raise _PortError() from error
        stack.callback(session.close)
        try:
            tmpdir = _tempfile.mkdtemp(dir=real, prefix="authpub-")
        except OSError as error:
            raise _PortError() from error
        stack.callback(_rmtree, tmpdir)
        try:
            _os.chmod(tmpdir, 0o700)
        except OSError as error:
            raise _PortError() from error
        walked = _chain(tmpdir)
        final = walked[-1][1]
        if _stat.S_IMODE(final.st_mode) != 0o700:
            _fail()
        parents = tuple((st.st_uid, st.st_gid) for _, st in walked[:-1])
        for _, st in walked[:-1]:
            if st.st_mode & 0o002 and not (st.st_uid == 0 and st.st_mode & _stat.S_ISVTX):
                _fail()
        try:
            draft = session.reserve(operation_id=operation_id, installation_ref=installation_ref,
                                    target_identity_ref=target_identity_ref,
                                    closed_effects=closed_effects, key_id=key_id,
                                    trust_policy_version=trust_policy_version)
        except _SessionError as error:
            raise _PortError() from error
        if type(draft) is not _Draft:
            _fail()
        try:
            intent = session.prepare_initial(draft, password1=_PASSWORD, password2=_PASSWORD,
                                             selection=selection, external_subject=_SUBJECT)
        except _SessionError as error:
            raise _PortError() from error
        if type(intent) is not str or not intent:
            _fail()
        # Builders : erreurs inattendues propagees au harness, jamais masquees.
        writer = make_writer(session=session, draft=draft, credential_intent_ref=intent)
        if type(writer) is not _Writer or writer._using != session.using or writer._clock is not session.clock:
            _fail()
        binding = _Binding(writer=writer, session=session, draft=draft)
        if type(binding) is not _Binding:
            _fail()
        challenge = binding.resolve_challenge(draft, alias=session.using, operation_id=draft.operation_id)
        if type(challenge) is not _Challenge or type(challenge.facts) is not _Facts:
            _fail()
        if (type(challenge.canonical_message) is not bytes or type(challenge.nonce) is not bytes
                or len(challenge.nonce) != 32
                or _hashlib.sha256(challenge.canonical_message).hexdigest() != challenge.challenge_sha256):
            _fail()
        facts = challenge.facts
        if tuple(facts.authorized_actions) != (_ACTION,):
            _fail()
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey as _Ed
        from cryptography.hazmat.primitives.serialization import Encoding as _Enc
        from cryptography.hazmat.primitives.serialization import PublicFormat as _PubF
        priv = _Ed.generate()
        pub_hex = priv.public_key().public_bytes(_Enc.Raw, _PubF.Raw).hex()
        message = challenge.canonical_message
        signature = priv.sign(message)
        del priv
        if len(signature) != 64:
            _fail()
        stamp = "%Y-%m-%dT%H:%M:%S.%fZ"
        key = {"key_id": facts.key_id, "operator_subject_ref": facts.operator_subject_ref,
               "installation_ref": facts.installation_ref,
               "authorized_actions": list(facts.authorized_actions),
               "public_key_hex": pub_hex, "valid_from": facts.valid_from.strftime(stamp),
               "valid_until": facts.expires_at.strftime(stamp), "revoked": False}
        policy_ref = "pixs.auth.trust:" + draft.operation_id
        publication_ref = "pixs.auth.publication:" + draft.operation_id
        for value in (policy_ref, publication_ref):
            if not value.isprintable() or len(value) > 1024:
                _fail()
        policy_doc = _json.dumps({"schema": _POLICY_SCHEMA, "policy_ref": policy_ref,
                                  "publication_ref": publication_ref,
                                  "policy": {"version": draft.trust_policy_version, "keys": [key]}},
                                 sort_keys=True, separators=(",", ":"),
                                 ensure_ascii=True).encode("ascii")
        msg_p = tmpdir + "/message.bin"
        sig_p = tmpdir + "/signature.bin"
        pol_p = tmpdir + "/policy.json"
        _write(msg_p, message)
        _write(sig_p, signature)
        _write(pol_p, policy_doc)
        proofs = _Proofs(_ProofCfg(_protect(msg_p, message, final, parents, 128 * 1024),
                                  _protect(sig_p, signature, final, parents, 64),
                                  draft.operator_proof_ref, challenge.challenge_sha256))
        trust = _Trust(_TrustCfg(_protect(pol_p, policy_doc, final, parents, 64 * 1024),
                                policy_ref, draft.trust_policy_version, publication_ref, 8))
        proof = proofs.resolve(draft.operator_proof_ref)
        policy = trust.resolve(draft.trust_policy_version)
        if type(proof) is not _Proof or type(policy) is not _Policy:
            _fail()
        classification = make_classification(session=session, draft=draft)
        if type(classification) is not _Bridge:
            _fail()
        link = classification.binding
        if (type(link) is not tuple or len(link) != 3 or link[0] != session.using
                or link[1] is not session or link[2] is not draft):
            _fail()
        facts_reader = _FactsReader()
        if type(facts_reader) is not _FactsReader:
            _fail()
        audit = _Audit(_AuditSrc(_Ctx(_ST.PLATFORM), audit_policy), clock, peer_alias)
        if type(audit) is not _Audit:
            _fail()
        kwargs = {"session": session, "draft": draft, "proofs": proofs, "trust": trust,
                  "facts_reader": facts_reader, "creation_classification": classification,
                  "plan_binding": binding, "audit": audit, "component_version": component_version}
        yield {"session": session, "draft": draft, "challenge": challenge, "proofs": proofs,
               "trust": trust, "facts_reader": facts_reader,
               "creation_classification": classification, "plan_binding": binding,
               "audit": audit, "kwargs": kwargs, "key_public_hex": pub_hex, "dir": tmpdir}
