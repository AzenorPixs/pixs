"""Propagation stricte : aucune autorisation accordée, refus audités."""

from dataclasses import dataclass

from .context import ScopeContext, ScopeStructureError, validate_structure
from .topology import TopologyError, TopologySnapshot, validate_context

CODE_PROPAGATION = "SCOPE_PROPAGATION_DENIED"
ELEMENT_PROPAGATION = "scope_propagation"
STEP_CHECK_CLAIM = "check_claim"


class PropagationDenied(ValueError):
    def __init__(self):
        super().__init__("Contexte de périmètre refusé.")
        self.code = CODE_PROPAGATION
        self.element = ELEMENT_PROPAGATION
        self.step = STEP_CHECK_CLAIM


@dataclass(frozen=True, slots=True)
class PropagationDiagnostic:
    code: str
    element: str
    step: str


def _deny(on_denied):
    diagnostic = PropagationDiagnostic(
        code=CODE_PROPAGATION,
        element=ELEMENT_PROPAGATION,
        step=STEP_CHECK_CLAIM,
    )
    try:
        on_denied(diagnostic)
    except Exception:
        raise PropagationDenied() from None
    raise PropagationDenied()


def check_claim(canonical, claim=None, *, snapshot, on_denied):
    """Valide le canonique contre snapshot puis l'égalité stricte du claim."""
    if not callable(on_denied):
        raise PropagationDenied()
    if type(canonical) is not ScopeContext:
        _deny(on_denied)
    if type(snapshot) is not TopologySnapshot:
        _deny(on_denied)
    try:
        validate_context(canonical, snapshot)
    except (ScopeStructureError, TopologyError):
        _deny(on_denied)
    if claim is not None:
        if type(claim) is not ScopeContext:
            _deny(on_denied)
        try:
            validate_structure(claim)
        except ScopeStructureError:
            _deny(on_denied)
        canon_type = object.__getattribute__(canonical, "scope_type")
        claim_type = object.__getattribute__(claim, "scope_type")
        canon_tenant = object.__getattribute__(canonical, "tenant_id")
        claim_tenant = object.__getattribute__(claim, "tenant_id")
        canon_scope = object.__getattribute__(canonical, "scope_id")
        claim_scope = object.__getattribute__(claim, "scope_id")
        if (
            canon_type is not claim_type
            or canon_tenant != claim_tenant
            or canon_scope != claim_scope
        ):
            _deny(on_denied)
    return canonical


__all__ = [
    "PropagationDenied",
    "PropagationDiagnostic",
    "check_claim",
    "CODE_PROPAGATION",
    "ELEMENT_PROPAGATION",
    "STEP_CHECK_CLAIM",
]
