"""Selection sur snapshot PyPI fige, constats non certifies S2b2.

Normes : https://packaging.python.org/en/latest/specifications/version-specifiers/
API : https://docs.pypi.org/api/json/
Pur : octets figes fournis, sans reseau, collecte, origine, registre,
admission, sonde ou compilation. Jamais la derniere version du jour,
seulement le maximum admissible DANS le snapshot donne. Stdlib seule.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

from pixs.pa_native.build_profile import ProfileError
from pixs.pa_native.campaign_envelope import CampaignEnvelopeError
from pixs.pa_native.campaign_envelope import parse_envelope

__all__ = [
    'SnapshotFile',
    'SnapshotSelection',
    'SnapshotSelectionError',
    'analyze_snapshot',
]

_EVIDENCE = 'PA01_CAMPAIGN_EVIDENCE_INVALID'
_METADATA = 'PA01_CAMPAIGN_METADATA_INVALID'
_SHA = re.compile(r'[0-9a-f]{64}')
_PUB = re.compile(
    r'^(?P<rel>[0-9]+(?:\.[0-9]+)*)'
    r'(?P<pre>[-_.]?(?:alpha|beta|preview|pre|rc|a|b|c)[-_.]?[0-9]*)?'
    r'(?P<post>(?:-[0-9]+|[-_.]?(?:post|rev|r)[-_.]?[0-9]*))?'
    r'(?P<dev>[-_.]?dev[-_.]?[0-9]*)?$',
    re.IGNORECASE,
)
_LOCAL = re.compile(r'[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*')
_EPOCH = re.compile(r'[0-9]+')


class SnapshotSelectionError(ProfileError):
    pass


@dataclass(frozen=True, slots=True)
class SnapshotFile:
    filename: str
    url: str
    sha256: str


@dataclass(frozen=True, slots=True)
class SnapshotSelection:
    project: str
    selected_key: str
    selected_normalized: str
    snapshot_sha256: str
    envelope_sha256: str
    files: tuple


class _Unparseable(ValueError):
    pass


def _fail() -> SnapshotSelectionError:
    return SnapshotSelectionError(_EVIDENCE + ' : preuve de selection invalide')


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_forbidden(value: str) -> bool:
    for c in value:
        o = ord(c)
        if o < 32 or 127 <= o <= 159 or 0xD800 <= o <= 0xDFFF:
            return True
    return False


def _text(value: object) -> str:
    if type(value) is not str or not value:
        raise _fail() from None
    if _is_forbidden(value):
        raise _fail() from None
    return value


def _norm_name(value: str) -> str:
    return re.sub(r'[-_.]+', '-', value).lower()


def _no_dupes(pairs: list) -> dict:
    keys = [k for k, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ValueError('cle dupliquee')
    return dict(pairs)


def _reject_constant(value: str) -> None:
    raise ValueError('constante interdite')


def _load_snapshot(data: bytes) -> dict:
    if type(data) is not bytes:
        raise _fail() from None
    try:
        text = data.decode('utf-8', 'strict')
    except UnicodeDecodeError:
        raise _fail() from None
    try:
        root = json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_reject_constant)
    except RecursionError:
        raise _fail() from None
    except ValueError:
        raise _fail() from None
    if type(root) is not dict:
        raise _fail() from None
    return root


def _to_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise _Unparseable() from None


def _parse_key(raw: str) -> dict:
    if type(raw) is not str or not raw:
        raise _Unparseable()
    t = raw.strip(' \t\n\r\f\u000b')
    if not t:
        raise _Unparseable()
    for c in t:
        o = ord(c)
        if o < 32 or 127 <= o <= 159 or 0xD800 <= o <= 0xDFFF:
            raise _Unparseable()
    if t[0] in 'vV':
        t = t[1:]
        if not t or t[0] in 'vV':
            raise _Unparseable()
    has_local = False
    if '+' in t:
        head, local = t.split('+', 1)
        if not local or _LOCAL.fullmatch(local) is None:
            raise _Unparseable()
        has_local = True
        t = head
        if not t:
            raise _Unparseable()
    epoch = 0
    if '!' in t:
        parts = t.split('!')
        if len(parts) != 2:
            raise _Unparseable()
        epart, t = parts
        if not epart or _EPOCH.fullmatch(epart) is None:
            raise _Unparseable()
        epoch = _to_int(epart)
        if not t:
            raise _Unparseable()
    m = _PUB.match(t)
    if m is None:
        raise _Unparseable()
    try:
        rel = tuple(_to_int(x) for x in m.group('rel').split('.'))
    except _Unparseable:
        raise _Unparseable() from None
    has_pre = m.group('pre') is not None
    has_post = m.group('post') is not None
    has_dev = m.group('dev') is not None
    post_num = -1
    if has_post:
        digits = re.search(r'[0-9]+', m.group('post'))
        post_num = _to_int(digits.group(0)) if digits is not None else 0
    rel_label = '.'.join(str(x) for x in rel)
    norm = rel_label
    if has_post:
        norm = norm + '.post' + str(post_num)
    if epoch:
        norm = str(epoch) + '!' + norm
    stripped = list(rel)
    while len(stripped) > 1 and stripped[-1] == 0:
        stripped.pop()
    return {
        'epoch': epoch,
        'rel': rel,
        'stripped': tuple(stripped),
        'has_pre': has_pre,
        'has_post': has_post,
        'has_dev': has_dev,
        'has_local': has_local,
        'post_num': post_num,
        'normalized': norm,
        'equiv': (epoch, tuple(stripped), post_num),
    }


def _lock_equiv(value: str) -> tuple:
    try:
        parsed = _parse_key(value)
    except _Unparseable:
        raise _fail() from None
    if parsed['has_pre'] or parsed['has_dev'] or parsed['has_local']:
        raise _fail() from None
    return parsed['equiv']


def analyze_snapshot(snapshot_bytes: bytes, envelope_bytes: bytes) -> SnapshotSelection:
    if type(snapshot_bytes) is not bytes:
        raise _fail() from None
    if type(envelope_bytes) is not bytes:
        raise _fail() from None
    try:
        envelope_text = envelope_bytes.decode('utf-8', 'strict')
    except UnicodeDecodeError:
        raise CampaignEnvelopeError(_METADATA + ' : enveloppe illisible') from None
    if '\r' in envelope_text:
        raise CampaignEnvelopeError(_METADATA + ' : enveloppe illisible') from None
    envelope = parse_envelope(envelope_text)
    root = _load_snapshot(snapshot_bytes)
    info = root.get('info')
    if type(info) is not dict:
        raise _fail() from None
    name = info.get('name')
    _text(name)
    if _norm_name(name) != 'cython':
        raise _fail() from None
    releases = root.get('releases')
    if type(releases) is not dict or not releases:
        raise _fail() from None
    parsed: dict = {}
    for key in releases:
        if type(key) is not str:
            raise _fail() from None
        try:
            parsed[key] = _parse_key(key)
        except _Unparseable:
            raise _fail() from None
    admissible = {k: v for k, v in parsed.items() if not v['has_pre'] and not v['has_dev'] and not v['has_local']}
    if not admissible:
        raise _fail() from None
    eligible: dict = {}
    officials: dict = {}
    for key, val in admissible.items():
        entries = releases[key]
        if type(entries) is not list:
            raise _fail() from None
        for item in entries:
            if type(item) is not dict:
                raise _fail() from None
            filename = item.get('filename')
            url = item.get('url')
            digests = item.get('digests')
            yanked = item.get('yanked')
            _text(filename)
            _text(url)
            if type(digests) is not dict:
                raise _fail() from None
            sha = digests.get('sha256')
            _text(sha)
            if _SHA.fullmatch(sha) is None:
                raise _fail() from None
            if type(yanked) is not bool:
                raise _fail() from None
        kept = []
        for item in entries:
            if item.get('yanked') is False:
                kept.append(SnapshotFile(filename=item.get('filename'), url=item.get('url'), sha256=item.get('digests').get('sha256')))
        if kept:
            eligible[key] = val
            officials[key] = kept
    if not eligible:
        raise _fail() from None
    seen_equiv: dict = {}
    for key, val in eligible.items():
        eq = (val['epoch'], val['stripped'], val['post_num'])
        if eq in seen_equiv:
            raise _fail() from None
        seen_equiv[eq] = key
    width = 1
    for val in eligible.values():
        if len(val['rel']) > width:
            width = len(val['rel'])
    best_key = ''
    best_ord: tuple = ()
    first = True
    for key, val in eligible.items():
        padded = tuple(val['rel']) + (0,) * (width - len(val['rel']))
        ordkey = (val['epoch'], padded, val['post_num'])
        if first or ordkey > best_ord:
            best_ord = ordkey
            best_key = key
            first = False
    raw_entries = releases[best_key]
    seen_names: set = set()
    for item in raw_entries:
        fn = item.get('filename')
        if fn in seen_names:
            raise _fail() from None
        seen_names.add(fn)
    official = officials[best_key]
    declared = list(envelope.distributions)
    if not declared:
        raise _fail() from None
    used: set = set()
    for decl in declared:
        hits = [i for i, off in enumerate(official) if off.filename == decl.filename and off.url == decl.url and off.sha256 == decl.sha256]
        if len(hits) != 1 or hits[0] in used:
            raise _fail() from None
        used.add(hits[0])
    if eligible[best_key]['equiv'] != _lock_equiv(envelope.toolchain.cython):
        raise _fail() from None
    snap_sha = _sha(snapshot_bytes)
    if snap_sha != envelope.selection.snapshot_sha256:
        raise _fail() from None
    return SnapshotSelection(
        project=name,
        selected_key=best_key,
        selected_normalized=eligible[best_key]['normalized'],
        snapshot_sha256=snap_sha,
        envelope_sha256=_sha(envelope_bytes),
        files=tuple(official),
    )
