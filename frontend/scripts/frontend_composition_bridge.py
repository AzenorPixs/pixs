"""Pont stateless stdin/stdout pour la composition frontend C11.

Aucun service, aucun mecanisme de composition nouveau, aucune attestation PASS
fabriquee. Ce pont decode un JSON borne, appelle les vrais helpers existants
(capture/plan/requirements/verify) puis renvoie une enveloppe bornee.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import codecs
import hashlib
import math
import re
import json
import sys
from pathlib import Path

BRIDGE_SCHEMA = "pixs.frontend.bridge/1.0.0"
BUILD_POLICY_SCHEMA = "pixs.frontend.build-policy/1.0.0"
FRONTEND_POLICY_SCHEMA = "pixs.frontend.policy/1.0.0"
SELECTION_SCHEMA = "pixs.frontend.selection/1.0.0"

_OPERATIONS = frozenset(("policy", "prepare", "facts", "verify"))
_LIMIT_KEYS = frozenset(("selection", "imports", "graph", "requirements", "sourceProfile", "presentation", "wire"))
_WIRE_KEYS = frozenset(("maxPolicyBytes", "maxWireBytes", "maxPolicyNodes"))
_DANGEROUS_KEYS = frozenset(("__proto__", "constructor", "prototype"))


class BridgeError(ValueError):
    """Erreur fermee du pont, sans valeur ni chemin prive."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _fail(code: str) -> BridgeError:
    return BridgeError(code)


def _no_dupes(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _fail("BRIDGE_JSON_DUPLICATE")
        result[key] = value
    return result


def _reject_const(value: str) -> object:
    raise _fail("BRIDGE_JSON_NONFINITE")


def _is_hex64(value: object) -> bool:
    if type(value) is not str or len(value) != 64:
        return False
    for character in value:
        if character not in "0123456789abcdef":
            return False
    return True


def _decode_strict_b64(value: object, code: str, *, allow_empty: bool = False) -> bytes:
    if type(value) is not str or (not value and not allow_empty):
        raise _fail(code)
    try:
        value.encode("ascii")
    except UnicodeEncodeError as error:
        raise _fail(code) from error
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as error:
        raise _fail(code) from error


def _check_bounds(max_wire_bytes: int, max_policy_bytes: int) -> None:
    for bound in (max_wire_bytes, max_policy_bytes):
        if type(bound) is not int or not 0 < bound < sys.maxsize:
            raise _fail("BRIDGE_BOUNDS_INVALID")


def _parse_wire_json(raw: bytes) -> object:
    if not raw or b"\x00" in raw or b"\r" in raw:
        raise _fail("BRIDGE_WIRE_INVALID")
    if raw.startswith(codecs.BOM_UTF8):
        raise _fail("BRIDGE_WIRE_BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise _fail("BRIDGE_WIRE_NOT_UTF8") from error
    if "\x00" in text:
        raise _fail("BRIDGE_WIRE_INVALID")
    try:
        return json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_reject_const)
    except BridgeError:
        raise
    except (ValueError, RecursionError) as error:
        raise _fail("BRIDGE_WIRE_JSON_INVALID") from error


def _walk_policy(node: object, budget: list[int]) -> None:
    pending = [node]
    while pending:
        if budget[0] <= 0:
            raise _fail("BRIDGE_POLICY_TOO_LARGE")
        budget[0] -= 1
        current = pending.pop()
        if current is None or type(current) in (bool, int):
            continue
        if type(current) is float:
            if not math.isfinite(current):
                raise _fail("BRIDGE_JSON_NONFINITE")
            continue
        if type(current) is str:
            try:
                current.encode("utf-8")
            except UnicodeEncodeError as error:
                raise _fail("BRIDGE_POLICY_NOT_UTF8") from error
            if chr(0) in current or chr(13) in current:
                raise _fail("BRIDGE_POLICY_INVALID")
            continue
        if type(current) is list:
            pending.extend(current)
            continue
        if type(current) is dict:
            for key, value in current.items():
                if type(key) is not str or key in _DANGEROUS_KEYS:
                    raise _fail("BRIDGE_POLICY_FORBIDDEN_KEY")
                pending.append(key)
                pending.append(value)
            continue
        raise _fail("BRIDGE_POLICY_INVALID")


def _positive_group(value: object, names: tuple[str, ...], nested: tuple[str, ...] = ()) -> None:
    if type(value) is not dict or set(value) != set(names) | set(nested):
        raise _fail("BRIDGE_POLICY_LIMITS_INVALID")
    for name in names:
        bound = value[name]
        # Le consommateur Node impose des entiers sûrs, sans arrondi JSON implicite.
        if type(bound) is not int or not 0 < bound <= (1 << 53) - 1:
            raise _fail("BRIDGE_POLICY_LIMITS_INVALID")


def _policy_limits(limits: dict) -> None:
    _positive_group(limits["selection"], (
        "max_selection_bytes", "max_owners", "max_files_per_owner",
        "max_total_files", "max_bytes_per_file", "max_total_bytes",
    ))
    _positive_group(limits["requirements"], (
        "max_contributions", "max_requirements_per_contribution", "max_total_requirements",
    ))
    _positive_group(limits["imports"], (
        "maxSourceBytes", "maxTotalSourceBytes", "maxModules", "maxImports",
        "maxBindings", "maxResolutions", "maxInputNodes",
    ), ("syntaxLimits",))
    _positive_group(limits["imports"]["syntaxLimits"], (
        "maxSourceBytes", "maxAstNodes", "maxDescriptorCount", "maxTextLength",
        "maxLiteralItems", "maxLiteralDepth",
    ))
    _positive_group(limits["graph"], (
        "maxContributions", "maxFacts", "maxEdges", "maxInputNodes",
    ), ("descriptorLimits",))
    _positive_group(limits["graph"]["descriptorLimits"], (
        "maxTextLength", "maxRequires", "maxPermissions", "maxPoints",
        "maxLocales", "maxCatalogKeys",
    ))
    _positive_group(limits["sourceProfile"], (
        "maxSourceBytes", "maxAstNodes", "maxBindings", "maxTextLength", "maxScopeDepth",
    ))
    _positive_group(limits["presentation"], (
        "maxNodes", "maxDepth", "maxChildren", "maxTextLength", "maxParams",
        "maxFields", "maxBindings", "maxDataNodes", "maxBodyDepth", "maxBodyNodes",
    ))
    _positive_group(limits["wire"], (
        "maxPolicyBytes", "maxWireBytes", "maxPolicyNodes",
    ))


def _bridge_policy(raw_policy: bytes, *, max_wire_bytes: int, max_policy_bytes: int) -> dict:
    if type(raw_policy) is not bytes or not raw_policy or len(raw_policy) > max_policy_bytes:
        raise _fail("BRIDGE_POLICY_TOO_LARGE")
    if raw_policy.startswith(codecs.BOM_UTF8) or b"\x00" in raw_policy or b"\r" in raw_policy:
        raise _fail("BRIDGE_POLICY_INVALID")
    try:
        text = raw_policy.decode("utf-8")
    except UnicodeDecodeError as error:
        raise _fail("BRIDGE_POLICY_NOT_UTF8") from error
    if "\x00" in text:
        raise _fail("BRIDGE_POLICY_INVALID")
    try:
        document = json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_reject_const)
    except BridgeError:
        raise
    except (ValueError, RecursionError) as error:
        raise _fail("BRIDGE_POLICY_JSON_INVALID") from error
    if type(document) is not dict or set(document) != {"schema", "policy", "limits"}:
        raise _fail("BRIDGE_POLICY_SCHEMA_INVALID")
    if document.get("schema") != BUILD_POLICY_SCHEMA:
        raise _fail("BRIDGE_POLICY_SCHEMA_INVALID")
    policy = document.get("policy")
    limits = document.get("limits")
    if type(policy) is not dict or policy.get("schema") != FRONTEND_POLICY_SCHEMA:
        raise _fail("BRIDGE_POLICY_SCHEMA_INVALID")
    if type(limits) is not dict or set(limits) != set(_LIMIT_KEYS):
        raise _fail("BRIDGE_POLICY_LIMITS_INVALID")
    wire = limits.get("wire")
    if type(wire) is not dict or set(wire) != set(_WIRE_KEYS):
        raise _fail("BRIDGE_POLICY_WIRE_INVALID")
    for name in ("maxPolicyBytes", "maxWireBytes", "maxPolicyNodes"):
        value = wire.get(name)
        if type(value) is not int or isinstance(value, bool) or value <= 0:
            raise _fail("BRIDGE_POLICY_WIRE_INVALID")
    if wire["maxPolicyBytes"] != max_policy_bytes or wire["maxWireBytes"] != max_wire_bytes:
        raise _fail("BRIDGE_POLICY_BOUNDS_MISMATCH")
    _walk_policy(document, [wire["maxPolicyNodes"]])
    _policy_limits(limits)
    return document


def _selection_limits(payload: object) -> object:
    from build_frontend_selection import SelectionError, SelectionLimits

    if type(payload) is not dict:
        raise _fail("BRIDGE_LIMITS_INVALID")
    expected = ("max_selection_bytes", "max_owners", "max_files_per_owner", "max_total_files", "max_bytes_per_file", "max_total_bytes")
    if set(payload) != set(expected):
        raise _fail("BRIDGE_LIMITS_INVALID")
    try:
        limits = SelectionLimits(*(payload[name] for name in expected))
        limits.__post_init__()
    except (SelectionError, TypeError, ValueError, AttributeError) as error:
        raise _fail("BRIDGE_LIMITS_INVALID") from error
    return limits


def _op_policy(request: dict, *, max_wire_bytes: int, max_policy_bytes: int) -> dict:
    if set(request) != {"operation", "policy_b64", "expected_policy_sha256"}:
        raise _fail("BRIDGE_REQUEST_INVALID")
    expected = request.get("expected_policy_sha256")
    if not _is_hex64(expected):
        raise _fail("BRIDGE_PIN_INVALID")
    raw = _decode_strict_b64(request.get("policy_b64"), "BRIDGE_POLICY_B64_INVALID")
    if len(raw) > max_policy_bytes:
        raise _fail("BRIDGE_POLICY_TOO_LARGE")
    if hashlib.sha256(raw).hexdigest() != expected:
        raise _fail("BRIDGE_PIN_MISMATCH")
    return _bridge_policy(raw, max_wire_bytes=max_wire_bytes, max_policy_bytes=max_policy_bytes)


def _op_prepare(request: dict, *, project_root: Path) -> dict:
    from build_frontend_plan import PlanError, prepare_frontend_plan
    from build_frontend_selection import SelectionError

    if set(request) != {"operation", "selection_b64", "expected_selection_sha256", "selection_limits"}:
        raise _fail("BRIDGE_REQUEST_INVALID")
    expected = request.get("expected_selection_sha256")
    if not _is_hex64(expected):
        raise _fail("BRIDGE_PIN_INVALID")
    limits = _selection_limits(request.get("selection_limits"))
    raw = _decode_strict_b64(request.get("selection_b64"), "BRIDGE_SELECTION_B64_INVALID")
    try:
        envelope = prepare_frontend_plan(raw, expected_sha256=expected, project_root=project_root, selection_limits=limits)
    except (SelectionError, PlanError) as error:
        raise _fail(error.code) from error
    except (ValueError, TypeError) as error:
        raise _fail("BRIDGE_PREPARE_FAILED") from error
    return envelope.to_dict()


def _op_facts(request: dict) -> dict:
    from composition_requirements_v1 import RequirementsError, RequirementsLimits, analyze_contribution_requirements

    if set(request) != {"operation", "facets", "component_order", "component_edges", "requirements_limits"}:
        raise _fail("BRIDGE_REQUEST_INVALID")
    raw_limits = request.get("requirements_limits")
    if type(raw_limits) is not dict or set(raw_limits) != {"max_contributions", "max_requirements_per_contribution", "max_total_requirements"}:
        raise _fail("BRIDGE_LIMITS_INVALID")
    try:
        limits = RequirementsLimits(raw_limits["max_contributions"], raw_limits["max_requirements_per_contribution"], raw_limits["max_total_requirements"])
        limits.__post_init__()
    except (RequirementsError, TypeError, ValueError) as error:
        raise _fail("BRIDGE_LIMITS_INVALID") from error
    raw_facets = request.get("facets")
    raw_order = request.get("component_order")
    raw_edges = request.get("component_edges")
    if type(raw_facets) is not list or type(raw_order) is not list or type(raw_edges) is not list:
        raise _fail("BRIDGE_REQUEST_INVALID")
    if any(type(item) is not list or len(item) != 2 for item in raw_edges):
        raise _fail("BRIDGE_REQUEST_INVALID")
    try:
        facets = tuple(raw_facets)
        order = tuple(raw_order)
        edges = tuple(tuple(item) for item in raw_edges)
        result = analyze_contribution_requirements(facets, component_order=order, component_edges=edges, limits=limits)
    except RequirementsError as error:
        raise _fail(error.code) from error
    except (ValueError, TypeError) as error:
        raise _fail("BRIDGE_FACTS_FAILED") from error
    return result.to_dict()


def _captured_file(payload: object) -> object:
    from build_frontend_selection import CapturedFile, SelectionError

    if type(payload) is not dict or set(payload) != {"owner_index", "path", "sha256", "size", "data_b64"}:
        raise _fail("BRIDGE_CAPTURE_INVALID")
    data = _decode_strict_b64(payload.get("data_b64"), "BRIDGE_CAPTURE_B64_INVALID", allow_empty=True)
    try:
        record = CapturedFile(payload["owner_index"], payload["path"], payload["sha256"], payload["size"], data)
    except (SelectionError, TypeError, ValueError, AttributeError) as error:
        raise _fail("BRIDGE_CAPTURE_INVALID") from error
    return record


def _rebuild_capture(payload: object) -> object:
    from build_frontend_selection import AttestationRecord, BatchCapture, CaptureError, CompositionSnapshot, OwnerCapture, SelectionError

    if type(payload) is not dict:
        raise _fail("BRIDGE_CAPTURE_INVALID")
    if set(payload) != {"schema", "selection_sha256", "environment", "provenance_reference", "context_fingerprint", "composition", "owners", "errors"}:
        raise _fail("BRIDGE_CAPTURE_INVALID")
    if payload.get("schema") != SELECTION_SCHEMA:
        raise _fail("BRIDGE_CAPTURE_INVALID")
    raw_composition = payload.get("composition")
    if type(raw_composition) is not dict or set(raw_composition) != {"official_ids", "required_ids", "configured_providers", "attestations"}:
        raise _fail("BRIDGE_CAPTURE_INVALID")
    providers = raw_composition.get("configured_providers")
    if providers is None:
        pairs = None
    elif type(providers) is dict:
        pairs = tuple(sorted(providers.items()))
    else:
        raise _fail("BRIDGE_CAPTURE_INVALID")
    raw_attestations = raw_composition.get("attestations")
    raw_owners = payload.get("owners")
    raw_errors = payload.get("errors")
    if type(raw_attestations) is not list or type(raw_owners) is not list or type(raw_errors) is not list:
        raise _fail("BRIDGE_CAPTURE_INVALID")
    try:
        for key in ("official_ids", "required_ids"):
            if type(raw_composition[key]) is not list:
                raise _fail("BRIDGE_CAPTURE_INVALID")
        attestation_fields = {
            "component_id", "component_version", "scope", "target_id", "target_version",
            "suite_id", "suite_version", "verdict", "proof_ref",
        }
        attestations = []
        for item in raw_attestations:
            if type(item) is not dict or set(item) != attestation_fields:
                raise _fail("BRIDGE_CAPTURE_INVALID")
            attestations.append(AttestationRecord(**item))
        composition = CompositionSnapshot(
            tuple(raw_composition["official_ids"]), tuple(raw_composition["required_ids"]),
            pairs, tuple(attestations),
        )
        owners = []
        for item in raw_owners:
            if type(item) is not dict or set(item) != {"index", "owner", "owner_version", "root", "trust", "manifest", "sources"}:
                raise _fail("BRIDGE_CAPTURE_INVALID")
            manifest = _captured_file(item.get("manifest"))
            raw_sources = item.get("sources")
            if type(raw_sources) is not list:
                raise _fail("BRIDGE_CAPTURE_INVALID")
            sources = tuple(_captured_file(item) for item in raw_sources)
            owners.append(OwnerCapture(item["index"], item["owner"], item["owner_version"], item["root"], item["trust"], manifest, sources))
        errors = []
        for item in raw_errors:
            if type(item) is not dict or set(item) != {"owner_index", "owner", "path", "code", "observed_sha256"}:
                raise _fail("BRIDGE_CAPTURE_INVALID")
            errors.append(CaptureError(item["owner_index"], item["owner"], item["path"], item["code"], item["observed_sha256"]))
        capture = BatchCapture(payload["selection_sha256"], payload["environment"], payload["provenance_reference"], payload["context_fingerprint"], composition, tuple(owners), tuple(errors))
    except BridgeError:
        raise
    except (SelectionError, TypeError, ValueError, AttributeError) as error:
        raise _fail("BRIDGE_CAPTURE_INVALID") from error
    return capture


def _op_verify(request: dict, *, project_root: Path) -> dict:
    from build_frontend_selection import SelectionError, verify_before_publish

    if set(request) != {"operation", "capture", "selection_b64", "expected_selection_sha256", "selection_limits"}:
        raise _fail("BRIDGE_REQUEST_INVALID")
    expected = request.get("expected_selection_sha256")
    if not _is_hex64(expected):
        raise _fail("BRIDGE_PIN_INVALID")
    limits = _selection_limits(request.get("selection_limits"))
    capture = _rebuild_capture(request.get("capture"))
    raw = _decode_strict_b64(request.get("selection_b64"), "BRIDGE_SELECTION_B64_INVALID")
    try:
        verified = verify_before_publish(capture, selection_bytes=raw, expected_sha256=expected, project_root=project_root, limits=limits)
    except SelectionError as error:
        raise _fail(error.code) from error
    except (ValueError, TypeError) as error:
        raise _fail("BRIDGE_VERIFY_FAILED") from error
    return {"verified": True, "selection_sha256": verified.selection_sha256, "context_fingerprint": verified.context_fingerprint}


def dispatch_bridge(request: object, *, project_root: Path, max_wire_bytes: int, max_policy_bytes: int) -> dict:
    """Aiguille une requete pure, sans entree/sortie ni etat."""
    _check_bounds(max_wire_bytes, max_policy_bytes)
    if not isinstance(project_root, Path) or type(request) is not dict:
        raise _fail("BRIDGE_REQUEST_INVALID")
    operation = request.get("operation")
    if type(operation) is not str or operation not in _OPERATIONS:
        raise _fail("BRIDGE_OPERATION_UNKNOWN")
    if operation == "policy":
        return _op_policy(request, max_wire_bytes=max_wire_bytes, max_policy_bytes=max_policy_bytes)
    if operation == "prepare":
        return _op_prepare(request, project_root=project_root)
    if operation == "facts":
        return _op_facts(request)
    return _op_verify(request, project_root=project_root)


def _project_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def _error_code(error: BaseException) -> str:
    code = getattr(error, "code", None)
    if type(code) is str and re.fullmatch(r"[A-Z][A-Z0-9_]{0,63}", code):
        return code
    return "BRIDGE_FAILED"


def _emit(response: dict, max_wire_bytes: int) -> int:
    body = (json.dumps(response, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
    if len(body) > max_wire_bytes:
        response = {"schema": BRIDGE_SCHEMA, "ok": False,
                    "error_code": "BRIDGE_RESPONSE_TOO_LARGE"}
        body = (json.dumps(response, separators=(",", ":")) + "\n").encode("utf-8")
        if len(body) > max_wire_bytes:
            # La borne ne permet même pas une enveloppe d'erreur ; aucun octet hors quota.
            sys.stderr.write("BRIDGE_RESPONSE_TOO_LARGE\n")
            return 2
    sys.stdout.buffer.write(body)
    if response["ok"] is not True:
        sys.stderr.write(response["error_code"] + "\n")
        return 2
    return 0


def _read_wire(stream, maximum: int) -> bytes:
    chunks = []
    received = 0
    while received <= maximum:
        block = stream.read(min(65536, maximum + 1 - received))
        if not block:
            break
        chunks.append(block)
        received += len(block)
    return b"".join(chunks)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="frontend_composition_bridge")
    parser.add_argument("--max-wire-bytes", required=True)
    parser.add_argument("--max-policy-bytes", required=True)
    options = parser.parse_args(argv)
    try:
        max_wire_bytes = int(options.max_wire_bytes)
        max_policy_bytes = int(options.max_policy_bytes)
        _check_bounds(max_wire_bytes, max_policy_bytes)
    except (BridgeError, TypeError, ValueError):
        sys.stderr.write("BRIDGE_BOUNDS_INVALID\n")
        return 2
    try:
        raw_input = _read_wire(sys.stdin.buffer, max_wire_bytes)
        if not raw_input or len(raw_input) > max_wire_bytes:
            raise _fail("BRIDGE_WIRE_TOO_LARGE")
        request = _parse_wire_json(raw_input)
        result = dispatch_bridge(
            request, project_root=_project_root_from_script(),
            max_wire_bytes=max_wire_bytes, max_policy_bytes=max_policy_bytes,
        )
        response = {"schema": BRIDGE_SCHEMA, "ok": True, "result": result}
    except BridgeError as error:
        response = {"schema": BRIDGE_SCHEMA, "ok": False, "error_code": _error_code(error)}
    except Exception:
        # Frontière CLI : diagnostic fermé pour ne pas projeter sources ou chemins privés.
        response = {"schema": BRIDGE_SCHEMA, "ok": False, "error_code": "BRIDGE_FAILED"}
    return _emit(response, max_wire_bytes)


if __name__ == "__main__":
    raise SystemExit(main())
