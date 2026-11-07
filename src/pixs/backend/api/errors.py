"""Projection publique constante d'erreur d'infrastructure (fondation pure).

`build_infrastructure_error` normalise une erreur d'infrastructure vers
l'enveloppe publique à 5 champs TECHNICAL : `internal_error` opaque
requis mais jamais inspecté, `correlation_id` UUID exact revalidé puis
sérialisé canoniquement. Conteneurs frais par appel. Aucune
vérification HTTP, runtime ou trace backend.
"""

from __future__ import annotations

import uuid
from types import MappingProxyType

__all__ = [
    "API_ERROR_CONTRACT_VERSION",
    "API_ERROR_MESSAGE_VERSION",
    "ApiErrorProjectionError",
    "build_infrastructure_error",
]

API_ERROR_CONTRACT_VERSION = "1.0.0"
API_ERROR_MESSAGE_VERSION = "1.0.0"

_API_MESSAGES = MappingProxyType({
    "INTERNAL_ERROR": ("Internal service error.", "Erreur interne du service."),
})

_ERROR_CODE = "INTERNAL_ERROR"
_ERROR_CORRELATION = "Identifiant de corrélation invalide."

_MAX_INT = 2**128


class ApiErrorProjectionError(ValueError):
    """Erreur de projection stable, sans écho de valeurs brutes."""

    def __init__(self, message=_ERROR_CORRELATION):
        super().__init__(message)


def _canonical_correlation_id(correlation_id):
    """Revalide l'UUID exact puis retourne sa forme canonique."""
    if type(correlation_id) is not uuid.UUID:
        raise ApiErrorProjectionError(_ERROR_CORRELATION) from None
    try:
        number = object.__getattribute__(correlation_id, "int")
    except AttributeError:
        raise ApiErrorProjectionError(_ERROR_CORRELATION) from None
    if type(number) is not int or not 0 <= number < _MAX_INT:
        raise ApiErrorProjectionError(_ERROR_CORRELATION) from None
    return str(uuid.UUID(int=number))


def build_infrastructure_error(
    correlation_id: object, *, internal_error: object, language: str = "en"
) -> dict:
    """Projette une erreur d'infrastructure vers l'enveloppe publique constante."""
    text = _canonical_correlation_id(correlation_id)
    language_index = 1 if type(language) is str and language == "fr" else 0
    message = _API_MESSAGES[_ERROR_CODE][language_index]
    return {
        "error_code": _ERROR_CODE,
        "message": message,
        "details": {},
        "field_errors": [],
        "correlation_id": text,
    }
