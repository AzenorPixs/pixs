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

from .time import (
    REFUSAL_REASONS,
    TIME_CONTRACT_ID,
    TIME_CONTRACT_VERSION,
    TIME_DESCRIPTOR,
    TimeDiagnostic,
    TimeDoubtError,
    TimeOutcome,
    TimeProducer,
    TimePublicRef,
    TimeRefusedError,
    UtcInstant,
    validate_utc,
)

__all__ = __all__ + [
    "REFUSAL_REASONS",
    "TIME_CONTRACT_ID",
    "TIME_CONTRACT_VERSION",
    "TIME_DESCRIPTOR",
    "TimeDiagnostic",
    "TimeDoubtError",
    "TimeOutcome",
    "TimeProducer",
    "TimePublicRef",
    "TimeRefusedError",
    "UtcInstant",
    "validate_utc",
]
