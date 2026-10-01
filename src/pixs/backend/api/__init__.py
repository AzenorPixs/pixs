"""Façade pure des plans de contrats API."""

from .contracts import (
    ApiContractPlan,
    ApiContractPlanError,
    DECLARATIVE_API_EVOLUTION_VALID,
    api_major_prefix,
    check_api_evolution,
)

__all__ = [
    "ApiContractPlan",
    "ApiContractPlanError",
    "DECLARATIVE_API_EVOLUTION_VALID",
    "api_major_prefix",
    "check_api_evolution",
]

from .errors import (
    API_ERROR_CONTRACT_VERSION,
    ApiErrorProjectionError,
    build_infrastructure_error,
)

__all__ += [
    "API_ERROR_CONTRACT_VERSION",
    "ApiErrorProjectionError",
    "build_infrastructure_error",
]

from .responses import build_infrastructure_response

__all__ += ["build_infrastructure_response"]

from .success import (
    ApiSuccessEnvelopeError,
    build_success_envelope,
    build_success_response,
)

__all__ += [
    "ApiSuccessEnvelopeError",
    "build_success_envelope",
    "build_success_response",
]
