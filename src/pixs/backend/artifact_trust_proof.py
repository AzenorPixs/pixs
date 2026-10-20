"""Preuves de distribution du lot N03.

Assemblage par port signataire fiable, verification reelle Ed25519
par OpenSSL isole. Aucune cle privee manipulee ici.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import os
import re
import subprocess
import tempfile
from collections.abc import Callable
from pixs.backend.artifact_trust_materials import ArtifactTrustRefused
from pixs.backend.artifact_trust_materials import canonical_bundle_bytes
from pixs.backend.artifact_trust_materials import check_revocation_policy
from pixs.backend.artifact_trust_materials import decode_pem_spki_key32
from pixs.backend.artifact_trust_materials import key_fingerprint_hex
from pixs.backend.artifact_trust_materials import validate_anchor
from pixs.backend.artifact_trust_materials import validate_authorities
from pixs.backend.artifact_trust_materials import validate_channel
from pixs.backend.artifact_trust_materials import validate_bundle_structure
__all__ = ["OPENSSL_PATH", "assemble_proof", "canonical_proof_bytes", "parse_bundle_json", "parse_proof_json", "proof_sha256", "verify_bundle_signature", "verify_proof"]
OPENSSL_PATH = "/usr/bin/openssl"
OPENSSL_TIMEOUT = 10
MAX_JSON_BYTES = 65536
MAX_CANONICAL_BYTES = 16384
MAX_FIELD_LEN = 256
_HEX64_RE = re.compile(r"[0-9a-f]{64}")
_HEX128_RE = re.compile(r"[0-9a-f]{128}")
_SIGNED = ("allowed_operations", "artifact_sha256", "channel", "compatibility_evidence_sha256", "composition", "critical_findings", "inventory_sha256", "key_id", "prev_version", "proof_version", "provenance_sha256", "security_waivers", "source", "version")
_OPS = ("install", "startup", "upgrade")
SignerPort = Callable[[bytes], bytes]


def _deny(code: str) -> None:
    raise ArtifactTrustRefused(code) from None


def _drop(token: str) -> None:
    _deny("PROOF_MALFORMED")


def _unique(pairs: list) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            _deny("PROOF_MALFORMED")
        result[key] = value
    return result


def _label(value: object) -> str:
    if type(value) is not str:
        _deny("PROOF_MALFORMED")
    assert type(value) is str
    if value == "" or len(value) > MAX_FIELD_LEN:
        _deny("PROOF_MALFORMED")
    try:
        value.encode("utf-8")
    except UnicodeError:
        _deny("PROOF_MALFORMED")
    return value


def _version_label(value: object) -> str:
    if type(value) is not str:
        _deny("PROOF_MALFORMED")
    assert type(value) is str
    if len(value) > MAX_FIELD_LEN:
        _deny("PROOF_MALFORMED")
    try:
        value.encode("utf-8")
    except UnicodeError:
        _deny("PROOF_MALFORMED")
    return value


def _digest(value: object) -> str:
    if type(value) is not str:
        _deny("PROOF_MALFORMED")
    assert type(value) is str
    if _HEX64_RE.fullmatch(value) is None:
        _deny("PROOF_MALFORMED")
    return value


def _signature(value: object) -> str:
    if type(value) is not str:
        _deny("PROOF_MALFORMED")
    assert type(value) is str
    if _HEX128_RE.fullmatch(value) is None:
        _deny("PROOF_MALFORMED")
    return value


def _evidence(value: object) -> str:
    if type(value) is not str:
        _deny("PROOF_MALFORMED")
    assert type(value) is str
    if value != "" and _HEX64_RE.fullmatch(value) is None:
        _deny("PROOF_MALFORMED")
    return value


def _load(text: str) -> dict:
    if type(text) is not str:
        _deny("PROOF_MALFORMED")
    try:
        raw = text.encode("utf-8")
    except UnicodeError:
        _deny("PROOF_MALFORMED")
    if len(raw) == 0 or len(raw) > MAX_JSON_BYTES:
        _deny("PROOF_MALFORMED")
    try:
        parsed = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique, parse_constant=_drop)
    except ArtifactTrustRefused:
        raise
    except ValueError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    except RecursionError:
        _deny("PROOF_MALFORMED")
    if type(parsed) is not dict:
        _deny("PROOF_MALFORMED")
    return parsed


def _waivers(items: object, now: int) -> list:
    if type(items) is not list or len(items) > 8:
        _deny("PROOF_MALFORMED")
    checked: list[dict] = []
    for entry in items:
        if type(entry) is not dict or set(entry.keys()) != {"finding_id", "waiver_id", "reason", "expires_at", "audit_receipt_sha256"}:
            _deny("PROOF_MALFORMED")
        try:
            finding = entry["finding_id"]
            waiver = entry["waiver_id"]
            reason = entry["reason"]
            expiry = entry["expires_at"]
            receipt = entry["audit_receipt_sha256"]
        except KeyError:
            _deny("PROOF_MALFORMED")
        _label(finding)
        _label(waiver)
        _label(reason)
        if type(expiry) is bool or type(expiry) is not int or not (expiry > now):
            _deny("WAIVER_EXPIRED")
        _digest(receipt)
        checked.append({"finding_id": finding, "waiver_id": waiver, "reason": reason, "expires_at": expiry, "audit_receipt_sha256": receipt})
    return checked


def _signed_content(content: object, now: int) -> dict:
    if type(content) is not dict or set(content.keys()) != set(_SIGNED):
        _deny("PROOF_MALFORMED")
    try:
        allowed = content["allowed_operations"]
        artifact = content["artifact_sha256"]
        channel = content["channel"]
        evidence = content["compatibility_evidence_sha256"]
        composition = content["composition"]
        findings = content["critical_findings"]
        inventory = content["inventory_sha256"]
        key_id = content["key_id"]
        prev = content["prev_version"]
        version_tag = content["proof_version"]
        provenance = content["provenance_sha256"]
        waivers = content["security_waivers"]
        source = content["source"]
        version = content["version"]
    except KeyError:
        _deny("PROOF_MALFORMED")
    if type(version_tag) is bool or type(version_tag) is not int or version_tag != 1:
        _deny("PROOF_MALFORMED")
    _label(channel)
    _label(version)
    _version_label(prev)
    _label(source)
    _label(composition)
    _digest(artifact)
    _digest(provenance)
    _digest(inventory)
    _label(key_id)
    _evidence(evidence)
    if type(allowed) is not list or len(allowed) == 0 or len(allowed) > 3:
        _deny("PROOF_MALFORMED")
    seen: set[str] = set()
    for operation in allowed:
        _label(operation)
        if operation not in _OPS or operation in seen:
            _deny("PROOF_MALFORMED")
        seen.add(operation)
    if type(findings) is not list or len(findings) > 16:
        _deny("PROOF_MALFORMED")
    found: set[str] = set()
    for finding in findings:
        _label(finding)
        if finding in found:
            _deny("PROOF_MALFORMED")
        found.add(finding)
    checked_waivers = _waivers(waivers, now)
    return {"allowed_operations": list(allowed), "artifact_sha256": artifact, "channel": channel, "compatibility_evidence_sha256": evidence, "composition": composition, "critical_findings": list(findings), "inventory_sha256": inventory, "key_id": key_id, "prev_version": prev, "proof_version": 1, "provenance_sha256": provenance, "security_waivers": checked_waivers, "source": source, "version": version}


def parse_proof_json(text: str) -> dict:
    parsed = _load(text)
    if set(parsed.keys()) != (set(_SIGNED) | {"signature_hex", "proof_sha256"}):
        _deny("PROOF_MALFORMED")
    try:
        signed = {key: parsed[key] for key in _SIGNED}
        signature = parsed["signature_hex"]
        digest = parsed["proof_sha256"]
    except KeyError:
        _deny("PROOF_MALFORMED")
    _signature(signature)
    _digest(digest)
    _signed_content(signed, 1)
    return parsed


def parse_bundle_json(text: str) -> dict:
    from pixs.backend.artifact_trust_materials import validate_bundle_structure
    parsed = _load(text)
    validate_bundle_structure(parsed)
    return parsed


def canonical_proof_bytes(content: object) -> bytes:
    if type(content) is not dict:
        _deny("PROOF_MALFORMED")
    try:
        useful = {key: content[key] for key in _SIGNED}
    except KeyError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    useful = _signed_content(useful, 1)
    try:
        raw = json.dumps(useful, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    except ValueError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    except RecursionError:
        _deny("PROOF_MALFORMED")
    if len(raw) == 0 or len(raw) > MAX_CANONICAL_BYTES:
        _deny("PROOF_MALFORMED")
    return raw


def proof_sha256(content: object) -> str:
    if type(content) is not dict:
        _deny("PROOF_MALFORMED")
    try:
        signature_hex = content["signature_hex"]
    except KeyError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    _signature(signature_hex)
    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        _deny("PROOF_MALFORMED")
    if len(signature) != 64:
        _deny("PROOF_MALFORMED")
    try:
        signed = {key: content[key] for key in _SIGNED}
    except KeyError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    data = canonical_proof_bytes(signed)
    try:
        return hashlib.sha256(data + signature).hexdigest()
    except ValueError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    _deny("PROOF_MALFORMED")
    return ""


def _ossl_verify(public_pem: bytes, data: bytes, signature: bytes, parent: str) -> bool:
    if type(public_pem) is not bytes or type(data) is not bytes or type(signature) is not bytes:
        return False
    if not (80 <= len(public_pem) <= 4096 and 1 <= len(data) <= MAX_CANONICAL_BYTES and len(signature) == 64):
        return False
    if type(parent) is not str or parent == "":
        return False
    try:
        if not os.path.isdir(parent):
            return False
    except OSError:
        return False
    except ValueError:
        return False
    try:
        with tempfile.TemporaryDirectory(prefix="artifact-trust-", dir=parent) as workdir:
            pub_path = os.path.join(workdir, "pub.pem")
            data_path = os.path.join(workdir, "data.bin")
            sig_path = os.path.join(workdir, "sig.bin")
            with open(pub_path, "wb") as handle:
                handle.write(public_pem)
            with open(data_path, "wb") as handle:
                handle.write(data)
            with open(sig_path, "wb") as handle:
                handle.write(signature)
            command = [OPENSSL_PATH, "pkeyutl", "-verify", "-pubin", "-inkey", pub_path, "-rawin", "-in", data_path, "-sigfile", sig_path]
            done = subprocess.run(command, shell=False, timeout=OPENSSL_TIMEOUT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return done.returncode == 0
    except OSError:
        return False
    except ValueError:
        return False
    except subprocess.TimeoutExpired:
        return False


def assemble_proof(*, channel: str, version: str, prev_version: str, source: str, composition: str, artifact_sha256: str, provenance_sha256: str, inventory_sha256: str, key_id: str, allowed_operations: list, critical_findings: list, security_waivers: list, compatibility_evidence_sha256: str, signer: SignerPort) -> dict:
    if not callable(signer):
        _deny("POLICY_MALFORMED")
    useful = {"allowed_operations": allowed_operations, "artifact_sha256": artifact_sha256, "channel": channel, "compatibility_evidence_sha256": compatibility_evidence_sha256, "composition": composition, "critical_findings": critical_findings, "inventory_sha256": inventory_sha256, "key_id": key_id, "prev_version": prev_version, "proof_version": 1, "provenance_sha256": provenance_sha256, "security_waivers": security_waivers, "source": source, "version": version}
    useful = _signed_content(useful, 1)
    data = canonical_proof_bytes(useful)
    try:
        signature = signer(data)
    except ArtifactTrustRefused:
        raise
    except ValueError:
        _deny("SIGNER_FAILED")
    except TypeError:
        _deny("SIGNER_FAILED")
    except OSError:
        _deny("SIGNER_FAILED")
    except subprocess.TimeoutExpired:
        _deny("SIGNER_FAILED")
    if type(signature) is not bytes or len(signature) != 64:
        _deny("SIGNER_FAILED")
    result = {"allowed_operations": list(useful["allowed_operations"]), "artifact_sha256": useful["artifact_sha256"], "channel": useful["channel"], "compatibility_evidence_sha256": useful["compatibility_evidence_sha256"], "composition": useful["composition"], "critical_findings": list(useful["critical_findings"]), "inventory_sha256": useful["inventory_sha256"], "key_id": useful["key_id"], "prev_version": useful["prev_version"], "proof_version": 1, "provenance_sha256": useful["provenance_sha256"], "security_waivers": [dict(item) for item in useful["security_waivers"]], "source": useful["source"], "version": useful["version"]}
    result["signature_hex"] = signature.hex()
    try:
        result["proof_sha256"] = hashlib.sha256(data + signature).hexdigest()
    except ValueError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    return result


def verify_bundle_signature(bundle: dict, anchor_pem: bytes, anchor_id: str, now: int, floor: int, parent: str) -> None:
    if type(bundle) is not dict or type(anchor_id) is not str:
        _deny("BUNDLE_MALFORMED")
    try:
        issuer = bundle["issuer_key_id"]
        signature_hex = bundle["bundle_signature_hex"]
    except KeyError:
        _deny("BUNDLE_MALFORMED")
    except TypeError:
        _deny("BUNDLE_MALFORMED")
    if issuer != anchor_id:
        _deny("BUNDLE_MALFORMED")
    _signature(signature_hex)
    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        _deny("BUNDLE_MALFORMED")
    data = canonical_bundle_bytes(bundle)
    if type(anchor_pem) is str:
        try:
            raw = anchor_pem.encode("ascii")
        except UnicodeError:
            _deny("BUNDLE_MALFORMED")
    elif type(anchor_pem) is bytes:
        raw = anchor_pem
    else:
        _deny("BUNDLE_MALFORMED")
    check_revocation_policy(issuer, key_fingerprint_hex(raw), bundle, now, 0)
    if bundle["sequence"] < floor:
        _deny("BUNDLE_STALE")
    if not _ossl_verify(raw, data, signature, parent):
        _deny("SIGNATURE_INVALID")


def verify_proof(content: dict, anchor: dict, bundle: dict, authorities: dict, stable_id: str, security_id: str, experimental_id: str, now: int, parent: str) -> dict:
    checked_anchor = validate_anchor(anchor)
    bundle = validate_bundle_structure(bundle)
    checked_authorities = validate_authorities(stable_id, security_id, experimental_id, authorities)
    if type(content) is not dict or set(content.keys()) != (set(_SIGNED) | {"signature_hex", "proof_sha256"}):
        _deny("PROOF_MALFORMED")
    try:
        signed = {key: content[key] for key in _SIGNED}
    except KeyError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    if type(now) is bool or type(now) is not int:
        _deny("POLICY_MALFORMED")
    checked = _signed_content(signed, now)
    try:
        expected = content["proof_sha256"]
        signature_hex = content["signature_hex"]
    except KeyError:
        _deny("PROOF_MALFORMED")
    except TypeError:
        _deny("PROOF_MALFORMED")
    _digest(expected)
    _signature(signature_hex)
    if not hmac.compare_digest(proof_sha256({**checked, "signature_hex": signature_hex}), expected):
        _deny("SIGNATURE_INVALID")
    signer_id = checked["key_id"]
    if signer_id not in checked_authorities:
        _deny("AUTHORITY_UNKNOWN")
    entry = checked_authorities[signer_id]
    validate_channel(checked["channel"], entry["channels"])
    if not (checked_anchor["valid_from"] <= now < checked_anchor["valid_until"]):
        _deny("CERT_EXPIRED")
    if not (entry["valid_from"] <= now < entry["valid_until"]):
        _deny("CERT_EXPIRED")
    if type(bundle) is not dict:
        _deny("BUNDLE_MALFORMED")
    verify_bundle_signature(bundle, checked_anchor["public_key_pem"], checked_anchor["anchor_id"], now, checked_anchor["sequence_floor"], parent)
    raw_entry = entry["public_key_pem"]
    if type(raw_entry) is str:
        try:
            raw_signer = raw_entry.encode("ascii")
        except UnicodeError:
            _deny("PROOF_MALFORMED")
    elif type(raw_entry) is bytes:
        raw_signer = raw_entry
    else:
        _deny("PROOF_MALFORMED")
    fingerprint = key_fingerprint_hex(raw_signer)
    check_revocation_policy(signer_id, fingerprint, bundle, now, checked_anchor["sequence_floor"])
    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        _deny("PROOF_MALFORMED")
    data = canonical_proof_bytes(checked)
    if not _ossl_verify(raw_signer, data, signature, parent):
        _deny("SIGNATURE_INVALID")
    validate_channel(checked["channel"], ("stable", "security", "experimental"))
    return {"allowed_operations": list(checked["allowed_operations"]), "artifact_sha256": checked["artifact_sha256"], "channel": checked["channel"], "compatibility_evidence_sha256": checked["compatibility_evidence_sha256"], "composition": checked["composition"], "critical_findings": list(checked["critical_findings"]), "inventory_sha256": checked["inventory_sha256"], "key_id": signer_id, "prev_version": checked["prev_version"], "proof_version": 1, "provenance_sha256": checked["provenance_sha256"], "security_waivers": [dict(item) for item in checked["security_waivers"]], "source": checked["source"], "version": checked["version"], "signature_hex": signature_hex, "proof_sha256": expected}
