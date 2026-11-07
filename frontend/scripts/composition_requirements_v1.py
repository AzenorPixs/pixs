"""Faits de dependances entre contributions frontend (tache 2.2, build seul).

Calcule des faits, pas une composition : aucun registre/lifecycle composant,
aucune decision de trust/autorisation/activation. Les entrees (facettes,
ordre/edges Kernel, inventaire) viennent de l'appelant de confiance ; ce
module ne fabrique ni preuve ni authenticite des sources.
`all_satisfied` est une propriete calculee depuis les faits, jamais un etat
pret/active.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass


class RequirementsError(ValueError):
    def __init__(self, code: str, diagnostics: tuple = ()) -> None:
        super().__init__(code)
        self.code = code
        self.diagnostics = tuple(diagnostics)


CODES = frozenset({
    "SATISFIED",
    "MISSING",
    "AMBIGUOUS",
    "INCOMPATIBLE",
    "OWNER_DEPENDENCY_UNDECLARED",
})

_FACET_KEYS = frozenset({
    "owner", "owner_version", "type", "id",
    "entry", "version", "requires", "scope",
})

_SCHEMA = "pixs.frontend.requirement-facts/1.0.0"


def _strict_text(value: object, code: str) -> str:
    if type(value) is not str or not value or "\x00" in value:
        raise RequirementsError(code)
    for unit in value:
        point = ord(unit)
        if point < 32 or point == 127:
            raise RequirementsError(code)
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise RequirementsError(code) from error
    return value


@dataclass(frozen=True, slots=True)
class RequirementsLimits:
    max_contributions: int
    max_requirements_per_contribution: int
    max_total_requirements: int

    def __post_init__(self) -> None:
        for value in (
            self.max_contributions,
            self.max_requirements_per_contribution,
            self.max_total_requirements,
        ):
            if type(value) is not int or isinstance(value, bool) or value <= 0:
                raise RequirementsError("REQ_LIMITS_INVALID")


@dataclass(frozen=True, slots=True)
class RequirementCandidate:
    owner: str
    id: str
    version: str

    def __post_init__(self) -> None:
        _strict_text(self.owner, "REQ_FACET_INVALID")
        _strict_text(self.id, "REQ_FACET_INVALID")
        _strict_text(self.version, "REQ_FACET_INVALID")
        try:
            from pixs.kernel.frontend_contribution_ids import validate_frontend_contribution_id_v1
            from pixs.kernel.manifest.semver import parse_version
            validate_frontend_contribution_id_v1(self.id)
            parse_version(self.version)
        except (TypeError, ValueError) as error:
            raise RequirementsError("REQ_FACET_INVALID") from error

    def to_dict(self) -> dict:
        return {"owner": self.owner, "id": self.id, "version": self.version}


@dataclass(frozen=True, slots=True)
class RequirementFact:
    owner: str
    id: str
    index: int
    requirement: str
    target_id: str
    candidates: tuple[RequirementCandidate, ...]
    code: str

    def __post_init__(self) -> None:
        _strict_text(self.owner, "REQ_FACET_INVALID")
        _strict_text(self.id, "REQ_FACET_INVALID")
        if type(self.index) is not int or isinstance(self.index, bool) or self.index < 0:
            raise RequirementsError("REQ_FACET_INVALID")
        _strict_text(self.requirement, "REQ_FACET_INVALID")
        _strict_text(self.target_id, "REQ_FACET_INVALID")
        if type(self.candidates) is not tuple:
            raise RequirementsError("REQ_FACET_INVALID")
        for item in self.candidates:
            if type(item) is not RequirementCandidate:
                raise RequirementsError("REQ_FACET_INVALID")
        if type(self.code) is not str or self.code not in CODES:
            raise RequirementsError("REQ_FACET_INVALID")
        if self.code == "MISSING":
            if len(self.candidates) != 0:
                raise RequirementsError("REQ_FACET_INVALID")
        elif self.code == "AMBIGUOUS":
            if len(self.candidates) <= 1:
                raise RequirementsError("REQ_FACET_INVALID")
        else:
            if len(self.candidates) != 1:
                raise RequirementsError("REQ_FACET_INVALID")
        try:
            from pixs.kernel.frontend_contribution_ids import validate_frontend_contribution_id_v1
            from pixs.kernel.manifest.semver import parse_requirement
            validate_frontend_contribution_id_v1(self.id)
            parsed = parse_requirement(self.requirement)
        except (TypeError, ValueError) as error:
            raise RequirementsError("REQ_FACET_INVALID") from error
        if parsed.target_id != self.target_id or any(item.id != self.target_id for item in self.candidates):
            raise RequirementsError("REQ_FACET_INVALID")

    def to_dict(self) -> dict:
        return {
            "owner": self.owner,
            "id": self.id,
            "index": self.index,
            "requirement": self.requirement,
            "target_id": self.target_id,
            "candidates": [item.to_dict() for item in self.candidates],
            "code": self.code,
        }


@dataclass(frozen=True, slots=True)
class RequirementFacts:
    facts: tuple[RequirementFact, ...]
    frontend_edges: tuple[tuple[str, str, str, str], ...]

    def __post_init__(self) -> None:
        if type(self.facts) is not tuple:
            raise RequirementsError("REQ_FACET_INVALID")
        for item in self.facts:
            if type(item) is not RequirementFact:
                raise RequirementsError("REQ_FACET_INVALID")
        if type(self.frontend_edges) is not tuple:
            raise RequirementsError("REQ_FACET_INVALID")
        seen: set[tuple[str, str, str, str]] = set()
        for edge in self.frontend_edges:
            if (
                type(edge) is not tuple
                or len(edge) != 4
                or type(edge[0]) is not str
                or type(edge[1]) is not str
                or type(edge[2]) is not str
                or type(edge[3]) is not str
            ):
                raise RequirementsError("REQ_FACET_INVALID")
            if edge in seen:
                raise RequirementsError("REQ_FACET_INVALID")
            seen.add(edge)
        expected: set[tuple[str, str, str, str]] = set()
        for item in self.facts:
            if item.code == "SATISFIED":
                expected.add((item.owner, item.id, item.candidates[0].owner, item.target_id))
        if seen != expected:
            raise RequirementsError("REQ_FACET_INVALID")

    @property
    def all_satisfied(self) -> bool:
        return all(item.code == "SATISFIED" for item in self.facts)

    def to_dict(self) -> dict:
        return {
            "schema": _SCHEMA,
            "facts": [item.to_dict() for item in self.facts],
            "frontend_edges": [list(edge) for edge in self.frontend_edges],
            "all_satisfied": self.all_satisfied,
        }


def _validate_order(value: object) -> tuple[str, ...]:
    if type(value) is not tuple or not value:
        raise RequirementsError("REQ_ORDER_INVALID")
    seen: set[str] = set()
    for item in value:
        _strict_text(item, "REQ_ORDER_INVALID")
        if item in seen:
            raise RequirementsError("REQ_ORDER_INVALID")
        seen.add(item)
    return value


def _validate_edges(value: object, rank: dict[str, int]) -> tuple[tuple[str, str], ...]:
    if type(value) is not tuple:
        raise RequirementsError("REQ_EDGES_INVALID")
    seen: set[tuple[str, str]] = set()
    for edge in value:
        if type(edge) is not tuple or len(edge) != 2:
            raise RequirementsError("REQ_EDGES_INVALID")
        source, target = edge
        _strict_text(source, "REQ_EDGES_INVALID")
        _strict_text(target, "REQ_EDGES_INVALID")
        if source not in rank or target not in rank:
            raise RequirementsError("REQ_EDGES_INVALID")
        if not rank[target] < rank[source]:
            raise RequirementsError("REQ_EDGES_INVALID")
        if edge in seen:
            raise RequirementsError("REQ_EDGES_INVALID")
        seen.add(edge)
    return value


def _closure(order: tuple[str, ...], edges: tuple[tuple[str, str], ...]) -> dict[str, set[str]]:
    direct: dict[str, set[str]] = {node: set() for node in order}
    for source, target in edges:
        direct[source].add(target)
    result: dict[str, set[str]] = {}
    for node in order:
        seen: set[str] = set()
        stack = list(direct[node])
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            stack.extend(direct[current] - seen)
        result[node] = seen
    return result


def analyze_contribution_requirements(
    facets: tuple[dict[str, object], ...],
    *,
    component_order: tuple[str, ...],
    component_edges: tuple[tuple[str, str], ...],
    limits: RequirementsLimits,
) -> RequirementFacts:
    from pixs.kernel.frontend_contribution_declarations import (
        validate_frontend_contribution_declaration_v1,
    )
    from pixs.kernel.manifest.semver import matches, parse_requirement, parse_version

    if type(limits) is not RequirementsLimits:
        raise RequirementsError("REQ_LIMITS_INVALID")
    limits.__post_init__()
    if type(facets) is not tuple or len(facets) > limits.max_contributions:
        raise RequirementsError("REQ_FACET_INVALID")
    order = _validate_order(component_order)
    rank = {name: index for index, name in enumerate(order)}
    edges = _validate_edges(component_edges, rank)
    reachable = _closure(order, edges)
    snapshots: list[tuple[str, str, str, str, str, str, tuple[str, ...], str]] = []
    seen_refs: set[tuple[str, str]] = set()
    owner_versions: dict[str, str] = {}
    total = 0
    for facet in facets:
        if type(facet) is not dict:
            raise RequirementsError("REQ_FACET_INVALID")
        for key in facet.keys():
            if type(key) is not str:
                raise RequirementsError("REQ_FACET_INVALID")
        if set(facet.keys()) != set(_FACET_KEYS):
            raise RequirementsError("REQ_FACET_INVALID")
        requires_raw = facet["requires"]
        if type(requires_raw) is not list:
            raise RequirementsError("REQ_FACET_INVALID")
        if len(requires_raw) > limits.max_requirements_per_contribution:
            raise RequirementsError("REQ_LIMITS_INVALID")
        total += len(requires_raw)
        if total > limits.max_total_requirements:
            raise RequirementsError("REQ_LIMITS_INVALID")
        for entry in requires_raw:
            if type(entry) is not str:
                raise RequirementsError("REQ_FACET_INVALID")
        try:
            snapshot = validate_frontend_contribution_declaration_v1({
                "type": facet["type"],
                "id": facet["id"],
                "entry": facet["entry"],
                "version": facet["version"],
                "requires": list(requires_raw),
                "scope": facet["scope"],
            })
        except (TypeError, ValueError) as error:
            raise RequirementsError("REQ_FACET_INVALID") from error
        owner = facet["owner"]
        owner_version = facet["owner_version"]
        _strict_text(owner, "REQ_FACET_INVALID")
        _strict_text(owner_version, "REQ_FACET_INVALID")
        try:
            parse_version(owner_version)
        except ValueError as error:
            raise RequirementsError("REQ_FACET_INVALID") from error
        if owner not in rank:
            raise RequirementsError("REQ_FACET_INVALID")
        previous = owner_versions.get(owner)
        if previous is None:
            owner_versions[owner] = owner_version
        elif previous != owner_version:
            raise RequirementsError("REQ_FACET_INVALID")
        key = (owner, snapshot.id)
        if key in seen_refs:
            raise RequirementsError("REQ_DUPLICATE_CONTRIBUTION")
        seen_refs.add(key)
        snapshots.append((
            owner, owner_version, snapshot.type, snapshot.id,
            snapshot.entry, snapshot.version, snapshot.requires, snapshot.scope,
        ))
    pool: dict[str, list[tuple[str, str, str]]] = {}
    for owner, _owner_version, _type, identity, _entry, version, _requires, _scope in snapshots:
        pool.setdefault(identity, []).append((owner, identity, version))
    ordered = sorted(snapshots, key=lambda item: (rank[item[0]], item[3]))
    facts: list[RequirementFact] = []
    edge_set: set[tuple[str, str, str, str]] = set()
    for owner, _owner_version, _type, identity, _entry, _version, requires, _scope in ordered:
        for index, entry in enumerate(requires):
            try:
                parsed = parse_requirement(entry)
            except ValueError as error:
                raise RequirementsError("REQ_FACET_INVALID") from error
            target_id = parsed.target_id
            group = pool.get(target_id, [])
            ordered_group = sorted(group, key=lambda item: (rank[item[0]], item[0], item[2]))
            candidates = tuple(
                RequirementCandidate(item_owner, item_id, item_version)
                for item_owner, item_id, item_version in ordered_group
            )
            if not candidates:
                code = "MISSING"
            elif len(candidates) > 1:
                code = "AMBIGUOUS"
            else:
                try:
                    ok = matches(candidates[0].version, entry)
                except ValueError as error:
                    raise RequirementsError("REQ_FACET_INVALID") from error
                if not ok:
                    code = "INCOMPATIBLE"
                elif candidates[0].owner == owner:
                    code = "SATISFIED"
                elif candidates[0].owner in reachable[owner]:
                    code = "SATISFIED"
                else:
                    code = "OWNER_DEPENDENCY_UNDECLARED"
                if code == "SATISFIED":
                    edge_set.add((owner, identity, candidates[0].owner, target_id))
            facts.append(RequirementFact(
                owner, identity, index, entry, target_id, candidates, code,
            ))
    result_edges = tuple(sorted(edge_set))
    return RequirementFacts(tuple(facts), result_edges)


def _pairs(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise RequirementsError("REQ_INPUT_INVALID")
        result[key] = value
    return result


def _reject_const(value: str) -> object:
    raise RequirementsError("REQ_INPUT_INVALID")


def main(argv: object = None) -> int:
    parser = argparse.ArgumentParser(description="Faits requires contributions, sans activation.")
    parser.add_argument("--max-input-bytes", type=int, required=True)
    parser.add_argument("--max-contributions", type=int, required=True)
    parser.add_argument("--max-requirements-per-contribution", type=int, required=True)
    parser.add_argument("--max-total-requirements", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        for value in (
            args.max_input_bytes,
            args.max_contributions,
            args.max_requirements_per_contribution,
            args.max_total_requirements,
        ):
            if type(value) is not int or isinstance(value, bool) or value <= 0:
                raise RequirementsError("REQ_LIMITS_INVALID")
        if args.max_input_bytes > sys.maxsize - 1:
            raise RequirementsError("REQ_LIMITS_INVALID")
        raw = sys.stdin.buffer.read(args.max_input_bytes + 1)
        if len(raw) > args.max_input_bytes:
            raise RequirementsError("REQ_INPUT_TOO_LARGE")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise RequirementsError("REQ_INPUT_INVALID") from error
        try:
            payload = json.loads(
                text,
                object_pairs_hook=_pairs,
                parse_constant=_reject_const,
            )
        except RequirementsError:
            raise
        except (ValueError, RecursionError) as error:
            raise RequirementsError("REQ_INPUT_INVALID") from error
        if type(payload) is not dict or set(payload.keys()) != {
            "facets", "component_order", "component_edges",
        }:
            raise RequirementsError("REQ_INPUT_INVALID")
        if type(payload["facets"]) is not list:
            raise RequirementsError("REQ_INPUT_INVALID")
        if type(payload["component_order"]) is not list:
            raise RequirementsError("REQ_INPUT_INVALID")
        if type(payload["component_edges"]) is not list:
            raise RequirementsError("REQ_INPUT_INVALID")
        facets = tuple(payload["facets"])
        order = tuple(payload["component_order"])
        edges = tuple(tuple(item) if type(item) is list else item for item in payload["component_edges"])
        limits = RequirementsLimits(
            args.max_contributions,
            args.max_requirements_per_contribution,
            args.max_total_requirements,
        )
        result = analyze_contribution_requirements(
            facets,
            component_order=order,
            component_edges=edges,
            limits=limits,
        )
        sys.stdout.write(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
        return 0
    except RequirementsError as error:
        sys.stderr.write(error.code + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
