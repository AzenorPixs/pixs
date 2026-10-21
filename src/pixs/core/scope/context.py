"""Contexte de périmètre : structure seule, ne vaut pas autorisation."""

from dataclasses import dataclass
from enum import Enum

CODE_STRUCTURE = "SCOPE_STRUCTURE_INVALID"
ELEMENT_CONTEXT = "scope_context"
STEP_VALIDATE_STRUCTURE = "validate_structure"


class ScopeStructureError(ValueError):
    """Erreur structurelle stable sans valeurs brutes."""

    def __init__(self):
        super().__init__("ScopeContext structure invalide.")
        self.code = CODE_STRUCTURE
        self.element = ELEMENT_CONTEXT
        self.step = STEP_VALIDATE_STRUCTURE


class ScopeType(Enum):
    TENANT = "TENANT"
    PLATFORM = "PLATFORM"


def _is_opaque_id(value):
    return type(value) is str and value != ""


@dataclass(frozen=True, slots=True)
class ScopeContext:
    scope_type: ScopeType
    tenant_id: object = None
    scope_id: object = None

    def __post_init__(self):
        validate_structure(self)


def validate_structure(ctx):
    """Valide la structure sans invoquer __str__/__repr__ des entrées."""
    if type(ctx) is not ScopeContext:
        raise ScopeStructureError()
    scope_type = object.__getattribute__(ctx, "scope_type")
    tenant_id = object.__getattribute__(ctx, "tenant_id")
    scope_id = object.__getattribute__(ctx, "scope_id")
    if type(scope_type) is not ScopeType:
        raise ScopeStructureError()
    if scope_type is ScopeType.TENANT:
        if not _is_opaque_id(tenant_id):
            raise ScopeStructureError()
        if scope_id is not None and not _is_opaque_id(scope_id):
            raise ScopeStructureError()
    else:
        if tenant_id is not None or scope_id is not None:
            raise ScopeStructureError()
    return True


__all__ = [
    "ScopeType",
    "ScopeContext",
    "ScopeStructureError",
    "validate_structure",
    "CODE_STRUCTURE",
    "ELEMENT_CONTEXT",
    "STEP_VALIDATE_STRUCTURE",
]
