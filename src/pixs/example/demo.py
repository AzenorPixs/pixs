"""Demo pure exemple P0 : composition, scope et autorisation via façades."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pixs.core.authz import (
    AuditSink,
    Clock,
    FilterConfig,
    FilterLot,
    FilterPlan,
    Request,
    Snapshot,
    TrustedFactsProvider,
    plan_filter,
)
from pixs.core.scope import ScopeContext, ScopeType, TopologySnapshot
from pixs.kernel.composition import CompositionResult, compose

CONSUMER_TEXT = """schema_version = "1"
id = "example.client"
type = "MODULE"
version = "1.0.0"
[dependencies]
components = []
capabilities = []
contracts = ["example.hello.contract ==1.0.0"]
"""


def example_texts(provider_text: str) -> tuple[str, str]:
    return (provider_text, CONSUMER_TEXT)


def example_scope() -> tuple[ScopeContext, TopologySnapshot]:
    context = ScopeContext(ScopeType.TENANT, "t1")
    topology = TopologySnapshot(("t1",), ())
    return (context, topology)


def example_compose(
    texts: Sequence[str],
    attestations: Sequence[Any] = (),
) -> CompositionResult:
    return compose(texts, attestations=attestations)


def example_plan(
    snapshot: Snapshot,
    provider: TrustedFactsProvider,
    clock: Clock,
    audit: AuditSink,
    topology: TopologySnapshot,
    config: FilterConfig,
    context: ScopeContext,
) -> FilterPlan:
    lot = FilterLot(
        "s1",
        "a1",
        context,
        "c1",
        (
            Request("d-r1", "s1", "r1", "a1", context, "c1"),
            Request("d-r2", "s1", "r2", "a1", context, "c1"),
        ),
    )
    return plan_filter(
        lot, snapshot, provider, clock, audit, topology, config
    )


__all__ = [
    "CONSUMER_TEXT",
    "example_compose",
    "example_plan",
    "example_scope",
    "example_texts",
]
