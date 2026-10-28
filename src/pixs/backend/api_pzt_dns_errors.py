"""Projection fermée des refus C14 vers la frontière HTTP publique."""
from __future__ import annotations

from dataclasses import dataclass

from pixs.auth.api_request_source import ApiRequestSourceError
from pixs.auth.runtime_verifier import AuthVerificationError
from pixs.backend.api_pzt_dns_catalog import C14HttpCatalogError
from pixs.backend.api_pzt_dns_inputs import C14HttpInputError
from pixs.dns.services import DnsServiceError
from pixs.pzt.services import PztServiceError

__all__ = ["C14ErrorProjection", "project_c14_http_error"]


@dataclass(frozen=True, slots=True, repr=False)
class C14ErrorProjection:
    status: int
    error: dict


_MESSAGES = {
    "INPUT_INVALID": (400, "Requête de gestion invalide.", "Invalid management request."),
    "AUTH_REQUIRED": (401, "Authentification requise.", "Authentication required."),
    "ACCESS_DENIED": (403, "Accès refusé.", "Access denied."),
    "RESOURCE_UNAVAILABLE": (404, "Ressource de gestion indisponible.", "Management resource unavailable."),
    "REVISION_CONFLICT": (409, "La version a changé ; rechargez la configuration.", "The revision changed; reload the configuration."),
    "IDEMPOTENCE_CONFLICT": (409, "La clé d'idempotence porte un contenu différent.", "The idempotency key has different content."),
    "IDEMPOTENCE_EXPIRED": (409, "La validité de la clé d'idempotence est expirée.", "The idempotency key has expired."),
    "NAMESPACE_MIGRATION_REQUIRED": (409, "Le changement d'espace de noms exige une migration.", "The namespace change requires migration."),
    "NAMES_IN_USE": (409, "Des noms sont encore gérés dans cette zone.", "Names are still managed in this zone."),
    "VIEW_IN_USE": (409, "Cette vue est encore utilisée.", "This view is still in use."),
    "NAME_RETIREMENT_REQUIRED": (409, "Retirez le nom existant avant sa réaffectation.", "Retire the existing name before reassignment."),
    "NAME_OUTSIDE_ZONE": (400, "Le nom est hors de la zone déclarée.", "The name is outside the declared zone."),
    "VIEW_UNAVAILABLE": (404, "La vue demandée est indisponible.", "The requested view is unavailable."),
    "AUDIT_UNAVAILABLE": (503, "L'audit requis est indisponible.", "The required audit is unavailable."),
    "UNKNOWN_OUTCOME": (503, "L'issue reste inconnue ; rapprochez les faits avant toute nouvelle mutation.", "The outcome is unknown; reconcile before any new mutation."),
    "SERVICE_UNAVAILABLE": (503, "Le service de gestion requis est indisponible.", "The required management service is unavailable."),
    "INTERNAL_ERROR": (500, "Erreur interne du service de gestion.", "Internal management service error."),
}
_DOMAIN_CODES = {
    "DENIED": "ACCESS_DENIED", "INPUT_INVALID": "INPUT_INVALID", "NAME_INVALID": "INPUT_INVALID",
    "GOVERNANCE_INVALID": "INPUT_INVALID",
    "RESOURCE_UNAVAILABLE": "RESOURCE_UNAVAILABLE", "NAME_UNAVAILABLE": "RESOURCE_UNAVAILABLE",
    "REVISION_CONFLICT": "REVISION_CONFLICT", "IDEMPOTENCE_CONFLICT": "IDEMPOTENCE_CONFLICT",
    "IDEMPOTENCE_EXPIRED": "IDEMPOTENCE_EXPIRED",
    "NAMESPACE_MIGRATION_REQUIRED": "NAMESPACE_MIGRATION_REQUIRED", "NAMES_IN_USE": "NAMES_IN_USE",
    "VIEW_IN_USE": "VIEW_IN_USE", "NAME_RETIREMENT_REQUIRED": "NAME_RETIREMENT_REQUIRED",
    "NAME_OUTSIDE_ZONE": "NAME_OUTSIDE_ZONE", "VIEW_UNAVAILABLE": "VIEW_UNAVAILABLE",
    "AUDIT_UNAVAILABLE": "AUDIT_UNAVAILABLE", "OUTCOME_UNKNOWN": "UNKNOWN_OUTCOME",
}


def project_c14_http_error(owner, cause, *, language):
    """Aucune entrée, exception brute ou preuve n'entre dans la réponse publique."""
    if type(owner) is not str or owner not in ("pixs.pzt", "pixs.dns"):
        raise C14HttpInputError()
    if type(language) is not str or language not in ("fr", "en"):
        raise C14HttpInputError()
    code = "INTERNAL_ERROR"
    if type(cause) in (C14HttpInputError, C14HttpCatalogError):
        code = "INPUT_INVALID"
    elif type(cause) in (ApiRequestSourceError, AuthVerificationError):
        code = "AUTH_REQUIRED"
    elif ((owner == "pixs.pzt" and type(cause) is PztServiceError)
          or (owner == "pixs.dns" and type(cause) is DnsServiceError)):
        prefix = "PZT_" if owner == "pixs.pzt" else "DNS_"
        if type(cause.code) is str and cause.code.startswith(prefix):
            code = _DOMAIN_CODES.get(cause.code[len(prefix):], "SERVICE_UNAVAILABLE")
    status, french, english = _MESSAGES[code]
    return C14ErrorProjection(status, {
        "error_code": owner + ".api.v1." + code,
        "message": french if language == "fr" else english,
        "details": {}, "field_errors": [],
    })
