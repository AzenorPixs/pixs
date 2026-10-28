"""Coherence des octets figes S2b1, donnee non certifiee.

Verifie qu'une map exacte path->bytes correspond au manifeste S2a et aux
textes profil/enveloppe/pyproject resolus depuis leurs roles, sans IO,
sans reseau, sans autorite ni utilisabilite.
"""
from __future__ import annotations

import hashlib
import re
import tomllib
from dataclasses import dataclass

from pixs.pa_native.build_profile import ProfileError, parse_profile
from pixs.pa_native.campaign_envelope import CampaignEnvelopeError, parse_envelope
from pixs.pa_native.selection_evidence import parse_manifest

__all__ = [
    'CythonMismatchError',
    'FileConsistency',
    'FileConsistencyError',
    'verify_selection_files',
]

_EVIDENCE = 'PA01_CAMPAIGN_EVIDENCE_INVALID'
_MISMATCH = 'PA01_BUILD_CYTHON_MISMATCH'
_METADATA = 'PA01_CAMPAIGN_METADATA_INVALID'

_PIN = re.compile(r'^[ \t]*cython[ \t]*==[ \t]*([^ \t\r\n;@]+)[ \t]*$', re.IGNORECASE)
_NAME = re.compile(r'^[ \t]*([A-Za-z0-9_.\-]+)')


class FileConsistencyError(ProfileError):
    pass


class CythonMismatchError(ProfileError):
    pass


@dataclass(frozen=True, slots=True)
class FileConsistency:
    campaign_id: str
    cython_version: str
    manifest_sha256: str
    envelope_sha256: str
    profile_sha256: str
    pyproject_sha256: str
    snapshot_sha256: str
    distributions: tuple
    pyproject_decl: str
    pyproject_version: str


def _fail_evidence() -> FileConsistencyError:
    return FileConsistencyError(_EVIDENCE + ' : preuve ou fichier incoherent')


def _fail_mismatch() -> CythonMismatchError:
    return CythonMismatchError(_MISMATCH + ' : versions verrouillees divergentes')


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _dist_name(req: str) -> str | None:
    m = _NAME.match(req)
    if m is None:
        return None
    return re.sub(r'[-_.]+', '-', m.group(1)).lower()


def _is_cython_req(req: str) -> bool:
    return _dist_name(req) == 'cython'


def _extract_pyproject(data: bytes) -> tuple[str, str]:
    try:
        text = data.decode('utf-8', 'strict')
    except UnicodeDecodeError:
        raise _fail_evidence() from None
    if '\r' in text:
        raise _fail_evidence() from None
    try:
        root = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        raise _fail_evidence() from None
    if type(root) is not dict:
        raise _fail_evidence() from None
    bs = root.get('build-system')
    if type(bs) is not dict:
        raise _fail_evidence() from None
    reqs = bs.get('requires')
    if type(reqs) is not list or not reqs:
        raise _fail_evidence() from None
    for r in reqs:
        if type(r) is not str or not r:
            raise _fail_evidence() from None
    refs = [r for r in reqs if _is_cython_req(r)]
    if len(refs) != 1:
        raise _fail_evidence() from None
    decl = refs[0]
    if ';' in decl:
        raise _fail_evidence() from None
    if '@' in decl.split(';', 1)[0]:
        raise _fail_evidence() from None
    for c in decl:
        o = ord(c)
        if o == 32 or o == 9:
            continue
        if o < 32 or 127 <= o <= 159 or 0xD800 <= o <= 0xDFFF:
            raise _fail_evidence() from None
    m = _PIN.match(decl)
    if m is None:
        raise _fail_evidence() from None
    return (decl, m.group(1))


def verify_selection_files(manifest_bytes: bytes, files: dict) -> FileConsistency:
    if type(manifest_bytes) is not bytes:
        raise _fail_evidence() from None
    if type(files) is not dict:
        raise _fail_evidence() from None
    owned = dict(files)
    for k, v in owned.items():
        if type(k) is not str or type(v) is not bytes:
            raise _fail_evidence() from None
    manifest = parse_manifest(manifest_bytes)
    want: dict = {}
    for f in manifest.files:
        want[f.path] = f
    if set(owned) != set(want):
        raise _fail_evidence() from None
    for path, entry in want.items():
        if _sha(owned[path]) != entry.sha256:
            raise _fail_evidence() from None
    role_path: dict = {}
    for f in manifest.files:
        if f.role != 'distribution':
            role_path[f.role] = f.path
    try:
        envelope_bytes = owned[role_path['campaign_metadata']]
        profile_bytes = owned[role_path['build_profile']]
        pyproject_bytes = owned[role_path['pyproject']]
        snapshot_bytes = owned[role_path['pypi_snapshot']]
    except KeyError:
        raise _fail_evidence() from None
    try:
        envelope_text = envelope_bytes.decode('utf-8', 'strict')
    except UnicodeDecodeError:
        raise CampaignEnvelopeError(_METADATA + ' : enveloppe illisible') from None
    try:
        profile_text = profile_bytes.decode('utf-8', 'strict')
    except UnicodeDecodeError:
        raise ProfileError('profil : texte illisible') from None
    if '\r' in envelope_text:
        raise CampaignEnvelopeError(_METADATA + ' : enveloppe illisible') from None
    if '\r' in profile_text:
        raise ProfileError('profil : texte illisible') from None
    envelope = parse_envelope(envelope_text)
    profile = parse_profile(profile_text)
    decl, py_version = _extract_pyproject(pyproject_bytes)
    if manifest.campaign_id != envelope.campaign.id:
        raise _fail_evidence() from None
    if manifest.component != envelope.campaign.component:
        raise _fail_evidence() from None
    if manifest.verified_at != envelope.selection.verified_at:
        raise _fail_evidence() from None
    if envelope.selection.snapshot != role_path['pypi_snapshot']:
        raise _fail_evidence() from None
    snap_sha = _sha(snapshot_bytes)
    if snap_sha != envelope.selection.snapshot_sha256:
        raise _fail_evidence() from None
    mdists = [f for f in manifest.files if f.role == 'distribution']
    seen: dict = {}
    for f in mdists:
        base = f.path.split('/')[-1]
        if base in seen:
            raise _fail_evidence() from None
        seen[base] = f.sha256
    emap: dict = {}
    for d in envelope.distributions:
        if d.filename in emap:
            raise _fail_evidence() from None
        emap[d.filename] = d.sha256
    if set(seen) != set(emap):
        raise _fail_evidence() from None
    for base, sha in seen.items():
        if emap[base] != sha:
            raise _fail_evidence() from None
    if not (profile.cython_version == manifest.cython_version == envelope.toolchain.cython == py_version):
        raise _fail_mismatch() from None
    dists = tuple(sorted(seen.items()))
    return FileConsistency(
        campaign_id=manifest.campaign_id,
        cython_version=manifest.cython_version,
        manifest_sha256=_sha(manifest_bytes),
        envelope_sha256=_sha(envelope_bytes),
        profile_sha256=_sha(profile_bytes),
        pyproject_sha256=_sha(pyproject_bytes),
        snapshot_sha256=snap_sha,
        distributions=dists,
        pyproject_decl=decl,
        pyproject_version=py_version,
    )
