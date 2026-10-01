"""Façade pure des descripteurs de contrats."""

from .models import (
    ContractCategory,
    ContractDescriptor,
    ContractDescriptorError,
    DECLARATIVE_DEPRECATION_VALID,
    DECLARATIVE_EVOLUTION_VALID,
    DECLARATIVE_RETIREMENT_VALID,
    DeprecationNotice,
    check_deprecation,
    check_evolution,
    check_retirement,
    require_category,
)

__all__ = [
    "ContractCategory",
    "ContractDescriptor",
    "ContractDescriptorError",
    "DECLARATIVE_DEPRECATION_VALID",
    "DECLARATIVE_EVOLUTION_VALID",
    "DECLARATIVE_RETIREMENT_VALID",
    "DeprecationNotice",
    "check_deprecation",
    "check_evolution",
    "check_retirement",
    "require_category",
]
