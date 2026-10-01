"""Fabrique backend de réponse JSON d'infrastructure (fondation Django isolée).

`build_infrastructure_response` délègue d'abord à la projection publique
existante, exige des réglages Django déjà configurés, puis matérialise un
`JsonResponse` non streaming, statut 500 fixe, Content-Type exact. Import
Django local seul, sans configure/setup ni fallback, sans lecture
d'environnement.
"""

from __future__ import annotations

__all__ = ["build_infrastructure_response"]

_ERROR_UNCONFIGURED = "Réglages Django non configurés."


def build_infrastructure_response(
    correlation_id: object, *, internal_error: object
) -> object:
    """Construit la réponse JSON d'infrastructure 500 non streaming."""
    from pixs.backend.api.errors import build_infrastructure_error

    envelope = build_infrastructure_error(
        correlation_id, internal_error=internal_error
    )
    from django.conf import settings

    if not settings.configured:
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured(_ERROR_UNCONFIGURED)
    from django.http import JsonResponse

    return JsonResponse(
        envelope,
        status=500,
        content_type="application/json; charset=utf-8",
        json_dumps_params={"ensure_ascii": False},
    )
