"""Materiaux publics de confiance du lot N03.

Purs, sans reseau, sans subprocess, sans filesystem. Les donnees
viennent de l appelant de confiance. Identifiants en anglais,
commentaires et docstrings en francais. Refus a code sur.
"""
from __future__ import annotations
import base64
import hashlib
import json
import re
__all__ = ["ArtifactTrustRefused", "canonical_bundle_bytes", "check_revocation_policy", "decode_pem_spki_key32", "key_fingerprint_hex", "validate_anchor", "validate_authorities", "validate_bundle_structure", "validate_channel"]
MAX_PEM_BYTES = 4096
MAX_KEY_ID_LEN = 128
MAX_ID_LEN = 128
MAX_REVOKED_KEYS = 256
MAX_AUTHORITIES = 32
_SPKI_PREFIX = bytes.fromhex("302a300506032b6570032100")
_SPKI_LEN = 44
_HEX128_RE = re.compile(r"[0-9a-f]{128}")
_HEX64_RE = re.compile(r"[0-9a-f]{64}")
_ALLOWED_CHANNELS = ("stable", "security", "experimental")


class ArtifactTrustRefused(ValueError):
    """Echec ferme a code sur, sans valeur libre."""
    def __init__(self, code: str, observed: str = "", expected: str = "") -> None:
        super().__init__(code)
        self.code = code
        self.observed = observed
        self.expected = expected


def _deny(code: str) -> None:
    raise ArtifactTrustRefused(code) from None


def _deny_channel(observed: str, expected_list: list) -> None:
    # Constate et attendu uniquement si valeurs enumerees connues.
    safe_observed = observed if observed in _ALLOWED_CHANNELS else ""
    safe_expected = ",".join([e for e in expected_list if e in _ALLOWED_CHANNELS])
    raise ArtifactTrustRefused("CHANNEL_MISMATCH", safe_observed, safe_expected) from None


def _need_text(value: object, limit: int, code: str) -> str:
    if type(value) is not str:
        _deny(code)
    assert type(value) is str
    if value == "" or len(value) > limit:
        _deny(code)
    try:
        value.encode("utf-8")
    except UnicodeError:
        _deny(code)
    except ValueError:
        _deny(code)
    return value


def _need_moment(value: object, code: str) -> int:
    if type(value) is bool or type(value) is not int:
        _deny(code)
    assert type(value) is int
    if value < 0:
        _deny(code)
    return value


def decode_pem_spki_key32(pem: object) -> bytes:
    # Decode strict PEM PUBLIC KEY vers cle Ed25519 32 octets.
    if type(pem) is str:
        try:
            raw = pem.encode("ascii")
        except UnicodeError:
            _deny("BUNDLE_MALFORMED")
        except ValueError:
            _deny("BUNDLE_MALFORMED")
    elif type(pem) is bytes:
        raw = pem
    else:
        _deny("BUNDLE_MALFORMED")
    if len(raw) == 0 or len(raw) > MAX_PEM_BYTES:
        _deny("BUNDLE_MALFORMED")
    try:
        lines = raw.strip().split(b"\n")
    except ValueError:
        _deny("BUNDLE_MALFORMED")
    except TypeError:
        _deny("BUNDLE_MALFORMED")
    if len(lines) < 3:
        _deny("BUNDLE_MALFORMED")
    if lines[0].strip() != b"-----BEGIN PUBLIC KEY-----":
        _deny("BUNDLE_MALFORMED")
    if lines[-1].strip() != b"-----END PUBLIC KEY-----":
        _deny("BUNDLE_MALFORMED")
    body = b"".join(line.strip() for line in lines[1:-1])
    if body == b"":
        _deny("BUNDLE_MALFORMED")
    try:
        der = base64.b64decode(body, validate=True)
    except ValueError:
        _deny("BUNDLE_MALFORMED")
    except TypeError:
        _deny("BUNDLE_MALFORMED")
    if len(der) != _SPKI_LEN:
        _deny("BUNDLE_MALFORMED")
    if der[:12] != _SPKI_PREFIX:
        _deny("BUNDLE_MALFORMED")
    return der[12:]


def key_fingerprint_hex(pem: object) -> str:
    # Empreinte SHA256 des 32 octets, comparee meme sous alias.
    raw32 = decode_pem_spki_key32(pem)
    try:
        return hashlib.sha256(raw32).hexdigest()
    except ValueError:
        _deny("BUNDLE_MALFORMED")
    except TypeError:
        _deny("BUNDLE_MALFORMED")
    _deny("BUNDLE_MALFORMED")
    return ""


def _checked_pem(value: object, code: str) -> bytes:
    decode_pem_spki_key32(value)
    if type(value) is str:
        return value.encode("ascii")
    return value


def validate_channel(channel: object, allowed: object) -> str:
    current = _need_text(channel, 64, "CHANNEL_MISMATCH")
    if type(allowed) is not tuple and type(allowed) is not list:
        _deny("POLICY_MALFORMED")
    if len(allowed) == 0 or len(allowed) > 16:
        _deny("POLICY_MALFORMED")
    seen: set[str] = set()
    for entry in allowed:
        name = _need_text(entry, 64, "POLICY_MALFORMED")
        if name not in _ALLOWED_CHANNELS:
            _deny("POLICY_MALFORMED")
        if name in seen:
            _deny("POLICY_MALFORMED")
        seen.add(name)
    if current not in seen:
        _deny_channel(current, sorted(seen))
    return current


def _checked_entry(entry: object) -> dict:
    if type(entry) is not dict:
        _deny("POLICY_MALFORMED")
    if set(entry.keys()) != {"public_key_pem", "channels", "valid_from", "valid_until"}:
        _deny("POLICY_MALFORMED")
    try:
        pem = entry["public_key_pem"]
        channels = entry["channels"]
        start = entry["valid_from"]
        end = entry["valid_until"]
    except KeyError:
        _deny("POLICY_MALFORMED")
    _checked_pem(pem, "POLICY_MALFORMED")
    if type(channels) is not tuple and type(channels) is not list:
        _deny("POLICY_MALFORMED")
    if len(channels) == 0 or len(channels) > 8:
        _deny("POLICY_MALFORMED")
    seen: set[str] = set()
    for item in channels:
        name = _need_text(item, 64, "POLICY_MALFORMED")
        if name not in _ALLOWED_CHANNELS:
            _deny("POLICY_MALFORMED")
        if name in seen:
            _deny("POLICY_MALFORMED")
        seen.add(name)
    _need_moment(start, "POLICY_MALFORMED")
    _need_moment(end, "POLICY_MALFORMED")
    if start >= end:
        _deny("POLICY_MALFORMED")
    return {"public_key_pem": pem, "channels": list(channels), "valid_from": start, "valid_until": end}


def validate_authorities(stable_id: object, security_id: object, experimental_id: object, authorities: object) -> dict:
    a = _need_text(stable_id, MAX_KEY_ID_LEN, "POLICY_MALFORMED")
    b = _need_text(security_id, MAX_KEY_ID_LEN, "POLICY_MALFORMED")
    c = _need_text(experimental_id, MAX_KEY_ID_LEN, "POLICY_MALFORMED")
    if type(authorities) is not dict:
        _deny("POLICY_MALFORMED")
    if len(authorities) == 0 or len(authorities) > MAX_AUTHORITIES:
        _deny("POLICY_MALFORMED")
    for wanted in (a, b, c):
        if wanted not in authorities:
            _deny("POLICY_MALFORMED")
    checked: dict[str, dict] = {}
    for key_id, entry in authorities.items():
        _need_text(key_id, MAX_KEY_ID_LEN, "POLICY_MALFORMED")
        checked[key_id] = _checked_entry(entry)
    for key_id, required_channel in ((a, "stable"), (b, "security"), (c, "experimental")):
        if required_channel not in checked[key_id]["channels"]:
            _deny("AUTHORITY_MISMATCH")
    stable_group: set[bytes] = set()
    experimental_group: set[bytes] = set()
    for key_id, entry in checked.items():
        raw32 = decode_pem_spki_key32(entry["public_key_pem"])
        channels = entry["channels"]
        if "experimental" in channels:
            experimental_group.add(raw32)
        if "stable" in channels or "security" in channels:
            stable_group.add(raw32)
    for raw32 in experimental_group:
        if raw32 in stable_group:
            _deny("AUTHORITY_MISMATCH")
    return {key_id: dict(entry) for key_id, entry in checked.items()}


def validate_anchor(anchor: object) -> dict:
    if type(anchor) is not dict:
        _deny("POLICY_MALFORMED")
    if set(anchor.keys()) != {"anchor_id", "public_key_pem", "valid_from", "valid_until", "sequence_floor"}:
        _deny("POLICY_MALFORMED")
    try:
        anchor_id = anchor["anchor_id"]
        pem = anchor["public_key_pem"]
        start = anchor["valid_from"]
        end = anchor["valid_until"]
        floor = anchor["sequence_floor"]
    except KeyError:
        _deny("POLICY_MALFORMED")
    _need_text(anchor_id, MAX_ID_LEN, "POLICY_MALFORMED")
    _checked_pem(pem, "POLICY_MALFORMED")
    _need_moment(start, "POLICY_MALFORMED")
    _need_moment(end, "POLICY_MALFORMED")
    if start >= end:
        _deny("POLICY_MALFORMED")
    _need_moment(floor, "POLICY_MALFORMED")
    return {"anchor_id": anchor_id, "public_key_pem": pem, "valid_from": start, "valid_until": end, "sequence_floor": floor}


def validate_bundle_structure(bundle: object) -> dict:
    if type(bundle) is not dict:
        _deny("BUNDLE_MALFORMED")
    if set(bundle.keys()) != {"bundle_id", "bundle_version", "issuer_key_id", "issued_at", "valid_until", "sequence", "revoked_key_ids", "revoked_key_fingerprints", "bundle_signature_hex"}:
        _deny("BUNDLE_MALFORMED")
    try:
        bundle_id = bundle["bundle_id"]
        version = bundle["bundle_version"]
        issuer = bundle["issuer_key_id"]
        issued = bundle["issued_at"]
        valid = bundle["valid_until"]
        sequence = bundle["sequence"]
        revoked = bundle["revoked_key_ids"]
        fingerprints = bundle["revoked_key_fingerprints"]
        signature = bundle["bundle_signature_hex"]
    except KeyError:
        _deny("BUNDLE_MALFORMED")
    _need_text(bundle_id, MAX_ID_LEN, "BUNDLE_MALFORMED")
    if type(version) is bool or type(version) is not int or version != 1:
        _deny("BUNDLE_MALFORMED")
    _need_text(issuer, MAX_KEY_ID_LEN, "BUNDLE_MALFORMED")
    _need_moment(issued, "BUNDLE_MALFORMED")
    _need_moment(valid, "BUNDLE_MALFORMED")
    if issued >= valid:
        _deny("BUNDLE_MALFORMED")
    _need_moment(sequence, "BUNDLE_MALFORMED")
    if type(revoked) is not list or type(fingerprints) is not list:
        _deny("BUNDLE_MALFORMED")
    if len(revoked) > MAX_REVOKED_KEYS or len(fingerprints) > MAX_REVOKED_KEYS:
        _deny("BUNDLE_MALFORMED")
    seen: set[str] = set()
    for item in revoked:
        name = _need_text(item, MAX_KEY_ID_LEN, "BUNDLE_MALFORMED")
        if name in seen:
            _deny("BUNDLE_MALFORMED")
        seen.add(name)
    seen_fp: set[str] = set()
    for item in fingerprints:
        if type(item) is not str or _HEX64_RE.fullmatch(item) is None:
            _deny("BUNDLE_MALFORMED")
        if item in seen_fp:
            _deny("BUNDLE_MALFORMED")
        seen_fp.add(item)
    if type(signature) is not str or _HEX128_RE.fullmatch(signature) is None:
        _deny("BUNDLE_MALFORMED")
    return {"bundle_id": bundle_id, "bundle_version": 1, "issuer_key_id": issuer, "issued_at": issued, "valid_until": valid, "sequence": sequence, "revoked_key_ids": list(revoked), "revoked_key_fingerprints": list(fingerprints), "bundle_signature_hex": signature}


def canonical_bundle_bytes(bundle: dict) -> bytes:
    checked = validate_bundle_structure(bundle)
    useful = {"bundle_id": checked["bundle_id"], "bundle_version": 1, "issued_at": checked["issued_at"], "issuer_key_id": checked["issuer_key_id"], "revoked_key_fingerprints": sorted(checked["revoked_key_fingerprints"]), "revoked_key_ids": sorted(checked["revoked_key_ids"]), "sequence": checked["sequence"], "valid_until": checked["valid_until"]}
    try:
        raw = json.dumps(useful, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    except ValueError:
        _deny("BUNDLE_MALFORMED")
    except TypeError:
        _deny("BUNDLE_MALFORMED")
    except RecursionError:
        _deny("BUNDLE_MALFORMED")
    except UnicodeError:
        _deny("BUNDLE_MALFORMED")
    if len(raw) == 0 or len(raw) > 16384:
        _deny("BUNDLE_MALFORMED")
    return raw


def check_revocation_policy(key_id: object, fingerprint_hex: object, bundle: dict, now: object, floor: object) -> dict:
    target = _need_text(key_id, MAX_KEY_ID_LEN, "BUNDLE_MALFORMED")
    if type(fingerprint_hex) is not str or _HEX64_RE.fullmatch(fingerprint_hex) is None:
        _deny("BUNDLE_MALFORMED")
    checked = validate_bundle_structure(bundle)
    moment = _need_moment(now, "BUNDLE_EXPIRED")
    minimum = _need_moment(floor, "POLICY_MALFORMED")
    if not (checked["issued_at"] <= moment < checked["valid_until"]):
        _deny("BUNDLE_EXPIRED")
    if checked["sequence"] < minimum:
        _deny("BUNDLE_STALE")
    if target in checked["revoked_key_ids"]:
        _deny("REVOKED")
    if fingerprint_hex in checked["revoked_key_fingerprints"]:
        _deny("REVOKED")
    return checked
