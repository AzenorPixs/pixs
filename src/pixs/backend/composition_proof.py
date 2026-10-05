"""Initial partial proof from real discover validate resolve controls."""

from __future__ import annotations

import json

from pixs.backend.composition_initial import COMPOSITION_VERSION
from pixs.backend.composition_initial import OFFICIAL_IDS
from pixs.backend.composition_initial import REQUIRED_IDS
from pixs.kernel.composition import UNEVALUATED_DIMENSIONS
from pixs.kernel.composition import discover
from pixs.kernel.composition import resolve
from pixs.kernel.composition import validate

__all__ = ["InitialProofError", "PROOF_VERSION", "build_initial_proof"]

PROOF_VERSION = "0.1.0"

_MAX_TEXT_BYTES = 65536

_EXPECTED_TYPES = dict(zip(REQUIRED_IDS, ("KERNEL", "MODULE", "MODULE")))

_EVALUATED_SCOPE = ("capabilities", "components", "contracts")

_EXTRA_UNEVALUATED = ("conformity", "profiles")

_CHECKS = ("discover", "validate", "resolve")

_GENERIC_MESSAGE = "initial composition invalid"


class InitialProofError(ValueError):
    """Generic refusal for initial proof without raw echo."""


def _fail() -> None:
    raise InitialProofError(_GENERIC_MESSAGE) from None


def _checked_texts(manifest_texts: object) -> tuple[str, str, str]:
    if type(manifest_texts) is not tuple:
        _fail()
    if len(manifest_texts) != 3:
        _fail()
    for item in manifest_texts:
        if type(item) is not str:
            _fail()
        if item == "":
            _fail()
        try:
            encoded = item.encode("utf-8")
        except UnicodeError:
            _fail()
        if len(encoded) == 0:
            _fail()
        if len(encoded) > _MAX_TEXT_BYTES:
            _fail()
    if len(set(manifest_texts)) != 3:
        _fail()
    return manifest_texts


def build_initial_proof(manifest_texts: tuple[str, str, str]) -> str:
    """Build canonical internal proof from real initial controls."""
    texts = _checked_texts(manifest_texts)
    try:
        discovered = discover(texts)
    except Exception:
        _fail()
    try:
        manifests, validate_diagnostics = validate(
            discovered, official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS
        )
    except Exception:
        _fail()
    if validate_diagnostics:
        _fail()
    if len(manifests) != 3:
        _fail()
    found_ids = [manifest.id for manifest in manifests]
    if len(set(found_ids)) != 3:
        _fail()
    if set(found_ids) != set(REQUIRED_IDS):
        _fail()
    by_id = {manifest.id: manifest for manifest in manifests}
    for required_id in REQUIRED_IDS:
        current = by_id.get(required_id)
        if current is None:
            _fail()
        if current.type != _EXPECTED_TYPES[required_id]:
            _fail()
        if current.version == "":
            _fail()
    try:
        edges, order, resolve_diagnostics = resolve(manifests)
    except Exception:
        _fail()
    if resolve_diagnostics:
        _fail()
    if len(order) != 3:
        _fail()
    if set(order) != set(REQUIRED_IDS):
        _fail()
    components = sorted(
        (
            {
                "id": manifest.id,
                "type": manifest.type,
                "version": manifest.version,
            }
            for manifest in manifests
        ),
        key=lambda entry: entry["id"],
    )
    capabilities = sorted(
        (
            {
                "id": capability.id,
                "owner": manifest.id,
                "version": capability.version,
            }
            for manifest in manifests
            for capability in manifest.provided_capabilities
        ),
        key=lambda entry: (entry["id"], entry["owner"], entry["version"]),
    )
    contracts = sorted(
        (
            {
                "id": contract.id,
                "owner": manifest.id,
                "version": contract.version,
            }
            for manifest in manifests
            for contract in manifest.implemented_contracts
        ),
        key=lambda entry: (entry["id"], entry["owner"], entry["version"]),
    )
    ordered_edges = sorted(set(edges))
    proof = {
        "activated": False,
        "capabilities": capabilities,
        "checks": list(_CHECKS),
        "components": components,
        "composition_version": COMPOSITION_VERSION,
        "contracts": contracts,
        "edges": [list(edge) for edge in ordered_edges],
        "evaluated_scope": sorted(_EVALUATED_SCOPE),
        "globally_compatible": False,
        "order": list(order),
        "partial": True,
        "proof_version": PROOF_VERSION,
        "unevaluated_dimensions": sorted(set(UNEVALUATED_DIMENSIONS) | set(_EXTRA_UNEVALUATED)),
    }
    return json.dumps(proof, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
