"""C11 plan depuis capture epinglee, survivants seuls, sans activation."""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from build_frontend_composition import BuildError, BuildLimits, BuildPlan, build_plan
from build_frontend_selection import BatchCapture, SelectionError, SelectionLimits, capture_selection
from pixs.kernel.conformity import ConformityAttestation

_ENVELOPE_SCHEMA = "pixs.frontend.plan-envelope/1.0.0"
_SELECTION_SCHEMA = "pixs.frontend.selection/1.0.0"


class PlanError(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _no_dupes(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PlanError("SELECTION_JSON_INVALID")
        result[key] = value
    return result


def _reject_const(value: str) -> object:
    raise PlanError("SELECTION_JSON_INVALID")


def _checksum_build(build_limits: BuildLimits, context_fingerprint: str, declared_ids: tuple[str, ...]) -> str:
    payload = {
        "declared_owner_ids": list(declared_ids),
        "allowed_sources": list(build_limits.allowed_sources),
        "context_fingerprint": context_fingerprint,
        "max_manifest_bytes": build_limits.max_manifest_bytes,
        "max_manifests": build_limits.max_manifests,
        "max_total_bytes": build_limits.max_total_bytes,
        "schema": _ENVELOPE_SCHEMA,
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True, slots=True)
class PlanEnvelope:
    capture: BatchCapture
    plan: BuildPlan
    ignored_attestation_indices: tuple[int, ...]
    build_limits: BuildLimits
    context_checksum: str
    declared_owner_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.capture) is not BatchCapture or type(self.plan) is not BuildPlan:
            raise PlanError("PLAN_ENVELOPE_INVALID")
        if type(self.ignored_attestation_indices) is not tuple:
            raise PlanError("PLAN_ENVELOPE_INVALID")
        if type(self.build_limits) is not BuildLimits or type(self.context_checksum) is not str:
            raise PlanError("PLAN_ENVELOPE_INVALID")
        try:
            self.build_limits.__post_init__()
        except BuildError as error:
            raise PlanError("PLAN_LIMITS_INVALID") from error
        if (type(self.declared_owner_ids) is not tuple or not self.declared_owner_ids
                or any(type(x) is not str or not x for x in self.declared_owner_ids)):
            raise PlanError("PLAN_ENVELOPE_INVALID")
        if len(set(self.declared_owner_ids)) != len(self.declared_owner_ids):
            raise PlanError("PLAN_ENVELOPE_INVALID")
        if self.context_checksum != _checksum_build(self.build_limits, self.capture.context_fingerprint, self.declared_owner_ids):
            raise PlanError("PLAN_CHECKSUM_MISMATCH")
        n_att = len(self.capture.composition.attestations)
        if any(type(i) is not int or i < 0 or i >= n_att for i in self.ignored_attestation_indices):
            raise PlanError("PLAN_ENVELOPE_INVALID")
        if len(set(self.ignored_attestation_indices)) != len(self.ignored_attestation_indices):
            raise PlanError("PLAN_ENVELOPE_INVALID")
        captured_ids = {o.owner for o in self.capture.owners}
        for idx in self.ignored_attestation_indices:
            if type(idx) is not int or isinstance(idx, bool) or idx < 0 or idx >= n_att:
                raise PlanError("PLAN_ENVELOPE_INVALID")
            if self.capture.composition.attestations[idx].component_id in captured_ids:
                raise PlanError("PLAN_ENVELOPE_INVALID")
        allowed = tuple(self.build_limits.allowed_sources)
        expected_allowed = tuple(o.manifest.path for o in self.capture.owners)
        if allowed != expected_allowed:
            raise PlanError("PLAN_ENVELOPE_INVALID")
        if set(self.plan.order) != captured_ids or not captured_ids.issubset(self.declared_owner_ids):
            raise PlanError("PLAN_ENVELOPE_INVALID")
        expected_ignored = tuple(i for i, att in enumerate(self.capture.composition.attestations)
                                 if att.component_id in self.declared_owner_ids and att.component_id not in captured_ids)
        if self.ignored_attestation_indices != expected_ignored:
            raise PlanError("PLAN_ENVELOPE_INVALID")
        by_manifest = {o.owner: o.manifest.sha256 for o in self.capture.owners}
        for owner, digest in self.plan.sources_sha256:
            if by_manifest.get(owner) != digest:
                raise PlanError("PLAN_ENVELOPE_INVALID")
        if self.plan.globally_compatible is not False:
            raise PlanError("PLAN_ENVELOPE_INVALID")

    def to_dict(self) -> dict:
        return {
            "schema": _ENVELOPE_SCHEMA,
            "capture": self.capture.to_dict(),
            "plan": self.plan.to_dict(),
            "ignored_attestation_indices": list(self.ignored_attestation_indices),
            "build_limits": {
                "max_manifests": self.build_limits.max_manifests,
                "max_manifest_bytes": self.build_limits.max_manifest_bytes,
                "max_total_bytes": self.build_limits.max_total_bytes,
                "allowed_sources": list(self.build_limits.allowed_sources),
            },
            "context_checksum": self.context_checksum,
            "declared_owner_ids": list(self.declared_owner_ids),
        }


def _document_components(selection_bytes: bytes) -> dict:
    try:
        text = selection_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PlanError("SELECTION_NOT_UTF8") from error
    try:
        obj = json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_reject_const)
    except PlanError:
        raise
    except (ValueError, RecursionError) as error:
        raise PlanError("SELECTION_JSON_INVALID") from error
    if not isinstance(obj, dict) or set(obj.keys()) != {"schema", "environment", "provenance", "components", "composition"}:
        raise PlanError("SELECTION_SCHEMA_INVALID")
    if obj["schema"] != _SELECTION_SCHEMA:
        raise PlanError("SELECTION_SCHEMA_INVALID")
    comps = obj["components"]
    if type(comps) is not list or not comps:
        raise PlanError("SELECTION_SCHEMA_INVALID")
    for c in comps:
        if not isinstance(c, dict) or set(c.keys()) != {"owner", "owner_version", "root", "trust", "manifest", "sources"}:
            raise PlanError("SELECTION_SCHEMA_INVALID")
        if type(c["owner"]) is not str or type(c["root"]) is not str:
            raise PlanError("SELECTION_SCHEMA_INVALID")
    return obj


def plan_from_capture(capture: BatchCapture, *, selection_bytes: bytes, limits: BuildLimits) -> PlanEnvelope:
    if type(capture) is not BatchCapture or type(selection_bytes) is not bytes:
        raise PlanError("PLAN_INPUT_INVALID")
    if type(limits) is not BuildLimits:
        raise PlanError("PLAN_LIMITS_INVALID")
    try:
        limits.__post_init__()
    except BuildError as error:
        raise PlanError("PLAN_LIMITS_INVALID") from error
    digest = hashlib.sha256(selection_bytes).hexdigest()
    if not hmac.compare_digest(digest, capture.selection_sha256):
        raise PlanError("SELECTION_DRIFT")
    document = _document_components(selection_bytes)
    comps = document["components"]
    if (document["environment"] != capture.environment
            or document["provenance"].get("reference") != capture.provenance_reference
            or document["composition"] != capture.composition.to_dict()):
        raise PlanError("PLAN_CAPTURE_INVALID")
    n = len(comps)
    owners_idx = [o.index for o in capture.owners]
    errors_idx = [e.owner_index for e in capture.errors]
    for i in owners_idx + errors_idx:
        if type(i) is not int or i < 0 or i >= n:
            raise PlanError("PLAN_CAPTURE_INVALID")
    if len(set(owners_idx)) != len(owners_idx) or set(owners_idx) & set(errors_idx):
        raise PlanError("PLAN_CAPTURE_INVALID")
    if set(owners_idx) | set(errors_idx) != set(range(n)):
        raise PlanError("PLAN_CAPTURE_INVALID")
    for o in capture.owners:
        doc = comps[o.index]
        if o.owner != doc["owner"] or o.owner_version != doc["owner_version"]:
            raise PlanError("PLAN_CAPTURE_INVALID")
        if o.root != doc["root"] or o.trust != doc["trust"]:
            raise PlanError("PLAN_CAPTURE_INVALID")
        if o.manifest.path != doc["root"] + "/component.toml":
            raise PlanError("PLAN_CAPTURE_INVALID")
        if o.manifest.sha256 != doc["manifest"]["sha256"]:
            raise PlanError("PLAN_CAPTURE_INVALID")
        doc_sources = {s["path"]: s["sha256"] for s in doc["sources"]}
        if len(doc_sources) != len(doc["sources"]):
            raise PlanError("PLAN_CAPTURE_INVALID")
        if len(o.sources) != len(doc_sources):
            raise PlanError("PLAN_CAPTURE_INVALID")
        for s in o.sources:
            rel = s.path[len(o.root) + 1:] if s.path.startswith(o.root + "/") else None
            if rel is None or doc_sources.get(rel) != s.sha256:
                raise PlanError("PLAN_CAPTURE_INVALID")
    if not capture.owners:
        raise PlanError("PLAN_NO_CAPTURE")
    captured_ids = tuple(o.owner for o in capture.owners)
    if len(set(captured_ids)) != len(captured_ids):
        raise PlanError("PLAN_CAPTURE_INVALID")
    for req in capture.composition.required_ids:
        if req not in captured_ids:
            raise PlanError("REQUIRED_COMPONENT_UNCAPTURED")
    declared_owners = {c["owner"] for c in comps}
    kept: list[ConformityAttestation] = []
    ignored: list[int] = []
    for idx, rec in enumerate(capture.composition.attestations):
        if rec.component_id in captured_ids:
            kept.append(ConformityAttestation(**rec.to_dict()))
        elif rec.component_id in declared_owners:
            ignored.append(idx)
        else:
            kept.append(ConformityAttestation(**rec.to_dict()))
    texts = tuple(o.manifest.data.decode("utf-8") for o in capture.owners)
    prov = capture.composition.configured_providers
    providers: dict[str, str] | None = None if prov is None else {k: v for k, v in prov}
    result = build_plan(tuple(texts),
                        official_ids=tuple(capture.composition.official_ids),
                        required_ids=tuple(capture.composition.required_ids),
                        configured_providers=providers,
                        attestations=tuple(kept), limits=limits)
    declared_ids = tuple(c["owner"] for c in comps)
    checksum = _checksum_build(limits, capture.context_fingerprint, declared_ids)
    return PlanEnvelope(capture, result, tuple(ignored), limits, checksum, declared_ids)


def prepare_frontend_plan(selection_bytes: bytes, *, expected_sha256: str,
                          project_root: Path, selection_limits: SelectionLimits) -> PlanEnvelope:
    if type(selection_bytes) is not bytes or type(expected_sha256) is not str:
        raise PlanError("PLAN_INPUT_INVALID")
    if not isinstance(project_root, Path) or type(selection_limits) is not SelectionLimits:
        raise PlanError("PLAN_INPUT_INVALID")
    try:
        selection_limits.__post_init__()
    except SelectionError as error:
        raise PlanError("PLAN_LIMITS_INVALID") from error
    capture = capture_selection(selection_bytes, expected_sha256=expected_sha256,
                                project_root=project_root, limits=selection_limits)
    if not capture.owners:
        raise PlanError("PLAN_NO_CAPTURE")
    allowed = tuple(o.manifest.path for o in capture.owners)
    build_limits = BuildLimits(selection_limits.max_owners, selection_limits.max_bytes_per_file,
                               selection_limits.max_total_bytes, allowed)
    return plan_from_capture(capture, selection_bytes=selection_bytes, limits=build_limits)


def _sel_limits(ns: argparse.Namespace) -> SelectionLimits:
    return SelectionLimits(int(ns.max_selection_bytes), int(ns.max_owners),
                           int(ns.max_files_per_owner), int(ns.max_total_files),
                           int(ns.max_bytes_per_file), int(ns.max_total_bytes))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="build_frontend_plan")
    ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--max-selection-bytes", required=True)
    ap.add_argument("--max-owners", required=True)
    ap.add_argument("--max-files-per-owner", required=True)
    ap.add_argument("--max-total-files", required=True)
    ap.add_argument("--max-bytes-per-file", required=True)
    ap.add_argument("--max-total-bytes", required=True)
    ns = ap.parse_args(argv)
    try:
        sel_limits = _sel_limits(ns)
    except (SelectionError, PlanError, TypeError, ValueError):
        sys.stderr.write("SELECTION_LIMITS_INVALID\n")
        return 2
    data = sys.stdin.buffer.read(sel_limits.max_selection_bytes + 1)
    if not data or len(data) > sel_limits.max_selection_bytes:
        sys.stderr.write("SELECTION_TOO_LARGE\n")
        return 2
    try:
        env = prepare_frontend_plan(data, expected_sha256=ns.expected_sha256,
                                    project_root=Path(ns.project_root), selection_limits=sel_limits)
    except SelectionError as error:
        sys.stderr.write(error.code + "\n")
        return 2
    except PlanError as error:
        sys.stderr.write(error.code + "\n")
        return 2
    except BuildError as error:
        sys.stderr.write(error.code + "\n")
        return 2
    sys.stdout.write(json.dumps(env.to_dict(), sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
