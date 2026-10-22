"""Erreurs publiques Core API v1 : messages catalogués, aucune donnée d'exception."""
from __future__ import annotations

from types import MappingProxyType

__all__ = ["API_ERROR_VERSION", "CoreApiError", "classify_error", "error_schema"]

API_ERROR_VERSION = "1.0.0"
_ERRORS = MappingProxyType({
    "INPUT_INVALID": (400, "Invalid request.", "Requête invalide."),
    "CONTEXT_MISMATCH": (400, "Request context mismatch.", "Contexte de requête contradictoire."),
    "METHOD_NOT_ALLOWED": (405, "Method not allowed.", "Méthode non autorisée."),
    "NOT_FOUND": (404, "Resource not found.", "Ressource introuvable."),
    "AUTH_REQUIRED": (401, "Authentication required.", "Authentification requise."),
    "ACCESS_DENIED": (403, "Access denied.", "Accès refusé."),
    "CSRF_REQUIRED": (403, "CSRF verification required.", "Vérification CSRF requise."),
    "TRANSPORT_REQUIRED": (403, "Approved HTTPS transport required.", "Transport HTTPS approuvé requis."),
    "IDEMPOTENCE_CONFLICT": (409, "Idempotency content conflict.", "Conflit de contenu d'idempotence."),
    "VERSION_CONFLICT": (409, "Resource version conflict.", "Conflit de version de ressource."),
    "SESSION_LIMIT": (409, "Session limit reached.", "Limite de sessions atteinte."),
    "CURSOR_INVALID": (400, "Invalid or expired cursor.", "Curseur invalide ou périmé."),
    "PAYLOAD_TOO_LARGE": (413, "Request is too large.", "Requête trop volumineuse."),
    "AUDIT_UNAVAILABLE": (503, "Required audit unavailable.", "Audit requis indisponible."),
    "SERVICE_UNAVAILABLE": (503, "Required service unavailable.", "Service requis indisponible."),
    "UNKNOWN_OUTCOME": (503, "Operation outcome is unknown.", "Issue de l'opération inconnue."),
    "INTERNAL_ERROR": (500, "Internal service error.", "Erreur interne du service."),
})
_PREFIX = "pixs.core.api.v1."


class CoreApiError(ValueError):
    def __init__(self, code):
        if type(code) is not str or code not in _ERRORS:
            raise ValueError("Code d'erreur API inconnu.")
        self.public_code = code
        self.code = _PREFIX + code
        self.status = _ERRORS[code][0]
        super().__init__("Erreur API Core.")

    def envelope(self, *, correlation_id, language="en"):
        if (type(correlation_id) is not str or not correlation_id or len(correlation_id) > 128
                or any(c in correlation_id for c in (chr(0), chr(10), chr(13)))):
            raise ValueError("Corrélation API invalide.")
        try:
            correlation_id.encode("utf-8")
        except UnicodeError:
            raise ValueError("Corrélation API invalide.") from None
        language = language if type(language) is str and language in ("en", "fr") else "en"
        message = _ERRORS[self.public_code][2 if language == "fr" else 1]
        return {"error_code": self.code, "message": message, "details": {},
                "correlation_id": correlation_id}


def _has_auth_cause(error, authentication_error_type):
    cause = error.__cause__
    for _ in range(4):
        if cause is None:
            return False
        if type(cause) is authentication_error_type:
            return True
        cause = cause.__cause__
    return False


def classify_error(error):
    from pixs.backend.api_core_catalog import ApiCatalogError
    from pixs.backend.api_core_pagination import CoreCursorError
    from pixs.core.services_common import CoreServiceError
    from pixs.core.dto import CoreInputInvalid
    from pixs.core.ports import CorePortError
    from pixs.auth.contracts import AuthServiceError
    from pixs.auth.runtime_verifier import AuthVerificationError
    from pixs.auth.tokens import AuthTokenError
    from pixs.auth.api_request_source import ApiRequestSourceError
    if type(error) is CoreApiError:
        return error
    if type(error) in (AuthVerificationError, AuthTokenError, ApiRequestSourceError):
        return CoreApiError("AUTH_REQUIRED")
    if type(error) is CoreCursorError:
        return CoreApiError("CURSOR_INVALID")
    if type(error) is ApiCatalogError:
        code = getattr(error, "code", None)
        return CoreApiError("CONTEXT_MISMATCH" if type(code) is str and code in
                            ("API_CONTEXT_INVALID", "API_TENANT_MISMATCH") else "INPUT_INVALID")
    if type(error) is CoreInputInvalid:
        return CoreApiError("INPUT_INVALID")
    if type(error) is CorePortError:
        return CoreApiError("AUTH_REQUIRED" if _has_auth_cause(error, AuthVerificationError) else "SERVICE_UNAVAILABLE")
    if type(error) not in (CoreServiceError, AuthServiceError):
        return CoreApiError("INTERNAL_ERROR")
    code = error.code
    if type(code) is not str:
        return CoreApiError("INTERNAL_ERROR")
    if code in ("IDEMPOTENCE_CONFLIT", "AUTH_OPERATION_CONFLICT"):
        return CoreApiError("IDEMPOTENCE_CONFLICT")
    if code in ("CONFLIT_CAS", "CONFLIT_INTEGRITE", "UUID_REUTILISE"):
        return CoreApiError("VERSION_CONFLICT")
    if code == "AUTH_SESSION_LIMIT":
        return CoreApiError("SESSION_LIMIT")
    if code in ("AUTH_REAUTH_REQUIRED", "AUTH_DENIED"):
        return CoreApiError("AUTH_REQUIRED")
    if code == "FAITS_ILLISIBLES":
        return CoreApiError("AUTH_REQUIRED" if _has_auth_cause(error, AuthVerificationError) else "SERVICE_UNAVAILABLE")
    if code in ("DECISION_REFUSEE", "DECISION_EXPIREE", "FAITS_INVALIDES", "SUJET_DIVERGENT"):
        return CoreApiError("ACCESS_DENIED")
    if code in ("CONTEXTE_DIVERGENT", "CONTEXTE_INVALIDE", "TENANT_DIVERGENT"):
        return CoreApiError("CONTEXT_MISMATCH")
    if code in ("ISSUE_INCONNUE", "AUTH_COMMIT_UNKNOWN"):
        return CoreApiError("UNKNOWN_OUTCOME")
    if code in ("AUDIT_REFUS_INDISPONIBLE", "AUDIT_ABSENT", "AUTH_AUDIT_UNAVAILABLE"):
        return CoreApiError("AUDIT_UNAVAILABLE")
    if code in ("BORNE_INVALIDE", "DEPASSEMENT_LOT", "REFERENCE_INVALIDE", "CAS_REQUIS",
                "VERSION_INVALIDE", "COMMANDE_INVALIDE", "ENTREES_INVALIDES", "AUTH_INPUT_INVALID"):
        return CoreApiError("INPUT_INVALID")
    return CoreApiError("SERVICE_UNAVAILABLE")


def error_schema():
    return {
        "type": "object", "additionalProperties": False,
        "required": ["error_code", "message", "details", "correlation_id"],
        "properties": {
            "error_code": {"type": "string", "enum": [_PREFIX + code for code in _ERRORS]},
            "message": {"type": "string"},
            "details": {"type": "object", "additionalProperties": False},
            "correlation_id": {"type": "string", "minLength": 1, "maxLength": 128},
        },
    }
