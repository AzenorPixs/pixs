"""Gates avant installation, demarrage et mise a niveau.

Retournent les octets verifies. Politique, historique et recus
fournis par le port local de confiance, jamais lus depuis l auteur.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from pixs.backend.artifact_trust_materials import ArtifactTrustRefused
from pixs.backend.artifact_trust_materials import validate_channel
from pixs.backend.artifact_trust_proof import verify_proof
__all__ = ["VerifiedArtifact", "build_distribution_id", "check_install", "check_startup", "check_upgrade", "verify_immutability"]
MAX_ARTIFACT_BYTES = 67108864
MAX_SIDE_BYTES = 1048576
ArtifactProvider = Callable[[], dict[str, bytes]]


@dataclass(frozen=True, slots=True)
class VerifiedArtifact:
    operation: str
    channel: str
    version: str
    prev_version: str
    source: str
    composition: str
    artifact_sha256: str
    provenance_sha256: str
    inventory_sha256: str
    artifact: bytes
    provenance: bytes
    inventory: bytes


def _deny(code: str) -> None:
    raise ArtifactTrustRefused(code) from None


def build_distribution_id(channel: str, source: str, composition: str, version: str) -> str:
    for value in (channel, source, composition, version):
        if type(value) is not str or value == "" or len(value) > 256:
            _deny("POLICY_MALFORMED")
    try:
        raw = json.dumps([channel, source, composition, version], separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    except ValueError:
        _deny("POLICY_MALFORMED")
    except TypeError:
        _deny("POLICY_MALFORMED")
    except RecursionError:
        _deny("POLICY_MALFORMED")
    return raw.decode("utf-8")


def _checked_receipt(entry: object) -> dict:
    if type(entry) is not dict or set(entry.keys()) != {"waiver_id", "finding_id", "artifact_sha256", "reason", "expires_at", "audit_receipt_sha256"}:
        _deny("POLICY_MALFORMED")
    try:
        waiver = entry["waiver_id"]
        finding = entry["finding_id"]
        digest = entry["artifact_sha256"]
        reason = entry["reason"]
        expiry = entry["expires_at"]
        receipt = entry["audit_receipt_sha256"]
    except KeyError:
        _deny("POLICY_MALFORMED")
    for value in (waiver, finding, reason):
        if type(value) is not str or value == "" or len(value) > 256:
            _deny("POLICY_MALFORMED")
    if type(digest) is not str or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        _deny("POLICY_MALFORMED")
    if type(receipt) is not str or re.fullmatch(r"[0-9a-f]{64}", receipt) is None:
        _deny("POLICY_MALFORMED")
    if type(expiry) is bool or type(expiry) is not int:
        _deny("POLICY_MALFORMED")
    return {"waiver_id": waiver, "finding_id": finding, "artifact_sha256": digest, "reason": reason, "expires_at": expiry, "audit_receipt_sha256": receipt}


def _need_policy(policy: object) -> dict:
    if type(policy) is not dict or set(policy.keys()) != {"expected_channel", "expected_version", "expected_prev_version", "expected_source", "expected_composition", "audit_receipts", "compatibility_receipt"}:
        _deny("POLICY_MALFORMED")
    try:
        channel = policy["expected_channel"]
        version = policy["expected_version"]
        prev = policy["expected_prev_version"]
        source = policy["expected_source"]
        composition = policy["expected_composition"]
        receipts = policy["audit_receipts"]
        compat = policy["compatibility_receipt"]
    except KeyError:
        _deny("POLICY_MALFORMED")
    for value in (channel, version, source, composition):
        if type(value) is not str or value == "" or len(value) > 256:
            _deny("POLICY_MALFORMED")
    if type(prev) is not str or len(prev) > 256:
        _deny("POLICY_MALFORMED")
    if type(receipts) is not list or len(receipts) > 16:
        _deny("POLICY_MALFORMED")
    checked_receipts: list[dict] = []
    for entry in receipts:
        checked_receipts.append(_checked_receipt(entry))
    if compat is not None:
        if type(compat) is not dict or set(compat.keys()) != {"from_version", "to_version", "artifact_sha256", "evidence_sha256"}:
            _deny("POLICY_MALFORMED")
        try:
            from_version = compat["from_version"]
            to_version = compat["to_version"]
            artifact = compat["artifact_sha256"]
            evidence = compat["evidence_sha256"]
        except KeyError:
            _deny("POLICY_MALFORMED")
        for value in (from_version, to_version):
            if type(value) is not str or value == "" or len(value) > 256:
                _deny("POLICY_MALFORMED")
        if type(artifact) is not str or re.fullmatch(r"[0-9a-f]{64}", artifact) is None:
            _deny("POLICY_MALFORMED")
        if type(evidence) is not str or re.fullmatch(r"[0-9a-f]{64}", evidence) is None:
            _deny("POLICY_MALFORMED")
        checked_compat: dict | None = {"from_version": from_version, "to_version": to_version, "artifact_sha256": artifact, "evidence_sha256": evidence}
    else:
        checked_compat = None
    return {"expected_channel": channel, "expected_version": version, "expected_prev_version": prev, "expected_source": source, "expected_composition": composition, "audit_receipts": checked_receipts, "compatibility_receipt": checked_compat}


def _need_history(history: object) -> dict:
    if type(history) is not dict or len(history) > 256:
        _deny("POLICY_MALFORMED")
    checked: dict[str, dict] = {}
    for identity, digests in history.items():
        if type(identity) is not str or len(identity) == 0 or len(identity) > 1024:
            _deny("POLICY_MALFORMED")
        try:
            parts = json.loads(identity)
        except ValueError:
            _deny("POLICY_MALFORMED")
        except TypeError:
            _deny("POLICY_MALFORMED")
        except RecursionError:
            _deny("POLICY_MALFORMED")
        if type(parts) is not list or len(parts) != 4:
            _deny("POLICY_MALFORMED")
        for part in parts:
            if type(part) is not str or part == "":
                _deny("POLICY_MALFORMED")
        try:
            canonical = json.dumps(parts, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        except ValueError:
            _deny("POLICY_MALFORMED")
        except TypeError:
            _deny("POLICY_MALFORMED")
        except RecursionError:
            _deny("POLICY_MALFORMED")
        if canonical != identity:
            _deny("POLICY_MALFORMED")
        if type(digests) is not dict or set(digests.keys()) != {"artifact_sha256", "provenance_sha256", "inventory_sha256"}:
            _deny("POLICY_MALFORMED")
        for key in ("artifact_sha256", "provenance_sha256", "inventory_sha256"):
            try:
                value = digests[key]
            except KeyError:
                _deny("POLICY_MALFORMED")
            if type(value) is not str or re.fullmatch(r"[0-9a-f]{64}", value) is None:
                _deny("POLICY_MALFORMED")
        checked[identity] = {"artifact_sha256": digests["artifact_sha256"], "provenance_sha256": digests["provenance_sha256"], "inventory_sha256": digests["inventory_sha256"]}
    return checked


def verify_immutability(history: object, proof: dict, artifact_hex: str, provenance_hex: str, inventory_hex: str) -> None:
    checked_history = _need_history(history)
    if type(proof) is not dict:
        _deny("PROOF_MALFORMED")
    try:
        channel = proof["channel"]
        source = proof["source"]
        composition = proof["composition"]
        version = proof["version"]
        prev = proof["prev_version"]
    except KeyError:
        _deny("PROOF_MALFORMED")
    for value in (artifact_hex, provenance_hex, inventory_hex):
        if type(value) is not str or re.fullmatch(r"[0-9a-f]{64}", value) is None:
            _deny("PROOF_MALFORMED")
    identity = build_distribution_id(channel, source, composition, version)
    if identity in checked_history:
        current = checked_history[identity]
        if not (hmac.compare_digest(current["artifact_sha256"], artifact_hex) and hmac.compare_digest(current["provenance_sha256"], provenance_hex) and hmac.compare_digest(current["inventory_sha256"], inventory_hex)):
            _deny("IMMUTABLE_VIOLATION")
        return
    lineage_known = False
    for stored in checked_history.keys():
        try:
            parts = json.loads(stored)
        except ValueError:
            _deny("POLICY_MALFORMED")
        if parts[0] == channel and parts[1] == source and parts[2] == composition:
            lineage_known = True
            break
    if not lineage_known:
        if prev != "":
            _deny("IMMUTABLE_VIOLATION")
        return
    if prev == "":
        _deny("IMMUTABLE_VIOLATION")
    prev_identity = build_distribution_id(channel, source, composition, prev)
    if prev_identity not in checked_history:
        _deny("IMMUTABLE_VIOLATION")


def _read_once(provider: ArtifactProvider) -> dict:
    if not callable(provider):
        _deny("PROVIDER_FAILED")
    try:
        packet = provider()
    except ArtifactTrustRefused:
        raise
    except ValueError:
        _deny("PROVIDER_FAILED")
    except TypeError:
        _deny("PROVIDER_FAILED")
    except OSError:
        _deny("PROVIDER_FAILED")
    if type(packet) is not dict or set(packet.keys()) != {"artifact", "provenance", "inventory"}:
        _deny("PROVIDER_FAILED")
    try:
        artifact = packet["artifact"]
        provenance = packet["provenance"]
        inventory = packet["inventory"]
    except KeyError:
        _deny("PROVIDER_FAILED")
    for content, limit in ((artifact, MAX_ARTIFACT_BYTES), (provenance, MAX_SIDE_BYTES), (inventory, MAX_SIDE_BYTES)):
        if type(content) is not bytes or len(content) == 0 or len(content) > limit:
            _deny("PROVIDER_FAILED")
    return {"artifact": artifact, "provenance": provenance, "inventory": inventory}


def _check(operation: str, proof: dict, anchor: dict, bundle: dict, authorities: dict, stable_id: str, security_id: str, experimental_id: str, policy: dict, now: int, provider: ArtifactProvider, parent: str, history: dict) -> VerifiedArtifact:
    if operation not in ("install", "startup", "upgrade"):
        _deny("POLICY_MALFORMED")
    if type(now) is bool or type(now) is not int or type(parent) is not str or parent == "":
        _deny("POLICY_MALFORMED")
    checked_policy = _need_policy(policy)
    checked_history = _need_history(history)
    if type(proof) is not dict:
        _deny("PROOF_MALFORMED")
    if type(bundle) is not dict:
        _deny("BUNDLE_MALFORMED")
    if type(authorities) is not dict:
        _deny("POLICY_MALFORMED")
    checked = verify_proof(proof, anchor, bundle, authorities, stable_id, security_id, experimental_id, now, parent)
    validate_channel(checked["channel"], (checked_policy["expected_channel"],))
    packet = _read_once(provider)
    artifact = packet["artifact"]
    provenance = packet["provenance"]
    inventory = packet["inventory"]
    try:
        artifact_hex = hashlib.sha256(artifact).hexdigest()
        provenance_hex = hashlib.sha256(provenance).hexdigest()
        inventory_hex = hashlib.sha256(inventory).hexdigest()
    except ValueError:
        _deny("PROVIDER_FAILED")
    except TypeError:
        _deny("PROVIDER_FAILED")
    if checked["version"] != checked_policy["expected_version"] or checked["source"] != checked_policy["expected_source"] or checked["composition"] != checked_policy["expected_composition"] or checked["prev_version"] != checked_policy["expected_prev_version"]:
        _deny("POLICY_MISMATCH")
    if operation not in checked["allowed_operations"]:
        _deny("OPERATION_FORBIDDEN")
    if operation == "upgrade":
        if checked["compatibility_evidence_sha256"] == "":
            _deny("COMPAT_MISMATCH")
        compat = checked_policy["compatibility_receipt"]
        if compat is None:
            _deny("COMPAT_MISMATCH")
        if compat["from_version"] != checked["prev_version"] or compat["to_version"] != checked["version"] or not hmac.compare_digest(compat["artifact_sha256"], artifact_hex) or not hmac.compare_digest(compat["evidence_sha256"], checked["compatibility_evidence_sha256"]):
            _deny("COMPAT_MISMATCH")
    else:
        if checked["compatibility_evidence_sha256"] != "":
            _deny("COMPAT_MISMATCH")
        if checked_policy["compatibility_receipt"] is not None:
            _deny("COMPAT_MISMATCH")
    if not hmac.compare_digest(artifact_hex, checked["artifact_sha256"]) or not hmac.compare_digest(provenance_hex, checked["provenance_sha256"]) or not hmac.compare_digest(inventory_hex, checked["inventory_sha256"]):
        _deny("ARTIFACT_MISMATCH")
    findings = list(checked["critical_findings"])
    waivers = [dict(item) for item in checked["security_waivers"]]
    receipts = list(checked_policy["audit_receipts"])
    if len(findings) != len(waivers):
        _deny("WAIVER_UNKNOWN")
    by_finding: dict[str, dict] = {}
    for waiver in waivers:
        finding = waiver["finding_id"]
        if finding in by_finding:
            _deny("WAIVER_UNKNOWN")
        by_finding[finding] = waiver
    if set(by_finding.keys()) != set(findings):
        _deny("WAIVER_UNKNOWN")
    for finding in findings:
        waiver = by_finding[finding]
        if waiver["expires_at"] <= now:
            _deny("WAIVER_EXPIRED")
        matched = None
        for receipt in receipts:
            if receipt["waiver_id"] == waiver["waiver_id"] and receipt["finding_id"] == finding and receipt["artifact_sha256"] == artifact_hex and receipt["reason"] == waiver["reason"] and receipt["expires_at"] == waiver["expires_at"] and receipt["audit_receipt_sha256"] == waiver["audit_receipt_sha256"]:
                matched = receipt
                break
        if matched is None:
            _deny("RECEIPT_UNKNOWN")
    verify_immutability(checked_history, checked, artifact_hex, provenance_hex, inventory_hex)
    return VerifiedArtifact(operation=operation, channel=checked["channel"], version=checked["version"], prev_version=checked["prev_version"], source=checked["source"], composition=checked["composition"], artifact_sha256=artifact_hex, provenance_sha256=provenance_hex, inventory_sha256=inventory_hex, artifact=artifact, provenance=provenance, inventory=inventory)


def check_install(proof, anchor, bundle, authorities, stable_id, security_id, experimental_id, policy, now, provider, parent, history):
    return _check("install", proof, anchor, bundle, authorities, stable_id, security_id, experimental_id, policy, now, provider, parent, history)


def check_startup(proof, anchor, bundle, authorities, stable_id, security_id, experimental_id, policy, now, provider, parent, history):
    return _check("startup", proof, anchor, bundle, authorities, stable_id, security_id, experimental_id, policy, now, provider, parent, history)


def check_upgrade(proof, anchor, bundle, authorities, stable_id, security_id, experimental_id, policy, now, provider, parent, history):
    return _check("upgrade", proof, anchor, bundle, authorities, stable_id, security_id, experimental_id, policy, now, provider, parent, history)
