"""Propriété canonique : contexte direct, distinct des droits.

La validation topologique est faite à la frontière de consommation via
validate_context/check_claim ; la propriété reste distincte des droits.
"""

from dataclasses import dataclass

from .context import ScopeContext, validate_structure

CODE_OWNERSHIP = "SCOPE_OWNERSHIP_INVALID"
ELEMENT_OWNERSHIP = "resource_ownership"
STEP_VALIDATE_OWNERSHIP = "validate_ownership"


class OwnershipError(ValueError):
    def __init__(self):
        super().__init__("Propriété de ressource invalide.")
        self.code = CODE_OWNERSHIP
        self.element = ELEMENT_OWNERSHIP
        self.step = STEP_VALIDATE_OWNERSHIP


@dataclass(frozen=True, slots=True)
class ResourceOwnership:
    resource_id: str
    context: ScopeContext

    def __post_init__(self):
        rid = object.__getattribute__(self, "resource_id")
        ctx = object.__getattribute__(self, "context")
        if type(rid) is not str or rid == "":
            raise OwnershipError()
        if type(ctx) is not ScopeContext:
            raise OwnershipError()
        try:
            validate_structure(ctx)
        except Exception:
            raise OwnershipError() from None


__all__ = [
    "ResourceOwnership",
    "OwnershipError",
    "CODE_OWNERSHIP",
    "ELEMENT_OWNERSHIP",
    "STEP_VALIDATE_OWNERSHIP",
]
